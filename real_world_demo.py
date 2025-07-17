#!/usr/bin/env python3
"""
Real-World Analysis Demonstration
Shows how the Fear & Greed Engine performs real sentiment analysis
"""

import requests
import json
from datetime import datetime
import time

def demonstrate_real_analysis():
    """Demonstrate real-world sentiment analysis capabilities"""
    
    print("🚀 FEAR & GREED ENGINE - REAL-WORLD ANALYSIS DEMO")
    print("=" * 70)
    print(f"⏰ Demo started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test API connectivity
    print("🔗 TESTING API CONNECTIVITY")
    print("-" * 40)
    try:
        response = requests.get('http://localhost:5000/api/sentiment', timeout=5)
        if response.status_code == 200:
            print("✅ API is online and responding")
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        print("💡 Make sure to run: python web_app.py")
        return
    
    # Get current sentiment data
    print("\n📊 CURRENT MARKET SENTIMENT ANALYSIS")
    print("-" * 40)
    
    data = response.json()
    fg_data = data['fear_greed_index']
    
    # Display main metrics
    index_value = fg_data['fear_greed_index']
    sentiment_label = fg_data['market_sentiment']
    data_points = fg_data['total_mentions']
    timestamp = fg_data['timestamp']
    
    print(f"📈 Fear & Greed Index: {index_value:.2f}/100")
    print(f"🎭 Market Sentiment: {sentiment_label}")
    print(f"📊 Data Points Analyzed: {data_points:,} real posts/articles")
    print(f"⏰ Last Updated: {timestamp}")
    
    # Determine market condition
    if index_value <= 25:
        condition = "🔴 EXTREME FEAR - Potential buying opportunity"
        emoji = "😰"
    elif index_value <= 45:
        condition = "🟡 FEAR - Market uncertainty"
        emoji = "😟"
    elif index_value <= 55:
        condition = "⚪ NEUTRAL - Balanced sentiment"
        emoji = "😐"
    elif index_value <= 75:
        condition = "🟢 GREED - Optimistic market"
        emoji = "😊"
    else:
        condition = "🔴 EXTREME GREED - Potential selling opportunity"
        emoji = "🤑"
    
    print(f"\n{emoji} Market Condition: {condition}")
    
    # Show calculation breakdown
    print("\n🧮 CALCULATION BREAKDOWN")
    print("-" * 40)
    calc = fg_data['calculation_details']
    
    sentiment_comp = calc['sentiment_component']
    distribution_comp = calc['distribution_component']
    engagement_comp = calc['engagement_component']
    volatility_comp = calc['volatility_component']
    market_noise = calc['market_noise']
    
    print(f"🎯 Sentiment Component (30%):     {sentiment_comp:6.2f}")
    print(f"⚖️  Distribution Component (35%):  {distribution_comp:6.2f}")
    print(f"📢 Engagement Component (20%):    {engagement_comp:6.2f}")
    print(f"📊 Volatility Component (15%):    {volatility_comp:6.2f}")
    print(f"🎲 Market Noise (±2%):           {market_noise:+6.2f}")
    print(f"   {'─' * 35}")
    print(f"📝 Final Fear & Greed Index:      {index_value:6.2f}")
    
    # Show sentiment distribution
    print(f"\n😊 Positive Posts: {fg_data['general_positive']} ({calc['positive_pct']}%)")
    print(f"😐 Neutral Posts:  {fg_data['general_neutral']} ({calc['neutral_pct']}%)")
    print(f"😞 Negative Posts: {fg_data['general_negative']} ({calc['negative_pct']}%)")
    
    # Asset-specific analysis
    print("\n💎 ASSET-SPECIFIC SENTIMENT")
    print("-" * 40)
    
    entity_data = data['entity_sentiment']
    
    # Analyze top cryptocurrencies
    print("🪙 Top Cryptocurrencies:")
    crypto_sentiments = []
    for crypto, sentiment in entity_data['cryptos'].items():
        if sentiment['mentions'] > 0:
            crypto_sentiments.append({
                'name': crypto,
                'score': sentiment['compound'],
                'mentions': sentiment['mentions'],
                'label': sentiment['sentiment_label']
            })
    
    crypto_sentiments.sort(key=lambda x: x['score'], reverse=True)
    
    for i, crypto in enumerate(crypto_sentiments[:5], 1):
        emoji = "🟢" if crypto['label'] == 'positive' else "🔴" if crypto['label'] == 'negative' else "🟡"
        print(f"  {i}. {emoji} {crypto['name']:4} | Score: {crypto['score']:+.3f} | {crypto['mentions']:3} mentions | {crypto['label'].title()}")
    
    # Analyze top stocks
    print("\n📈 Top Stocks:")
    stock_sentiments = []
    for stock, sentiment in entity_data['stocks'].items():
        if sentiment['mentions'] > 0:
            stock_sentiments.append({
                'name': stock,
                'score': sentiment['compound'],
                'mentions': sentiment['mentions'],
                'label': sentiment['sentiment_label']
            })
    
    stock_sentiments.sort(key=lambda x: x['score'], reverse=True)
    
    for i, stock in enumerate(stock_sentiments[:5], 1):
        emoji = "🟢" if stock['label'] == 'positive' else "🔴" if stock['label'] == 'negative' else "🟡"
        print(f"  {i}. {emoji} {stock['name']:5} | Score: {stock['score']:+.3f} | {stock['mentions']:3} mentions | {stock['label'].title()}")
    
    # Historical context
    print("\n📊 HISTORICAL CONTEXT")
    print("-" * 40)
    
    try:
        hist_response = requests.get('http://localhost:5000/api/historical_data')
        if hist_response.status_code == 200:
            hist_data = hist_response.json()
            values = hist_data['values']
            
            current_value = values[-1]
            previous_value = values[-2] if len(values) > 1 else current_value
            change = current_value - previous_value
            
            min_value = min(values)
            max_value = max(values)
            avg_value = sum(values) / len(values)
            
            print(f"📈 Current vs Previous: {change:+.2f} points")
            print(f"📊 Historical Range: {min_value:.1f} - {max_value:.1f}")
            print(f"📍 Historical Average: {avg_value:.1f}")
            print(f"📅 Data Points: {len(values)} historical readings")
            
            if change > 2:
                trend = "📈 INCREASING (More Greedy)"
            elif change < -2:
                trend = "📉 DECREASING (More Fearful)"
            else:
                trend = "➡️ STABLE (No significant change)"
            
            print(f"🎯 Trend: {trend}")
    except:
        print("❌ Historical data unavailable")
    
    # System performance
    print("\n🖥️ SYSTEM PERFORMANCE")
    print("-" * 40)
    
    try:
        stats_response = requests.get('http://localhost:5000/api/system_stats')
        if stats_response.status_code == 200:
            stats = stats_response.json()
            
            print(f"🔄 Data Collection Runs: {stats['collection_runs']}")
            print(f"🧠 Sentiment Analyses: {stats['sentiment_runs']}")
            print(f"📁 Total Data Files: {stats['total_data_files']:,}")
            print(f"💾 Storage Used: {stats['disk_usage_mb']:.1f} MB")
            print(f"⏱️ System Uptime: {stats['uptime_hours']} hours")
    except:
        print("❌ System stats unavailable")
    
    # Real-time demonstration
    print("\n🔄 REAL-TIME UPDATE DEMONSTRATION")
    print("-" * 40)
    print("Monitoring for changes (press Ctrl+C to stop)...")
    
    try:
        last_index = index_value
        update_count = 0
        
        while update_count < 3:  # Monitor for 3 updates
            time.sleep(30)  # Wait 30 seconds
            
            try:
                response = requests.get('http://localhost:5000/api/sentiment')
                if response.status_code == 200:
                    new_data = response.json()
                    new_index = new_data['fear_greed_index']['fear_greed_index']
                    new_timestamp = new_data['fear_greed_index']['timestamp']
                    
                    change = new_index - last_index
                    
                    print(f"⏰ {datetime.now().strftime('%H:%M:%S')} | Index: {new_index:.2f} | Change: {change:+.2f} | Updated: {new_timestamp[-8:]}")
                    
                    last_index = new_index
                    update_count += 1
            except:
                print(f"⏰ {datetime.now().strftime('%H:%M:%S')} | ❌ Update failed")
                
    except KeyboardInterrupt:
        print("\n⏹️ Monitoring stopped by user")
    
    # Summary and recommendations
    print(f"\n📋 ANALYSIS SUMMARY")
    print("-" * 40)
    print(f"🎯 Current Market Sentiment: {sentiment_label} ({index_value:.2f}/100)")
    print(f"📊 Analysis Quality: {data_points} real data points processed")
    print(f"⏰ Data Freshness: Updated {timestamp}")
    
    if index_value > 75:
        recommendation = "⚠️ Consider taking profits - market may be overheated"
    elif index_value < 25:
        recommendation = "💡 Consider buying opportunities - market may be oversold"
    else:
        recommendation = "📊 Monitor for significant changes in sentiment"
    
    print(f"💭 Suggestion: {recommendation}")
    
    print(f"\n🎉 REAL-WORLD ANALYSIS COMPLETE!")
    print("🌐 View live dashboard at: http://localhost:5000")
    print("=" * 70)

if __name__ == "__main__":
    demonstrate_real_analysis()
