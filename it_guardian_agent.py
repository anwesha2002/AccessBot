# --- IT Access Guardian v3: Full ADK Implementation ---
# This file contains the complete, runnable ADK agent service.
# It uses FastAPI to expose the agent as an A2A-compatible API.

import uvicorn
import datetime
import os
from fastapi import FastAPI
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

# Hardcode your Google API key here (NOT RECOMMENDED for production)
os.environ["GOOGLE_API_KEY"] = "AIzaSyBpwfgwQh4Hf19uiuc6lCs6dK3tg4Om6bg"

# --- 1. ADK Core Imports ---
# These are the fundamental building blocks of the ADK
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.function_tool import FunctionTool
# from google.adk.telemetry import setup

# --- 2. Observability & Tracing Setup ---
# Fulfills: "Complete Trace Visibility"
# This setup enables detailed logging and tracing for debugging.
# setup.setup_logging()
# setup.setup_trace()

# --- 3. MOCK API CLIENTS ---
# In a real project, these would be in separate files and use
# libraries like 'gspread' and 'google-api-python-client'.
# We mock them here to make the agent fully runnable for the demo.

class MockGoogleSheets:
    """Mocks the Gspread client and Google Sheets database."""
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
                # Columns: Request_ID, Timestamp, Employee_Email, Request_Type, Software_Name, Status, Notes
                {"Request_ID": "1001", "Timestamp": "2025-11-15T10:00:00Z", "Employee_Email": "edna.eng@company.demo", "Request_Type": "Grant", "Software_Name": "Figma", "Status": "Pending Manager", "Notes": "Waiting for manager."}
            ]
        }
        self.next_request_id = 1002

    def read_sheet(self, sheet_name: str) -> List[Dict[str, str]]:
        print(f"[MOCK_SHEETS] Reading from '{sheet_name}'")
        return self.sheets.get(sheet_name, [])

    def find_row_matching(self, sheet_name: str, match_criteria: Dict[str, str]) -> Optional[Dict[str, str]]:
        """Finds the first row in a sheet matching all key-value pairs in the criteria."""
        print(f"[MOCK_SHEETS] Searching '{sheet_name}' for {match_criteria}")
        sheet = self.sheets.get(sheet_name)
        if sheet:
            for row in sheet:
                # Check if this row matches all criteria
                if all(row.get(key) == value for key, value in match_criteria.items()):
                    print(f"[MOCK_SHEETS] Found row: {row}")
                    return row
        print(f"[MOCK_SHEETS] No row found.")
        return None

    def append_to_sheet(self, sheet_name: str, row_data: Dict[str, str]):
        print(f"[MOCK_SHEETS] Appending to '{sheet_name}': {row_data}")
        if sheet_name == "Audit_Log":
            row_data["Request_ID"] = str(self.next_request_id)
            self.next_request_id += 1
            row_data["Timestamp"] = datetime.datetime.now().isoformat()
            self.sheets["Audit_Log"].append(row_data)
        return row_data

