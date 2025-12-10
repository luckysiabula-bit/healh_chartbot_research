# ZNPHI Measles Chatbot - Testing Guide

## 🎉 Your Chatbot is LIVE!

### Running Services
- **Backend (Node.js):** http://localhost:8000
- **Frontend (React):** http://localhost:5173

### Quick Start

#### Start Backend
```bash
cd backend
node server.js
```

#### Start Frontend (in another terminal)
```bash
npm run dev
```

### 📝 Test Prompts

Copy and paste these into your chatbot at http://localhost:5173:

#### Basic Questions
1. **What is the standard case definition for a suspected measles case?**
2. **What are the immediate reporting requirements for measles?**
3. **What is the Alert Threshold for measles?**

#### Laboratory/Technical
4. **How should serum samples be stored if testing is not performed immediately?**
5. **What is the exact dilution ratio for patient samples in the Measles ELISA test?**
6. **How are the results of the Measles ELISA interpreted?**

#### Treatment
7. **What is the recommended Vitamin A dose for an infant under 6 months?**
8. **What is the recommended Vitamin A dose for children aged 12 months and older?**

#### Surveillance
9. **What does a confirmed measles outbreak look like?**
10. **What should be done if a sample yields an equivocal result?**

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Chat Request
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the Alert Threshold for measles?",
    "context": "IDSR and Measles Detection Guidelines"
  }'
```

### Expected Response Format
```json
{
  "answer": "The alert threshold for measles is...",
  "timestamp": "2025-12-10T14:05:31.791Z",
  "confidence": "high",
  "model": "ZNPHI-Measles-v1",
  "context": "IDSR and Measles Detection Guidelines"
}
```

### Architecture

```
User Browser
    ↓
React Frontend (Port 5173)
    ↓ HTTP POST /chat
Node.js Backend (Port 8000)
    ↓ Keyword Matching
Response Database
    ↓
Answer → Frontend → Display
```

### Troubleshooting

**Backend won't start:**
```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill if needed
kill -9 <PID>
```

**Frontend won't start:**
```bash
# Check if port 5173 is in use
lsof -i :5173
# Kill if needed
kill -9 <PID>
```

**Connection refused:**
- Make sure backend is running first
- Check backend logs for errors
- Verify CORS is enabled (already configured)

### Files Structure

```
my-chatbot/
├── backend/
│   ├── server.js          # Node.js API server
│   ├── package.json       # Backend dependencies
│   └── node_modules/      # Installed packages
├── src/
│   ├── App.jsx           # React frontend
│   └── App.css           # Styles
├── package.json          # Frontend dependencies
└── TESTING_GUIDE.md      # This file
```

### Next Steps

1. **Test in Browser:** Open http://localhost:5173
2. **Try Prompts:** Use the test prompts above
3. **Verify Responses:** Check that answers match expected content
4. **Customize:** Edit `backend/server.js` to add more responses
5. **Connect Model:** Replace keyword matching with actual model inference

### Stopping Services

```bash
# Stop backend
pkill -f "node server.js"

# Stop frontend
pkill -f "vite"

# Or press Ctrl+C in each terminal
```

---

**Created:** 2025-12-10  
**Status:** ✅ Working
