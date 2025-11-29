# AccessBot - Kaggle Capstone Demo Video Script
**Duration:** 3 minutes  
**Format:** Problem → Agents → Architecture → Demo → Build

---

## 🎬 OPENING: Problem Statement (0:00 - 0:30)

### **Visual:**
- Screen showing a typical email inbox flooded with IT access requests
- OR: Simple diagram showing employees waiting for access

### **Script:**

> "In most organizations, employees spend **days or even weeks** waiting for software access approvals. 
>
> A new sales hire needs Salesforce? Submit a ticket. Wait for IT. Wait for manager approval. Eventually get access - maybe.
>
> Meanwhile, productivity suffers. IT teams are overwhelmed with repetitive requests. Managers are bottlenecked approving routine access. And employees are stuck waiting.
>
> **The problem:** Manual IT access workflows are slow, inefficient, and don't scale.
>
> This is what we set out to solve with **AccessBot**."

---

## 🤖 WHY AGENTS? (0:30 - 1:00)

### **Visual:**
- Simple comparison: Human workflow (slow, manual) vs. Agent workflow (instant, automated)

### **Script:**

> "Why use an AI agent instead of a simple automation script?
>
> Because access requests aren't simple. They require **intelligence**:
>
> - **Understanding natural language** - 'I need Salesforce' versus 'Grant me access to the CRM system'
> - **Making policy decisions** - Does this role get auto-approved, or does it need manager approval?
> - **Handling edge cases** - What if the user doesn't exist? What if they already requested this?
> - **Maintaining conversation** - Asking follow-up questions when information is missing.
>
> An agent can **reason** about company policy, **orchestrate** multiple tools, and provide a **conversational** experience - all in real-time.
>
> That's the power of Google's Agent Development Kit with Gemini AI."

---

## 🏗️ ARCHITECTURE (1:00 - 1:30)

### **Visual:**
- Architecture diagram showing:
  - User → Agent → Tools → Data Sources
  - Workflow branches (auto-approve, manager approval, rejection)

### **Script:**

> "Here's how AccessBot works.
>
> [Point to diagram]
>
> **At the core**, we have the **Gemini 2.5 Flash LLM** - this is the brain that understands user requests and makes decisions.
>
> **Around it**, we have **5 custom Python tools** built with Google ADK:
> - **find_employee_by_email** - validates users
> - **find_policy_for_user** - checks access policies  
> - **check_audit_log_for_duplicate** - prevents duplicate requests
> - **append_to_audit_log** - maintains compliance trail
> - **send_gmail** - automates notifications
>
> The agent **orchestrates** these tools based on conversation context.
>
> It's deployed as a **FastAPI REST API**, making it an A2A-compatible service that can integrate with any system.
>
> And every decision, every action, is **logged for audit and compliance**."

---

## 🎥 DEMO (1:30 - 2:15)

### **Visual:**
- Split screen: Browser (left) + Server logs (right)
- OR: Just browser with picture-in-picture of logs

### **Script:**

> "Let me show you AccessBot in action.
>
> **Scenario 1: Auto-Approval**
>
> [Type in browser]
>
> I'm requesting Salesforce access as a Sales user.
>
> [Point to logs]
>
> Watch the server - the agent finds my employee record, checks the policy, sees Sales + Salesforce is auto-approved, logs it to the audit trail, and sends an email to IT.
>
> [Point to browser]
>
> Instant approval. No waiting. No tickets.
>
> **Scenario 2: Duplicate Detection**
>
> [New request]
>
> Now I'll request something I already have pending.
>
> [Show result]
>
> The agent **intelligently** detects the duplicate, tells me about my existing request, and prevents creating duplicate entries.
>
> **That's intelligence.** Not just automation - **reasoning** about system state and making smart decisions."

---

## 🛠️ THE BUILD (2:15 - 2:50)

### **Visual:**
- Quick montage of:
  - Code editor showing tool definitions
  - FastAPI docs interface
  - Test results

### **Script:**

> "How we built this:
>
> **Technology Stack:**
> - **Google Agent Development Kit (ADK)** - the agent framework
> - **Gemini 2.5 Flash** - our LLM for intelligence
> - **FastAPI** - for the REST API deployment
> - **Python** - for custom tool development
>
> **Key Implementation Features:**
> - **Session management** - the agent remembers context across conversation turns
> - **Tool orchestration** - automatic selection and chaining of tools based on user intent
> - **Observability** - complete logging and tracing for debugging
> - **LLM-as-Judge evaluation** - automated testing of all workflows
>
> We implemented **all 5 workflows** - auto-approval, manager approval, policy rejection, new user handling, and de-provisioning - plus duplicate detection.
>
> Complete with a **comprehensive test suite**, handling API rate limits, and full documentation."

