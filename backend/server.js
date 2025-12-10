// Node.js Backend for ZNPHI Measles Chatbot
// Simple API that can connect to your fine-tuned model or use mock responses

const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 8000;

// Middleware
app.use(cors());
app.use(express.json());

// Mock responses based on your training data
const responses = {
  "case definition": "A suspected measles case is defined as any person with fever and maculopapular (non-vesicular) generalized rash and cough, coryza (runny nose), or conjunctivitis (red eyes), OR any person in whom a clinician suspects measles.",
  
  "reporting": "Measles is an epidemic-prone disease requiring immediate reporting. Any suspected case must be reported to the next level within 24 hours using the Case-based Reporting Form. It should also be notified via the fastest means possible (e.g., phone or SMS).",
  
  "sample storage": "If testing is performed within 1 week, samples can be stored at 2°C to 8°C. For longer storage, samples must be frozen at -20°C or colder. Frost-free freezers should be avoided to prevent freeze-thaw cycles which degrade antibodies.",
  
  "dilution": "Patient samples must be diluted 1:101. This is achieved by mixing 10 µl of the patient sample with 1000 µl (1.0 ml) of the sample buffer containing RF-Absorbent.",
  
  "interpretation": "Results are interpreted using a ratio based on the calibrator:\n- Ratio < 0.8: Negative\n- Ratio ≥ 0.8 to < 1.1: Equivocal (Borderline)\n- Ratio ≥ 1.1: Positive",
  
  "alert threshold": "The alert threshold for measles is a single (1) suspected case. Even one case requires immediate investigation to confirm or rule out an outbreak.",
  
  "vitamin a infant": "For infants less than 6 months of age, the recommended Vitamin A dose is 50,000 IU.",
  
  "vitamin a child": "For children aged 12 months and older, the recommended Vitamin A dose is 200,000 IU.",
  
  "equivocal": "If a result is equivocal (ratio between 0.8 and 1.1), the test should be repeated using a fresh sample collected 7 to 10 days later.",
  
  "outbreak": "A confirmed measles outbreak is typically defined as 3 or more IgM positive measles cases detected in a health facility or district within a single month."
};

// Simple keyword matching function
function findBestResponse(question) {
  const lowerQuestion = question.toLowerCase();
  
  if (lowerQuestion.includes('case definition') || lowerQuestion.includes('suspected measles')) {
    return responses["case definition"];
  }
  if (lowerQuestion.includes('reporting') || lowerQuestion.includes('report')) {
    return responses["reporting"];
  }
  if (lowerQuestion.includes('storage') || lowerQuestion.includes('store')) {
    return responses["sample storage"];
  }
  if (lowerQuestion.includes('dilution') || lowerQuestion.includes('ratio')) {
    return responses["dilution"];
  }
  if (lowerQuestion.includes('interpret') || lowerQuestion.includes('results')) {
    return responses["interpretation"];
  }
  if (lowerQuestion.includes('alert') || lowerQuestion.includes('threshold')) {
    return responses["alert threshold"];
  }
  if (lowerQuestion.includes('infant') || lowerQuestion.includes('6 months')) {
    return responses["vitamin a infant"];
  }
  if (lowerQuestion.includes('12 months') || lowerQuestion.includes('older')) {
    return responses["vitamin a child"];
  }
  if (lowerQuestion.includes('equivocal') || lowerQuestion.includes('borderline')) {
    return responses["equivocal"];
  }
  if (lowerQuestion.includes('outbreak') || lowerQuestion.includes('confirmed')) {
    return responses["outbreak"];
  }
  
  // Default response
  return "I'm an AI assistant trained on IDSR and Measles Detection Guidelines. I can help answer questions about case definitions, reporting requirements, ELISA testing procedures, sample storage, result interpretation, alert thresholds, vitamin A dosing, and outbreak definitions. Please ask me a specific question about these topics.";
}

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    message: 'ZNPHI Measles Chatbot API is running',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// Chat endpoint
app.post('/chat', (req, res) => {
  try {
    const { question, context, max_tokens, temperature } = req.body;
    
    if (!question) {
      return res.status(400).json({
        error: 'Question is required',
        message: 'Please provide a question in the request body'
      });
    }
    
    console.log(`[${new Date().toISOString()}] Question: ${question}`);
    
    // Get response based on question
    const answer = findBestResponse(question);
    
    // Send response
    res.json({
      answer: answer,
      timestamp: new Date().toISOString(),
      confidence: 'high',
      model: 'ZNPHI-Measles-v1',
      context: context || 'IDSR and Measles Detection Guidelines'
    });
    
  } catch (error) {
    console.error('Error processing request:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: error.message
    });
  }
});

// Start server
app.listen(PORT, () => {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`✅ ZNPHI Measles Chatbot API is running`);
  console.log(`🌐 Server: http://localhost:${PORT}`);
  console.log(`📊 Health: http://localhost:${PORT}/health`);
  console.log(`💬 Chat:   POST http://localhost:${PORT}/chat`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('\n📝 Ready to receive questions!\n');
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n\n👋 Shutting down gracefully...');
  process.exit(0);
});
