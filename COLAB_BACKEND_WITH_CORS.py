# --- 0. INSTALL DEPENDENCIES (If not already installed) ---
!pip install -q -U langchain langchain-community faiss-cpu sentence-transformers pypdf python-docx langchain-text-splitters
!pip install -q -U fastapi uvicorn pyngrok nest_asyncio peft transformers bitsandbytes

import os
import torch
import uvicorn
import nest_asyncio
import shutil
from threading import Thread
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- ADDED FOR CORS
from pydantic import BaseModel
from pyngrok import ngrok
from typing import List

# LangChain & RAG Imports
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Model Imports
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

# ==========================================
# 1. SETUP & LOAD RAG VECTOR INDEX
# ==========================================
print("🚀 STARTING SETUP...")

# Define Paths (Aligned with your Drive structure)
# Ensure you have run: drive.mount('/content/drive')
rag_folder_path = "/content/drive/MyDrive/Measles_Chatbot_Project/RAG Files"
vector_db_path = "/content/drive/MyDrive/Measles_Chatbot_Project/faiss_index_measles"

# Initialize Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def build_or_load_vector_db():
    # If index already exists, load it
    if os.path.exists(vector_db_path):
        print(f"📂 Found existing Vector DB at {vector_db_path}. Loading...")
        try:
            return FAISS.load_local(vector_db_path, embedding_model, allow_dangerous_deserialization=True)
        except Exception as e:
            print(f"⚠️ Error loading index: {e}. Rebuilding...")

    print("⚙️ Building new Vector DB from 'RAG Files'...")
    documents = []

    # Check if folder exists
    if not os.path.exists(rag_folder_path):
        os.makedirs(rag_folder_path, exist_ok=True)
        print(f"⚠️ Created folder {rag_folder_path}. Please upload your files here!")
        return None

    # Load Files
    for filename in os.listdir(rag_folder_path):
        file_path = os.path.join(rag_folder_path, filename)
        if filename.endswith(".pdf"):
            try:
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
                print(f"   - Loaded PDF: {filename}")
            except Exception as e:
                print(f"   ⚠️ Error loading PDF {filename}: {e}")
        elif filename.endswith(".docx"):
            try:
                loader = Docx2txtLoader(file_path)
                documents.extend(loader.load())
                print(f"   - Loaded DOCX: {filename}")
            except Exception as e:
                 print(f"   ⚠️ Error loading DOCX {filename}: {e}")

    if not documents:
        print("❌ No documents found. Index will be empty.")
        return None

    # Split Text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    print(f"📊 Created {len(chunks)} chunks.")

    # Create & Save Vector Store
    vector_db = FAISS.from_documents(chunks, embedding_model)
    vector_db.save_local(vector_db_path)
    print(f"💾 Vector DB saved to {vector_db_path}")
    return vector_db

# Initialize Vector DB
vector_store = build_or_load_vector_db()

# ==========================================
# 2. LOAD LLM (MISTRAL)
# ==========================================
print("⚙️ Loading Mistral 7B Model...")

# 1. Config
base_model_id = "mistralai/Mistral-7B-Instruct-v0.2"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

# 2. Tokenizer & Base Model
tokenizer = AutoTokenizer.from_pretrained(base_model_id)
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    quantization_config=bnb_config,
    device_map="auto"
)

# 3. Load Adapter (Update path if you have trained one)
# adapter_path = "/content/drive/MyDrive/Measles_Chatbot_Project/final_mistral_adapter"
# if os.path.exists(adapter_path):
#     print(f"✅ Loading Adapter from {adapter_path}")
#     model = PeftModel.from_pretrained(base_model, adapter_path)
# else:
print("ℹ️ Using Base Mistral Model (Adapter not found/configured)")
model = base_model

print("✅ Model Ready!")

# ==========================================
# 3. DEFINE API (FastAPI)
# ==========================================
app = FastAPI(title="ZNPHI Measles Chatbot")

# ✅ ADD CORS MIDDLEWARE - THIS IS THE FIX!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (you can restrict this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_query = request.message

    # 1. Retrieve Context
    context_text = ""
    source_docs = []

    if vector_store:
        results = vector_store.similarity_search(user_query, k=3)
        for doc in results:
            context_text += f"\n- {doc.page_content}"
            source_docs.append(doc.metadata.get("source", "unknown"))
    else:
        context_text = "No context available."

    # 2. Format Prompt
    prompt = f"""### Instruction:
You are an expert medical assistant for measles surveillance in Zambia.
Use the Context below to answer the Question strictly based on the guidelines.
If the answer is not in the context, say "I cannot find that information in the guidelines."

### Context:{context_text}

### Question:
{user_query}

### Response:
"""

    # 3. Generate
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.3,
            do_sample=True
        )

    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if "### Response:" in full_response:
        answer = full_response.split("### Response:")[-1].strip()
    else:
        answer = full_response

    return {
        "response": answer,
        "sources": list(set(source_docs))
    }

# ==========================================
# 4. START SERVER (Ngrok + Uvicorn)
# ==========================================
nest_asyncio.apply()

def run_server():
    # Force IPv4 to avoid "Connection Refused"
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Kill old tunnels
ngrok.kill()

# Start Server Thread
thread = Thread(target=run_server)
thread.start()

# Set Auth Token
ngrok.set_auth_token("36eSFPyRmXAfKsTQ7WRyqWpsmDj_25rrefuGQpKA8PJjhAA6e")

try:
    public_url = ngrok.connect(8000).public_url
    print(f"\n🚀 API IS LIVE AT: {public_url}/chat")
    print("✅ CORS is enabled - Frontend can now connect!")
    print("Use Postman with method: POST")
except Exception as e:
    print("Ngrok Error:", e)
