# main.py
import os
import uuid
import datetime
import logging
from typing import Optional, Dict, Any

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get Google API key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set. Set it in environment or .env file.")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# ADK imports (1.18.0)
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.function_tool import FunctionTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
Part = types.Part

# ---------- Logging ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("it-access-guardian")

# ---------- Mock services ----------
class MockGoogleSheets:
    def __init__(self):
        self.sheets = {
            "Employee_Directory": [
                {"Employee_Email": "sam.sales@company.demo", "Employee_Name": "Sam Sales", "Role": "Sales", "Manager_Email": "sales.manager@company.demo"},
                {"Employee_Email": "edna.eng@company.demo", "Employee_Name": "Edna Engineer", "Role": "Engineering", "Manager_Email": "eng.manager@company.demo"},
            ],
            "Software_Access_Policy": [
                {"Software_Name": "Salesforce", "Role": "Sales", "Requires_Manager_Approval": "No", "Approval_Contact_Email": "it-support@company.demo"},
                {"Software_Name": "GitHub", "Role": "Sales", "Requires_Manager_Approval": "Yes", "Approval_Contact_Email": "it-support@company.demo"},
                {"Software_Name": "GitHub", "Role": "Engineering", "Requires_Manager_Approval": "No", "Approval_Contact_Email": "it-support@company.demo"},
                {"Software_Name": "Figma", "Role": "Design", "Requires_Manager_Approval": "No", "Approval_Contact_Email": "it-support@company.demo"},
            ],
            "Audit_Log": [
                {"Request_ID": "1001", "Timestamp": "2025-11-15T10:00:00Z", "Employee_Email": "edna.eng@company.demo", "Request_Type": "Grant", "Software_Name": "Figma", "Status": "Pending Manager", "Notes": "Waiting for manager."}
            ]
        }
        self.next_request_id = 1002

    def read_sheet(self, sheet_name: str):
        logger.info("[MOCK_SHEETS] read %s", sheet_name)
        return self.sheets.get(sheet_name, [])

    def find_row_matching(self, sheet_name: str, match_criteria: Dict[str, str]):
        logger.info("[MOCK_SHEETS] search %s for %s", sheet_name, match_criteria)
        sheet = self.sheets.get(sheet_name)
        if sheet:
            for row in sheet:
                if all(row.get(k) == v for k, v in match_criteria.items()):
                    logger.info("[MOCK_SHEETS] found row: %s", row)
                    return row
        logger.info("[MOCK_SHEETS] no row found")
        return None

    def append_to_sheet(self, sheet_name: str, row_data: Dict[str, str]):
        logger.info("[MOCK_SHEETS] append %s -> %s", sheet_name, row_data)
        if sheet_name == "Audit_Log":
            row_data = row_data.copy()
            row_data["Request_ID"] = str(self.next_request_id)
            self.next_request_id += 1
            row_data["Timestamp"] = datetime.datetime.now().isoformat()
            self.sheets["Audit_Log"].append(row_data)
        return row_data

class MockGmail:
    def send_email(self, to: str, subject: str, body: str, cc: Optional[str] = None):
        logger.info("[MOCK_GMAIL] To: %s Cc: %s Subject: %s Body: %s", to, cc, subject, body)
        return {"status": "success", "to": to, "subject": subject}

mock_sheets_db = MockGoogleSheets()
mock_gmail_service = MockGmail()

# ---------- Tools ----------
def find_employee_by_email(email: str):
    return mock_sheets_db.find_row_matching("Employee_Directory", {"Employee_Email": email})

def find_policy_for_user(software_name: str, user_role: str):
    return mock_sheets_db.find_row_matching("Software_Access_Policy", {"Software_Name": software_name, "Role": user_role})

def check_audit_log_for_duplicate(employee_email: str, software_name: str):
    log = mock_sheets_db.read_sheet("Audit_Log")
    for row in log:
        if row.get("Employee_Email") == employee_email and row.get("Software_Name") == software_name:
            return row
    return None

def append_to_audit_log(employee_email: str, request_type: str, software_name: str, status: str, notes: str):
    row = {
        "Employee_Email": employee_email,
        "Request_Type": request_type,
        "Software_Name": software_name,
        "Status": status,
        "Notes": notes
    }
    return mock_sheets_db.append_to_sheet("Audit_Log", row)

def send_gmail(to: str, subject: str, body: str, cc: Optional[str] = None):
    return mock_gmail_service.send_email(to=to, subject=subject, body=body, cc=cc)

ALL_TOOLS = [
    FunctionTool(func=find_employee_by_email),
    FunctionTool(func=find_policy_for_user),
    FunctionTool(func=check_audit_log_for_duplicate),
    FunctionTool(func=append_to_audit_log),
    FunctionTool(func=send_gmail),
]

# ---------- Agent ----------
llm_provider = Gemini()
AGENT_INSTRUCTIONS = """(your long instructions here, keep original)"""

def create_it_guardian_agent():
    return LlmAgent(
        name="AccessBot",
        model=llm_provider,
        tools=ALL_TOOLS,
        instruction=AGENT_INSTRUCTIONS
    )

# ---------- FastAPI App ----------
app = FastAPI(title="IT Access Guardian Agent")
APP_NAME = "it-access-guardian"

session_store = InMemorySessionService()
agent = create_it_guardian_agent()
runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_store)

# ---------- Request Models ----------
class AdkInvokeIn(BaseModel):
    text: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class InvokeOut(BaseModel):
    text: str
    session_id: str

# Optional endpoint to create session explicitly
@app.post("/session")
async def create_session():
    session = await session_store.create_session(app_name=APP_NAME, user_id="default_user")
    return {"session_id": session.id}  # <-- use .id

# ---------- /invoke endpoint ----------
@app.post("/invoke", response_model=InvokeOut)
async def invoke_agent(input: AdkInvokeIn):
    # 1️⃣ Validate or create session
    session_id = input.session_id
    if session_id:
        try:
            existing = await session_store.get_session(session_id)
        except Exception:
            existing = None
        if existing is None:
            logger.warning("client provided session_id not found, creating a new session")
            new_sess = await session_store.create_session(app_name=APP_NAME, user_id="default_user")
            session_id = new_sess.id
    else:
        new_sess = await session_store.create_session(app_name=APP_NAME, user_id="default_user")
        session_id = new_sess.id

    # 2️⃣ Build Content
    new_message = types.Content(role="user", parts=[Part(text=input.text)])

    # 3️⃣ Run agent
    response_text = ""
    user_id = "default_user"
    agen = runner.run_async(session_id=session_id, user_id=user_id, new_message=new_message)
    try:
        async for event in agen:
            if getattr(event, "content", None) and getattr(event.content, "parts", None):
                for p in event.content.parts:
                    if getattr(p, "text", None):
                        response_text += p.text
            if getattr(event, "is_final", None) and event.is_final():
                break
    finally:
        try:
            await agen.aclose()
        except Exception:
            pass

    if not response_text:
        raise HTTPException(status_code=500, detail="Agent returned no text")

    return InvokeOut(text=response_text, session_id=session_id)

# ---------- Run ----------
if __name__ == "__main__":
    logger.info("Starting IT Access Guardian Agent server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