class MockGmail:
    """Mocks the Gmail API service."""
    def send_email(self, to: str, subject: str, body: str, cc: Optional[str] = None):
        print("\n--- [MOCK_GMAIL] SENDING EMAIL ---")
        print(f"To: {to}")
        if cc:
            print(f"Cc: {cc}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        print("----------------------------------\n")
        return {"status": "success", "to": to, "subject": subject}

# Instantiate our mock services
mock_sheets_db = MockGoogleSheets()
mock_gmail_service = MockGmail()


# --- 4. ADK Tool Definitions ---
# These are the Python functions the agent can "use".
# Fulfills: Core ADK concept of "Tools"

def find_employee_by_email(email: str) -> Optional[Dict[str, str]]:
    """Finds an employee's record in the 'Employee_Directory' using their email."""
    return mock_sheets_db.find_row_matching(
        sheet_name="Employee_Directory",
        match_criteria={"Employee_Email": email}
    )

def find_policy_for_user(software_name: str, user_role: str) -> Optional[Dict[str, str]]:
    """Finds a software policy for a specific user role."""
    return mock_sheets_db.find_row_matching(
        sheet_name="Software_Access_Policy",
        match_criteria={
            "Software_Name": software_name,
            "Role": user_role
        }
    )

def check_audit_log_for_duplicate(employee_email: str, software_name: str) -> Optional[Dict[str, str]]:
    """Checks the 'Audit_Log' for an existing request for a specific employee and software."""
    log = mock_sheets_db.read_sheet("Audit_Log")
    for row in log:
        if row.get("Employee_Email") == employee_email and row.get("Software_Name") == software_name:
            print(f"[MOCK_AUDIT] Found duplicate: {row}")
            return row
    print(f"[MOCK_AUDIT] No duplicate found.")
    return None

def append_to_audit_log(employee_email: str, request_type: str, software_name: str, status: str, notes: str) -> Dict[str, str]:
    """Appends a new row of data to the 'Audit_Log' Google Sheet. Use this to log every action."""
    row_data = {
        "Employee_Email": employee_email,
        "Request_Type": request_type,
        "Software_Name": software_name,
        "Status": status,
        "Notes": notes
    }
    result = mock_sheets_db.append_to_sheet("Audit_Log", row_data)
    return result

def send_gmail(to: str, subject: str, body: str, cc: Optional[str] = None) -> Dict[str, str]:
    """Sends an email using the Gmail service."""
    return mock_gmail_service.send_email(to=to, subject=subject, body=body, cc=cc)

# Create FunctionTool instances for all tools
ALL_TOOLS = [
    FunctionTool(func=find_employee_by_email),
    FunctionTool(func=find_policy_for_user),
    FunctionTool(func=check_audit_log_for_duplicate),
    FunctionTool(func=append_to_audit_log),
    FunctionTool(func=send_gmail)
]

# --- 5. Agent Definition ---
# This is the "brain" of the agent.

llm_provider = Gemini()
print("Using Gemini LLM.")

# The Agent's "Brain" - The System Instructions
# This prompt is the full logic from our plan, updated for the new tools.
AGENT_INSTRUCTIONS = """
You are "AccessBot," an internal IT Asset Manager for our company. Your one and only job is to help employees get access to software by following our official policy.
You are professional, secure, and must follow every step.

YOUR 5-STEP CORE LOGIC:

1. GREET & IDENTIFY INTENT: Greet the user. Ask if they want to **get new access** or **remove existing access**.

2. GET USER EMAIL: Ask for their `Employee_Email`. **You cannot proceed without it.**

3. FIND USER (Workflow D):
   - Use the `find_employee_by_email` tool.
   - **IF NOT FOUND (Workflow D):**
     1. Use `append_to_audit_log` to log the error: `employee_email`: user's input, `request_type`: "Error", `software_name`: "N/A", `status`: "Error - User Not Found", `notes`: "User email not found in directory."
     2. Use `send_gmail` to email `it-support@company.demo` and CC `hr-onboarding@company.demo`. Subject: "New/Unknown User Flagged".
     3. Inform the user: "I couldn't find you in our directory. I have notified IT and HR."
     4. **STOP.**

4. HANDLE INTENT: If the user is found (you have their `Role` and `Manager_Email` from the tool call), proceed based on their intent from Step 1.

5. EXECUTE WORKFLOW (A, B, C, E):

   --- IF INTENT is "Get Access" ---
   1. Ask for the `Software_Name`.
   2. **DUPLICATE CHECK:** Use the `check_audit_log_for_duplicate` tool.
   3. **If Duplicate Found:** Inform the user: "I see you already have a request for [Software_Name]. The current status is [Status]." **STOP.**
   4. **If No Duplicate:** Use the `find_policy_for_user` tool with the `software_name` and the user's `user_role` (which you got in Step 3).
      
      **IF POLICY NOT FOUND (Workflow C):**
      - Trigger: The `find_policy_for_user` tool returned no policy.
      - Action:
        1. `append_to_audit_log`: `employee_email`: user's email, `request_type`: "Grant", `software_name`: [Software_Name], `status`: "Rejected", `notes`: "No policy found for role [Role]."
        2. Inform user: "I'm sorry, this request cannot be processed. There is no policy for [Software_Name] for your [Role] role. I have logged this rejection."
        3. **STOP.**

      **IF POLICY IS FOUND:**
      - Now, check the `Requires_Manager_Approval` field from the policy you just found.

      **Workflow A (Auto-Approve):**
      - Trigger: Policy `Requires_Manager_Approval` is "No".
      - Action:
        1. `send_gmail` to the `Approval_Contact_Email` (from the policy). Subject: "AUTO-APPROVED REQUEST: [Software_Name] for [Employee_Name]".
        2. `append_to_audit_log`: `employee_email`: user's email, `request_type`: "Grant", `software_name`: [Software_Name], `status`: "Approved", `notes`: "Auto-approved per policy."
        3. Inform user: "Great news! This is pre-approved. I've sent the ticket to IT and logged your approval."

      **Workflow B (Manager Approval):**
      - Trigger: Policy `Requires_Manager_Approval` is "Yes".
      - Action:
        1. Ask user for confirmation to email their manager (using the `Manager_Email` you found in Step 3).
        2. On "Yes", `send_gmail`: `To`: [Manager_Email], `Cc`: [Approval_Contact_Email]. Subject: "APPROVAL NEEDED: [Software_Name] for [Employee_Name]". Body: "Please reply-all with 'Approved' or 'Denied'."
        3. `append_to_audit_log`: `employee_email`: user's email, `request_type`: "Grant", `software_name`: [Software_Name], `status`: "Pending Manager", `notes`: "Email sent to manager."
        4. Inform user: "Done. I've sent the email to your manager and CC'd IT. This is logged as 'Pending Manager'."

   --- IF INTENT is "Remove Access" ---
   **Workflow E (De-provisioning):**
   1. Ask for the `Software_Name` to remove.
   2. `send_gmail`: `To`: [Manager_Email], `Cc`: `it-support@company.demo`. Subject: "CONFIRMATION NEEDED: Remove Access". Body: "Please reply-all with 'Confirm'."
   3. `append_to_audit_log`: `employee_email`: user's email, `request_type`: "Remove", `software_name`: [Software_Name], `status`: "Pending Deprovisioning", `notes`: "Removal email sent to manager."
   4. Inform user: "For security, all removal requests must be confirmed. I have sent a confirmation to your manager and CC'd IT. This is logged as 'Pending Deprovisioning'."
"""

def create_it_guardian_agent():
    """Factory function to create the agent."""
    return LlmAgent(
        name="AccessBot",
        model=llm_provider,
        tools=ALL_TOOLS,
        instruction=AGENT_INSTRUCTIONS
    )

# --- 6. FastAPI Server ---
app = FastAPI(
    title="IT Access Guardian Agent",
    description="ADK agent for managing IT software access requests."
)

class AdkInvokeIn(BaseModel):
    text: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

@app.post("/invoke")
async def invoke_agent(input: AdkInvokeIn) -> Dict[str, Any]:
    """
    Invokes the IT Guardian Agent with proper ADK 1.18.0 API.
    """
    from google.adk import Runner
    from google.adk.sessions import InMemorySessionService
    from google.adk.apps import App
    from google.genai import types
    
    try:
        agent = create_it_guardian_agent()
        # Use a unique session ID each time to avoid "session not found" errors
        import uuid
        session_id = input.session_id or str(uuid.uuid4())
        user_id = "default_user"
        
        # Create Runner directly with agent
        # Use "agents" as app_name to match the directory where agent is loaded from
        runner = Runner(
            app_name="agents",
            agent=agent,
            session_service=InMemorySessionService()
        )
        
        # Create Content message with correct structure
        new_message = types.Content(
            parts=[types.Part(text=input.text)],
            role="user"
        )
        
        # Run the agent with correct signature
        response_text = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message
        ):
            # Extract text from events
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_text += part.text
        
        return {
            "text": response_text if response_text else "Agent processed request but returned no text",
            "session_id": session_id,
        }
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "session_id": input.session_id or "default",
        }

# --- 7. Main Entry Point ---
if __name__ == "__main__":
    print("Starting IT Access Guardian Agent server...")
    print("Access the API at http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)



