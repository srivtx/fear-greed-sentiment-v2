#!/bin/bash
# Fear & Greed Sentiment Engine - Quick Start Script
# This script sets up and runs the complete system

set -e  # Exit on any error

echo "🚀 Fear & Greed Sentiment Engine - Quick Start"
echo "=============================================="
echo "📅 Started: $(date)"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Python is installed
print_info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
print_status "Python $PYTHON_VERSION found"

# Set up environment
PROJECT_ROOT=$(pwd)
export PYTHONPATH="$PROJECT_ROOT"
print_status "PYTHONPATH set to: $PROJECT_ROOT"

# Install dependencies
print_info "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_status "Dependencies installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Download NLTK data
print_info "Downloading NLTK data..."
if [ -f "scripts/download_nltk_data.py" ]; then
    python scripts/download_nltk_data.py
    print_status "NLTK data downloaded"
else
    print_warning "NLTK data script not found, downloading manually..."
    python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
    print_status "NLTK data downloaded manually"
fi

# Check configuration
print_info "Checking configuration..."
if [ -f "config/config.json" ]; then
    print_status "Configuration file found"
else
    print_warning "No config.json found, creating from example..."
    if [ -f "config/config.json.example" ]; then
        cp config/config.json.example config/config.json
        print_status "Configuration created from example"
    else
        print_warning "No example config found, system will use defaults"
    fi
fi

# Create necessary directories
print_info "Creating necessary directories..."
mkdir -p data logs
print_status "Directories created"

# Menu for user choice
echo
echo "🎯 What would you like to do?"
echo "1. 🔄 Run basic data collection and analysis (Simple mode)"
echo "2. 🌐 Start web dashboard"
echo "3. 🧪 Run system tests"
echo "4. ⚡ Run GoQuant real-time engine (Recommended for trading)"
echo "5. 📊 Run GoQuant batch analysis (Comprehensive analysis)"
echo "6. 🎯 Run GoQuant performance test (System benchmarking)"
echo "7. 🔧 Complete setup and start dashboard"
echo "8. 🚀 GoQuant full pipeline (Real-time + Dashboard)"
echo

read -p "Enter your choice (1-8): " choice

