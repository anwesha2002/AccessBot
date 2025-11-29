# AccessBot Demo - Video Narration Script

**Duration:** ~6 minutes  
**Format:** Split screen (Browser left, Server logs right)  
**Pace:** Moderate - pause after each point for viewers to absorb

---

## 🎬 OPENING (0:00 - 0:30)

### **What to Show:**
- Both screens visible
- Server ready to start
- Browser ready to open

### **Script:**

> "Hi, I'm Vasav, and this is **AccessBot** - an intelligent IT access management agent I built for the Kaggle AI Agents Intensive Course capstone project.
> 
> AccessBot automates the entire IT access request workflow using **Google's Agent Development Kit**, or **ADK**, and the **Gemini AI model**. 
>
> Instead of employees waiting days for access approvals, AccessBot handles everything instantly - from auto-approving requests that meet company policy, to routing complex requests through proper approval chains, all while maintaining a complete audit trail.
>
> Today I'll demonstrate how it works by showing you **both** the user interface on the left, and the server logs on the right, so you can see exactly what's happening behind the scenes."

---

## 🚀 SETUP (0:30 - 1:00)

### **What to Show:**
- Starting the server
- Server logs initializing

### **Actions:**
```bash
python src/it_guardian_agent.py
```

### **Script:**

> "Let me start the server.
>
> [Type command]
>
> You can see in the server logs, it's initializing the **FastAPI** web server, loading the **Google ADK agent**, and connecting to our mock data sources - in this case, **Google Sheets** for the employee directory and access policies, and **Gmail** for notifications.
>
> [Point to logs showing initialization]
>
> The server is now running on **localhost port 8000**. Let me open the browser to the **FastAPI interactive documentation**."

### **Actions:**
- Open browser to http://127.0.0.1:8000/docs
- Show the /invoke endpoint

### **Script:**

> "This is FastAPI's built-in documentation interface. The key endpoint here is **/invoke** - this is how we send messages to the agent and get responses back. It's a **RESTful API** that maintains **session state** across multiple conversation turns.
>
> Now let me demonstrate the core workflows, starting with an error case."

---

## 📋 TEST CASE 1: New User - Employee Not Found (1:00 - 2:15)

### **What to Show:**
- Click "Try it out" on /invoke
- Type requests step by step

### **Script:**

> "**Test Case 1: New User Error Handling**
>
> First, I'll show what happens when someone who's not in our system tries to request access. This tests **error handling** and **data validation**.
>
> [Click Try it out]
>
> I'll send an initial greeting."

### **Actions:**
```json
{"text": "Hi"}
```

### **Script:**

> "[Send request]
>
> The agent responds professionally, asking for my email address. This is important - it **always verifies identity first** before processing any access requests.
>
> Now I'll provide an email that doesn't exist in our employee directory."

### **Actions:**
```json
{"text": "I am new.user@company.demo", "session_id": "PASTE_SESSION_ID"}
```

### **Script:**

> "[Send request]
>
> Watch the server logs on the right...
>
> [Point to logs]
>
> You can see the agent calling the **find_employee_by_email** tool - that's one of our custom Python functions decorated with the **@tool** decorator from Google ADK.
>
> It searches the employee directory... and finds nothing. The employee doesn't exist.
>
> [Point to browser response]
>
> Notice how the agent handles this gracefully. It doesn't crash or show an error - instead, it politely informs the user that the email isn't found and suggests they double-check it or contact HR. This demonstrates **robust error handling** and **user-friendly messaging**.
>
> This would trigger our **Workflow D** in a real scenario, where it would send an alert to IT and HR about a potential new employee inquiry."

---

## ✅ TEST CASE 2: Auto-Approval (2:15 - 3:45)

### **Script:**

> "**Test Case 2: Auto-Approval Workflow**
>
> Now let me show the most common scenario - an **auto-approved** access request.
>
> I'll start a new conversation as Sam Sales, a sales team member requesting Salesforce access."

### **Actions:**
New conversation - click "Try it out" again

```json
Turn 1: {"text": "Hi"}
Turn 2: {"text": "I am sam.sales@company.demo", "session_id": "..."}
Turn 3: {"text": "I need access", "session_id": "..."}
Turn 4: {"text": "Salesforce", "session_id": "..."}
```

### **Script:**

