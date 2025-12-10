# znphi_api.py
"""
ZNPHI Measles Chatbot API
FastAPI backend for the fine-tuned Mistral model
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import uvicorn
from datetime import datetime
# ============================================================================
# CONFIGURATION
# ============================================================================
app = FastAPI(
    title="ZNPHI Measles Chatbot API",
    description="AI-powered assistant for IDSR and Measles Detection",
    version="1.0.0"
)
# Enable CORS for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ============================================================================
# MODELS
# ============================================================================
class ChatRequest(BaseModel):
    question: str
    context: Optional[str] = "IDSR and Measles Detection Guidelines"
    max_tokens: Optional[int] = 256
    temperature: Optional[float] = 0.7
class ChatResponse(BaseModel):
    answer: str
    timestamp: str
    model_version: str
    confidence: Optional[str] = "medium"
class HealthCheck(BaseModel):
    status: str
    model_loaded: bool
    timestamp: str
# ============================================================================
# GLOBAL MODEL VARIABLES
# ============================================================================
model = None
tokenizer = None
MODEL_PATH = "./znphi-measles-chatbot-final"  # Update with your model path
BASE_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
# ============================================================================
# MODEL LOADING
# ============================================================================
def load_model():
    """Load the fine-tuned model and tokenizer"""
    global model, tokenizer
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    tokenizer.pad_token = tokenizer.eos_token
    print("Loading base model...")
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    print("Loading LoRA adapters...")
    model = PeftModel.from_pretrained(base_model, MODEL_PATH)
    model.eval()
    print("Model loaded successfully!")
# ============================================================================
# INFERENCE FUNCTION
# ============================================================================
def generate_response(question: str, context: str, max_tokens: int, temperature: float):
    """Generate response from the model"""
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    prompt = f"""### Instruction:
{question}
### Context:
{context}
### Response:
"""
    try:
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1
            )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        answer = response.split("### Response:")[-1].strip()
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")
# ============================================================================
# API ENDPOINTS
# ============================================================================
@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    try:
        load_model()
    except Exception as e:
        print(f"Warning: Could not load model on startup: {e}")
        print("API will start but model queries will fail until model is loaded")
@app.get("/", response_model=HealthCheck)
async def root():
    """Health check endpoint"""
    return HealthCheck(
        status="running",
        model_loaded=model is not None,
        timestamp=datetime.now().isoformat()
    )
@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy" if model is not None else "model_not_loaded",
        "model_loaded": model is not None,
        "tokenizer_loaded": tokenizer is not None,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint
    Send a question and receive an AI-generated response based on IDSR guidelines
    """
    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    answer = generate_response(
        question=request.question,
        context=request.context,
        max_tokens=request.max_tokens,
        temperature=request.temperature
    )
    return ChatResponse(
        answer=answer,
        timestamp=datetime.now().isoformat(),
        model_version="ZNPHI-Measles-v1.0",
        confidence="high" if len(answer) > 50 else "medium"
    )
@app.post("/batch")
async def batch_chat(questions: List[str]):
    """
    Batch processing endpoint
    Send multiple questions and get responses for all
    """
    if not questions:
        raise HTTPException(status_code=400, detail="Questions list cannot be empty")
    responses = []
    for question in questions:
        try:
            answer = generate_response(
                question=question,
                context="IDSR and Measles Detection Guidelines",
                max_tokens=256,
                temperature=0.7
            )
            responses.append({
                "question": question,
                "answer": answer,
                "status": "success"
            })
        except Exception as e:
            responses.append({
                "question": question,
                "answer": None,
                "status": "error",
                "error": str(e)
            })
    return {"results": responses, "timestamp": datetime.now().isoformat()}
@app.get("/examples")
async def get_examples():
    """Get example questions"""
    return {
        "examples": [
            "What is the standard case definition for a suspected measles case?",
            "How should serum samples be stored for measles testing?",
            "What is the Alert Threshold for measles?",
            "What is the recommended Vitamin A dose for children aged 12 months and older?",
            "How do you prepare the wash buffer for the Measles ELISA test?",
            "What should be done if a sample yields an equivocal result?"
        ]
    }
# ============================================================================
# RUN SERVER
# ============================================================================
if __name__ == "__main__":
    print("Starting ZNPHI Chatbot API...")
    print("API will be available at: http://localhost:8000")
    print("Documentation at: http://localhost:8000/docs")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False  # Set to True for development
    )
