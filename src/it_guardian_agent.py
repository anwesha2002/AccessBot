# main.py
import warnings
# Suppress warnings FIRST before any other imports
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
warnings.filterwarnings("ignore", category=UserWarning, message=".*protected namespace.*")
warnings.filterwarnings("ignore", category=UserWarning, message=".*model_.*")

import os
import uuid
import datetime
import logging
from typing import Optional, Dict, Any

from google.adk.agents import Agent

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

# Suppress ADK runner warnings
logging.getLogger("google_adk.google.adk.runners").setLevel(logging.ERROR)

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
def find_employee_by_email(email: str) -> str:
    """
    Looks up an employee by their email address and returns their role.
    """
    employees = mock_sheets_db.read_sheet("Employee_Directory")
    for emp in employees:
        if emp["Employee_Email"].lower() == email.lower():
            return f"Employee found: {emp['Employee_Name']}, Role: {emp['Role']}"
    return "Employee not found."

def find_policy_for_user(software_name: str, user_role: str):
    """
    Looks up access policy for a given software and user role.
    """
    return mock_sheets_db.find_row_matching("Software_Access_Policy", {"Software_Name": software_name, "Role": user_role})

def check_audit_log_for_duplicate(employee_email: str, software_name: str):
    """
    Checks if there's already a pending request for this employee and software.
    """
    log = mock_sheets_db.read_sheet("Audit_Log")
    for row in log:
        if row.get("Employee_Email") == employee_email and row.get("Software_Name") == software_name:
            return row
    return None

def append_to_audit_log(employee_email: str, request_type: str, software_name: str, status: str, notes: str):
    """
    Adds a new entry to the audit log.
    """
    row = {
        "Employee_Email": employee_email,
        "Request_Type": request_type,
        "Software_Name": software_name,
        "Status": status,
        "Notes": notes
    }
    return mock_sheets_db.append_to_sheet("Audit_Log", row)

def send_gmail(to: str, subject: str, body: str, cc: Optional[str] = None):
    """
    Sends an email notification.
    """
    return mock_gmail_service.send_email(to=to, subject=subject, body=body, cc=cc)

def find_manager_email(employee_email: str) -> str:
    """
    Looks up the manager's email for a given employee.
    """
    employees = mock_sheets_db.read_sheet("Employee_Directory")
    for emp in employees:
        if emp["Employee_Email"].lower() == employee_email.lower():
            manager_email = emp.get("Manager_Email", "")
            if manager_email:
                return f"Manager email: {manager_email}"
            else:
                return "Manager email not found."
    return "Employee not found."

ALL_TOOLS = [
    FunctionTool(func=find_employee_by_email),
    FunctionTool(func=find_policy_for_user),
    FunctionTool(func=check_audit_log_for_duplicate),
    FunctionTool(func=append_to_audit_log),
    FunctionTool(func=send_gmail),
    FunctionTool(func=find_manager_email),
]

# ---------- Agent ----------
AGENT_INSTRUCTIONS = """
You are an IT Access Guardian Agent that helps employees request access to software applications.
Your role is to streamline the approval process by checking company policies and automating approvals when possible.

**WORKFLOW:**

1. **Identify the Employee:**
   - Ask for the employee's email if not provided
   - Use find_employee_by_email() to verify the employee exists and get their role
   - If employee not found, politely inform them and end the request

2. **Identify the Software:**
   - Ask what software they need access to if not provided
   - Get the exact software name (e.g., "Salesforce", "GitHub", "Figma")

3. **Check for Duplicates:**
   - Use check_audit_log_for_duplicate() to see if there's already a pending request
   - If duplicate found, inform the employee about the existing request status
   - Do NOT create a new request if one already exists

4. **Check Access Policy:**
   - Use find_policy_for_user() with the software name and employee's role
   - If no policy exists for this role and software:
     * Inform the employee that this software is not typically available for their role
     * Ask if they have a business justification
     * Do NOT auto-approve - escalate to manager

5. **Process Request Based on Policy:**
   
   **If policy exists and Requires_Manager_Approval = "No":**
   - AUTO-APPROVE the request
   - Add to audit log with Status="Approved"
   - Send email to IT support (from policy's Approval_Contact_Email) with:
     * Subject: "Access Request Approved: [Software] for [Employee Name]"
     * Body: Include employee email, name, role, software, and approval details
   - Inform the employee their request has been approved
   
   **If policy exists and Requires_Manager_Approval = "Yes":**
   - PENDING MANAGER APPROVAL
   - Add to audit log with Status="Pending Manager Approval"
   - Use find_manager_email() to get the manager's email
   - Send email to manager with:
     * Subject: "Access Request Requires Your Approval: [Software] for [Employee Name]"
     * Body: Include employee details, software requested, and ask for approval
   - CC the IT support email (from policy's Approval_Contact_Email)
   - Inform the employee that their request has been sent to their manager for approval
   
   **If no policy exists for this role:**
   - Add to audit log with Status="Pending Manager Approval" and Notes="No policy for role"
   - Use find_manager_email() to get the manager's email
   - Send email to manager explaining this is an exceptional request
   - Inform the employee that their request requires manager approval

6. **Confirmation:**
   - Provide a clear summary of what action was taken
   - Include the request ID from the audit log if available
   - Be friendly and professional

**IMPORTANT RULES:**
- ALWAYS check for duplicates before creating a new request
- ALWAYS add entries to the audit log for all requests
- Use append_to_audit_log() with request_type="Grant" for access requests
- Be conversational and helpful, but follow the workflow strictly
- If you're unsure about any information, ask clarifying questions
- Keep responses concise and professional
"""

def create_it_guardian_agent():
    llm_provider = Gemini()
    return LlmAgent(
        name="AccessBot",
        model=llm_provider,
        tools=ALL_TOOLS,
        instruction=AGENT_INSTRUCTIONS
    )

def build_agent() -> Agent:
    """
    Factory function to return an instance of your IT Guardian Agent.
    Used by local evaluation scripts.
    """
    return create_it_guardian_agent()

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
    return {"session_id": session.id}

# ---------- /invoke endpoint ----------
@app.post("/invoke", response_model=InvokeOut)
async def invoke_agent(input: AdkInvokeIn):
    import asyncio
    
    # Retry configuration
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            # 1️⃣ Get or create session
            session_id = input.session_id
            if not session_id:
                # Only create new session if no session_id was provided
                new_sess = await session_store.create_session(app_name=APP_NAME, user_id="default_user")
                session_id = new_sess.id
            # If session_id was provided, use it as-is (Runner handles session persistence)

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
                error_msg = f"Agent returned no text (attempt {attempt + 1}/{max_retries})"
                logger.warning(error_msg)
                
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    # Provide a helpful error message instead of failing
                    return InvokeOut(
                        text="I apologize, but I'm having trouble processing your request right now. This might be due to API rate limits. Please try again in a moment.",
                        session_id=session_id
                    )

            return InvokeOut(text=response_text, session_id=session_id)
            
        except Exception as e:
            error_msg = f"Error in invoke_agent (attempt {attempt + 1}/{max_retries}): {str(e)}"
            logger.error(error_msg)
            
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2
                continue
            else:
                # Last attempt failed
                raise HTTPException(
                    status_code=500, 
                    detail=f"Agent failed after {max_retries} attempts: {str(e)}"
                )

# ---------- Run ----------
if __name__ == "__main__":
    logger.info("Starting IT Access Guardian Agent server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
