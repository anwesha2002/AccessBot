# AccessBot - PowerPoint Slide Deck Outline
**For Kaggle Capstone Demo Video (3 minutes)**

---

## 🎯 Slide Deck Structure (9 Slides Total)

### **Slide 1: TITLE SLIDE** (0:00-0:05)

**Layout:** Title Slide

**Content:**
```
Title (Large, Bold):
AccessBot
Intelligent IT Access Management

Subtitle:
Powered by Google Agent Development Kit & Gemini AI

Bottom Right:
Kaggle 5-Day AI Agents Intensive Course
Capstone Project
```

**Visual:**
- Clean, professional design
- Blue/Green color scheme
- Optional: Small robot or AI icon

**Speaker Notes:**
> "Hi, I'm Laxmi Gunda, and this is AccessBot..."

---

### **Slide 2: THE PROBLEM** (0:05-0:30)

**Layout:** Title and Content

**Title:** The Problem: IT Access Bottleneck

**Content (Left Side - Text):**
```
❌ Manual IT access workflows are:
• Slow (days or weeks of waiting)
• Inefficient (repetitive manual work)
• Frustrating (bottlenecks everywhere)

Impact:
• New employees can't be productive
• IT teams are overwhelmed
• Managers waste time on routine approvals
```

**Content (Right Side - Visual):**
- Simple flowchart showing: 
  - Employee → Ticket → Wait → IT → Wait → Manager → Wait → Access
  - Clock icons showing "Days/Weeks"
  
**Speaker Notes:**
> "In most organizations, employees spend days or even weeks waiting for software access approvals. A new sales hire needs Salesforce? Submit a ticket. Wait for IT. Wait for manager approval..."

---

### **Slide 3: WHY AI AGENTS?** (0:30-1:00)

**Layout:** Title and Content (2 Columns)

**Title:** Why AI Agents? Intelligence Beyond Automation

**Content:**

**Column 1 - Simple Automation:**
```
🤖 Traditional Scripts:
• Fixed rules only
• Can't understand context
• No reasoning capability
• Breaks on edge cases
```

**Column 2 - AI Agents:**
```
🧠 AccessBot Agent:
• Understands natural language
• Makes policy decisions
• Handles edge cases intelligently
• Maintains conversation context
```

**Bottom (Highlighted Box):**
```
AI Agents = Automation + Intelligence + Reasoning
```

**Speaker Notes:**
> "Why use an AI agent instead of a simple automation script? Because access requests aren't simple. They require understanding natural language, making policy decisions, handling edge cases..."

---

### **Slide 4: ARCHITECTURE OVERVIEW** (1:00-1:30)

**Layout:** Title and Content (Visual Heavy)

**Title:** AccessBot Architecture

**Content:**
- **USE THE DIAGRAM FROM ARCHITECTURE_DIAGRAM_GUIDE.md**
- Or simplified version showing:
  - User at top
  - Agent in middle (Gemini 2.5 Flash)
  - 5 Tools below
  - Data sources at bottom

**Side Panel (Right):**
```
Key Components:
✓ Gemini 2.5 Flash LLM
✓ 5 custom Python tools
✓ FastAPI REST API
✓ Session management
✓ Complete audit trail
```

**Workflow Indicators:**
- Green: Auto-Approve
- Yellow: Manager Approval
- Red: Policy Rejection

**Speaker Notes:**
> "Here's how AccessBot works. At the core, we have the Gemini 2.5 Flash LLM - this is the brain. Around it, we have 5 custom Python tools..."

---

### **Slide 5: DEMO TITLE** (1:30)

**Layout:** Section Header

**Content:**
```
Live Demo
AccessBot in Action
```

**Visual:**
- Simple, clean slide
- Maybe a "play" icon or "live demo" graphic

**Speaker Notes:**
> "Let me show you AccessBot in action."

**Note:** This is a transition slide - very brief (5 seconds)

---

### **Slide 6: DEMO - SCREEN RECORDING** (1:30-2:10)

**Layout:** Blank Slide (Full Screen)

**Content:**
- **EMBEDDED VIDEO** or **LIVE DEMO**
- Split screen showing:
  - Browser on left (FastAPI /docs)
  - Server logs on right

**Scenarios to Show:**
1. Auto-Approval (Sales + Salesforce) - 20 seconds
2. Duplicate Detection - 20 seconds

**OR - Alternative if not embedding video:**
- Screenshots showing:
  - Slide 6a: Browser request
  - Slide 6b: Server logs highlighting tools
  - Slide 6c: Agent response

**Speaker Notes:**
> "Scenario 1: Auto-Approval. I'm requesting Salesforce access as a Sales user. Watch the server - the agent finds my employee record, checks the policy..."

---

### **Slide 7: THE BUILD - Technology Stack** (2:10-2:35)

**Layout:** Title and Content (Icon Grid)

**Title:** How We Built AccessBot

**Content (2x2 Grid with Icons/Logos):**

```
┌─────────────────┬─────────────────┐
│  Google ADK     │  Gemini 2.5     │
│  Agent          │  Flash LLM      │
│  Framework      │  Intelligence   │
├─────────────────┼─────────────────┤
│  FastAPI        │  Python 3.x     │
│  REST API       │  Tools & Logic  │
└─────────────────┴─────────────────┘
```

**Bottom Section:**
```
Key Features Implemented:
✓ All 5 workflows (A-E) + duplicate detection
✓ Session management across conversation turns
✓ Tool orchestration with intelligent selection
✓ Complete observability and audit logging
✓ LLM-as-Judge automated evaluation
```

