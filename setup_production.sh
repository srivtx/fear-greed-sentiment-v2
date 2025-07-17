#!/bin/bash

# 🚀 GoQuant Fear & Greed Sentiment Engine - Production Setup
# Automated setup script for production deployment

set -e  # Exit on any error

echo "🎯 GoQuant Fear & Greed Sentiment Engine - Production Setup"
echo "============================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python version
check_python() {
    print_step "Checking Python version..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
            print_success "Python $PYTHON_VERSION found"
            PYTHON_CMD="python3"
        else
            print_error "Python 3.8+ required, found $PYTHON_VERSION"
            exit 1
        fi
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
            print_success "Python $PYTHON_VERSION found"
            PYTHON_CMD="python"
        else
            print_error "Python 3.8+ required, found $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python not found. Please install Python 3.8+"
        exit 1
    fi
}

# Create virtual environment
setup_venv() {
    print_step "Setting up virtual environment..."
    
    if [ ! -d "venv" ]; then
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        print_success "Virtual environment activated"
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
        print_success "Virtual environment activated (Windows)"
    else
        print_error "Could not activate virtual environment"
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    print_step "Installing Python dependencies..."
    
    if [ -f "requirements.txt" ]; then
        pip install --upgrade pip
        pip install -r requirements.txt
        print_success "Dependencies installed successfully"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Setup configuration
setup_config() {
    print_step "Setting up configuration..."
    
    if [ ! -f "config/config.json" ]; then
        if [ -f "config/config.json.example" ]; then
            cp config/config.json.example config/config.json
            print_success "Configuration template copied to config/config.json"
            print_warning "Please edit config/config.json with your API keys"
        else
            print_error "config/config.json.example not found"
            exit 1
        fi
    else
        print_warning "config/config.json already exists"
    fi
}

# Setup NLTK data
setup_nltk() {
    print_step "Setting up NLTK data..."
    
    $PYTHON_CMD -c "
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('vader_lexicon', quiet=True)

print('NLTK data downloaded successfully')
"
    
    if [ $? -eq 0 ]; then
        print_success "NLTK data setup completed"
    else
        print_error "NLTK data setup failed"
        exit 1
    fi
}

# Create data directories
setup_directories() {
    print_step "Creating data directories..."
    
    directories=(
        "data"
        "data/signals"
        "data/visualizations"
        "data/temp"
        "data/market_cache"
        "logs"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
        fi
    done
    
    print_success "Data directories created"
}

# Validate installation
validate_installation() {
    print_step "Validating installation..."
    
    # Test import of main modules
    $PYTHON_CMD -c "
import sys
sys.path.append('.')

try:
    import numpy
    import pandas
    import yfinance
    import textblob
    import praw
    import requests
    import aiohttp
    
    # Test core modules
    from engine import FearGreedEngine
    from real_time_engine import RealTimeFearGreedEngine
    from advanced_sentiment_analyzer import AdvancedFinancialSentimentAnalyzer
    from advanced_signal_generator import AdvancedSignalGenerator
    
    print('✅ All core modules imported successfully')
    
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        print_success "Installation validation passed"
    else
        print_error "Installation validation failed"
        exit 1
    fi
}

# Run system test
run_system_test() {
    print_step "Running system test..."
    
    if [ -f "validate_goquant_system.py" ]; then
        $PYTHON_CMD validate_goquant_system.py
        
        if [ $? -eq 0 ]; then
            print_success "System test completed"
        else
            print_warning "System test completed with warnings (check API keys)"
        fi
    else
        print_warning "System validation script not found"
    fi
}

# Main setup process
main() {
    echo "Starting production setup..."
    echo
    
    check_python
    setup_venv
    install_dependencies
    setup_config
    setup_nltk
    setup_directories
    validate_installation
    run_system_test
    
    echo
    echo "============================================================"
    print_success "🎉 GoQuant Fear & Greed Sentiment Engine setup complete!"
    echo
    echo "📋 Next steps:"
    echo "1. Edit config/config.json with your API keys"
    echo "2. Run: python goquant_main.py --mode real-time"
    echo "3. For validation: python validate_goquant_system.py"
    echo
    echo "📚 Documentation:"
    echo "- DEPLOYMENT_GUIDE.md: Production deployment guide"
    echo "- GOQUANT_DOCUMENTATION.md: Technical documentation"
    echo "- FILE_STRUCTURE.md: Project structure overview"
    echo
    print_success "Your production-ready trading engine is ready to deploy!"
}

# Run main function
main "$@"