> "[After Turn 2]
>
> Great - the agent found Sam Sales in the employee directory. You can see in the logs it's calling **find_employee_by_email** again, and this time it returns successfully - Role: Sales.
>
> [After asking for software]
>
> Now I'll specify Salesforce.
>
> [Send Turn 4]
>
> This is where it gets interesting. Watch the server logs carefully...
>
> [Point to logs]
>
> **First**, the agent calls **find_policy_for_user** with the parameters Software_Name equals Salesforce and Role equals Sales. This queries our access policy database.
>
> The policy comes back as 'No manager approval required' - that means this can be **auto-approved**.
>
> **Second**, you see **append_to_audit_log** being called. This is creating an **immutable audit trail** - it logs Request ID 1002, Status: Approved, Software: Salesforce, with a timestamp. This is critical for compliance and security audits.
>
> **Third**, the **send_gmail** tool is called - sending an automated email to IT support at it-support@company.demo with the subject 'Access Request Approved: Salesforce for Sam Sales.'
>
> [Point to browser]
>
> And in the browser, the agent confirms everything - tells the user the request is approved, mentions the email to IT, and provides the Request ID for tracking.
>
> All of this happened in **real-time** - no human intervention required. That's the power of **AI-driven automation** with proper **tool orchestration**."

---

## 📧 TEST CASE 3: Manager Approval Required (3:45 - 5:15)

### **Script:**

> "**Test Case 3: Manager Approval Workflow**
>
> Not all requests can be auto-approved. Let me show you what happens when **manager approval is required**.
>
> Same user - Sam Sales - but this time requesting GitHub access."

### **Actions:**
Continue same session or start new:
```json
{"text": "I also need GitHub access", "session_id": "..."}
```
OR start fresh with sam.sales and request GitHub

### **Script:**

> "[Send request]
>
> Notice the difference in the server logs...
>
> [Point to logs]
>
> The **find_policy_for_user** tool is called again - Software: GitHub, Role: Sales.
>
> But this time, the policy states 'Requires_Manager_Approval: Yes' - this is a **conditional approval workflow**.
>
> Watch what the agent does...
>
> [Point to browser]
>
> It asks for confirmation - 'Would you like me to send this to your manager for approval?' This is the agent being **conversational** and **user-friendly**.
>
> I'll confirm yes.
>
> [Send "Yes, please send it"]
>
> Now look at the logs again...
>
> [Point to logs]
>
> **First**, it calls **find_manager_email** to look up Sam's manager - sales.manager@company.demo.
>
> **Second**, it logs to the audit trail with Status: 'Pending Manager Approval' - a different status than before.
>
> **Third**, the **send_gmail** tool is called, but notice the recipients - To: sales.manager@company.demo, with a CC to it-support@company.demo. The email subject is different too: 'Access Request Requires Your Approval.'
>
> This demonstrates **workflow branching** - the same agent handles **different approval paths** based on policy rules. It's not just executing a script; it's making **intelligent routing decisions** based on the context.
>
> In the browser, you can see the agent clearly communicates this to the user - explains that manager approval is needed, confirms the email was sent, and provides the Request ID.
>
> This is **Workflow B** - one of our five core workflows."

---

## 🔍 TEST CASE 4: Duplicate Detection (5:15 - 6:15)

### **Script:**

> "**Test Case 4: Duplicate Request Prevention**
>
> Finally, let me show you a critical feature - **duplicate detection**.
>
> I'll request access as Edna Engineer for Figma - but there's already a pending request for this in our system."

### **Actions:**
New conversation:
```json
Turn 1: {"text": "Hi"}
Turn 2: {"text": "edna.eng@company.demo", "session_id": "..."}
Turn 3: {"text": "I need Figma access", "session_id": "..."}
```

### **Script:**

> "[After Turn 3]
>
> Watch the server logs carefully...
>
> [Point to logs]
>
> Before doing anything else, the agent calls **check_audit_log_for_duplicate** - this searches for existing requests with the same employee email and software name.
>
> It finds one! Request ID 1001, Status: Pending Manager, for Figma.
>
> [Point to browser]
>
> See how the agent handles this - it doesn't create a duplicate request. Instead, it **informs the user** about the existing request, tells them the status, and suggests they follow up with their manager.
>
> This prevents **request spam**, **audit log pollution**, and **user confusion**. It's a perfect example of the agent being **contextually aware** and **proactive**.
>
> Notice in the server logs - **no new audit entry was created**, **no email was sent**. The agent intelligently recognized the duplicate and took the appropriate action.
>
> This demonstrates **stateful awareness** - the agent isn't just responding to individual messages; it's checking the **entire system state** before taking action."

