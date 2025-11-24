import torch
import pickle
import json

def load_model(model_dir='./'):
    """Load the trained CodeBridge model"""
    
    # Load model checkpoint
    checkpoint = torch.load(f'{model_dir}/model.pt', map_location='cpu')
    
    # Load tokenizer
    with open(f'{model_dir}/tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    
    # Load config
    with open(f'{model_dir}/config.json', 'r') as f:
        config = json.load(f)
    
    print(f"Model loaded: {config['parameters']:,} parameters")
    print(f"Vocabulary size: {config['vocab_size']}")
    print(f"Training date: {config['training_date']}")
    
    return checkpoint, tokenizer, config

def generate_explanation(model, tokenizer, code, language='javascript'):
    """Generate explanation for given code"""
    
    # Prepare input
    input_text = f"{language}: {code}"
    input_ids = torch.tensor([tokenizer.encode(input_text)])
    
    # Generate (simplified - just forward pass for demo)
    with torch.no_grad():
        output = model(input_ids)
        predicted_ids = output.argmax(dim=-1)
    
    # Decode
    explanation = tokenizer.decode(predicted_ids[0].tolist())
    
    return explanation

if __name__ == "__main__":
    # Example usage
    checkpoint, tokenizer, config = load_model('./')
    
    # Test with sample code
    test_code = "function validateUser(data) { return data.email != null; }"
    print(f"\nCode: {test_code}")
    print(f"Language: JavaScript")
    
    # Note: Full model reconstruction would require the SimpleTransformer class definition
    print("\nTo use the model, you need to:")
    print("1. Import the SimpleTransformer class")
    print("2. Reconstruct model with config parameters")
    print("3. Load the saved state_dict")
