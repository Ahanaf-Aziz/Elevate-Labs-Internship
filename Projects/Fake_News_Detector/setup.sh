#!/bin/bash

echo "🚀 Setting up Fake News Detector..."

# Create models directory
mkdir -p models

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Prepare dataset and train model
echo "🤖 Training model..."
python -c "
import sys
sys.path.insert(0, '.')
from scripts.prepare_dataset import *
print('✓ Dataset prepared and model trained!')
"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the app, use:"
echo "  streamlit run app.py"
