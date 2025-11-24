import pytest
import pytest_asyncio
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from it_guardian_agent import create_it_guardian_agent, mock_sheets_db

import time

# ... imports ...

# Helper to run a turn
async def run_turn(runner: Runner, session_id: str, user_id: str, text: str) -> str:
    """Runs a single turn of the agent and returns the text response."""
    # Create user message
    new_message = types.Content(role="user", parts=[types.Part(text=text)])
    
    # Run the agent - it will automatically handle tool execution
    response_text = ""
    agen = runner.run_async(session_id=session_id, user_id=user_id, new_message=new_message)
    try:
        async for event in agen:
            # Capture text from assistant responses only
            if getattr(event, "content", None) and getattr(event.content, "parts", None):
                # Only capture text from model/assistant, not function calls
                if getattr(event.content, "role", None) == "model":
                    for p in event.content.parts:
                        if getattr(p, "text", None):
                            response_text += p.text
    finally:
        try:
            await agen.aclose()
        except Exception:
            pass
    
    return response_text

@pytest_asyncio.fixture
async def services():
    # Rate limit handling: sleep before each test to avoid hitting Gemini API limits.
    # The free tier has a limit of 15 requests per minute (RPM).
    # Since each test makes multiple API calls, a 40s sleep ensures we stay within quota
    # and avoid 'google.genai.errors.ResourceExhausted' errors.
    time.sleep(40) 
    
    agent = create_it_guardian_agent()
    session_store = InMemorySessionService()
    runner = Runner(agent=agent, app_name="it-access-guardian", session_service=session_store)
    return runner, session_store

@pytest.mark.asyncio
async def test_agent_initialization(services):
    """Verify that the agent can be initialized and responds to a basic greeting."""
    runner, session_store = services
    user_id = "test.user@company.demo"
    session = await session_store.create_session(app_name="it-access-guardian", user_id=user_id)
    
    # Simple greeting
    response = await run_turn(runner, session.id, user_id, "Hello")
    print(f"Agent Response: {response}")
    
    assert len(response) > 0, "Agent should return a non-empty response"

@pytest.mark.asyncio
async def test_auto_approval_sales(services):
    """Verify that Sales requesting Salesforce gets auto-approved."""
    runner, session_store = services
    user_id = "sam.sales@company.demo"
    session = await session_store.create_session(app_name="it-access-guardian", user_id=user_id)
    
    await run_turn(runner, session.id, user_id, "Hi, I am sam.sales@company.demo")
    response = await run_turn(runner, session.id, user_id, "I need to get access to Salesforce")
    print(f"Agent Response (Salesforce): {response}")
    
    # If agent asks for confirmation, confirm it
    if "confirm" in response.lower() or "proceed" in response.lower():
         response = await run_turn(runner, session.id, user_id, "Yes, please proceed.")
         print(f"Agent Response (Confirmation): {response}")

    # Check side effect: Audit log should have an entry for Salesforce
    log = mock_sheets_db.read_sheet("Audit_Log")
    found = any(row.get("Employee_Email") == "sam.sales@company.demo" and 
                row.get("Software_Name") == "Salesforce" and 
                row.get("Status") == "Approved" 
                for row in log)
    assert found, "Audit log should contain Approved entry for Salesforce"

@pytest.mark.asyncio
async def test_manager_approval_sales(services):
    """Verify that Sales requesting GitHub triggers manager approval."""
    runner, session_store = services
    user_id = "sam.sales@company.demo"
    session = await session_store.create_session(app_name="it-access-guardian", user_id=user_id)
    
    await run_turn(runner, session.id, user_id, "Hi, I am sam.sales@company.demo")
    response = await run_turn(runner, session.id, user_id, "I need access to GitHub")
    print(f"Agent Response (GitHub): {response}")
    
    # Check side effect: Audit log should be "Pending Manager"
    log = mock_sheets_db.read_sheet("Audit_Log")
    found = any(row.get("Employee_Email") == "sam.sales@company.demo" and 
                row.get("Software_Name") == "GitHub" and
                "Pending" in row.get("Status", "")
                for row in log)
    
    assert found, "Audit log should contain Pending entry for GitHub"

@pytest.mark.asyncio
async def test_duplicate_check(services):
    """Verify that the agent detects duplicate requests."""
    runner, session_store = services
    user_id = "edna.eng@company.demo"
    session = await session_store.create_session(app_name="it-access-guardian", user_id=user_id)
    
    # Edna already has a pending request for Figma in the mock DB (see MockGoogleSheets init)
    await run_turn(runner, session.id, user_id, "Hi, I am edna.eng@company.demo")
    response = await run_turn(runner, session.id, user_id, "I need access to Figma")
    print(f"Agent Response (Duplicate Figma): {response}")
    
    # Agent should mention it's already pending or duplicate
    assert "already" in response.lower() or "pending" in response.lower() or "duplicate" in response.lower(), \
        "Agent should detect duplicate request"