**Speaker Notes:**
> "How we built this: Technology Stack - Google Agent Development Kit, Gemini 2.5 Flash, FastAPI, Python..."

---

### **Slide 8: THE BUILD - Implementation Highlights** (2:35-2:50)

**Layout:** Title and Content (Bullet List)

**Title:** Implementation Highlights

**Content:**
```
🛠️ What Makes AccessBot Special:

✓ 5 Custom Python Tools
  • find_employee_by_email - validates users
  • find_policy_for_user - checks policies
  • check_audit_log_for_duplicate - prevents spam
  • append_to_audit_log - maintains compliance
  • send_gmail - automates notifications

✓ Intelligent Decision Making
  • Auto-approve when policy allows
  • Route to manager when approval needed
  • Reject with helpful explanation when not allowed
  • Detect and handle duplicates

✓ Production Ready
  • Complete test suite with API rate limit handling
  • Comprehensive documentation
  • Deployed as REST API (A2A compatible)
```

**Speaker Notes:**
> "We implemented all 5 workflows - auto-approval, manager approval, policy rejection, new user handling, and de-provisioning - plus duplicate detection..."

---

### **Slide 9: CLOSING** (2:50-3:00)

**Layout:** Title and Content

**Title:** AccessBot: Intelligence + Automation + Compliance

**Content:**
```
Key Takeaways:

🤖 AI Agents are Intelligent Orchestrators
   Not just automation - reasoning about policies,
   maintaining context, and making smart decisions

✅ Real Business Impact
   • Instant approvals vs. days of waiting
   • Zero manual intervention for routine requests
   • Complete audit trail for compliance

🔗 Open Source
   Complete code, documentation, and test results
   on GitHub
```

**Bottom:**
```
github.com/anwesha2002/AccessBot

Thank You!
```

**Speaker Notes:**
> "AccessBot demonstrates that AI agents aren't just chatbots - they're intelligent orchestrators that can understand complex policies, make autonomous decisions, maintain compliance, and scale instantly..."

---

## 🎨 Design Guidelines

### **Color Scheme:**
- **Primary:** Blue (#2196F3) - Technology, trust
- **Secondary:** Green (#4CAF50) - Success, approval
- **Accent:** Orange (#FF9800) - Warning, attention
- **Background:** White or very light gray (#F5F5F5)

### **Fonts:**
- **Titles:** Arial Bold, 44pt
- **Subtitles:** Arial, 32pt
- **Body Text:** Arial, 24pt
- **Bullet Points:** Arial, 20pt

### **Layout Tips:**
- Use **consistent margins** (1 inch on all sides)
- **Align left** for bullet points
- **Center** for titles and key callouts
- **White space** is your friend - don't overcrowd

### **Icons/Visuals:**
- Use simple, flat icons (PowerPoint has built-in icons)
- Stick to 2-3 colors max per icon
- Make sure visuals support the message, not distract

---

## 📹 Recording Tips

### **Option 1: Record PowerPoint Directly**
1. PowerPoint → Slide Show → Record Slide Show
2. Narrate as you advance slides
3. Export as video (File → Export → Create Video)

**Pros:** Easy, built-in  
**Cons:** Less flexible

### **Option 2: Use OBS to Record Presentation**
1. Open PowerPoint in presentation mode
2. Open OBS and capture window
3. Record yourself presenting
4. Advance slides manually as you narrate

**Pros:** More control, can edit later  
**Cons:** Requires OBS setup

### **Option 3: Pre-record Demo, Embed in Slide**
1. Record your live demo separately
2. Embed video in Slide 6
3. Present the entire deck with embedded demo

**Pros:** Best quality demo  
**Cons:** Need video editing

---

## ⏱️ Slide Timing Guide

| Slide # | Topic | Duration | Cumulative |
|---------|-------|----------|------------|
| 1 | Title | 5s | 0:05 |
| 2 | Problem | 25s | 0:30 |
| 3 | Why Agents | 30s | 1:00 |
| 4 | Architecture | 30s | 1:30 |
| 5 | Demo Title | 5s | 1:35 |
| 6 | Demo | 40s | 2:15 |
| 7 | Tech Stack | 20s | 2:35 |
| 8 | Implementation | 15s | 2:50 |
| 9 | Closing | 10s | 3:00 |

---

## ✅ Creation Checklist

- [ ] Create all 9 slides in PowerPoint/Google Slides
- [ ] Add architecture diagram to Slide 4
- [ ] Prepare demo recording or screenshots for Slide 6
- [ ] Apply consistent color scheme
- [ ] Add speaker notes to each slide
- [ ] Practice presentation 2-3 times
- [ ] Time yourself (should be ~3:00)
- [ ] Export as PDF backup
- [ ] Record final video

---

## 🚀 Quick Start

**To create this presentation fast:**

1. **Open PowerPoint** (or Google Slides)
2. **Create 9 blank slides**
3. **Follow this guide slide-by-slide**
4. **Use built-in layouts** (Title Slide, Title and Content, etc.)
5. **Copy-paste the content** from this guide
6. **Add visuals** from PowerPoint's built-in icons/images
7. **Practice once**, then **record**

**Total creation time: 45-60 minutes**

---

## 💡 Pro Tips

1. **Keep it simple** - Don't overdesign
2. **Use animations sparingly** - Maybe just fade-in for bullet points
3. **Test readability** - View at 50% zoom to check text size
4. **Have a backup** - Save as PDF in case of tech issues
5. **Practice transitions** - Know exactly when to advance each slide

---

**This slide deck follows your narration script exactly - each slide matches a section of your CAPSTONE_DEMO_SCRIPT.md!** 🎬
