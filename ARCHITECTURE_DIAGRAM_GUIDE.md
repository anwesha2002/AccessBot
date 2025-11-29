# AccessBot Architecture Diagram - Creation Guide

## 📐 Visual Architecture Diagram

### Text-Based Version (Use This as Reference)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
│                        USER LAYER                          │
│                                                             │
│                    ┌─────────────────┐                     │
│                    │   👤 Employee   │                     │
│                    │  (Web Browser)  │                     │
│                    └────────┬────────┘                     │
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                              │
                              │ HTTP POST /invoke
                              │ (JSON Request/Response)
                              ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
│                      AGENT LAYER                           │
│                                                             │
│              ┌─────────────────────────────┐               │
│              │     🤖 AccessBot Agent      │               │
│              │                              │               │
│              │   Powered by Gemini 2.5     │               │
│              │        Flash LLM            │               │
│              │                              │               │
│              │   • Session Management      │               │
│              │   • Tool Orchestration      │               │
│              │   • Policy Reasoning        │               │
│              └──────────┬──────────────────┘               │
┗━━━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                         │
                         │ Calls Tools Based on Context
                         │
        ┌────────────────┼────────────────┬────────────┐
        │                │                │            │
        ▼                ▼                ▼            ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
│                      TOOL LAYER                            │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   📋 Tool 1  │  │   🔍 Tool 2  │  │   ✅ Tool 3  │    │
│  │              │  │              │  │              │    │
│  │  find_       │  │  find_       │  │  check_      │    │
│  │  employee_   │  │  policy_     │  │  audit_log_  │    │
│  │  by_email    │  │  for_user    │  │  for_dup     │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐                       │
│  │   📝 Tool 4  │  │   ✉️ Tool 5  │                       │
│  │              │  │              │                       │
│  │  append_to_  │  │  send_       │                       │
│  │  audit_log   │  │  gmail       │                       │
│  └──────────────┘  └──────────────┘                       │
┗━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                      │         │
                      │         │
        ┌─────────────┼─────────┼──────────────┐
        │             │         │              │
        ▼             ▼         ▼              ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
│                    DATA LAYER                              │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   📊 Sheets  │  │   📊 Sheets  │  │   📊 Sheets  │    │
│  │              │  │              │  │              │    │
│  │  Employee    │  │   Access     │  │   Audit      │    │
│  │  Directory   │  │   Policies   │  │   Log        │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                             │
│                    ┌──────────────┐                        │
│                    │   ✉️ Gmail   │                        │
│                    │              │                        │
│                    │ Notifications│                        │
│                    └──────────────┘                        │
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


═══════════════════════════════════════════════════════════
                    WORKFLOW BRANCHES
═══════════════════════════════════════════════════════════

From Agent to Decision:

    ┌─────────────┐
    │ Policy      │
    │ Decision    │
    └──────┬──────┘
           │
    ┌──────┴──────┬──────────────┬──────────────┐
    │             │              │              │
    ▼             ▼              ▼              ▼
┌────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  Auto  │   │ Manager │   │ Policy  │   │  Error  │
│Approve │   │Approval │   │Reject   │   │ Handle  │
│  ✅    │   │   ⏳    │   │   ❌    │   │   ⚠️    │
└────────┘   └─────────┘   └─────────┘   └─────────┘
  GREEN        YELLOW         RED          ORANGE

