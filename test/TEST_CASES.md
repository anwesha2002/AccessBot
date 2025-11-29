# AccessBot - Manual Test Cases Documentation

**Project:** IT Guardian Agent  
**Version:** 1.0  
**Date:** November 2025  
**Testing Method:** Manual Browser Testing via FastAPI Interactive Docs  
**Test Environment:** http://127.0.0.1:8000/docs

---

## 🚀 Prerequisites

### Before Testing:
1. ✅ Start the agent server:
   ```bash
   python src/it_guardian_agent.py
   ```
2. ✅ Open browser to: http://127.0.0.1:8000/docs
3. ✅ Keep terminal visible to monitor server logs

### Important Notes:
- 📝 Copy the `session_id` from each response to continue conversations
- 👀 Watch server logs for tool calls and confirmations
- ⏱️ Natural pacing between requests (no rate limit concerns)

---

## 📋 Test Cases

### **Test Case 1: New User - Employee Not Found (Workflow D)**

**Test ID:** TC-001  
**Priority:** High  
**Workflow:** D (Error Handling)

**Objective:** Verify the agent correctly handles requests from users not in the employee directory.

**Preconditions:**
- Email `new.user@company.demo` does NOT exist in employee directory

**Test Steps:**

| Step | Action | Input JSON |
|------|--------|------------|
| 1 | Initial greeting | `{"text": "Hi"}` |
| 2 | Provide new user email | `{"text": "I am new.user@company.demo", "session_id": "SESSION_ID"}` |

**Expected Results:**

✅ **Agent Response:**
- Politely informs user that email is not found in the system
- Suggests double-checking email address
- Recommends contacting HR if issue persists
- Does NOT proceed with access request

✅ **Server Logs Should Show:**
```
[MOCK_SHEETS] read Employee_Directory
[MOCK_SHEETS] no row found
```