case $choice in
    1)
        print_info "Running basic data collection and analysis..."
        python main.py
        print_status "Data collection completed!"
        
        print_info "Starting web dashboard..."
        print_status "Dashboard will be available at: http://localhost:5000"
        python web_app.py
        ;;
    2)
        print_info "Starting web dashboard..."
        if [ ! -d "data/sentiment_"* ] 2>/dev/null; then
            print_warning "No sentiment data found. Running quick analysis first..."
            python main.py
        fi
        print_status "Dashboard will be available at: http://localhost:5000"
        python web_app.py
        ;;
    3)
        print_info "Starting web dashboard in background..."
        python web_app.py &
        WEBAPP_PID=$!
        sleep 5
        
        print_info "Running system tests..."
        ./scripts/testing/run_tests_demo.sh
        
        print_info "Stopping web dashboard..."
        kill $WEBAPP_PID
        print_status "Tests completed!"
        ;;
    4)
        print_info "Starting GoQuant Real-time Engine..."
        print_status "This is the recommended mode for live trading"
        print_info "The engine will run continuously with live data processing"
        
        echo "Select duration:"
        echo "1. Run for 10 minutes"
        echo "2. Run for 1 hour"
        echo "3. Run indefinitely (until stopped)"
        read -p "Enter choice (1-3): " duration_choice
        
        case $duration_choice in
            1) python goquant_main.py --mode=real-time --duration=10 ;;
            2) python goquant_main.py --mode=real-time --duration=60 ;;
            3) python goquant_main.py --mode=real-time ;;
            *) print_warning "Invalid choice, running for 10 minutes"
               python goquant_main.py --mode=real-time --duration=10 ;;
        esac
        ;;
    5)
        print_info "Running GoQuant Batch Analysis..."
        print_status "This provides comprehensive analysis with detailed reports"
        
        echo "Select data source:"
        echo "1. All sources (Reddit + News + Market)"
        echo "2. Reddit only"
        echo "3. News only"
        echo "4. Analyze existing data"
        read -p "Enter choice (1-4): " source_choice
        
        case $source_choice in
            1) python goquant_main.py --mode=batch ;;
            2) python goquant_main.py --mode=batch --source=reddit ;;
            3) python goquant_main.py --mode=batch --source=news ;;
            4) python goquant_main.py --mode=batch --analyze-only ;;
            *) print_warning "Invalid choice, using all sources"
               python goquant_main.py --mode=batch ;;
        esac
        
        print_status "Batch analysis completed! Check data/ directory for results"
        ;;
    6)
        print_info "Running GoQuant Performance Test..."
        print_status "This will benchmark the system against GoQuant requirements"
        
        echo "Select test duration:"
        echo "1. Quick test (2 minutes)"
        echo "2. Standard test (5 minutes)"
        echo "3. Extended test (10 minutes)"
        read -p "Enter choice (1-3): " test_choice
        
        case $test_choice in
            1) python goquant_main.py --mode=performance-test --duration=2 ;;
            2) python goquant_main.py --mode=performance-test --duration=5 ;;
            3) python goquant_main.py --mode=performance-test --duration=10 ;;
            *) print_warning "Invalid choice, running quick test"
               python goquant_main.py --mode=performance-test --duration=2 ;;
        esac
        
        print_status "Performance test completed!"
        ;;
    7)
        print_info "Running complete setup..."
        
        # Run data collection
        print_info "Step 1/3: Collecting initial data..."
        python main.py
        
        # Run tests
        print_info "Step 2/3: Running system validation..."
        python web_app.py &
        WEBAPP_PID=$!
        sleep 5
        
        if [ -f "tests/test_comprehensive_suite.py" ]; then
            python tests/test_comprehensive_suite.py
        else
            print_warning "Test files not found in tests directory"
        fi
        
        print_info "Step 3/3: Starting dashboard..."
        print_status "Dashboard is ready at: http://localhost:5000"
        print_status "Press Ctrl+C to stop the dashboard"
        
        # Keep the web app running
        wait $WEBAPP_PID
        ;;
    8)
        print_info "Starting GoQuant Full Pipeline..."
        print_status "This is the complete professional trading setup"
        
        # Step 1: Initial data collection
        print_info "Step 1/4: Initial data collection..."
        python goquant_main.py --mode=batch --duration=2
        
        # Step 2: Start web dashboard
        print_info "Step 2/4: Starting web dashboard..."
        python web_app.py &
        WEBAPP_PID=$!
        sleep 5
        
        # Step 3: Run validation tests
        print_info "Step 3/4: Running system validation..."
        if [ -f "tests/test_comprehensive_suite.py" ]; then
            python tests/test_comprehensive_suite.py
        fi
        
        # Step 4: Start real-time engine
        print_info "Step 4/4: Starting real-time engine..."
        print_status "Dashboard: http://localhost:5000"
        print_status "Real-time engine will run with live updates"
        print_status "Press Ctrl+C to stop both services"
        
        # Start real-time engine (this will run indefinitely)
        python goquant_main.py --mode=real-time --duration=60 &
        REALTIME_PID=$!
        
        # Wait for either process to finish
        wait $WEBAPP_PID $REALTIME_PID
        
        # Clean up
        kill $WEBAPP_PID $REALTIME_PID 2>/dev/null || true
        ;;
    *)
        print_error "Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo
print_status "Quick start completed at $(date)"
echo "=============================================="
echo "📚 For more information, check the docs/ directory"
echo "🧪 For testing, use scripts in scripts/testing/"
echo "⚙️  For setup scripts, check scripts/setup/"
echo "🎉 Happy analyzing!"
