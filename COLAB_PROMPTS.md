# Colab Notebook Prompts for ZNPHI Measles Chatbot

## 📋 Model Information
- **Base Model:** Mistral-7B-Instruct-v0.2
- **Fine-tuning Method:** QLoRA (4-bit quantization)
- **Training Data:** IDSR 3rd Edition & Measles Detection Guidelines

## 🔧 Prompt Template Used in Training

```python
def format_instruction(sample):
    return f"""### Instruction:
{sample['instruction']}

### Context:
{sample['context']}

### Response:
{sample['response']}"""
```

## 💻 Code to Add to Your Colab Notebook for Testing

### Step 1: Load Your Fine-Tuned Model (After Training)

```python
# After training is complete, merge the LoRA weights with base model
from peft import PeftModel

# Load the fine-tuned model
fine_tuned_model = PeftModel.from_pretrained(model, "./measles_model_output")
fine_tuned_model = fine_tuned_model.merge_and_unload()
```

### Step 2: Create Inference Function

```python
def generate_response(instruction, context="IDSR and Measles Detection Guidelines", max_new_tokens=256):
    """
    Generate a response from the fine-tuned model
    
    Args:
        instruction: The question to ask
        context: Context for the question
        max_new_tokens: Maximum tokens to generate
    
    Returns:
        Generated response text
    """
    # Format the prompt according to training template
    prompt = f"""### Instruction:
{instruction}

### Context:
{context}

### Response:
"""
    
    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode and extract only the response part
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract only the generated response (after "### Response:")
    if "### Response:" in full_response:
        response = full_response.split("### Response:")[-1].strip()
    else:
        response = full_response
    
    return response

# Test the function
print("Testing the fine-tuned model...\n")
response = generate_response("What is the Alert Threshold for measles?")
print(response)
```

### Step 3: Test with Multiple Prompts

```python
# Test prompts from your training data
test_prompts = [
    {
        "instruction": "What is the standard case definition for a suspected measles case?",
        "context": "IDSR 3rd Edition - Standard Case Definitions"
    },
    {
        "instruction": "How should serum samples be stored if testing is not performed immediately?",
        "context": "VIR-TECH-011-v2 Detection of Anti-Measles IgM Antibodies"
    },
    {
        "instruction": "What is the Alert Threshold for measles?",
        "context": "IDSR 3rd Edition - Section 11"
    },
    {
        "instruction": "What is the recommended Vitamin A dose for children aged 12 months and older?",
        "context": "IDSR 3rd Edition - Measles Treatment Guidelines"
    },
    {
        "instruction": "How are the results of the Measles ELISA interpreted?",
        "context": "VIR-TECH-011-v2 Detection of Anti-Measles IgM Antibodies"
    }
]

print("="*80)
print("TESTING FINE-TUNED MODEL WITH MULTIPLE PROMPTS")
print("="*80)

for i, test in enumerate(test_prompts, 1):
    print(f"\n\n{'='*80}")
    print(f"TEST {i}/{len(test_prompts)}")
    print('='*80)
    print(f"Question: {test['instruction']}")
    print(f"Context: {test['context']}")
    print("-"*80)
    
    response = generate_response(test['instruction'], test['context'])
    
    print(f"Response:\n{response}")
    print('='*80)
```

## 🧪 Example Prompts to Test in Colab

### Basic Medical Questions

```python
# Test 1: Case Definition
generate_response(
    "What is the standard case definition for a suspected measles case?",
    "IDSR 3rd Edition - Standard Case Definitions"
)

# Test 2: Reporting Requirements
generate_response(
    "What are the immediate reporting requirements for a suspected measles case?",
    "IDSR 3rd Edition - Section 2: Reporting"
)

# Test 3: Vitamin A Administration
generate_response(
    "When should Vitamin A be administered to a measles patient?",
    "IDSR 3rd Edition - Measles Treatment Guidelines"
)
```

### Laboratory/Technical Questions

