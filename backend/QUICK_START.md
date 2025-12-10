# Quick Start - ZNPHI Backend

## 🚀 How to Run the Backend

### Option 1: Using the startup script (Easiest)
```bash
cd backend
./start-backend.sh
```

### Option 2: Manual setup
```bash
cd backend

# Step 1: Create virtual environment
python3 -m venv venv

# Step 2: Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Run the server
python znphi_api.py
```

### Option 3: Quick run (if dependencies already installed)
```bash
cd backend
source venv/bin/activate  # Skip if already activated
python znphi_api.py
```

## ⚠️ Important Notes

- **This is a Python backend, NOT Node.js!**
- Don't use `npm start` - that's for Node.js projects
- Use `python znphi_api.py` instead

## 🔍 Verify It's Running

Once started, check:
```bash
# Health check
curl http://localhost:8000/health

# Or open in browser
open http://localhost:8000/docs
```

## 📋 Prerequisites

Before running, ensure:
- [ ] Python 3.8+ installed
- [ ] Model files at `./znphi-measles-chatbot-final/` (or update path in znphi_api.py)
- [ ] GPU with 8GB+ VRAM (recommended)

## ❌ Common Errors

### "ModuleNotFoundError"
→ Install dependencies: `pip install -r requirements.txt`

### "Model not found"
→ Update `MODEL_PATH` in `znphi_api.py` (line 52)

### "Port 8000 already in use"
→ Kill existing process: `lsof -ti:8000 | xargs kill -9`

## 🎯 What Happens When You Run It

1. ✅ Loads the tokenizer
2. ✅ Loads base Mistral-7B model
3. ✅ Loads LoRA adapters
4. ✅ Starts FastAPI server on port 8000
5. ✅ Ready to receive chat requests!

## 📚 Next Steps

After backend is running:
1. Keep this terminal open (backend running)
2. Open a new terminal
3. Start the frontend: `npm run dev`
4. Open browser: http://localhost:5173