---

## 🎯 CLOSING (2:50 - 3:00)

### **Visual:**
- GitHub repo page
- Or: Simple slide with project name and link

### **Script:**

> "AccessBot demonstrates that AI agents aren't just chatbots - they're **intelligent orchestrators** that can:
> - Understand complex policies
> - Make autonomous decisions  
> - Maintain compliance
> - Scale instantly
>
> All the code, documentation, and test results are on GitHub.
>
> Thank you!"

---

## 📊 TIMING BREAKDOWN

| Section | Duration | Purpose |
|---------|----------|---------|
| Problem Statement | 30s | Hook + Context |
| Why Agents? | 30s | Justify approach |
| Architecture | 30s | Technical overview |
| Demo | 45s | Proof it works |
| The Build | 35s | Tech stack + features |
| Closing | 10s | Call to action |
| **TOTAL** | **3:00** | **Perfect!** |

---

## 🎨 VISUAL REQUIREMENTS

### **Slides You'll Need:**

1. **Title Slide**: "AccessBot - Intelligent IT Access Management"
2. **Problem Slide**: Stats or visual showing IT bottleneck
3. **Agent Value Slide**: Why agents > simple automation
4. **Architecture Diagram**: User → Agent → Tools → Data
5. **Demo**: Live browser + server logs
6. **Tech Stack Slide**: Logos/names of Google ADK, Gemini, FastAPI, Python
7. **Closing Slide**: GitHub link

### **Architecture Diagram Elements:**

```
┌─────────────┐
│    User     │
│ (Browser)   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│   AccessBot Agent       │
│   (Gemini 2.5 Flash)    │
└──────┬──────────────────┘
       │
       ├──► find_employee_by_email
       ├──► find_policy_for_user
       ├──► check_audit_log_for_duplicate
       ├──► append_to_audit_log
       └──► send_gmail
              │
              ▼
       ┌──────────────┐
       │ Data Sources │
       │ (Sheets/DB)  │
       └──────────────┘
```

**Workflow Branches:**
- Auto-Approve → Green arrow
- Manager Approval → Yellow arrow  
- Rejection → Red arrow

---

## 🎤 DELIVERY TIPS FOR 3-MINUTE FORMAT

### **Pace:**
- **Fast but clear** - this is condensed!
- No long pauses - keep moving
- Practice to hit exactly 3:00

### **Energy:**
- **High energy** - you have limited time to make an impact
- **Confident** - you know this project inside-out
- **Enthusiastic** - show passion for the problem you solved

### **Visual Transitions:**
- Use slide transitions to signal section changes
- Don't linger on any single visual too long
- Demo should be the longest visual section (45s)

---

## 💡 PRO TIPS

### **Recording Strategy:**

**Option 1: All Slides + Demo Insert**
- Record slides with narration
- Insert demo recording at the demo section
- Edit together in video editor

**Option 2: Live Recording**
- Have slides on one monitor
- Browser on another
- Record both, switch focus as you narrate

**Option 3: Presentation Software**
- Use PowerPoint/Google Slides
- Embed demo video in the demo slide
- Record entire presentation

### **What to Emphasize:**

✅ **DO emphasize:**
- The PROBLEM (everyone relates to slow IT tickets)
- The INTELLIGENCE (not just automation)
- The DEMO (proof it works)
- Google ADK (it's a capstone requirement)

❌ **DON'T emphasize:**
- Deep technical details (no time!)
- Individual code snippets
- Every single feature

### **Time Savers:**

If running over 3 minutes:
- Cut 5-10 seconds from Problem (just state it, move on)
- Reduce Architecture to 20s (just show diagram, mention tools)
- Keep Demo at 45s (this is your proof!)
- Cut 5s from Build (just list tech stack)

---

## ✅ PRE-RECORDING CHECKLIST

- [ ] Create architecture diagram
- [ ] Prepare demo (pre-record or practice live)
- [ ] Create slides for each section
- [ ] Practice entire script 2-3 times
- [ ] Time yourself (should be ≤ 3:00)
- [ ] Test all visual transitions
- [ ] Set up recording environment (OBS, lighting, audio)
- [ ] Have water nearby
- [ ] Close notifications
- [ ] Take deep breath and GO! 🎬

---

**This script is optimized for maximum impact in minimal time. Focus on clarity, energy, and showing that agents provide UNIQUE value beyond simple automation!** 🚀
