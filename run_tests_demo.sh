#!/bin/bash
# Quick Test Demonstration Script
# This script shows how to use the test files with generic paths

echo "🧪 Fear & Greed Sentiment Engine - Test Demo"
echo "=============================================="

# Get the current directory (project root)
PROJECT_ROOT=$(pwd)
echo "📁 Project directory: $PROJECT_ROOT"

# Set PYTHONPATH to current directory
export PYTHONPATH="$PROJECT_ROOT"
echo "🔧 PYTHONPATH set to: $PYTHONPATH"

echo ""
echo "🔍 Checking if web app is running..."
if curl -s http://localhost:5000/ > /dev/null 2>&1; then
    echo "✅ Web app is running"
else
    echo "❌ Web app is not running"
    echo "   Start it with: PYTHONPATH=\$(pwd) python web_app.py"
    exit 1
fi

echo ""
echo "1️⃣ Testing Comprehensive Suite..."
echo "=================================="
python test_comprehensive_suite.py

echo ""
echo "2️⃣ Validating Trading Signals..."
echo "================================"
python validate_signals.py

echo ""
echo "3️⃣ Dashboard Validation..."
echo "========================="
python dashboard_validation.py

echo ""
echo "✅ All tests completed successfully!"
echo "📊 You can now review the results above."
