#!/bin/bash

# 🚀 Fear & Greed Sentiment Engine - Quick Setup Script
# This script sets up and runs the complete sentiment analysis system

echo "🚀 FEAR & GREED SENTIMENT ENGINE - QUICK SETUP"
echo "=============================================="
echo ""

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>/dev/null || python --version 2>/dev/null)
if [[ $? -eq 0 ]]; then
    echo "✅ Found: $python_version"
else
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

# Install dependencies if needed
echo ""
echo "📦 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Check if config exists
echo ""
echo "⚙️ Checking configuration..."
if [ ! -f "config/config.json" ]; then
    if [ -f "config/config.json.example" ]; then
        cp config/config.json.example config/config.json
        echo "⚠️ Created config.json from example"
        echo "💡 Edit config/config.json to add your API keys (optional)"
    else
        echo "❌ No config file found"
        exit 1
    fi
else
    echo "✅ Configuration file exists"
fi

# Create data directory if needed
echo ""
echo "📁 Setting up data directory..."
mkdir -p data
echo "✅ Data directory ready"

# Function to run data collection
run_collection() {
    echo ""
    echo "📊 RUNNING DATA COLLECTION & ANALYSIS"
    echo "-----------------------------------"
    python main.py
    if [[ $? -eq 0 ]]; then
        echo "✅ Data collection completed successfully"
        return 0
    else
        echo "⚠️ Data collection had issues, but continuing..."
        return 1
    fi
}

# Function to start web app
start_webapp() {
    echo ""
    echo "🌐 STARTING WEB DASHBOARD"
    echo "----------------------"
    echo "🚀 Dashboard will be available at: http://localhost:5000"
    echo "💡 Press Ctrl+C to stop the server"
    echo ""
    python web_app.py
}

# Function to run tests
run_tests() {
    echo ""
    echo "🧪 RUNNING COMPREHENSIVE TESTS"
    echo "----------------------------"
    python test_comprehensive_suite.py
}

# Function to validate data
validate_data() {
    echo ""
    echo "📋 VALIDATING CURRENT DATA"
    echo "------------------------"
    python dashboard_validation.py
}

# Function to demonstrate real analysis
demo_analysis() {
    echo ""
    echo "🎯 REAL-WORLD ANALYSIS DEMO"
    echo "-------------------------"
    python real_world_demo.py
}

# Main menu
show_menu() {
    echo ""
    echo "🎯 WHAT WOULD YOU LIKE TO DO?"
    echo "1. 📊 Quick Start (Collection + Web Dashboard)"
    echo "2. 📡 Run Data Collection Only"
    echo "3. 🌐 Start Web Dashboard Only"
    echo "4. 🧪 Run Tests"
    echo "5. 📋 Validate Data"
    echo "6. 🎬 Real-World Analysis Demo"
    echo "7. ❌ Exit"
    echo ""
    read -p "Enter your choice (1-7): " choice
}

# Main execution
echo ""
echo "🔄 Initial setup complete!"

while true; do
    show_menu
    
    case $choice in
        1)
            echo "🚀 QUICK START SELECTED"
            run_collection
            echo ""
            echo "🌐 Starting web dashboard..."
            echo "📱 Open http://localhost:5000 in your browser"
            start_webapp
            ;;
        2)
            run_collection
            ;;
        3)
            start_webapp
            ;;
        4)
            run_tests
            ;;
        5)
            validate_data
            ;;
        6)
            demo_analysis
            ;;
        7)
            echo ""
            echo "👋 Thanks for using Fear & Greed Sentiment Engine!"
            echo "🌐 Remember: Dashboard available at http://localhost:5000"
            echo ""
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please enter 1-7."
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done
