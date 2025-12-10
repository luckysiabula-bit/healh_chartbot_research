# ZNPHI Measles Chatbot Backend

AI-powered chatbot for IDSR (Integrated Disease Surveillance and Response) and Measles Detection Guidelines, powered by a fine-tuned Mistral-7B model.

## Features

- Fine-tuned Mistral-7B language model with LoRA adapters
- FastAPI backend with CORS support
- Batch processing support
- Health check endpoints
- Example questions endpoint

## Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Model Setup

Ensure your fine-tuned model is available at:
```
./znphi-measles-chatbot-final
```

Or update the `MODEL_PATH` variable in `znphi_api.py` to point to your model location.

### 3. Run the Server

```bash
python znphi_api.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

## API Endpoints

### Health Check
```bash
GET /health
```

### Chat Endpoint
```bash
POST /chat
Content-Type: application/json

{
  "question": "What is the standard case definition for measles?",
  "context": "IDSR and Measles Detection Guidelines",
  "max_tokens": 256,
  "temperature": 0.7
}
```

### Batch Processing
```bash
POST /batch
Content-Type: application/json

{
  "questions": [
    "What is the Alert Threshold for measles?",
    "How should samples be stored?"
  ]
}
```

### Get Examples
```bash
GET /examples
```

## Model Requirements

- GPU recommended (NVIDIA with CUDA support)
- Minimum 8GB VRAM for inference
- ~14GB disk space for model weights

## Configuration

Key variables in `znphi_api.py`:
- `MODEL_PATH`: Path to fine-tuned model
- `BASE_MODEL`: Base Mistral model
- `PORT`: API port (default: 8000)
