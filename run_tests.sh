#!/bin/bash
# Quick Test Runner Script for Fear & Greed Sentiment Engine

cd /workspaces/fear-greed-sentiment-v2
export PYTHONPATH=/workspaces/fear-greed-sentiment-v2

echo "🚀 Fear & Greed Sentiment Engine - Quick Test Runner"
echo "=================================================="
echo "📅 Started: $(date)"
echo

# Check if web app is running
if curl -s http://localhost:5000/ > /dev/null 2>&1; then
    echo "✅ Web app is running"
else
    echo "❌ Web app not running. Please start with: python web_app.py"
    exit 1
fi

echo

# Menu for user choice
echo "Choose what to test:"
echo "1. 🧪 Comprehensive Test Suite (Full system validation)"
echo "2. 📊 Trading Signals Validation (Signal analysis)"
echo "3. 🎛️ Dashboard Data Validation (Data validation report)"
echo "4. 🔄 Run All Tests (Complete validation)"
echo "5. 📋 Quick Health Check (Basic system check)"
echo

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "🧪 Running Comprehensive Test Suite..."
        echo "======================================"
        python test_comprehensive_suite.py
        ;;
    2)
        echo "📊 Running Trading Signals Validation..."
        echo "======================================="
        python validate_signals.py
        ;;
    3)
        echo "🎛️ Running Dashboard Data Validation..."
        echo "======================================="
        python dashboard_validation.py
        ;;
    4)
        echo "🔄 Running All Tests..."
        echo "====================="
        
        timestamp=$(date +"%Y%m%d_%H%M%S")
        report_dir="test_reports_$timestamp"
        mkdir -p "$report_dir"
        
        echo "1/3 🧪 Comprehensive Test Suite..."
        python test_comprehensive_suite.py | tee "$report_dir/comprehensive_test.txt"
        
        echo
        echo "2/3 📊 Trading Signals Validation..."
        python validate_signals.py | tee "$report_dir/signal_validation.txt"
        
        echo
        echo "3/3 🎛️ Dashboard Data Validation..."
        python dashboard_validation.py | tee "$report_dir/dashboard_validation.txt"
        
        echo
        echo "✅ All tests completed! Reports saved in $report_dir/"
        ;;
    5)
        echo "📋 Quick Health Check..."
        echo "======================="
        
        # Check API endpoints
        endpoints=("/api/sentiment" "/api/signals" "/api/system_stats")
        
        for endpoint in "${endpoints[@]}"; do
            if curl -s -f "http://localhost:5000$endpoint" > /dev/null; then
                echo "✅ $endpoint: OK"
            else
                echo "❌ $endpoint: ERROR"
            fi
        done
        
        # Get basic metrics
        echo
        echo "📊 Current Metrics:"
        curl -s http://localhost:5000/api/sentiment | python -c "
import json, sys
try:
    data = json.load(sys.stdin)
    fg = data['fear_greed_index']
    print(f'💡 Fear & Greed Index: {fg[\"fear_greed_index\"]:.2f}')
    print(f'🎭 Market Sentiment: {fg[\"market_sentiment\"]}')
    print(f'📈 Data Points: {fg[\"total_mentions\"]:,}')
    print(f'⏰ Last Updated: {fg[\"timestamp\"]}')
except:
    print('❌ Unable to fetch metrics')
"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo
echo "🎉 Testing completed at $(date)"
echo "=================================================="