✅ **No Email Sent** (since user doesn't exist)

**Status:** [ ] Pass  [ ] Fail

**Notes:** _____________________

---

### **Test Case 2: Auto-Approval - Sales + Salesforce (Workflow A)**

**Test ID:** TC-002  
**Priority:** High  
**Workflow:** A (Auto-Approval)

**Objective:** Verify automatic approval for policy-allowed software requests.

**Preconditions:**
- Email `sam.sales@company.demo` exists with Role: Sales
- Policy exists: Sales + Salesforce = Auto-Approve

**Test Steps:**

| Step | Action | Input JSON |
|------|--------|------------|
| 1 | Initial greeting | `{"text": "Hi"}` |
| 2 | Identify as Sales user | `{"text": "I am sam.sales@company.demo", "session_id": "SESSION_ID"}` |
| 3 | Request access | `{"text": "I need access", "session_id": "SESSION_ID"}` |
| 4 | Specify software | `{"text": "Salesforce", "session_id": "SESSION_ID"}` |

**Expected Results:**

✅ **Agent Response:**
- Confirms identity (Sam Sales, Sales role)
- States request is auto-approved
- Mentions sending email to IT support
- Provides request ID from audit log
- Professional, friendly tone

✅ **Server Logs Should Show:**
```
[MOCK_SHEETS] find_employee_by_email: sam.sales@company.demo
[MOCK_SHEETS] find_policy_for_user: Software_Name=Salesforce, Role=Sales
[MOCK_SHEETS] append_to_sheet: Audit_Log (Status=Approved)
[MOCK_GMAIL] To: it-support@company.demo Subject: Access Request Approved...
```

✅ **Audit Log Entry:**
- Employee_Email: sam.sales@company.demo
- Software_Name: Salesforce
- Status: Approved
- Request_Type: Grant

**Status:** [ ] Pass  [ ] Fail

**Notes:** _____________________

---

### **Test Case 3: Manager Approval Required - Sales + GitHub (Workflow B)**

**Test ID:** TC-003  
**Priority:** High  
**Workflow:** B (Manager Approval)

**Objective:** Verify requests requiring manager approval are handled correctly.

**Preconditions:**
- Email `sam.sales@company.demo` exists with Role: Sales, Manager: sales.manager@company.demo
- Policy exists: Sales + GitHub = Requires Manager Approval

**Test Steps:**

| Step | Action | Input JSON |
|------|--------|------------|
| 1 | Initial greeting | `{"text": "Hi"}` |
| 2 | Identify as Sales user | `{"text": "I am sam.sales@company.demo", "session_id": "SESSION_ID"}` |
| 3 | Request access | `{"text": "I need access", "session_id": "SESSION_ID"}` |
| 4 | Specify software | `{"text": "GitHub", "session_id": "SESSION_ID"}` |
| 5 | Confirm sending to manager | `{"text": "Yes, please send it to my manager", "session_id": "SESSION_ID"}` |

**Expected Results:**

✅ **Agent Response:**
- States that GitHub access for Sales requires manager approval
- Asks if user wants to proceed
- Confirms sending approval request to manager
- Mentions manager email (sales.manager@company.demo)
- Provides request ID

✅ **Server Logs Should Show:**
```
[MOCK_SHEETS] find_policy_for_user: GitHub, Sales (Requires_Manager_Approval=Yes)
[MOCK_SHEETS] find_manager_email: sam.sales@company.demo
[MOCK_SHEETS] append_to_sheet: Audit_Log (Status=Pending Manager)
[MOCK_GMAIL] To: sales.manager@company.demo CC: it-support@company.demo
```

✅ **Audit Log Entry:**
- Status: Pending Manager Approval
- Notes: Waiting for manager authorization

**Status:** [ ] Pass  [ ] Fail

**Notes:** _____________________

---

### **Test Case 4: Policy Rejection - Sales + Figma (Workflow C)**

**Test ID:** TC-004  
**Priority:** High  
**Workflow:** C (Policy Rejection)

**Objective:** Verify requests for software not allowed by policy are rejected.

**Preconditions:**
- Email `sam.sales@company.demo` exists with Role: Sales
- Policy for Figma exists ONLY for Role: Design (NOT Sales)

**Test Steps:**

| Step | Action | Input JSON |
|------|--------|------------|
| 1 | Initial greeting | `{"text": "Hi"}` |
| 2 | Identify as Sales user | `{"text": "I am sam.sales@company.demo", "session_id": "SESSION_ID"}` |
| 3 | Request access | `{"text": "I need access", "session_id": "SESSION_ID"}` |
| 4 | Specify software | `{"text": "Figma", "session_id": "SESSION_ID"}` |

**Expected Results:**

✅ **Agent Response:**
- Politely explains Figma is not available for Sales role
- States it's typically for Design team members
- Suggests alternative: contact supervisor if there's a business need
- Professional, not dismissive tone

✅ **Server Logs Should Show:**
```
[MOCK_SHEETS] find_policy_for_user: Figma, Sales
[MOCK_SHEETS] no row found (no policy match)
[MOCK_SHEETS] append_to_sheet: Audit_Log (Status=Rejected)
```

✅ **Audit Log Entry:**
- Status: Rejected
- Notes: No policy for role

✅ **No Manager Email Sent** (outright rejection)

**Status:** [ ] Pass  [ ] Fail

**Notes:** _____________________

---

### **Test Case 5: Duplicate Request Detection**

**Test ID:** TC-005  
**Priority:** High  
**Workflow:** Duplicate Prevention

**Objective:** Verify the agent detects and prevents duplicate access requests.

**Preconditions:**
- Email `edna.eng@company.demo` exists with Role: Engineering
- Existing audit log entry: edna.eng + Figma = "Pending Manager"

**Test Steps:**

| Step | Action | Input JSON |
|------|--------|------------|
| 1 | Initial greeting | `{"text": "Hi"}` |
| 2 | Identify as Engineering user | `{"text": "I am edna.eng@company.demo", "session_id": "SESSION_ID"}` |
| 3 | Request same software | `{"text": "I need Figma access", "session_id": "SESSION_ID"}` |

**Expected Results:**

✅ **Agent Response:**
- Detects existing request
- States there's already a pending request for this software
- Tells user the current status ("Pending Manager")
- Provides request ID of existing request
- Does NOT create new request

✅ **Server Logs Should Show:**
```
[MOCK_SHEETS] check_audit_log_for_duplicate: edna.eng@company.demo, Figma
[MOCK_SHEETS] found existing request (Status=Pending Manager)
```

✅ **No New Audit Log Entry Created**

✅ **No Email Sent**

**Status:** [ ] Pass  [ ] Fail

**Notes:** _____________________

---

### **Test Case 6: Engineering Auto-Approval - Engineering + GitHub (Workflow A)**

**Test ID:** TC-006  
**Priority:** High  
**Workflow:** A (Auto-Approval for Different Role)

**Objective:** Verify engineering users get auto-approved for GitHub (different from Sales).

**Preconditions:**
- Email `edna.eng@company.demo` exists with Role: Engineering
- Policy exists: Engineering + GitHub = Auto-Approve (No manager needed)

**Test Steps:**

| Step | Action | Input JSON |
|------|--------|------------|
| 1 | Initial greeting | `{"text": "Hi"}` |
| 2 | Identify as Engineering user | `{"text": "edna.eng@company.demo", "session_id": "SESSION_ID"}` |
| 3 | Request GitHub | `{"text": "I need GitHub access", "session_id": "SESSION_ID"}` |

**Expected Results:**

✅ **Agent Response:**
- Confirms identity (Edna Engineer, Engineering role)
- States GitHub is auto-approved for Engineering
- Mentions email sent to IT
- Provides request ID

✅ **Server Logs Should Show:**
```
[MOCK_SHEETS] find_policy_for_user: GitHub, Engineering (Requires_Manager_Approval=No)
[MOCK_SHEETS] append_to_sheet: Status=Approved
[MOCK_GMAIL] To: it-support@company.demo Subject: Access Request Approved...
```

✅ **Audit Log Entry:**
- Status: Approved (NOT Pending Manager)

**Comparison Note:** Same software (GitHub) but different behavior based on role:
- Sales + GitHub → Manager Approval (TC-003)
- Engineering + GitHub → Auto-Approve (TC-006)

**Status:** [ ] Pass  [ ] Fail

**Notes:** _____________________

---

### **Test Case 7: De-provisioning - Remove Access (Workflow E)**

**Test ID:** TC-007  
**Priority:** Medium  
**Workflow:** E (De-provisioning)

**Objective:** Verify the agent handles access removal requests correctly.

**Preconditions:**
- Email `sam.sales@company.demo` exists
- User previously had GitHub access

**Test Steps:**

| Step | Action | Input JSON |
|------|--------|------------|
| 1 | Initial greeting | `{"text": "Hi"}` |
| 2 | Identify user | `{"text": "I am sam.sales@company.demo", "session_id": "SESSION_ID"}` |
| 3 | Request removal | `{"text": "I need to remove my GitHub access", "session_id": "SESSION_ID"}` |

**Expected Results:**

✅ **Agent Response:**
- Acknowledges de-provisioning request
- States request will be sent to manager for confirmation
- Provides request ID

✅ **Server Logs Should Show:**
```
[MOCK_SHEETS] append_to_sheet: Request_Type=Revoke, Status=Pending Deprovisioning
[MOCK_GMAIL] To: sales.manager@company.demo Subject: Access Removal Request
```

✅ **Audit Log Entry:**
- Request_Type: Revoke (or Remove)
- Status: Pending Deprovisioning
- Software_Name: GitHub

**Status:** [ ] Pass  [ ] Fail

**Notes:** _____________________

---

## 🧪 Additional Test Cases (Edge Cases)

### **Test Case 8: Natural Language Variations**

**Test ID:** TC-008  
**Priority:** Medium  
**Objective:** Verify agent handles different phrasings.

**Test Variations:**

| Variation | Input | Expected Behavior |
|-----------|-------|-------------------|
| Casual | `{"text": "hey can I get salesforce?"}` | Understands and processes |
| Formal | `{"text": "I would like to formally request access to Salesforce"}` | Understands and processes |
| Typo | `{"text": "I nee acces to GitHub"}` | Handles gracefully, asks for clarification if needed |
| Abbreviated | `{"text": "need SF"}` | May ask "Did you mean Salesforce?" |

**Status:** [ ] Pass  [ ] Fail

---

### **Test Case 9: Invalid Software Name**

**Test ID:** TC-009  
**Priority:** Low  
**Objective:** Verify handling of unknown software.

**Test Steps:**
```json
{"text": "I need access to NotARealSoftware", "session_id": "SESSION_ID"}
```

**Expected Results:**
- Agent politely states software is not recognized
- Asks user to clarify or check spelling
- Does not create audit log entry for invalid software

**Status:** [ ] Pass  [ ] Fail

---

### **Test Case 10: Incomplete Information**

**Test ID:** TC-010  
**Priority:** Medium  
**Objective:** Verify agent prompts for missing information.

**Test Steps:**
```json
{"text": "I need access", "session_id": "SESSION_ID"}
```

**Expected Results:**
- Agent asks "Which software do you need access to?"
- Waits for user to specify
- Continues workflow once information provided

**Status:** [ ] Pass  [ ] Fail

---

### **Test Case 11: Multiple Requests in One Session**

**Test ID:** TC-011  
**Priority:** Medium  
**Objective:** Verify agent handles multiple requests sequentially.

**Test Steps:**
1. Request Salesforce (approved)
2. In same session, request GitHub (needs manager)

**Expected Results:**
- Both requests processed correctly
- Separate audit log entries
- Appropriate emails sent for each
- Agent maintains context

**Status:** [ ] Pass  [ ] Fail

---

**Document Version:** 1.0  
**Last Updated:** November 2025  
**Maintained By:** Laxmi Gunda
