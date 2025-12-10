# Installing Dependencies for ZNPHI Backend

## ✅ Good News: You Have Python 3.10.12!

You just need to install `pip` (Python package manager) and `venv` (virtual environment).

## 🔧 Install pip and venv

**Run this command in your terminal:**

```bash
sudo apt update && sudo apt install -y python3-pip python3-venv
```

Enter your password when prompted.

## ✅ Verify Installation

After installation, check:

```bash
pip3 --version
# Should show: pip 22.x.x or similar
```

## 🚀 Then Start the Backend

Once pip is installed, you can run the backend:

### Option 1: Using the script
```bash
cd backend
./start-backend.sh
```

### Option 2: Manual steps
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python znphi_api.py
```

## 📦 What Gets Installed

The backend needs these Python packages:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `torch` - PyTorch for ML
- `transformers` - Hugging Face models
- `peft` - Parameter-efficient fine-tuning (LoRA)
- And more (see requirements.txt)

## ⚠️ Important Notes

**Installation Size:**
- pip install: ~50MB
- Python packages (torch, transformers): ~5-10GB
- Model files: ~14GB
- **Total: ~20GB+ disk space needed**

**Installation Time:**
- pip install: 1 minute
- Python packages: 10-20 minutes (depends on internet speed)

## 🐛 Troubleshooting

### "E: Unable to locate package"
Update package list first:
```bash
sudo apt update
```

### "Permission denied"
Make sure you have sudo privileges or ask your system admin.

### "pip3: command not found" (after install)
Try restarting your terminal or use:
```bash
python3 -m pip --version
```

## 🎯 Summary

**What you need to do:**

1. ✅ You have Python 3.10.12 (already installed!)
2. ⏳ Install pip: `sudo apt install -y python3-pip python3-venv`
3. ⏳ Run backend: `cd backend && ./start-backend.sh`
4. ✅ Done!

---

Need help? Check the other documentation files:
- `QUICK_START.md` - How to run the backend
- `README.md` - Backend overview
- `../README_INTEGRATION.md` - Full stack guide
