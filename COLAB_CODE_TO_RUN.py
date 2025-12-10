# ============================================================
# ADD THIS CODE TO YOUR COLAB NOTEBOOK
# Copy and paste this into a NEW CELL at the end of your notebook
# ============================================================

# Install required packages
!pip install -q flask flask-cors pyngrok

from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from pyngrok import ngrok
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

def generate_response(instruction, context="IDSR and Measles Detection Guidelines", max_new_tokens=256):
    """Generate response from fine-tuned model"""
    prompt = f"""### Instruction:
{instruction}

### Context:
{context}

### Response:
"""
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract only the response part
    if "### Response:" in full_response:
        response = full_response.split("### Response:")[-1].strip()
    else:
        response = full_response
    
    return response

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'ZNPHI Measles Chatbot Model API is running',
        'model': 'Mistral-7B-Instruct-v0.2 (Fine-tuned)',
        'version': '1.0.0'
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint - receives questions and returns answers"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        context = data.get('context', 'IDSR and Measles Detection Guidelines')
        max_tokens = data.get('max_tokens', 256)
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        print(f"\n[COLAB] Received question: {question}")
        
        # Generate response using fine-tuned model
        answer = generate_response(question, context, max_tokens)
        
        print(f"[COLAB] Generated answer: {answer[:100]}...")
        
        return jsonify({
            'answer': answer,
            'model': 'Mistral-7B-Instruct-v0.2-ZNPHI',
            'confidence': 'high',
            'timestamp': str(pd.Timestamp.now())
        })
        
    except Exception as e:
        print(f"[COLAB] Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Set ngrok authtoken
ngrok.set_auth_token("cr_36epaLI08B1bN9d0LGkpBby3KY3")

# Start ngrok tunnel
public_url = ngrok.connect(5000)

print("\n" + "="*70)
print("🚀 COLAB MODEL API IS NOW RUNNING!")
print("="*70)
print(f"\n📡 Public URL: {public_url}")
print(f"\n🔗 Copy this URL - you'll need it for the frontend!")
print("\n" + "="*70)
print("\n✅ Ready to receive requests from your UI!")
print("="*70 + "\n")

# Run Flask app (this will keep running)
from threading import Thread

def run_app():
    app.run(port=5000)

thread = Thread(target=run_app)
thread.start()

print("✅ Server is running in background!")
print(f"📋 Your ngrok URL: {public_url}")
print("\n⚠️  IMPORTANT: Copy the URL above and send it to me!")
