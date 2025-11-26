# Troubleshooting Common Gemini API Errors

## Error: "model output must contain either output text or tool calls"

This error occurs when the Gemini API returns an empty response. Here's how to handle it:

### ✅ **Solutions Implemented**

I've already updated your code with these fixes:

#### 1. **Server-Side Retry Logic** ([it_guardian_agent.py](file:///c:/Users/vasav/Kaggle-CAPStone/AccessBot/src/it_guardian_agent.py))
- Automatically retries up to 3 times with exponential backoff
- If all retries fail, returns a graceful error message instead of crashing
- Logs all retry attempts for debugging

#### 2. **Recommended Delays**

Use these conservative delays to avoid rate limits:

```bash
# Recommended: 20s between turns, 30s between scenarios, 120s between batches
python test/run_full_evaluation_with_server_logs.py \
  --batch-size 2 \
  --turn-delay 20 \
  --scenario-delay 30 \
  --batch-delay 120
```

---

## 🔍 **Common Causes**

### 1. **API Rate Limiting** (Most Common)
**Symptom:** Error appears after several successful requests

**Solution:**
```bash
# Increase delays significantly
python test/run_evaluation_batch_recorded.py \
  --batch-size 1 \
  --scenario-delay 30 \
  --batch-delay 180
```

### 2. **Session State Issues**
**Symptom:** Error on first message of a conversation

**Solution:** The retry logic will automatically handle this by creating a fresh session

### 3. **API Quota Exhausted**
**Symptom:** All requests fail immediately

**Solution:**
- Check your quota at: https://console.cloud.google.com/apis/dashboard
- Wait for quota to reset (usually daily)
- Consider upgrading to paid tier for higher limits

### 4. **Network Issues**
**Symptom:** Intermittent failures

**Solution:** The retry logic handles this automatically

---

## 🛠️ **Quick Fixes**

### **Immediate Fix: Use Longer Delays**

```bash
# Ultra-conservative mode (for quota-sensitive accounts)
python test/run_evaluation_batch_recorded.py \
  --batch-size 1 \          # One scenario at a time
  --scenario-delay 60 \     # 1 minute between scenarios
  --batch-delay 300         # 5 minutes between batches (if running multiple)
```

### **Split Testing Across Multiple Days**

```bash
# Day 1: Scenarios 0-2
python test/run_full_evaluation_with_server_logs.py --start 0 --end 3

# Day 2: Scenarios 3-4  
python test/run_full_evaluation_with_server_logs.py --start 3 --end 5

# Day 3: Scenarios 5-6
python test/run_full_evaluation_with_server_logs.py --start 5 --end 7
```

---

## 📊 **Understanding Your API Limits**

**Gemini Free Tier:**
- ~15 requests per minute (RPM)
- ~1,500 requests per day (RPD)

**Your Evaluation:**
- 7 scenarios
- 2-5 messages per scenario = ~27 total messages
- With agents, each message might trigger multiple API calls (for tools)
- **Estimated total:** 50-100 API calls for full evaluation

**Recommendation:** Use delays of at least:
- 15-20 seconds between conversation turns
- 30-60 seconds between scenarios
- 120-180 seconds between batches

---

## 🔧 **Manual Testing**

If issues persist, test individual components:

### Test 1: Verify Server is Working
```bash
curl -X POST http://127.0.0.1:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"text": "Hi"}'
```

Expected: Should get a response with agent greeting

### Test 2: Run Quick Evaluation
```bash
# Only 2 scenarios with long delays
python test/run_evaluation_quick.py
```

### Test 3: Check Server Logs
Look for patterns in `server_logs_*.log`:
- Are there retries happening?
- Are there rate limit errors from Google?
- Are there other exceptions?

---

## 📝 **Monitoring Your Test**

Watch the server logs in real-time while testing:

```powershell
# In one terminal, watch server logs
Get-Content server_logs_TIMESTAMP.log -Wait

# In another, run evaluation
python test/run_evaluation_batch_recorded.py
```

---

## 🎯 **Best Practice Workflow**

1. **Start Conservative:**
   ```bash
   python test/run_full_evaluation_with_server_logs.py \
     --batch-size 1 --scenario-delay 60
   ```

2. **Monitor First 2 Scenarios**
   - Check if you get any errors
   - Look at server logs for retry attempts

3. **If Successful, Gradually Reduce Delays:**
   ```bash
   # After confirming it works
   python test/run_full_evaluation_with_server_logs.py \
     --batch-size 2 --scenario-delay 30
   ```

4. **Split Across Sessions:**
   - Run 2-3 scenarios in one session
   - Wait several hours or until next day
   - Run the remaining scenarios

---

## 🚨 **If Nothing Works**

### Option 1: Contact Support
Check if there's an issue with your API key:
https://console.cloud.google.com/

### Option 2: Use Mock Mode (Development Only)
Create a mock evaluator that doesn't hit the real API:

```python
# For development/testing the evaluation framework itself
class MockEvaluator:
    def run_conversation(self, messages):
        return {
            "session_id": "mock-session",
            "transcript": [
                {"user": msg, "agent": f"Mock response to: {msg}"}
                for msg in messages
            ]
        }
```

### Option 3: Increase Initial Wait Time
The server might need more time to initialize:

Edit `run_full_evaluation_with_server_logs.py`:
```python
# Change from 15 to 30 seconds
time.sleep(30)  # Line ~49
```

---

## 📈 **Success Indicators**

You'll know it's working when:
- ✅ Server logs show successful agent responses
- ✅ Client logs show complete conversations
- ✅ No retry attempts in server logs
- ✅ JSON results file contains full conversation data

---

## 💡 **Pro Tips**

1. **Run during off-peak hours** (e.g., late night) when API load is lower
2. **Use --start and --end** to test one scenario at a time first
3. **Keep delays generous** - it's better to be slow than to fail
4. **Save successful runs** - once you have good results, keep them!

---

## 📞 **Still Having Issues?**

Check the server logs for the actual error message and search for it in:
- Google Gemini API documentation
- Stack Overflow
- GitHub issues for google-adk

The retry logic should handle most transient errors automatically.