```python
# Test 4: Sample Types
generate_response(
    "What sample types are accepted for the Measles IgM ELISA test?",
    "VIR-TECH-011-v2 Detection of Anti-Measles IgM Antibodies"
)

# Test 5: Sample Storage
generate_response(
    "How should serum samples be stored if testing is not performed immediately?",
    "VIR-TECH-011-v2 Detection of Anti-Measles IgM Antibodies"
)

# Test 6: Dilution Ratio
generate_response(
    "What is the exact dilution ratio for patient samples in the Measles ELISA test?",
    "VIR-TECH-011-v2 Detection of Anti-Measles IgM Antibodies"
)
```

### Procedure Questions

```python
# Test 7: ELISA Interpretation
generate_response(
    "How are the results of the Measles ELISA interpreted?",
    "VIR-TECH-011-v2 Detection of Anti-Measles IgM Antibodies"
)

# Test 8: Equivocal Results
generate_response(
    "What should be done if a sample yields an equivocal result?",
    "VIR-TECH-011-v2 Detection of Anti-Measles IgM Antibodies"
)

# Test 9: Waste Disposal
generate_response(
    "How should waste generated from the ELISA test be disposed of?",
    "VIR-TECH-011-v2 Detection of Anti-Measles IgM Antibodies"
)
```

### Public Health Surveillance

```python
# Test 10: Alert Threshold
generate_response(
    "What is the Alert Threshold for measles?",
    "IDSR 3rd Edition - Section 11"
)

# Test 11: Confirmed Outbreak
generate_response(
    "What does a confirmed measles outbreak look like?",
    "IDSR 3rd Edition - Section 11"
)

# Test 12: Community Surveillance
generate_response(
    "Who should be involved in Community-Based Surveillance for measles?",
    "IDSR 3rd Edition - Section 1"
)
```

## 🎯 Testing New Questions (Generalization)

Try questions NOT in the training data to test generalization:

```python
# Generalization Test 1
generate_response(
    "What are the clinical complications of measles?",
    "IDSR 3rd Edition - Measles"
)

# Generalization Test 2
generate_response(
    "How long is the measles incubation period?",
    "IDSR 3rd Edition - Measles"
)

# Generalization Test 3
generate_response(
    "What is the difference between suspected and confirmed measles cases?",
    "IDSR 3rd Edition - Case Definitions"
)
```

## 📊 Evaluation Metrics

```python
# Compare model output with expected responses
def evaluate_response(instruction, expected_response, context):
    """
    Simple evaluation function
    """
    generated = generate_response(instruction, context, max_new_tokens=200)
    
    print(f"Question: {instruction}")
    print(f"\nExpected: {expected_response[:200]}...")
    print(f"\nGenerated: {generated[:200]}...")
    print(f"\nMatch Score: {1 if expected_response.lower() in generated.lower() else 0}")
    print("-"*80)

# Example evaluation
evaluate_response(
    "What is the Alert Threshold for measles?",
    "The alert threshold for measles is a single (1) suspected case.",
    "IDSR 3rd Edition - Section 11"
)
```

## 💾 Save Model for Later Use

```python
# Save the fine-tuned model
model.save_pretrained("./znphi_measles_model")
tokenizer.save_pretrained("./znphi_measles_model")

# Later, to load:
# model = AutoModelForCausalLM.from_pretrained("./znphi_measles_model")
# tokenizer = AutoTokenizer.from_pretrained("./znphi_measles_model")
```

## 🚀 Export to Hugging Face Hub (Optional)

```python
# Push to Hugging Face Hub for easy deployment
from huggingface_hub import notebook_login

# Login
notebook_login()

# Push model
model.push_to_hub("your-username/znphi-measles-chatbot")
tokenizer.push_to_hub("your-username/znphi-measles-chatbot")

# Later, load from hub:
# model = AutoModelForCausalLM.from_pretrained("your-username/znphi-measles-chatbot")
```

## 📝 Notes

1. **Prompt Format:** Always use the exact format with `### Instruction:`, `### Context:`, and `### Response:` markers
2. **Temperature:** Adjust between 0.7-1.0 for creativity vs consistency
3. **Max Tokens:** Increase if responses are cut off
4. **Context:** Include relevant context for better responses

---

**Copy these code blocks into new cells in your Colab notebook AFTER training completes!**