@pytest.mark.asyncio
async def test_policy_rejection(services):
    """Verify that requests violating policy are rejected (or handled appropriately)."""
    runner, session_store = services
    user_id = "sam.sales@company.demo"
    session = await session_store.create_session(app_name="it-access-guardian", user_id=user_id)
    
    await run_turn(runner, session.id, user_id, "Hi, I am sam.sales@company.demo")
    response = await run_turn(runner, session.id, user_id, "I need access to Figma")
    print(f"Agent Response (Figma for Sales): {response}")
    
    # Mock policy: Figma is for Design role. Sam is Sales.
    # Agent should likely say it's restricted or ask for justification.
    # We check that it doesn't just say "Approved".
    assert "approved" not in response.lower(), "Agent should not auto-approve restricted software"

@pytest.mark.asyncio
async def test_employee_not_found(services):
    """Verify that the agent handles non-existent employee gracefully."""
    runner, session_store = services
    user_id = "unknown@company.demo"
    session = await session_store.create_session(app_name="it-access-guardian", user_id=user_id)
    
    response = await run_turn(runner, session.id, user_id, "Hi, I am unknown@company.demo and I need access to Salesforce")
    print(f"Agent Response (Unknown Employee): {response}")
    
    # Agent should respond that employee was not found or cannot process request
    # The agent might say "not found", "don't have", "unable", or "cannot"
    assert any(keyword in response.lower() for keyword in ["not found", "don't have", "unable", "cannot", "couldn't find", "no record"]), \
        f"Agent should indicate employee not found. Got: {response}"

@pytest.mark.asyncio
async def test_missing_employee_context(services):
    """Verify that the agent asks for employee email when not provided in context."""
    runner, session_store = services
    user_id = "anonymous@company.demo"
    session = await session_store.create_session(app_name="it-access-guardian", user_id=user_id)
    
    # Request without providing employee email
    response = await run_turn(runner, session.id, user_id, "I need access to GitHub")
    print(f"Agent Response (No Email): {response}")
    
    # Agent should ask for email or employee information
    assert "email" in response.lower() or "who" in response.lower(), \
        "Agent should request employee identification"

@pytest.mark.asyncio
async def test_nonexistent_software(services):
    """Verify that the agent handles requests for software not in the policy."""
    runner, session_store = services
    user_id = "sam.sales@company.demo"
    session = await session_store.create_session(app_name="it-access-guardian", user_id=user_id)
    
    await run_turn(runner, session.id, user_id, "Hi, I am sam.sales@company.demo")
    response = await run_turn(runner, session.id, user_id, "I need access to NonExistentSoftware")
    print(f"Agent Response (Nonexistent Software): {response}")
    
    # Agent should handle gracefully - either ask for justification or escalate
    # Should NOT auto-approve
    assert "approved" not in response.lower(), \
        "Agent should not auto-approve software not in policy"

def test_build_agent():
    """Verify that build_agent() factory function returns a valid agent."""
    from it_guardian_agent import build_agent
    from google.adk.agents import LlmAgent
    
    agent = build_agent()
    
    # Verify agent is created
    assert agent is not None, "build_agent should return an agent instance"
    
    # Verify it's the correct type
    assert isinstance(agent, LlmAgent), "build_agent should return an LlmAgent instance"
    
    # Verify agent has expected attributes
    assert agent.name == "AccessBot", "Agent should be named AccessBot"
    assert hasattr(agent, 'tools'), "Agent should have tools attribute"
    assert len(agent.tools) == 6, "Agent should have 6 tools registered"

def test_api_session_persistence():
    """Verify that the API maintains session ID across requests (fixes session bug)."""
    from fastapi.testclient import TestClient
    from it_guardian_agent import app, runner
    from unittest.mock import MagicMock
    
    client = TestClient(app)
    
    # Mock the runner to avoid real API calls
    # We need to mock run_async to return an async generator
    async def mock_gen(*args, **kwargs):
        # Yield a dummy event
        mock_event = MagicMock()
        # Mock the structure: event.content.parts[0].text
        mock_part = MagicMock()
        mock_part.text = "Mock response"
        mock_content = MagicMock()
        mock_content.parts = [mock_part]
        mock_event.content = mock_content
        mock_event.is_final.return_value = True
        yield mock_event
        
    # Patch the runner.run_async method
    original_run = runner.run_async
    runner.run_async = mock_gen
    
    try:
        # 1. First request - should create a new session
        resp1 = client.post("/invoke", json={"text": "Hello"})
        assert resp1.status_code == 200
        data1 = resp1.json()
        session_id_1 = data1.get("session_id")
        assert session_id_1 is not None, "First request should return a session_id"
        
        # 2. Second request - passing the session_id back
        resp2 = client.post("/invoke", json={"text": "Next", "session_id": session_id_1})
        assert resp2.status_code == 200
        data2 = resp2.json()
        session_id_2 = data2.get("session_id")
        
        # CRITICAL CHECK: Session IDs must match
        assert session_id_1 == session_id_2, f"Session ID changed! {session_id_1} != {session_id_2}"
        print(f"Session persistence verified: {session_id_1} == {session_id_2}")
        
    finally:
        # Restore original method
        runner.run_async = original_run

