# IT Guardian Agent - Evaluation Tests

Quick guide to running evaluation tests for the IT Guardian Agent.

## 🚀 Quick Start

### **Run Complete Evaluation (Recommended)**

```bash
python test/run_full_evaluation_with_server_logs.py --batch-size 1
```

This single command:
- ✅ Starts the server automatically
- ✅ Runs all test scenarios
- ✅ Captures both server and client logs
- ✅ Stops the server when complete
- ✅ Handles API rate limits

**Time:** ~15-20 minutes for all 7 scenarios

---

## 📊 Available Test Scripts

### 1. **Full Evaluation with Server Logs** (All-in-One) ⭐
```bash
python test/run_full_evaluation_with_server_logs.py [OPTIONS]
```

**Options:**
- `--batch-size N` - Scenarios per batch (default: 2)
- `--start N` - Start scenario index (default: 0)
- `--end N` - End scenario index (default: all)
- `--scenario-delay N` - Seconds between scenarios (default: 30)
- `--turn-delay N` - Seconds between turns (default: 20)
- `--batch-delay N` - Seconds between batches (default: 120)
- `--no-server` - Don't start server (if already running)

### 2. **Quick Evaluation** (Fast Testing)
```bash
python test/run_evaluation_quick.py
```

- Runs only 2 scenarios
- Takes ~2 minutes
- Good for quick validation

### 3. **Base Evaluation Script** (Manual Server Required)
```bash
# Terminal 1: Start server
python src/it_guardian_agent.py

# Terminal 2: Run tests
python test/run_evaluation.py
```

---

## 📁 Output Files

After running, you'll get:

```
AccessBot/
└── evidence/
    └── evaluation_results/
        ├── server_logs_TIMESTAMP.log                    # Server console output
        ├── evaluation_batch_recording_TIMESTAMP.log     # Client test output
        └── evaluation_batch_results_0_6_TIMESTAMP.json  # Structured results (JSON)
```

All evaluation results are automatically saved in `evidence/evaluation_results/`.

---

## 💡 Usage Examples

### Run All Scenarios (Conservative Timing)
```bash
python test/run_full_evaluation_with_server_logs.py --batch-size 1 --scenario-delay 60
```

### Split Across Multiple Sessions (Avoid Rate Limits)
```bash
# Session 1
python test/run_full_evaluation_with_server_logs.py --start 0 --end 3

# Session 2 (later)
python test/run_full_evaluation_with_server_logs.py --start 3 --end 7
```

### Quick Validation
```bash
python test/run_evaluation_quick.py
```

---

## ⚠️ API Rate Limits

**Gemini Free Tier:**
- ~15 requests per minute
- ~1,500 requests per day

**Tips:**
- Use longer delays if you hit rate limits
- Split testing across multiple sessions
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common errors

---

## 📚 Test Scenarios

The evaluation covers 7 scenarios across all workflows:

1. **New User (Workflow D)** - Employee not found
2. **Auto-Approval (Workflow A)** - Sales + Salesforce
3. **Manager Approval (Workflow B)** - Sales + GitHub
4. **Policy Rejection (Workflow C)** - Sales + Figma
5. **Duplicate Check** - Existing pending request
6. **Engineering Auto-Approval (Workflow A)** - Engineering + GitHub
7. **De-provisioning (Workflow E)** - Remove access request

---

## 📖 Additional Documentation

- **[EVALUATION_DOCUMENTATION.md](EVALUATION_DOCUMENTATION.md)** - Complete project documentation for capstone
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common API errors and solutions

---

## 🎯 Recommended Workflow

1. **First time:** Run quick evaluation to validate setup
   ```bash
   python test/run_evaluation_quick.py
   ```

2. **Full testing:** Run complete evaluation with logging
   ```bash
   python test/run_full_evaluation_with_server_logs.py --batch-size 1
   ```

3. **Review results:** Check the generated log and JSON files

4. **Troubleshooting:** If errors occur, see TROUBLESHOOTING.md

---

**Last Updated:** November 25, 2025