```

---

## 🎨 How to Create This in PowerPoint/Google Slides

### Step 1: Set Up Canvas
1. Create new slide
2. Use **Blank** layout
3. Set background to white or light gray

### Step 2: Create Layers (Top to Bottom)

#### **USER LAYER (Top)**
```
1. Insert → Shapes → Rectangle
2. Fill: Light Blue (#E3F2FD)
3. Border: Blue (#2196F3)
4. Text: "USER LAYER"
5. Add User Icon (Insert → Icons → search "user")
6. Text below: "Employee (Web Browser)"
```

#### **AGENT LAYER (Middle)**
```
1. Insert → Shapes → Rectangle (larger)
2. Fill: Light Green (#E8F5E9)
3. Border: Green (#4CAF50)
4. Text: "AGENT LAYER"
5. Inside: Add another rectangle
   - Text: "AccessBot Agent"
   - Subtext: "Powered by Gemini 2.5 Flash"
   - Add robot emoji or AI icon
```

#### **TOOL LAYER**
```
1. Insert → Shapes → Rectangle (wide)
2. Fill: Light Yellow (#FFF9C4)
3. Border: Orange (#FFC107)
4. Text: "TOOL LAYER"
5. Inside: Add 5 smaller rectangles in a row
   - Each with tool name
   - Different colored borders (blue, green, yellow, orange, red)
```

#### **DATA LAYER (Bottom)**
```
1. Insert → Shapes → Rectangle
2. Fill: Light Gray (#F5F5F5)
3. Border: Gray (#9E9E9E)
4. Text: "DATA LAYER"
5. Add 4 boxes for data sources
   - Google Sheets icons (3 boxes)
   - Gmail icon (1 box)
```

### Step 3: Add Arrows
```
1. Insert → Shapes → Block Arrow (or simple arrow)
2. Draw from User → Agent
3. Draw from Agent → Tools (one arrow that splits into 5)
4. Draw from Tools → Data sources
5. Color code arrows:
   - Main flow: Black or dark gray
   - Workflow branches: Green, Yellow, Red
```

### Step 4: Add Workflow Branches (Right Side)
```
1. Create 4 small boxes on the right
2. Label them:
   - "Auto-Approve ✅" (Green)
   - "Manager Approval ⏳" (Yellow)
   - "Policy Rejection ❌" (Red)
   - "Error Handling ⚠️" (Orange)
3. Add arrows from Agent to each
```

### Step 5: Polish
```
- Align all elements neatly
- Make sure text is readable
- Use consistent font (Arial or Calibri, 14-18pt)
- Add subtle shadows to boxes (optional)
```

---

## 🎨 How to Create in Canva (Even Easier!)

### Quick Method:
1. Go to **Canva.com**
2. Search: **"System Architecture Diagram"** template
3. Pick any template you like
4. Replace their boxes with:
   - Top: User
   - Middle: Agent (Gemini)
   - Tools: 5 boxes with tool names
   - Bottom: Data sources
5. Update text and colors
6. Download as PNG

**Time: 15 minutes!**

---

## 🎨 Color Scheme Recommendations

| Layer | Background | Border | Text |
|-------|-----------|--------|------|
| User | Light Blue #E3F2FD | Blue #2196F3 | Dark Gray |
| Agent | Light Green #E8F5E9 | Green #4CAF50 | Dark Gray |
| Tools | Light Yellow #FFF9C4 | Orange #FFC107 | Dark Gray |
| Data | Light Gray #F5F5F5 | Gray #9E9E9E | Dark Gray |

**Workflow Colors:**
- ✅ Auto-Approve: Green #4CAF50
- ⏳ Manager Approval: Yellow #FFC107
- ❌ Rejection: Red #F44336
- ⚠️ Error: Orange #FF9800

---

## 📐 Exact Dimensions (for PowerPoint)

**Slide Size:** 10" x 7.5" (standard)

**Box Sizes:**
- User Box: 8" wide × 1.5" tall
- Agent Box: 8" wide × 2" tall
- Tools Box: 8" wide × 2.5" tall
- Data Box: 8" wide × 2" tall

**Spacing:** 0.3" between layers

**Arrow width:** 0.2"

---

## 💡 Pro Tips

1. **Use Gridlines** (View → Gridlines) to align everything perfectly
2. **Group elements** (Ctrl+G) once positioned
3. **Save as PNG** with transparent background if possible
4. **Test readability** - zoom out to 50% and check if text is readable

---

## ✅ Checklist for Your Diagram

- [ ] 4 clear horizontal layers (User, Agent, Tools, Data)
- [ ] Agent box mentions "Gemini 2.5 Flash"
- [ ] 5 tool boxes clearly labeled
- [ ] Arrows show flow from top to bottom
- [ ] Workflow branches visible (Auto, Manager, Reject)
- [ ] Color coded for clarity
- [ ] All text is readable
- [ ] Professional appearance

---

## 🎯 Minimum Viable Diagram

**If you're really short on time, just make:**

1. **3 boxes vertically:**
   - Top: "User"
   - Middle: "AccessBot Agent (Gemini 2.5 Flash)"
   - Bottom: "5 Tools + Data Sources"

2. **Add arrows** between them

3. **Label the 5 tools** in the bottom box

**Time: 5 minutes in PowerPoint**

**This is enough to show the architecture!**

---

**Use this guide to create your diagram in any tool you're comfortable with. The text-based version can also be screenshot and used directly if you're really pressed for time!** 🎨