---

## 🎯 CLOSING (6:15 - 6:45)

### **Script:**

> "So that's **AccessBot** in action. 
>
> What you've seen today:
>
> - **Robust error handling** for invalid users
> - **Auto-approval workflows** with full audit trails  
> - **Conditional routing** for manager approvals
> - **Duplicate detection** to prevent issues
> 
> This agent uses **Google's Agent Development Kit** with **custom Python tools**, **session management** for multi-turn conversations, and **LLM-powered intelligence** from the Gemini 2.5 Flash model.
>
> Every action is **logged for compliance**, every email is **automatically sent**, and every decision is based on **company policy rules** - all happening in real-time with zero human intervention.
>
> The complete source code, documentation, automated test suite, and my detailed contributions are all available on GitHub. The link is in the description.
>
> Thanks for watching, and I hope this demonstrated not just what AccessBot does, but **how it does it**!"

---

## 📝 VISUAL CUES GUIDE

### **Throughout the Video:**

**When Pointing to Browser:**
- Use cursor to circle around key text
- Hover over request/response areas
- Highlight where agent asks questions vs. provides answers

**When Pointing to Server Logs:**
- Scroll to show the specific log line
- Let it sit on screen for 2-3 seconds
- Use cursor to underline tool names like `[MOCK_SHEETS]` and `[MOCK_GMAIL]`

**Technical Terms to Emphasize:**
- Speak slightly slower for these words
- **Google ADK** (Agent Development Kit)
- **FastAPI** and **RESTful API**
- **Session state** and **multi-turn conversations**
- **Tool orchestration**
- **Audit trail** and **immutable logging**
- **Workflow branching** and **conditional logic**
- **Gemini 2.5 Flash** (the LLM model)

---

## ⏱️ TIMING GUIDE

| Section | Duration | Purpose |
|---------|----------|---------|
| Introduction | 0:30 | Hook viewers, explain project |
| Setup | 0:30 | Show tech stack |
| TC-1: Error Handling | 1:15 | Demonstrate robustness |
| TC-2: Auto-Approval | 1:30 | Show main workflow |
| TC-3: Manager Approval | 1:30 | Show complexity handling |
| TC-4: Duplicate Detection | 1:00 | Show intelligence |
| Closing | 0:30 | Summarize, call to action |
| **TOTAL** | **~6:45** | **Perfect length!** |

---

## 🎤 DELIVERY TIPS

### **Pace:**
- Speak at **~120-140 words per minute** (moderate pace)
- **Pause for 2 seconds** after showing a key log
- **Breathe** between concepts

### **Tone:**
- **Enthusiastic** but professional
- **Confident** but not arrogant  
- **Educational** - you're teaching, not just showing

### **Energy:**
- Start with **high energy** in intro
- **Moderate energy** during demos (focus on clarity)
- **Positive energy** in closing

### **Variations:**
- Use **higher pitch** for questions: "Would you like me to send this...?"
- Use **lower, confident tone** for conclusions: "All happening in real-time..."
- Use **emphasis** on technical terms: "**Google ADK**, **tool orchestration**"

---

## ✅ PRE-RECORDING CHECKLIST

- [ ] Print this script or have it on another device
- [ ] Practice reading through once
- [ ] Test microphone levels
- [ ] Have water nearby
- [ ] Close all notifications
- [ ] Clear throat
- [ ] Take a deep breath
- [ ] Smile (it affects your voice tone!)

---

## 💡 AD-LIB ALLOWANCES

Feel free to add these natural fillers:

✅ **Good:**
- "You can see here..."
- "Notice how..."
- "This is interesting because..."
- "In the real world, this means..."

❌ **Avoid:**
- "Um..." or "Uh..."
- "So yeah..."
- Long pauses (edit them out)
- Apologies ("sorry if this doesn't make sense")

---

**You've got this! This script will make you sound professional, knowledgeable, and well-prepared. Good luck with your recording!** 🎬🚀
