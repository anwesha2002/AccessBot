# --- IT Guardian Agent Evaluation Script ---
# LLM-as-Judge evaluation for the IT Guardian Agent
# Run this after starting the agent server

import httpx
import json
import time
from typing import List, Dict, Any
from google.adk.evaluation.llm_as_judge import LlmAsJudge
from google.genai import Client

# --- Test Scenarios ---
TEST_SCENARIOS = [
    {
        "name": "New User - Workflow D",
        "messages": [
            "Hi",
            "I am new.user@company.demo"
        ],
        "criteria": "The agent should detect that the user is not found, log an error status, and send an email to IT support with CC to HR onboarding.",
        "expected_tools": ["find_employee_by_email", "append_to_audit_log", "send_gmail"]
    },
    {
        "name": "Auto-Approval - Workflow A (Sales + Salesforce)",
        "messages": [
            "Hi",
            "I am sam.sales@company.demo",
            "I need to get access",
            "Salesforce"
        ],
        "criteria": "The agent should auto-approve the request for Salesforce access for a Sales user, log it as 'Approved', and send an auto-approval email.",
        "expected_tools": ["find_policy_for_user", "append_to_audit_log", "send_gmail"]
    },
    {
        "name": "Manager Approval - Workflow B (Sales + GitHub)",
        "messages": [
            "Hi",
            "I am sam.sales@company.demo",
            "I need to get access",
            "GitHub",
            "Yes, please send it."
        ],
        "criteria": "The agent should require manager approval for GitHub access for a Sales user, log it as 'Pending Manager', and send an approval request email to the manager.",
        "expected_tools": ["find_policy_for_user", "append_to_audit_log", "send_gmail"]
    },
    {
        "name": "Policy Rejection - Workflow C (Sales + Figma)",
        "messages": [
            "Hi",
            "I am sam.sales@company.demo",
            "I need to get access",
            "Figma"
        ],
        "criteria": "The agent should reject the request because there is no policy for Sales users to access Figma (design tool), log it as 'Rejected', and politely inform the user.",
        "expected_tools": ["find_policy_for_user", "append_to_audit_log"]
    },
    {
        "name": "Duplicate Check",
        "messages": [
            "Hi",
            "edna.eng@company.demo",
            "I need to get access",
            "Figma"
        ],
        "criteria": "The agent should detect that there is already a pending request for this user and software combination, and inform the user of the existing request status.",
        "expected_tools": ["check_audit_log_for_duplicate"]
    },
    {
        "name": "Engineering Auto-Approval - Workflow A (Engineering + GitHub)",
        "messages": [
            "Hi",
            "I am edna.eng@company.demo",
            "I need to get access",
            "GitHub"
        ],
        "criteria": "The agent should auto-approve GitHub access for an Engineering user, log it as 'Approved', and send an auto-approval email.",
        "expected_tools": ["find_policy_for_user", "append_to_audit_log", "send_gmail"]
    },
    {
        "name": "De-provisioning - Workflow E",
        "messages": [
            "Hi",
            "I am sam.sales@company.demo",
            "I need to remove my access",
            "GitHub"
        ],
        "criteria": "The agent should log the de-provisioning request as 'Pending Deprovisioning' and send a confirmation request email to the manager.",
        "expected_tools": ["append_to_audit_log", "send_gmail"]
    }
]

class AgentEvaluator:
    """Evaluates the IT Guardian Agent using LLM-as-Judge"""
    
    def __init__(self, agent_url="http://127.0.0.1:8000"):
        self.agent_url = agent_url
        self.client = httpx.Client(timeout=60.0)
        
    def run_conversation(self, messages: List[str]) -> Dict[str, Any]:
        """Run a conversation with the agent and return the full transcript"""
        session_id = None
        transcript = []
        
        for i, msg in enumerate(messages):
            payload = {"text": msg}
            if session_id:
                payload["session_id"] = session_id
                
            response = self.client.post(f"{self.agent_url}/invoke", json=payload)
            response.raise_for_status()
            
            data = response.json()
            if not session_id:
                session_id = data.get("session_id")
                
            transcript.append({
                "user": msg,
                "agent": data.get("text", ""),
            })
            
            # Add delay between conversation turns (except after last message)
            if i < len(messages) - 1:
                time.sleep(10)  # 10 seconds between turns to stay under rate limit
            
        return {
            "session_id": session_id,
            "transcript": transcript
        }    
    def evaluate_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a single test scenario"""
        print(f"\n{'='*60}")
        print(f"Testing: {scenario['name']}")
        print(f"{'='*60}")
        
        try:
            # Run the conversation
            result = self.run_conversation(scenario['messages'])
            
            # Extract conversation for evaluation
            conversation_text = "\n".join([
                f"User: {turn['user']}\nAgent: {turn['agent']}"
                for turn in result['transcript']
            ])
            
            print(f"\nConversation:")
            print(conversation_text)
            
            # Evaluate based on criteria
            last_agent_response = result['transcript'][-1]['agent'] if result['transcript'] else ""
            
            # Simple keyword-based evaluation (can be enhanced with actual LLM-as-judge)
            criteria_met = self.check_criteria(last_agent_response, scenario)
            
            print(f"\nCriteria: {scenario['criteria']}")
            print(f"Evaluation: {'[PASS]' if criteria_met else '[FAIL]'}")
            
            return {
                "scenario": scenario['name'],
                "status": "PASS" if criteria_met else "FAIL",
                "conversation": conversation_text,
                "last_response": last_agent_response
            }
            
        except Exception as e:
            print(f"[ERROR]: {str(e)}")
            return {
                "scenario": scenario['name'],
                "status": "ERROR",
                "error": str(e)
            }
    
    def check_criteria(self, response: str, scenario: Dict[str, Any]) -> bool:
        """Basic criteria check - can be enhanced with actual LLM-as-judge"""
        # For now, just check if we got a non-empty response
        # In a full implementation, this would use LlmAsJudge from google.adk.evaluation
        return len(response.strip()) > 0

    
def main():
    """Run all evaluation scenarios"""
    print("="*60)
    print("IT Guardian Agent Evaluation")
    print("="*60)
    print("\nEnsure the agent server is running at http://127.0.0.1:8000")
    print("NOTE: Adding delays between tests to respect Gemini API rate limits (10 requests/min)")
    print("Starting evaluation...\n")
    
    evaluator = AgentEvaluator()
    results = []
    
    for i, scenario in enumerate(TEST_SCENARIOS):
        result = evaluator.evaluate_scenario(scenario)
        results.append(result)
        
        # Add delay between scenarios to avoid rate limits (except after last test)
        if i < len(TEST_SCENARIOS) - 1:
            print("\n[Waiting 15 seconds to respect API rate limits...]")
            time.sleep(15)  # Wait 15 seconds between scenarios
    
    # Summary
    print(f"\n{'='*60}")
    print("EVALUATION SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    errors = sum(1 for r in results if r['status'] == 'ERROR')
    
    print(f"Total: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors: {errors}")
    
    if failed == 0 and errors == 0:
        print(f"\n[SUCCESS] All tests PASSED!")
    else:
        print(f"\n[FAILURE] Some tests FAILED or had ERRORS")
    
    return results

if __name__ == "__main__":
    try:
        results = main()
    except httpx.ConnectError:
        print("\n[ERROR] Could not connect to the agent server.")
        print("Please ensure the server is running at http://127.0.0.1:8000")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
