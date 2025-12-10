# ZNPHI Measles Chatbot - Full Stack Integration Guide

This document explains how to run the complete ZNPHI Measles Chatbot application with both frontend and backend.

## 🏗️ Architecture

```
┌─────────────────────┐         ┌──────────────────────┐
│   React Frontend    │         │   FastAPI Backend    │
│   (Port 5173)       │◄───────►│   (Port 8000)        │
│                     │  HTTP   │                      │
│  - Chat Interface   │         │  - Mistral-7B Model  │
│  - Real-time UI     │         │  - LoRA Adapters     │
│  - Message History  │         │  - IDSR Guidelines   │
└─────────────────────┘         └──────────────────────┘
```

## 🚀 Quick Start

### Option 1: Automated Startup (Recommended)

```bash
chmod +x start-dev.sh
./start-dev.sh
```

This script will:
- Install all dependencies
- Start the backend API
- Start the frontend dev server
- Display all relevant URLs

### Option 2: Manual Startup

#### Terminal 1 - Backend:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python znphi_api.py
```

#### Terminal 2 - Frontend:
```bash
npm install  # If not already installed
npm run dev
```

## 📋 Prerequisites

### Required:
- **Python 3.8+** with pip
- **Node.js 18+** with npm
- **GPU recommended** (NVIDIA with CUDA) for backend
- **8GB+ VRAM** for model inference

### Model Setup:
Ensure your fine-tuned model is located at:
```
./znphi-measles-chatbot-final/
```

Or update `MODEL_PATH` in `backend/znphi_api.py`

## 🔌 API Integration

The frontend connects to the backend via:

**Endpoint:** `POST http://localhost:8000/chat`

**Request:**
```json
{
  "question": "What is the standard case definition for measles?",
  "context": "IDSR and Measles Detection Guidelines",
  "max_tokens": 256,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "answer": "A suspected measles case is defined as...",
  "timestamp": "2024-12-10T14:30:00",
  "model_version": "ZNPHI-Measles-v1.0",
  "confidence": "high"
}
```

## 🎨 Frontend Features

- ✅ Real-time chat interface
- ✅ Loading indicators
- ✅ Error handling with helpful messages
- ✅ Welcome screen with example questions
- ✅ Confidence indicators
- ✅ Responsive design (mobile-friendly)
- ✅ Smooth animations

## 🔧 Backend Features

- ✅ Fine-tuned Mistral-7B with LoRA
- ✅ CORS enabled for web access
- ✅ Health check endpoints
- ✅ Batch processing support
- ✅ Example questions API
- ✅ Interactive API documentation

## 🐛 Troubleshooting

### Backend Issues:

**Model not loading:**
```bash
# Check if model path exists
ls -la znphi-measles-chatbot-final/

# Check GPU availability
python -c "import torch; print(torch.cuda.is_available())"
```

**Port 8000 already in use:**
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues:

**CORS errors:**
- Backend CORS is configured to allow all origins
- Check that backend is running on port 8000

**Connection refused:**
- Verify backend is running: `curl http://localhost:8000/health`
- Check firewall settings

### Common Error Messages:

**"Make sure the backend server is running"**
- Start the backend: `cd backend && python znphi_api.py`

**"Model not loaded"**
- Check model path in `backend/znphi_api.py`
- Ensure model files exist

## 📊 Testing the Integration

1. **Start both servers** (frontend + backend)

2. **Open browser** → http://localhost:5173

3. **Try example questions:**
   - "What is the standard case definition for measles?"
   - "How should serum samples be stored?"
   - "What is the Alert Threshold for measles?"

4. **Check API docs** → http://localhost:8000/docs

## 🔒 Production Deployment

### Security Considerations:
- [ ] Update CORS to specific origins
- [ ] Add authentication/API keys
- [ ] Use HTTPS
- [ ] Set up rate limiting
- [ ] Configure environment variables

### Deployment Options:
- **Frontend:** Vercel, Netlify, AWS S3 + CloudFront
- **Backend:** AWS EC2 (GPU), Google Cloud VM, Azure ML

## 📚 Additional Resources

- [Backend Documentation](backend/README.md)
- [API Documentation](http://localhost:8000/docs) (when running)
- [Mistral AI Docs](https://docs.mistral.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

## 🤝 Support

For issues or questions about:
- **IDSR Guidelines:** Contact ZNPHI
- **Technical Issues:** Check logs in `backend.log`
- **Model Performance:** Review training data and hyperparameters
