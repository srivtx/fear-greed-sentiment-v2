#!/usr/bin/env python3
"""
Signals Validation Script
Tests and validates that trading signals are working correctly
"""

import requests
import json
from datetime import datetime

def validate_signals():
    """Validate that signals are working correctly"""
    
    print("🔍 SIGNALS VALIDATION REPORT")
    print("=" * 50)
    print(f"⏰ Validation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test signals API endpoint
    print("📡 TESTING SIGNALS API ENDPOINT")
    print("-" * 30)
    
    try:
        response = requests.get('http://localhost:5000/api/signals', timeout=5)
        
        if response.status_code == 200:
            print("✅ Signals API: Responding correctly")
            
            data = response.json()
            
            # Check data structure
            if 'signals' in data:
                signals = data['signals']
                signal_count = len(signals)
                
                print(f"📊 Signal Count: {signal_count}")
                
                if signal_count > 0:
                    print("✅ Trading Signals: FOUND")
                    print(f"🕒 Timestamp: {data.get('timestamp', 'N/A')}")
                    print(f"🎭 Market Sentiment: {data.get('market_sentiment', 'N/A')}")
                    print(f"📈 Fear & Greed Index: {data.get('fear_greed_index', 'N/A'):.2f}")
                    
                    print("\n🎯 ACTIVE TRADING SIGNALS:")
                    print("-" * 30)
                    
                    for i, signal in enumerate(signals, 1):
                        symbol = signal.get('symbol', 'N/A')
                        signal_type = signal.get('type', 'N/A')
                        confidence = signal.get('confidence', 0) * 100
                        sentiment = signal.get('sentiment', 0)
                        mentions = signal.get('mentions', 0)
                        entity_type = signal.get('entity_type', 'N/A')
                        
                        # Signal emoji
                        if signal_type == 'BUY':
                            emoji = "🟢"
                        elif signal_type == 'SELL':
                            emoji = "🔴"
                        else:
                            emoji = "🟡"
                        
                        print(f"  {i}. {emoji} {symbol:5} | {signal_type:4} | {confidence:5.1f}% confidence | {sentiment:+.3f} sentiment | {mentions:3} mentions | {entity_type}")
                    
                    # Signal analysis
                    buy_signals = len([s for s in signals if s.get('type') == 'BUY'])
                    sell_signals = len([s for s in signals if s.get('type') == 'SELL'])
                    hold_signals = len([s for s in signals if s.get('type') == 'HOLD'])
                    
                    print(f"\n📊 SIGNAL BREAKDOWN:")
                    print(f"  🟢 BUY signals: {buy_signals}")
                    print(f"  🔴 SELL signals: {sell_signals}")
                    print(f"  🟡 HOLD signals: {hold_signals}")
                    
                    # Entity type analysis
                    crypto_signals = len([s for s in signals if s.get('entity_type') == 'crypto'])
                    stock_signals = len([s for s in signals if s.get('entity_type') == 'stock'])
                    
                    print(f"\n💎 ASSET TYPE BREAKDOWN:")
                    print(f"  🪙 Crypto signals: {crypto_signals}")
                    print(f"  📈 Stock signals: {stock_signals}")
                    
                    # Confidence analysis
                    confidences = [s.get('confidence', 0) for s in signals]
                    avg_confidence = sum(confidences) / len(confidences) * 100
                    max_confidence = max(confidences) * 100
                    
                    print(f"\n🎯 CONFIDENCE ANALYSIS:")
                    print(f"  📊 Average confidence: {avg_confidence:.1f}%")
                    print(f"  🔝 Highest confidence: {max_confidence:.1f}%")
                    
                else:
                    print("⚠️ Trading Signals: No signals found")
                    print("💡 This could mean:")
                    print("   - No significant sentiment detected")
                    print("   - All assets below confidence threshold")
                    print("   - Signal generation not yet run")
                    
            else:
                print("❌ Invalid response structure - missing 'signals' field")
                
        else:
            print(f"❌ Signals API: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        print("💡 Make sure the web app is running: python web_app.py")
        return
    
    # Test dashboard integration
    print("\n🌐 TESTING DASHBOARD INTEGRATION")
    print("-" * 30)
    
    try:
        # Test main dashboard page
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard: Loading correctly")
            
            # Check if signals section exists in HTML
            if 'signalsTable' in response.text:
                print("✅ Signals Table: Present in dashboard")
            else:
                print("❌ Signals Table: Missing from dashboard")
                
            if 'activeSignals' in response.text:
                print("✅ Active Signals Counter: Present")
            else:
                print("❌ Active Signals Counter: Missing")
                
        else:
            print(f"❌ Dashboard: HTTP {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Dashboard Connection Error: {e}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("-" * 30)
    
    if signal_count > 0:
        print("✅ System Status: SIGNALS WORKING CORRECTLY")
        print("🎯 Next Steps:")
        print("  1. View signals in dashboard: http://localhost:5000")
        print("  2. Monitor signal confidence levels")
        print("  3. Track signal performance over time")
        print("  4. Consider setting up alerts for high-confidence signals")
    else:
        print("⚠️ System Status: NO ACTIVE SIGNALS")
        print("🔧 Troubleshooting:")
        print("  1. Run: python main.py  (to collect fresh data)")
        print("  2. Generate signals manually with signal generator")
        print("  3. Check sentiment analysis results")
        print("  4. Verify confidence thresholds in config")
    
    print(f"\n{'='*50}")
    print("🎉 SIGNALS VALIDATION COMPLETE")

if __name__ == "__main__":
    validate_signals()
