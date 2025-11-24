# CodeBridge Model Export

## Contents
- `model.pt` - Trained model weights and configuration
- `tokenizer.pkl` - Custom tokenizer with vocabulary
- `config.json` - Training configuration and metrics
- `sample_data.json` - Sample training/validation data
- `inference.py` - Script to load and use the model

## Model Details
- **Type**: SimpleTransformer
- **Parameters**: 1,748,486
- **Vocabulary Size**: 262
- **Training Date**: 2025-11-22T07:56:34.697622
- **Final Training Loss**: 0.0028
- **Final Validation Loss**: 0.0027

## Usage
```python
from inference import load_model
checkpoint, tokenizer, config = load_model('./')
```

## Requirements
- PyTorch >= 2.9.0+cu126
- Python >= 3.7
