# AccessBot - Test Execution Report

**Project:** IT Guardian Agent  
**Test Date:** November 26, 2025  
**Tester:** Laxmi Gunda  
**Environment:** Local Development (http://127.0.0.1:8000)  
**Server Version:** 1.0  
**Test Plan Reference:** [TEST_CASES.md](TEST_CASES.md)

---

## 📊 Executive Summary

| Metric | Result |
|--------|--------|
| **Total Test Cases Executed** | 7/11 |
| **Passed** | 7 |
| **Failed** | 0 |
| **Blocked** | 0 |
| **Pass Rate** | 100% |
| **High Priority Tests** | 7/7 ✅ |
| **Test Duration** | ~15 minutes |

**Overall Status:** ✅ **ALL HIGH PRIORITY TESTS PASSED**

---

## 🧪 Detailed Test Results

### **TC-001: New User - Employee Not Found** ✅ PASS

**Execution Date:** Nov 26, 2025, 12:45 PM  
**Status:** PASS

**Test Data:**
- Email: `new.user@company.demo`

**Actual Results:**
- Agent correctly identified user not found
- Response: "I'm sorry, but I couldn't find an employee with the email `new.user@company.demo` in our system. Please double-check your email address and try again."
- Suggested contacting HR
- Professional, helpful tone

**Server Logs Verification:**
```
[MOCK_SHEETS] read Employee_Directory
Employee not found.
```

**Evidence:**
- Screenshot: `evidence/screenshots/tc001_new_user.png` (optional)
- Session ID: `abc123...`

**Notes:** Behavior as expected. Clean error handling.

---

### **TC-002: Auto-Approval - Sales + Salesforce** ✅ PASS

**Execution Date:** Nov 26, 2025, 12:47 PM  
**Status:** PASS

**Test Data:**
- User: `sam.sales@company.demo`
- Role: Sales
- Software: Salesforce

**Actual Results:**
- Agent identified user: "Sam Sales, Role: Sales"
- Confirmed auto-approval based on policy
- Mentioned sending email to IT support
- Provided Request ID: 1002

**Server Logs Verification:**
```
[MOCK_SHEETS] find_employee_by_email: sam.sales@company.demo
[MOCK_SHEETS] find_policy_for_user: Salesforce, Sales
[MOCK_SHEETS] append_to_sheet: Audit_Log (Status=Approved)
[MOCK_GMAIL] To: it-support@company.demo Subject: Access Request Approved: Salesforce for Sam Sales
```

**Audit Log Confirmed:**
- Request_ID: 1002
- Status: Approved
- Software: Salesforce
- Timestamp: 2025-11-26T12:47:15

**Evidence:**
- Screenshot: `evidence/screenshots/tc002_auto_approval.png`
- Full conversation transcript saved

**Notes:** Perfect workflow execution. All tools called correctly.

---

### **TC-003: Manager Approval - Sales + GitHub** ✅ PASS

**Execution Date:** Nov 26, 2025, 12:49 PM  
**Status:** PASS

**Test Data:**
- User: `sam.sales@company.demo`
- Software: GitHub
- Manager: sales.manager@company.demo

**Actual Results:**
- Agent correctly identified manager approval needed
- Asked for confirmation before sending to manager
- Confirmed email sent to manager with CC to IT
- Provided Request ID: 1003
- Clear explanation of next steps

**Server Logs Verification:**
```
[MOCK_SHEETS] find_policy_for_user: GitHub, Sales (Requires_Manager_Approval=Yes)
[MOCK_SHEETS] find_manager_email: sam.sales@company.demo → sales.manager@company.demo
[MOCK_SHEETS] append_to_sheet: Status=Pending Manager
[MOCK_GMAIL] To: sales.manager@company.demo CC: it-support@company.demo
```

**Evidence:**
- Screenshots: Before/after confirmation
- Email log captured

**Notes:** Agent properly handled workflow branching. Professional communication.

---

### **TC-004: Policy Rejection - Sales + Figma** ✅ PASS

**Execution Date:** Nov 26, 2025, 12:51 PM  
**Status:** PASS

**Test Data:**
- User: `sam.sales@company.demo`
- Software: Figma (Design tool, not for Sales)

**Actual Results:**
- Agent politely explained Figma is not available for Sales role
- Mentioned it's for Design team
- Suggested contacting supervisor if business need exists
- Did NOT create access request
- Tone was professional, not dismissive

**Server Logs Verification:**
```
[MOCK_SHEETS] find_policy_for_user: Figma, Sales → No policy found
[MOCK_SHEETS] append_to_sheet: Status=Rejected
```

**Audit Log Confirmed:**
- Status: Rejected
- Notes: "No policy for role"
- No email sent (correct behavior)

**Notes:** Great handling of rejection scenario. Maintains user satisfaction while enforcing policy.

---

### **TC-005: Duplicate Request Detection** ✅ PASS

**Execution Date:** Nov 26, 2025, 12:53 PM  
**Status:** PASS

**Test Data:**
- User: `edna.eng@company.demo`
- Software: Figma
- Existing request: Pending Manager (Request ID: 1001)

**Actual Results:**
- Agent detected existing request
- Informed user: "I see you already have a pending request for Figma access"
- Provided existing request status and ID
- Did NOT create duplicate entry
- Suggested checking with manager about existing request

**Server Logs Verification:**
```
[MOCK_SHEETS] check_audit_log_for_duplicate: edna.eng@company.demo, Figma
Found existing request: ID=1001, Status=Pending Manager
```

**Audit Log Verified:**
- No new entry created (correct!)
- Existing entry preserved

**Notes:** Duplicate detection working perfectly. Prevents spam/confusion.

---

### **TC-006: Engineering Auto-Approval - GitHub** ✅ PASS

**Execution Date:** Nov 26, 2025, 12:55 PM  
**Status:** PASS

**Test Data:**
- User: `edna.eng@company.demo`
- Role: Engineering
- Software: GitHub

**Actual Results:**
- Auto-approved for Engineering role
- Different from Sales (which needs manager approval)
- Email sent to IT support
- Request ID: 1004

**Comparison Verified:**
- Sales + GitHub = Manager Approval (TC-003) ✅
- Engineering + GitHub = Auto-Approve (TC-006) ✅
- Role-based policy correctly enforced

**Server Logs Verification:**
```
[MOCK_SHEETS] find_policy_for_user: GitHub, Engineering (Requires_Manager_Approval=No)
[MOCK_SHEETS] append_to_sheet: Status=Approved
```

**Notes:** Demonstrates role-based access control working correctly.

---

### **TC-007: De-provisioning - Remove Access** ✅ PASS

**Execution Date:** Nov 26, 2025, 12:57 PM  
**Status:** PASS

**Test Data:**
- User: `sam.sales@company.demo`
- Action: Remove GitHub access

**Actual Results:**
- Agent recognized de-provisioning intent
- Logged as "Pending Deprovisioning"
- Sent confirmation request to manager
- Explained next steps to user

**Server Logs Verification:**
```
[MOCK_SHEETS] append_to_sheet: Request_Type=Revoke, Status=Pending Deprovisioning
[MOCK_GMAIL] To: sales.manager@company.demo Subject: Access Removal Request
```

**Audit Log Confirmed:**
- Request_Type: Revoke
- Status: Pending Deprovisioning
- Software: GitHub

**Notes:** De-provisioning workflow working correctly. Manager validation required.

---

## 🎯 Test Coverage Analysis

### Workflows Tested:

| Workflow | Test Case | Status |
|----------|-----------|--------|
| **A** - Auto-Approval | TC-002, TC-006 | ✅ ✅ |
| **B** - Manager Approval | TC-003 | ✅ |
| **C** - Policy Rejection | TC-004 | ✅ |
| **D** - New User Error | TC-001 | ✅ |
| **E** - De-provisioning | TC-007 | ✅ |
| **Duplicate Detection** | TC-005 | ✅ |

**All 5 core workflows + duplicate detection tested and passed!** ✅

---

## 🐛 Defects Found

**Total Defects:** 0

No defects identified during testing. All workflows performed as expected.

---

## 💡 Observations & Recommendations

### Positive Findings:

1. ✅ **Excellent Error Handling** - New user scenario handled gracefully
2. ✅ **Clear Communication** - Agent responses are professional and informative
3. ✅ **Accurate Tool Selection** - All appropriate tools called in correct order
4. ✅ **Audit Trail** - Complete logging of all actions
5. ✅ **Email Notifications** - Correct recipients for all scenarios

### Areas for Enhancement (Optional):

1. 💡 **Natural Language** - Could test more casual phrasings (future TC-008)
2. 💡 **Typo Handling** - Add tests for common misspellings (future TC-009)
3. 💡 **Multi-Request** - Test multiple requests in one session (future TC-011)

### Performance Notes:

- Average response time: ~2-3 seconds per turn
- No API rate limit issues observed
- Server remained stable throughout all tests

---

## 📸 Evidence & Artifacts

### Screenshots Captured:
- [ ] TC-001: New user error message
- [ ] TC-002: Auto-approval confirmation
- [ ] TC-003: Manager approval email
- [ ] TC-004: Policy rejection message
- [ ] TC-005: Duplicate detection
- [ ] TC-006: Engineering auto-approval
- [ ] TC-007: De-provisioning request

### Logs Saved:
- ✅ Server logs: `evidence/evaluation_results/server_logs_20251126_124500.log`
- ✅ Browser session recording: `evidence/videos/manual_test_demo.mp4` (if recorded)

### Additional Documentation:
- Test plan: `test/TEST_CASES.md`
- Troubleshooting guide: `test/TROUBLESHOOTING.md`
- Automated test results: `evidence/evaluation_results/evaluation_batch_results_*.json`

---

## ✅ Sign-Off

**Tester:** Laxmi Gunda  
**Date:** November 26, 2025  
**Signature:** _________________

**Test Manager/Reviewer:** _________________  
**Date:** _________________

**Comments:**
_______________________________________________________________________
_______________________________________________________________________

---

## 📋 Appendix

### Test Environment Details:

- **OS:** Windows 11
- **Python:** 3.11.x
- **Browser:** Chrome/Edge
- **Server:** FastAPI + Uvicorn
- **AI Model:** Google Gemini 2.5 Flash
- **Google ADK Version:** 1.18.0

### Test Data Summary:

| User | Role | Test Cases Used |
|------|------|-----------------|
| new.user@company.demo | N/A | TC-001 |
| sam.sales@company.demo | Sales | TC-002, TC-003, TC-004, TC-007 |
| edna.eng@company.demo | Engineering | TC-005, TC-006 |

---

**Report Version:** 1.0  
**Generated:** November 26, 2025  
**Next Review:** After automated test execution
