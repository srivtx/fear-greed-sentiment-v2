#!/bin/bash

# Fear & Greed Sentiment Engine Setup Script

echo "🚀 Setting up Fear & Greed Sentiment Engine..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
echo "✅ Python version: $python_version"

# Install requirements
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Setup NLTK
echo "🔤 Setting up NLTK resources..."
python3 setup_nltk.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Quick start commands:"
echo "  Full run:       python3 main.py --mode run --no-twitter"
echo "  Data only:      python3 main.py --mode collect --no-twitter"  
echo "  Analysis only:  python3 main.py --mode analyze"
echo "  Help:           python3 main.py --help"
echo ""
echo "📊 Results will be saved in the data/ directory"
echo "🖼️  Visualizations will be in data/visualizations/"
