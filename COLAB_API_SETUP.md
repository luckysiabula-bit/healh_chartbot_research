# Connect Your Colab Model to the Frontend UI

## 🎯 Goal
Make your fine-tuned model in Colab accessible to your React frontend running locally.

## 📋 Step 1: Add This to Your Colab Notebook

Copy and paste this code into a **NEW CELL** at the end of your Colab notebook (after training):

```python
# ============================================================
# EXPOSE MODEL AS API FOR TESTING WITH FRONTEND
# ============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from threading import Thread
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

# Install required packages (run once)
!pip install -q flask flask-cors pyngrok

# Set ngrok authtoken (get free token from https://ngrok.com/)
# Replace 'YOUR_NGROK_TOKEN' with your actual token
ngrok.set_auth_token("YOUR_NGROK_TOKEN")

# Start ngrok tunnel
public_url = ngrok.connect(5000)
print("\n" + "="*70)
print("🚀 COLAB MODEL API IS NOW RUNNING!")
print("="*70)
print(f"\n📡 Public URL: {public_url}")
print(f"\n🔗 Use this URL in your frontend:")
print(f"   Replace 'http://localhost:8000' with '{public_url}'")
print("\n" + "="*70)
print("\n✅ Ready to receive requests from your UI!")
print("="*70 + "\n")

# Run Flask app
app.run(port=5000)
```

## 📋 Step 2: Get ngrok Token (FREE)

1. Go to https://ngrok.com/
2. Sign up for free account
3. Go to https://dashboard.ngrok.com/get-started/your-authtoken
4. Copy your authtoken
5. Replace `YOUR_NGROK_TOKEN` in the code above

## 📋 Step 3: Update Your Frontend

Update `src/App.jsx` to use the ngrok URL:

```jsx
// At the top of App.jsx, change the API_URL
const API_URL = 'https://xxxx-xx-xx-xxx-xx.ngrok-free.app'  // Replace with your ngrok URL from Colab output
```

## 🎯 Alternative: Use Colab's Built-in Tunnel (No ngrok needed)

If you don't want to use ngrok, use this simpler version:

```python
# ============================================================
# SIMPLE API WITHOUT NGROK (Using Gradio)
# ============================================================

import gradio as gr

def chat_interface(question, context="IDSR and Measles Detection Guidelines"):
    """Gradio interface for testing"""
    prompt = f"""### Instruction:
{question}

### Context:
{context}

### Response:
"""
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    if "### Response:" in full_response:
        response = full_response.split("### Response:")[-1].strip()
    else:
        response = full_response
    
    return response

# Create Gradio interface
iface = gr.Interface(
    fn=chat_interface,
    inputs=[
        gr.Textbox(label="Question", placeholder="What is the Alert Threshold for measles?"),
        gr.Textbox(label="Context", value="IDSR and Measles Detection Guidelines")
    ],
    outputs=gr.Textbox(label="Response", lines=10),
    title="ZNPHI Measles Chatbot - Fine-tuned Model",
    description="Ask questions about IDSR and Measles Detection Guidelines",
    examples=[
        ["What is the standard case definition for a suspected measles case?", "IDSR 3rd Edition"],
        ["How should serum samples be stored?", "VIR-TECH-011-v2"],
        ["What is the Alert Threshold for measles?", "IDSR 3rd Edition"],
    ]
)

# Launch with public URL
iface.launch(share=True)
```

This will give you a public URL you can access directly in your browser!

## 🧪 Step 4: Test the Connection

Once you have the public URL from Colab, test it:

```bash
# Test health endpoint
curl https://your-ngrok-url.ngrok-free.app/health

# Test chat endpoint
curl -X POST https://your-ngrok-url.ngrok-free.app/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the Alert Threshold for measles?",
    "context": "IDSR and Measles Detection Guidelines"
  }'
```

## 🎨 Step 5: Update Frontend to Use Colab API

Modify `src/App.jsx`:

```jsx
import { useState } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  
  // 🔥 CHANGE THIS TO YOUR NGROK URL FROM COLAB
  const API_URL = 'https://xxxx-xx-xx-xxx-xx.ngrok-free.app'  // From Colab output
  
  const handleSend = async () => {
    if (input.trim() && !isLoading) {
      const userMessage = input.trim()
      setMessages([...messages, { text: userMessage, sender: 'user' }])
      setInput('')
      setIsLoading(true)
      
      try {
        const response = await fetch(`${API_URL}/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            question: userMessage,
            context: 'IDSR and Measles Detection Guidelines',
            max_tokens: 256,
            temperature: 0.7
          })
        })

        if (!response.ok) {
          throw new Error(`API error: ${response.status}`)
        }

        const data = await response.json()
        setMessages(prev => [...prev, { 
          text: data.answer, 
          sender: 'bot',
          model: data.model,
          timestamp: data.timestamp,
          confidence: data.confidence
        }])
      } catch (error) {
        console.error('Error:', error)
        setMessages(prev => [...prev, { 
          text: `Sorry, I encountered an error: ${error.message}. Make sure Colab is running and the ngrok URL is correct.`,
          sender: 'bot',
          isError: true
        }])
      } finally {
        setIsLoading(false)
      }
    }
  }

  return (
    <div className="App">
      <div className="chatbot-container">
        <h1>ZNPHI Measles Chatbot</h1>
        <div className="subtitle">🧠 Powered by Fine-tuned Mistral-7B Model</div>
        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h2>👋 Welcome!</h2>
              <p>Ask me anything about IDSR and Measles Detection Guidelines.</p>
              <p className="model-info">Using your fine-tuned model from Colab</p>
              <div className="example-questions">
                <strong>Try asking:</strong>
                <ul>
                  <li>What is the standard case definition for measles?</li>
                  <li>How should serum samples be stored?</li>
                  <li>What is the Alert Threshold for measles?</li>
                </ul>
              </div>
            </div>
          )}
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender} ${msg.isError ? 'error' : ''}`}>
              {msg.text}
              {msg.model && (
                <div className="model-badge">Model: {msg.model}</div>
              )}
              {msg.confidence && (
                <span className="confidence">{msg.confidence} confidence</span>
              )}
            </div>
          ))}
          {isLoading && (
            <div className="message bot loading">
              <span className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </span>
            </div>
          )}
        </div>
        <div className="input-area">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask about IDSR or Measles Detection..."
            disabled={isLoading}
          />
          <button onClick={handleSend} disabled={isLoading}>
            {isLoading ? 'Thinking...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default App
```

## 🚀 Complete Workflow

1. **In Colab**: Run the API code cell → Get ngrok URL
2. **In Frontend**: Update `API_URL` to ngrok URL
3. **In Browser**: Open http://localhost:5173
4. **Test**: Type questions in the UI, get responses from your fine-tuned model!

## 📝 Notes

- Keep Colab tab open while testing (closes after 12 hours on free tier)
- ngrok free tier has rate limits (40 requests/minute)
- For production, deploy model to Hugging Face Inference API or AWS

---

**Which method do you prefer?**
1. **Flask + ngrok** (Full API control)
2. **Gradio** (Simpler, built-in UI + shareable link)
