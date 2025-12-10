import { useState } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const API_URL = 'https://briley-prevocalic-carlo.ngrok-free.dev'

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
            'ngrok-skip-browser-warning': 'true'
          },
          body: JSON.stringify({
            question: userMessage,
            context: "IDSR and Measles Detection Guidelines",
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
          timestamp: data.timestamp || new Date().toISOString(),
          confidence: data.confidence || 'high'
        }])
      } catch (error) {
        console.error('Error:', error)
        setMessages(prev => [...prev, { 
          text: `Sorry, I encountered an error: ${error.message}. Make sure the backend server is running at ${API_URL}`,
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
        <div className="header">
          <img src="/znphi.jpeg" alt="ZNPHI Logo" className="logo" />
          <div className="header-text">
            <h1>ZNPHI Measles Chatbot</h1>
            <div className="subtitle">AI-Powered IDSR & Measles Detection Assistant</div>
          </div>
        </div>
        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h2>👋 Welcome!</h2>
              <p>Ask me anything about IDSR and Measles Detection Guidelines.</p>
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
