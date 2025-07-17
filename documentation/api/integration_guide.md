# Integration Guide

## 🔧 Overview

This guide provides comprehensive instructions for integrating the Fear & Greed Sentiment Engine into various platforms, applications, and trading systems. It covers everything from simple API integrations to complex real-time trading bot implementations.

## 🚀 Quick Start Integration

### Basic Setup

#### 1. Start the Application

```bash
# Clone and setup the repository
git clone https://github.com/your-repo/fear-greed-sentiment-v2.git
cd fear-greed-sentiment-v2

# Install dependencies
pip install -r requirements.txt

# Configure settings
cp config/config.json.example config/config.json

# Start the web application
python web_app.py
```

#### 2. Verify API Access

```bash
# Test API connection
curl -X GET "http://localhost:5000/api/sentiment"
```

#### 3. Basic Integration Test

```python
import requests
import json

# Test API connection
def test_api_connection():
    response = requests.get("http://localhost:5000/api/sentiment")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API Connected!")
        print(f"Fear & Greed Index: {data['fear_greed_index']['fear_greed_index']}")
        print(f"Market Sentiment: {data['fear_greed_index']['market_sentiment']}")
        return True
    else:
        print(f"❌ API Connection Failed: {response.status_code}")
        return False

# Run test
if __name__ == "__main__":
    test_api_connection()
```

---

## 📊 Integration Patterns

### **1. Real-Time Dashboard Integration**

```python
import requests
import time
import json

class SentimentDashboard:
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url
        self.last_update = None
        
    def get_real_time_data(self):
        """Get real-time sentiment and signals"""
        try:
            # Get sentiment data
            sentiment_resp = requests.get(f"{self.base_url}/sentiment")
            signals_resp = requests.get(f"{self.base_url}/signals")
            stats_resp = requests.get(f"{self.base_url}/system_stats")
            
            return {
                "sentiment": sentiment_resp.json(),
                "signals": signals_resp.json(),
                "stats": stats_resp.json(),
                "timestamp": time.time()
            }
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def update_dashboard(self):
        """Update dashboard with latest data"""
        data = self.get_real_time_data()
        if data:
            self.display_metrics(data)
            self.last_update = data['timestamp']
    
    def display_metrics(self, data):
        """Display key metrics"""
        sentiment = data['sentiment']
        signals = data['signals']
        
        print(f"\n📊 SENTIMENT DASHBOARD")
        print(f"🔥 Fear & Greed Index: {sentiment['fear_greed_index']['fear_greed_index']:.1f}")
        print(f"📈 Market Sentiment: {sentiment['fear_greed_index']['market_sentiment']}")
        print(f"📝 Total Mentions: {sentiment['fear_greed_index']['total_mentions']}")
        
        print(f"\n⚡ TRADING SIGNALS")
        for signal in signals.get('signals', []):
            print(f"• {signal['asset']}: {signal['signal']} (Confidence: {signal['confidence']:.2f})")
    
    def run_continuous(self, interval=30):
        """Run dashboard continuously"""
        print("🚀 Starting Real-Time Dashboard...")
        while True:
            self.update_dashboard()
            time.sleep(interval)

# Usage
dashboard = SentimentDashboard()
dashboard.run_continuous()
```

### **2. Trading Bot Integration**

```python
import requests
import logging
from datetime import datetime

class SentimentTradingBot:
    def __init__(self, api_base="http://localhost:5000/api"):
        self.api_base = api_base
        self.positions = {}
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def get_sentiment_signals(self):
        """Get trading signals from sentiment analysis"""
        try:
            response = requests.get(f"{self.api_base}/signals")
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get signals: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Error getting signals: {e}")
            return None
    
    def get_fear_greed_index(self):
        """Get current Fear & Greed Index"""
        try:
            response = requests.get(f"{self.api_base}/sentiment")
            if response.status_code == 200:
                data = response.json()
                return data['fear_greed_index']['fear_greed_index']
            return None
        except Exception as e:
            self.logger.error(f"Error getting Fear & Greed Index: {e}")
            return None
    
    def evaluate_signal(self, signal):
        """Evaluate if signal should be acted upon"""
        fear_greed = self.get_fear_greed_index()
        
        # Trading logic based on sentiment
        if signal['signal'] == 'BUY':
            # Buy on high confidence signals during moderate greed
            if signal['confidence'] > 0.7 and 30 < fear_greed < 70:
                return True
        elif signal['signal'] == 'SELL':
            # Sell on high confidence signals during extreme greed
            if signal['confidence'] > 0.7 and fear_greed > 70:
                return True
        
        return False
    
    def execute_trade(self, signal):
        """Execute trade based on signal"""
        # This would integrate with your actual trading platform
        self.logger.info(f"TRADE SIGNAL: {signal['signal']} {signal['asset']}")
        self.logger.info(f"Confidence: {signal['confidence']:.2f}")
        self.logger.info(f"Reasoning: {', '.join(signal['reasoning'])}")
        
        # Placeholder for actual trade execution
        if signal['signal'] == 'BUY':
            self.positions[signal['asset']] = 'LONG'
        elif signal['signal'] == 'SELL':
            self.positions[signal['asset']] = 'SHORT'
    
    def run_trading_loop(self):
        """Main trading loop"""
        self.logger.info("🤖 Starting Sentiment Trading Bot...")
        
        while True:
            try:
                # Get signals
                signals_data = self.get_sentiment_signals()
                if not signals_data:
                    time.sleep(30)
                    continue
                
                # Process each signal
                for signal in signals_data.get('signals', []):
                    if self.evaluate_signal(signal):
                        self.execute_trade(signal)
                
                # Wait before next check
                time.sleep(60)
                
            except KeyboardInterrupt:
                self.logger.info("Bot stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in trading loop: {e}")
                time.sleep(30)

# Usage
bot = SentimentTradingBot()
bot.run_trading_loop()
```

### **3. Portfolio Management Integration**

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

class SentimentPortfolioManager:
    def __init__(self, api_base="http://localhost:5000/api"):
        self.api_base = api_base
        self.portfolio = {}
        self.sentiment_history = []
    
    def get_portfolio_sentiment(self, assets):
        """Get sentiment for multiple assets"""
        portfolio_sentiment = {}
        
        # Get current sentiment
        response = requests.get(f"{self.api_base}/sentiment")
        if response.status_code == 200:
            data = response.json()
            
            for asset in assets:
                portfolio_sentiment[asset] = {
                    'fear_greed_index': data['fear_greed_index']['fear_greed_index'],
                    'market_sentiment': data['fear_greed_index']['market_sentiment'],
                    'timestamp': datetime.now()
                }
        
        return portfolio_sentiment
    
    def calculate_sentiment_weights(self, sentiment_data):
        """Calculate portfolio weights based on sentiment"""
        weights = {}
        total_weight = 0
        
        for asset, data in sentiment_data.items():
            fear_greed = data['fear_greed_index']
            
            # Weight calculation based on Fear & Greed Index
            if fear_greed < 25:  # Extreme Fear
                weight = 0.4  # Higher allocation during fear
            elif fear_greed < 45:  # Fear
                weight = 0.3
            elif fear_greed < 55:  # Neutral
                weight = 0.2
            elif fear_greed < 75:  # Greed
                weight = 0.15
            else:  # Extreme Greed
                weight = 0.1  # Lower allocation during extreme greed
            
            weights[asset] = weight
            total_weight += weight
        
        # Normalize weights
        for asset in weights:
            weights[asset] = weights[asset] / total_weight
        
        return weights
    
    def rebalance_portfolio(self, target_weights):
        """Rebalance portfolio based on sentiment"""
        print(f"\n📊 PORTFOLIO REBALANCING")
        print(f"Timestamp: {datetime.now()}")
        
        for asset, weight in target_weights.items():
            current_weight = self.portfolio.get(asset, 0)
            change = weight - current_weight
            
            print(f"• {asset}: {current_weight:.1%} → {weight:.1%} (Change: {change:+.1%})")
            
            # Update portfolio
            self.portfolio[asset] = weight
    
    def generate_report(self):
        """Generate sentiment-based portfolio report"""
        print(f"\n📈 SENTIMENT PORTFOLIO REPORT")
        print(f"Generated: {datetime.now()}")
        
        # Get current sentiment
        response = requests.get(f"{self.api_base}/sentiment")
        if response.status_code == 200:
            data = response.json()
            print(f"Fear & Greed Index: {data['fear_greed_index']['fear_greed_index']}")
            print(f"Market Sentiment: {data['fear_greed_index']['market_sentiment']}")
        
        # Portfolio allocation
        print(f"\nCurrent Portfolio Allocation:")
        for asset, weight in self.portfolio.items():
            print(f"• {asset}: {weight:.1%}")
    
    def run_portfolio_management(self, assets, rebalance_interval=3600):
        """Run continuous portfolio management"""
        print("💼 Starting Sentiment Portfolio Manager...")
        
        while True:
            try:
                # Get sentiment data
                sentiment_data = self.get_portfolio_sentiment(assets)
                
                # Calculate optimal weights
                target_weights = self.calculate_sentiment_weights(sentiment_data)
                
                # Rebalance if needed
                self.rebalance_portfolio(target_weights)
                
                # Generate report
                self.generate_report()
                
                # Wait for next rebalance
                time.sleep(rebalance_interval)
                
            except KeyboardInterrupt:
                print("Portfolio manager stopped by user")
                break
            except Exception as e:
                print(f"Error in portfolio management: {e}")
                time.sleep(60)

# Usage
assets = ['Bitcoin', 'Ethereum', 'Stock Market']
manager = SentimentPortfolioManager()
manager.run_portfolio_management(assets)
```

---

## 🔗 Web Application Integration

### **Frontend Integration (JavaScript)**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Sentiment Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div id="dashboard">
        <h1>Fear & Greed Sentiment Dashboard</h1>
        <div id="fear-greed-meter"></div>
        <div id="signals-panel"></div>
        <div id="chart-container">
            <canvas id="sentimentChart"></canvas>
        </div>
    </div>

    <script>
        class SentimentDashboard {
            constructor() {
                this.apiBase = 'http://localhost:5000/api';
                this.chart = null;
                this.initialize();
            }
            
            async initialize() {
                await this.setupChart();
                this.startAutoUpdate();
            }
            
            async fetchSentimentData() {
                try {
                    const response = await fetch(`${this.apiBase}/sentiment`);
                    return await response.json();
                } catch (error) {
                    console.error('Error fetching sentiment data:', error);
                    return null;
                }
            }
            
            async fetchSignals() {
                try {
                    const response = await fetch(`${this.apiBase}/signals`);
                    return await response.json();
                } catch (error) {
                    console.error('Error fetching signals:', error);
                    return null;
                }
            }
            
            updateFearGreedMeter(data) {
                const fearGreedIndex = data.fear_greed_index.fear_greed_index;
                const sentiment = data.fear_greed_index.market_sentiment;
                
                document.getElementById('fear-greed-meter').innerHTML = `
                    <h2>Fear & Greed Index</h2>
                    <div class="meter-value">${fearGreedIndex.toFixed(1)}</div>
                    <div class="meter-sentiment">${sentiment}</div>
                `;
            }
            
            updateSignalsPanel(signals) {
                const signalsHtml = signals.signals.map(signal => `
                    <div class="signal-item">
                        <strong>${signal.asset}</strong>: ${signal.signal}
                        <span class="confidence">(${(signal.confidence * 100).toFixed(1)}%)</span>
                    </div>
                `).join('');
                
                document.getElementById('signals-panel').innerHTML = `
                    <h3>Trading Signals</h3>
                    ${signalsHtml}
                `;
            }
            
            async setupChart() {
                const ctx = document.getElementById('sentimentChart').getContext('2d');
                this.chart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: [],
                        datasets: [{
                            label: 'Fear & Greed Index',
                            data: [],
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        }
                    }
                });
            }
            
            async updateDashboard() {
                const sentimentData = await this.fetchSentimentData();
                const signalsData = await this.fetchSignals();
                
                if (sentimentData) {
                    this.updateFearGreedMeter(sentimentData);
                    
                    // Update chart
                    const now = new Date().toLocaleTimeString();
                    this.chart.data.labels.push(now);
                    this.chart.data.datasets[0].data.push(sentimentData.fear_greed_index.fear_greed_index);
                    
                    // Keep only last 20 data points
                    if (this.chart.data.labels.length > 20) {
                        this.chart.data.labels.shift();
                        this.chart.data.datasets[0].data.shift();
                    }
                    
                    this.chart.update();
                }
                
                if (signalsData) {
                    this.updateSignalsPanel(signalsData);
                }
            }
            
            startAutoUpdate() {
                // Update immediately
                this.updateDashboard();
                
                // Update every 30 seconds
                setInterval(() => this.updateDashboard(), 30000);
            }
        }
        
        // Initialize dashboard when page loads
        document.addEventListener('DOMContentLoaded', () => {
            new SentimentDashboard();
        });
    </script>
    
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        
        #dashboard {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .meter-value {
            font-size: 48px;
            font-weight: bold;
            color: #333;
        }
        
        .meter-sentiment {
            font-size: 24px;
            color: #666;
        }
        
        .signal-item {
            padding: 10px;
            margin: 5px 0;
            background: white;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }
        
        .confidence {
            color: #666;
            font-size: 0.9em;
        }
    </style>
</body>
</html>
```

---

## 🔧 Advanced Integration Examples

### **Webhook Integration**

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/webhook/sentiment', methods=['POST'])
def sentiment_webhook():
    """Handle sentiment update webhooks"""
    data = request.json
    
    # Process sentiment update
    fear_greed = data.get('fear_greed_index', 0)
    
    # Trigger actions based on sentiment
    if fear_greed > 80:
        # Extreme greed - consider selling
        trigger_sell_alert(data)
    elif fear_greed < 20:
        # Extreme fear - consider buying
        trigger_buy_alert(data)
    
    return jsonify({'status': 'processed'})

def trigger_sell_alert(data):
    """Send sell alert"""
    # Integration with your notification system
    pass

def trigger_buy_alert(data):
    """Send buy alert"""
    # Integration with your notification system
    pass
```

### **Discord/Slack Bot Integration**

```python
import discord
import requests
from discord.ext import commands, tasks

class SentimentBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        
        self.api_base = "http://localhost:5000/api"
    
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        self.sentiment_updates.start()
    
    @commands.command(name='sentiment')
    async def get_sentiment(self, ctx):
        """Get current sentiment"""
        try:
            response = requests.get(f"{self.api_base}/sentiment")
            if response.status_code == 200:
                data = response.json()
                fear_greed = data['fear_greed_index']['fear_greed_index']
                sentiment = data['fear_greed_index']['market_sentiment']
                
                embed = discord.Embed(
                    title="📊 Market Sentiment",
                    color=0x00ff00 if fear_greed > 50 else 0xff0000
                )
                embed.add_field(
                    name="Fear & Greed Index",
                    value=f"{fear_greed:.1f}/100",
                    inline=True
                )
                embed.add_field(
                    name="Market Sentiment",
                    value=sentiment,
                    inline=True
                )
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Unable to fetch sentiment data")
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")
    
    @commands.command(name='signals')
    async def get_signals(self, ctx):
        """Get trading signals"""
        try:
            response = requests.get(f"{self.api_base}/signals")
            if response.status_code == 200:
                data = response.json()
                
                embed = discord.Embed(title="⚡ Trading Signals", color=0x0099ff)
                
                for signal in data.get('signals', []):
                    embed.add_field(
                        name=f"{signal['asset']} - {signal['signal']}",
                        value=f"Confidence: {signal['confidence']:.1%}",
                        inline=False
                    )
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Unable to fetch signals")
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")
    
    @tasks.loop(minutes=15)
    async def sentiment_updates(self):
        """Send periodic sentiment updates"""
        try:
            response = requests.get(f"{self.api_base}/sentiment")
            if response.status_code == 200:
                data = response.json()
                fear_greed = data['fear_greed_index']['fear_greed_index']
                
                # Send alert for extreme values
                if fear_greed > 80 or fear_greed < 20:
                    channel = self.get_channel(CHANNEL_ID)  # Your channel ID
                    if channel:
                        await channel.send(f"🚨 **EXTREME SENTIMENT ALERT** 🚨\n"
                                         f"Fear & Greed Index: {fear_greed:.1f}")
        except Exception as e:
            print(f"Error in sentiment updates: {e}")

# Run the bot
bot = SentimentBot()
bot.run('YOUR_BOT_TOKEN')
```

---

## 📱 Mobile App Integration

### **React Native Example**

```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, RefreshControl, ScrollView } from 'react-native';

const SentimentScreen = () => {
  const [sentimentData, setSentimentData] = useState(null);
  const [signals, setSignals] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  
  const API_BASE = 'http://localhost:5000/api';
  
  const fetchSentimentData = async () => {
    try {
      const response = await fetch(`${API_BASE}/sentiment`);
      const data = await response.json();
      setSentimentData(data);
    } catch (error) {
      console.error('Error fetching sentiment:', error);
    }
  };
  
  const fetchSignals = async () => {
    try {
      const response = await fetch(`${API_BASE}/signals`);
      const data = await response.json();
      setSignals(data.signals || []);
    } catch (error) {
      console.error('Error fetching signals:', error);
    }
  };
  
  const onRefresh = async () => {
    setRefreshing(true);
    await Promise.all([fetchSentimentData(), fetchSignals()]);
    setRefreshing(false);
  };
  
  useEffect(() => {
    fetchSentimentData();
    fetchSignals();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(() => {
      fetchSentimentData();
      fetchSignals();
    }, 30000);
    
    return () => clearInterval(interval);
  }, []);
  
  const getFearGreedColor = (index) => {
    if (index < 25) return '#ff4444';
    if (index < 50) return '#ff8800';
    if (index < 75) return '#ffff00';
    return '#44ff44';
  };
  
  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {sentimentData && (
        <View style={styles.sentimentCard}>
          <Text style={styles.title}>Fear & Greed Index</Text>
          <Text 
            style={[
              styles.indexValue,
              { color: getFearGreedColor(sentimentData.fear_greed_index.fear_greed_index) }
            ]}
          >
            {sentimentData.fear_greed_index.fear_greed_index.toFixed(1)}
          </Text>
          <Text style={styles.sentiment}>
            {sentimentData.fear_greed_index.market_sentiment}
          </Text>
        </View>
      )}
      
      <View style={styles.signalsCard}>
        <Text style={styles.title}>Trading Signals</Text>
        {signals.map((signal, index) => (
          <View key={index} style={styles.signalItem}>
            <Text style={styles.assetName}>{signal.asset}</Text>
            <Text style={[
              styles.signalType,
              { color: signal.signal === 'BUY' ? '#44ff44' : '#ff4444' }
            ]}>
              {signal.signal}
            </Text>
            <Text style={styles.confidence}>
              {(signal.confidence * 100).toFixed(1)}%
            </Text>
          </View>
        ))}
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  sentimentCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 10,
    marginBottom: 20,
    alignItems: 'center',
  },
  signalsCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 10,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  indexValue: {
    fontSize: 48,
    fontWeight: 'bold',
  },
  sentiment: {
    fontSize: 18,
    color: '#666',
    marginTop: 10,
  },
  signalItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  assetName: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  signalType: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  confidence: {
    fontSize: 14,
    color: '#666',
  },
});

export default SentimentScreen;
```

---

## 🛠️ Error Handling and Best Practices

### **Robust Error Handling**

```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging

class SentimentAPIClient:
    def __init__(self, base_url="http://localhost:5000/api", timeout=30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = self._create_session()
        self.logger = logging.getLogger(__name__)
    
    def _create_session(self):
        """Create session with retry strategy"""
        session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _make_request(self, endpoint, method='GET', data=None):
        """Make API request with error handling"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            self.logger.error(f"Request timeout for {endpoint}")
            raise Exception("API request timed out")
        
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Connection error for {endpoint}")
            raise Exception("Unable to connect to API")
        
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error for {endpoint}: {e}")
            if response.status_code == 429:
                raise Exception("Rate limit exceeded")
            else:
                raise Exception(f"API error: {e}")
        
        except Exception as e:
            self.logger.error(f"Unexpected error for {endpoint}: {e}")
            raise Exception(f"Unexpected error: {e}")
    
    def get_sentiment(self):
        """Get sentiment with error handling"""
        try:
            return self._make_request("sentiment")
        except Exception as e:
            self.logger.error(f"Error getting sentiment: {e}")
            return None
    
    def get_signals(self):
        """Get signals with error handling"""
        try:
            return self._make_request("signals")
        except Exception as e:
            self.logger.error(f"Error getting signals: {e}")
            return None

# Usage with error handling
client = SentimentAPIClient()

sentiment = client.get_sentiment()
if sentiment:
    print(f"Fear & Greed Index: {sentiment['fear_greed_index']['fear_greed_index']}")
else:
    print("Failed to get sentiment data")
```

### **Performance Optimization**

```python
import asyncio
import aiohttp
import time

class AsyncSentimentClient:
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def _make_request(self, endpoint):
        """Make async API request"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            async with self.session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            print(f"Error requesting {endpoint}: {e}")
            return None
    
    async def get_all_data(self):
        """Get all data concurrently"""
        tasks = [
            self._make_request("sentiment"),
            self._make_request("signals"),
            self._make_request("system_stats")
        ]
        
        results = await asyncio.gather(*tasks)
        
        return {
            "sentiment": results[0],
            "signals": results[1],
            "system_stats": results[2]
        }

# Usage
async def main():
    async with AsyncSentimentClient() as client:
        start_time = time.time()
        data = await client.get_all_data()
        end_time = time.time()
        
        print(f"Retrieved all data in {end_time - start_time:.2f} seconds")
        
        if data["sentiment"]:
            print(f"Fear & Greed Index: {data['sentiment']['fear_greed_index']['fear_greed_index']}")

# Run async
asyncio.run(main())
```

---

## 📚 Additional Resources

### **Related Documentation**
- **[API Reference](./api_reference.md)** - Complete API documentation
- **[Web Dashboard Guide](../../docs/EXTENDED_GUIDE.md)** - Dashboard usage
- **[System Architecture](../../docs/SYSTEM_OVERVIEW.md)** - Technical overview

### **Code Examples**
- **Integration Examples**: `/scripts/integration_examples/`
- **Test Scripts**: `/tests/integration/`
- **Sample Applications**: `/examples/`

### **Support and Community**
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: `/docs/` directory

---

**🎉 Start building amazing sentiment-powered applications today!**
        f'{os.getenv("FEARGREED_BASE_URL")}/health',
        headers=headers
    )
    
    if response.status_code == 200:
        print("✅ API connection successful!")
        return True
    else:
        print(f"❌ API connection failed: {response.status_code}")
        return False

# Test sentiment analysis
def test_sentiment_analysis():
    headers = {
        'Authorization': f'Bearer {os.getenv("FEARGREED_API_KEY")}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "text": "Apple stock is showing strong bullish momentum today",
        "entity": "AAPL",
        "options": {
            "include_confidence": True
        }
    }
    
    response = requests.post(
        f'{os.getenv("FEARGREED_BASE_URL")}/sentiment/analyze',
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Sentiment: {result['data']['sentiment']['label']}")
        print(f"   Score: {result['data']['sentiment']['score']}")
        print(f"   Confidence: {result['data']['sentiment']['confidence']}")
        return True
    else:
        print(f"❌ Sentiment analysis failed: {response.status_code}")
        return False

if __name__ == "__main__":
    test_api_connection()
    test_sentiment_analysis()
```

## Platform-Specific Integrations

### Trading Platforms

#### 1. MetaTrader 5 (MT5) Integration

```python
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import requests

class MT5SentimentIntegration:
    def __init__(self, api_key, mt5_login, mt5_password, mt5_server):
        self.api_key = api_key
        self.base_url = "https://api.feargreed-sentiment.com/v1"
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Initialize MT5
        if not mt5.initialize():
            raise Exception("MT5 initialization failed")
        
        # Login to MT5
        if not mt5.login(mt5_login, mt5_password, mt5_server):
            raise Exception("MT5 login failed")
    
    def get_sentiment_signal(self, symbol, timeframe='1h'):
        """Get sentiment-based trading signal"""
        
        # Get sentiment data
        response = requests.post(
            f'{self.base_url}/signals/generate',
            headers=self.headers,
            json={
                'entity': symbol,
                'timeframe': timeframe,
                'signal_types': ['sentiment', 'momentum'],
                'lookback_hours': 24
            }
        )
        
        if response.status_code != 200:
            return None
        
        signal_data = response.json()['data']
        return {
            'signal': signal_data['overall_signal']['recommendation'],
            'confidence': signal_data['overall_signal']['confidence'],
            'risk_level': signal_data['overall_signal']['risk_level']
        }
    
    def execute_sentiment_trade(self, symbol, signal_data, lot_size=0.1):
        """Execute trade based on sentiment signal"""
        
        if signal_data['confidence'] < 0.7:  # Only trade high-confidence signals
            print(f"Signal confidence too low: {signal_data['confidence']}")
            return None
        
        # Get current price
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            print(f"Failed to get tick for {symbol}")
            return None
        
        # Prepare trade request
        if signal_data['signal'] == 'buy':
            order_type = mt5.ORDER_TYPE_BUY
            price = tick.ask
            sl = price - 0.01  # Stop loss
            tp = price + 0.02  # Take profit
        elif signal_data['signal'] == 'sell':
            order_type = mt5.ORDER_TYPE_SELL
            price = tick.bid
            sl = price + 0.01
            tp = price - 0.02
        else:
            print(f"No actionable signal: {signal_data['signal']}")
            return None
        
        # Risk management based on sentiment confidence
        adjusted_lot_size = lot_size * signal_data['confidence']
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": adjusted_lot_size,
            "type": order_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 12345,
            "comment": f"Sentiment signal: {signal_data['confidence']:.2f}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        # Send order
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Trade failed: {result.retcode}")
            return None
        
        print(f"Trade executed: {signal_data['signal']} {adjusted_lot_size} lots of {symbol}")
        return result
    
    def run_sentiment_trading_bot(self, symbols, check_interval=300):
        """Run automated sentiment trading bot"""
        
        while True:
            for symbol in symbols:
                try:
                    # Get sentiment signal
                    signal = self.get_sentiment_signal(symbol)
                    
                    if signal and signal['confidence'] > 0.7:
                        print(f"High confidence signal for {symbol}: {signal}")
                        
                        # Check if we already have position
                        positions = mt5.positions_get(symbol=symbol)
                        
                        if len(positions) == 0:  # No existing position
                            result = self.execute_sentiment_trade(symbol, signal)
                            
                            if result:
                                print(f"Opened position for {symbol}")
                        else:
                            print(f"Position already exists for {symbol}")
                    
                except Exception as e:
                    print(f"Error processing {symbol}: {e}")
            
            # Wait before next check
            time.sleep(check_interval)

# Usage example
if __name__ == "__main__":
    bot = MT5SentimentIntegration(
        api_key="your_api_key",
        mt5_login=12345678,
        mt5_password="your_password",
        mt5_server="your_broker_server"
    )
    
    # Run bot for major currency pairs
    symbols = ["EURUSD", "GBPUSD", "USDJPY"]
    bot.run_sentiment_trading_bot(symbols)
```

#### 2. Interactive Brokers (TWS) Integration

```python
from ib_insync import *
import asyncio
from datetime import datetime
import requests

class IBSentimentTrader:
    def __init__(self, api_key, ib_host='127.0.0.1', ib_port=7497, client_id=1):
        self.api_key = api_key
        self.base_url = "https://api.feargreed-sentiment.com/v1"
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Connect to TWS/IB Gateway
        self.ib = IB()
        self.ib.connect(ib_host, ib_port, clientId=client_id)
        
        # Position tracking
        self.positions = {}
        
    def get_sentiment_data(self, symbol):
        """Get real-time sentiment data"""
        response = requests.post(
            f'{self.base_url}/sentiment/analyze',
            headers=self.headers,
            json={
                'text': f'Recent market activity for {symbol}',
                'entity': symbol,
                'options': {'include_confidence': True}
            }
        )
        
        if response.status_code == 200:
            return response.json()['data']
        return None
    
    def create_contract(self, symbol, exchange='SMART', currency='USD'):
        """Create IB contract object"""
        contract = Stock(symbol, exchange, currency)
        self.ib.qualifyContracts(contract)
        return contract
    
    def calculate_position_size(self, symbol, sentiment_confidence, account_risk=0.02):
        """Calculate position size based on sentiment confidence and risk management"""
        
        # Get account value
        account_values = self.ib.accountValues()
        net_liquidation = next(
            (float(av.value) for av in account_values 
             if av.tag == 'NetLiquidation'), 100000
        )
        
        # Risk amount based on account size
        risk_amount = net_liquidation * account_risk
        
        # Adjust position size based on sentiment confidence
        confidence_multiplier = min(sentiment_confidence * 2, 1.0)  # Max 100% of risk
        
        # Get current stock price for position sizing
        contract = self.create_contract(symbol)
        ticker = self.ib.reqMktData(contract)
        self.ib.sleep(2)  # Wait for market data
        
        if ticker.last and ticker.last > 0:
            # Assume 2% stop loss for position sizing
            stop_loss_percent = 0.02
            position_value = risk_amount / stop_loss_percent
            shares = int((position_value * confidence_multiplier) / ticker.last)
            
            self.ib.cancelMktData(contract)
            return max(shares, 1)  # Minimum 1 share
        
        return 0
    
    def place_sentiment_order(self, symbol, signal, confidence, order_type='MKT'):
        """Place order based on sentiment signal"""
        
        if confidence < 0.6:  # Minimum confidence threshold
            print(f"Confidence too low for {symbol}: {confidence}")
            return None
        
        contract = self.create_contract(symbol)
        position_size = self.calculate_position_size(symbol, confidence)
        
        if position_size == 0:
            print(f"Cannot calculate position size for {symbol}")
            return None
        
        # Determine order action
        if signal == 'buy' or signal == 'positive':
            action = 'BUY'
        elif signal == 'sell' or signal == 'negative':
            action = 'SELL'
        else:
            print(f"No actionable signal for {symbol}: {signal}")
            return None
        
        # Create order
        if order_type == 'MKT':
            order = MarketOrder(action, position_size)
        elif order_type == 'LMT':
            # Get current bid/ask for limit price
            ticker = self.ib.reqMktData(contract)
            self.ib.sleep(1)
            
            if action == 'BUY' and ticker.ask:
                limit_price = ticker.ask * 1.001  # Slightly above ask
            elif action == 'SELL' and ticker.bid:
                limit_price = ticker.bid * 0.999  # Slightly below bid
            else:
                print(f"Cannot get market data for limit order: {symbol}")
                return None
            
            order = LimitOrder(action, position_size, limit_price)
            self.ib.cancelMktData(contract)
        
        # Add stop loss and take profit
        order.transmit = False  # Don't transmit parent order yet
        
        # Calculate stop loss and take profit levels
        ticker = self.ib.reqMktData(contract)
        self.ib.sleep(1)
        current_price = ticker.last or ticker.close
        self.ib.cancelMktData(contract)
        
        if current_price:
            if action == 'BUY':
                stop_price = current_price * 0.98  # 2% stop loss
                profit_price = current_price * 1.04  # 4% take profit
            else:
                stop_price = current_price * 1.02
                profit_price = current_price * 0.96
            
            # Create bracket order
            bracket_order = self.ib.bracketOrder(
                action, position_size, 
                limitPrice=None if order_type == 'MKT' else order.lmtPrice,
                takeProfitPrice=profit_price,
                stopLossPrice=stop_price
            )
            
            # Submit bracket order
            trades = self.ib.placeOrder(contract, bracket_order[0])
            print(f"Placed sentiment-based {action} order for {position_size} shares of {symbol}")
            
            return trades
        
        return None
    
    async def run_sentiment_monitor(self, symbols, check_interval=60):
        """Monitor sentiment and place trades automatically"""
        
        while True:
            for symbol in symbols:
                try:
                    # Get current positions to avoid overtrading
                    current_positions = self.ib.positions()
                    symbol_position = next(
                        (pos for pos in current_positions 
                         if pos.contract.symbol == symbol), None
                    )
                    
                    if symbol_position and symbol_position.position != 0:
                        print(f"Already have position in {symbol}: {symbol_position.position}")
                        continue
                    
                    # Get sentiment signal
                    response = requests.post(
                        f'{self.base_url}/signals/generate',
                        headers=self.headers,
                        json={
                            'entity': symbol,
                            'timeframe': '1h',
                            'signal_types': ['sentiment'],
                            'lookback_hours': 4
                        }
                    )
                    
                    if response.status_code == 200:
                        signal_data = response.json()['data']
                        overall_signal = signal_data['overall_signal']
                        
                        if overall_signal['confidence'] > 0.7:
                            print(f"Strong signal for {symbol}: {overall_signal}")
                            
                            result = self.place_sentiment_order(
                                symbol, 
                                overall_signal['recommendation'],
                                overall_signal['confidence']
                            )
                            
                            if result:
                                print(f"Order placed for {symbol}")
                    
                except Exception as e:
                    print(f"Error processing {symbol}: {e}")
            
            # Wait before next check
            await asyncio.sleep(check_interval)

# Usage example
async def main():
    trader = IBSentimentTrader(api_key="your_api_key")
    
    # Monitor major tech stocks
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']
    await trader.run_sentiment_monitor(symbols)

if __name__ == "__main__":
    asyncio.run(main())
```

### Crypto Trading Integration

#### 1. Binance Integration

```python
from binance.client import Client
from binance.enums import *
import requests
import pandas as pd
from datetime import datetime, timedelta

class BinanceSentimentTrader:
    def __init__(self, binance_api_key, binance_secret, feargreed_api_key):
        self.binance = Client(binance_api_key, binance_secret)
        self.feargreed_api_key = feargreed_api_key
        self.base_url = "https://api.feargreed-sentiment.com/v1"
        self.headers = {
            'Authorization': f'Bearer {feargreed_api_key}',
            'Content-Type': 'application/json'
        }
        
        # Trading parameters
        self.min_confidence = 0.75
        self.position_size_pct = 0.1  # 10% of portfolio per trade
        
    def get_crypto_sentiment(self, symbol):
        """Get sentiment for cryptocurrency"""
        
        # Map Binance symbols to common crypto names
        symbol_map = {
            'BTCUSDT': 'BTC',
            'ETHUSDT': 'ETH', 
            'ADAUSDT': 'ADA',
            'DOTUSDT': 'DOT',
            'LINKUSDT': 'LINK'
        }
        
        crypto_symbol = symbol_map.get(symbol, symbol.replace('USDT', ''))
        
        response = requests.post(
            f'{self.base_url}/signals/generate',
            headers=self.headers,
            json={
                'entity': crypto_symbol,
                'timeframe': '4h',
                'signal_types': ['sentiment', 'momentum'],
                'lookback_hours': 24
            }
        )
        
        if response.status_code == 200:
            return response.json()['data']
        return None
    
    def get_portfolio_value(self):
        """Get total portfolio value in USDT"""
        account = self.binance.get_account()
        
        total_value = 0
        for balance in account['balances']:
            asset = balance['asset']
            free = float(balance['free'])
            locked = float(balance['locked'])
            total = free + locked
            
            if total > 0:
                if asset == 'USDT':
                    total_value += total
                else:
                    # Get current price in USDT
                    try:
                        ticker = self.binance.get_symbol_ticker(symbol=f"{asset}USDT")
                        price = float(ticker['price'])
                        total_value += total * price
                    except:
                        # Skip if can't get price
                        continue
        
        return total_value
    
    def calculate_quantity(self, symbol, signal_confidence):
        """Calculate trade quantity based on portfolio and confidence"""
        
        # Get available USDT balance
        account = self.binance.get_account()
        usdt_balance = float(next(
            balance['free'] for balance in account['balances'] 
            if balance['asset'] == 'USDT'
        ))
        
        # Calculate position size based on confidence
        confidence_multiplier = min(signal_confidence / 0.5, 2.0)  # Scale confidence
        position_value = usdt_balance * self.position_size_pct * confidence_multiplier
        
        # Get current price
        ticker = self.binance.get_symbol_ticker(symbol=symbol)
        price = float(ticker['price'])
        
        # Calculate quantity
        quantity = position_value / price
        
        # Round to symbol precision
        info = self.binance.get_symbol_info(symbol)
        step_size = float(next(
            f['stepSize'] for f in info['filters'] 
            if f['filterType'] == 'LOT_SIZE'
        ))
        
        precision = len(str(step_size).split('.')[-1].rstrip('0'))
        quantity = round(quantity, precision)
        
        return quantity
    
    def place_crypto_order(self, symbol, signal, confidence):
        """Place crypto order based on sentiment"""
        
        if confidence < self.min_confidence:
            print(f"Confidence too low for {symbol}: {confidence}")
            return None
        
        try:
            quantity = self.calculate_quantity(symbol, confidence)
            
            if quantity <= 0:
                print(f"Invalid quantity for {symbol}: {quantity}")
                return None
            
            # Place market order
            if signal == 'buy':
                order = self.binance.order_market_buy(
                    symbol=symbol,
                    quantity=quantity
                )
                print(f"Bought {quantity} {symbol} based on sentiment (confidence: {confidence:.2f})")
                
                # Set stop loss order
                self.set_stop_loss(symbol, quantity, 0.05)  # 5% stop loss
                
            elif signal == 'sell':
                # Get current holding
                account = self.binance.get_account()
                asset = symbol.replace('USDT', '')
                
                holding = float(next(
                    (balance['free'] for balance in account['balances'] 
                     if balance['asset'] == asset), 0
                ))
                
                if holding > 0:
                    order = self.binance.order_market_sell(
                        symbol=symbol,
                        quantity=min(quantity, holding)
                    )
                    print(f"Sold {quantity} {symbol} based on sentiment")
                else:
                    print(f"No {asset} holdings to sell")
                    return None
            
            return order
            
        except Exception as e:
            print(f"Error placing order for {symbol}: {e}")
            return None
    
    def set_stop_loss(self, symbol, quantity, stop_pct):
        """Set stop loss order"""
        try:
            # Get current price
            ticker = self.binance.get_symbol_ticker(symbol=symbol)
            current_price = float(ticker['price'])
            stop_price = current_price * (1 - stop_pct)
            
            # Place stop loss order
            stop_order = self.binance.create_order(
                symbol=symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_STOP_LOSS_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=str(stop_price * 0.99),  # Limit price slightly below stop
                stopPrice=str(stop_price)
            )
            
            print(f"Stop loss set for {symbol} at {stop_price}")
            return stop_order
            
        except Exception as e:
            print(f"Error setting stop loss for {symbol}: {e}")
            return None
    
    def run_crypto_sentiment_bot(self, symbols, check_interval=300):
        """Run automated crypto sentiment trading"""
        
        while True:
            for symbol in symbols:
                try:
                    # Get sentiment signal
                    sentiment_data = self.get_crypto_sentiment(symbol)
                    
                    if sentiment_data:
                        overall_signal = sentiment_data['overall_signal']
                        
                        if overall_signal['confidence'] > self.min_confidence:
                            print(f"Strong signal for {symbol}: {overall_signal}")
                            
                            # Check if we already have position
                            account = self.binance.get_account()
                            asset = symbol.replace('USDT', '')
                            current_holding = float(next(
                                (balance['free'] for balance in account['balances'] 
                                 if balance['asset'] == asset), 0
                            ))
                            
                            # Only trade if no existing position or signal is to sell
                            if current_holding == 0 or overall_signal['recommendation'] == 'sell':
                                result = self.place_crypto_order(
                                    symbol,
                                    overall_signal['recommendation'],
                                    overall_signal['confidence']
                                )
                                
                                if result:
                                    print(f"Order executed for {symbol}")
                    
                except Exception as e:
                    print(f"Error processing {symbol}: {e}")
            
            time.sleep(check_interval)

# Usage example
if __name__ == "__main__":
    trader = BinanceSentimentTrader(
        binance_api_key="your_binance_api_key",
        binance_secret="your_binance_secret",
        feargreed_api_key="your_feargreed_api_key"
    )
    
    # Monitor major crypto pairs
    crypto_symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT', 'LINKUSDT']
    trader.run_crypto_sentiment_bot(crypto_symbols)
```

### Web Application Integration

#### 1. Flask Web Dashboard

```python
from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.utils

app = Flask(__name__)

class SentimentDashboard:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.feargreed-sentiment.com/v1"
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def get_sentiment_data(self, entity, timeframe='24h'):
        """Get sentiment data for dashboard"""
        
        response = requests.get(
            f'{self.base_url}/data/social',
            headers=self.headers,
            params={
                'entity': entity,
                'timeframe': timeframe,
                'sources': 'twitter,reddit,news'
            }
        )
        
        if response.status_code == 200:
            return response.json()['data']
        return None
    
    def get_historical_sentiment(self, entity, days=7):
        """Get historical sentiment for charting"""
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        response = requests.get(
            f'{self.base_url}/signals/history',
            headers=self.headers,
            params={
                'entity': entity,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'limit': 1000
            }
        )
        
        if response.status_code == 200:
            return response.json()['data']
        return None
    
    def create_sentiment_chart(self, historical_data):
        """Create Plotly chart for sentiment trends"""
        
        if not historical_data or not historical_data['signals']:
            return json.dumps({})
        
        signals = historical_data['signals']
        
        # Extract data for plotting
        timestamps = [signal['timestamp'] for signal in signals]
        scores = [signal['strength'] if signal['signal'] == 'buy' 
                 else -signal['strength'] if signal['signal'] == 'sell' 
                 else 0 for signal in signals]
        
        # Create Plotly figure
        fig = go.Figure()
        
        # Add sentiment line
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=scores,
            mode='lines+markers',
            name='Sentiment Score',
            line=dict(color='blue', width=2),
            marker=dict(size=4)
        ))
        
        # Add horizontal lines for reference
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        fig.add_hline(y=0.5, line_dash="dot", line_color="green")
        fig.add_hline(y=-0.5, line_dash="dot", line_color="red")
        
        # Update layout
        fig.update_layout(
            title=f'Sentiment Trend for {historical_data["entity"]}',
            xaxis_title='Time',
            yaxis_title='Sentiment Score',
            yaxis=dict(range=[-1, 1]),
            height=400,
            template='plotly_white'
        )
        
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

dashboard = SentimentDashboard(api_key="your_api_key")

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/sentiment/<entity>')
def get_entity_sentiment(entity):
    """API endpoint for current sentiment data"""
    
    data = dashboard.get_sentiment_data(entity)
    if data:
        return jsonify({
            'status': 'success',
            'entity': entity,
            'sentiment': data['summary']['average_sentiment'],
            'total_posts': data['summary']['total_posts'],
            'distribution': data['summary']['sentiment_distribution'],
            'trending_keywords': data['summary']['trending_keywords']
        })
    else:
        return jsonify({'status': 'error', 'message': 'Failed to get sentiment data'}), 500

@app.route('/api/chart/<entity>')
def get_sentiment_chart(entity):
    """API endpoint for sentiment chart data"""
    
    days = request.args.get('days', 7, type=int)
    historical_data = dashboard.get_historical_sentiment(entity, days)
    
    if historical_data:
        chart_json = dashboard.create_sentiment_chart(historical_data)
        return jsonify({
            'status': 'success',
            'chart': chart_json
        })
    else:
        return jsonify({'status': 'error', 'message': 'Failed to get chart data'}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """API endpoint for real-time text analysis"""
    
    data = request.get_json()
    text = data.get('text', '')
    entity = data.get('entity', '')
    
    if not text:
        return jsonify({'status': 'error', 'message': 'No text provided'}), 400
    
    response = requests.post(
        f'{dashboard.base_url}/sentiment/analyze',
        headers=dashboard.headers,
        json={
            'text': text,
            'entity': entity,
            'options': {
                'include_confidence': True,
                'include_breakdown': True
            }
        }
    )
    
    if response.status_code == 200:
        result = response.json()['data']
        return jsonify({
            'status': 'success',
            'sentiment': result['sentiment'],
            'breakdown': result.get('breakdown', {}),
            'features': result.get('features', {})
        })
    else:
        return jsonify({'status': 'error', 'message': 'Analysis failed'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**HTML Template** (`templates/dashboard.html`):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fear & Greed Sentiment Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .sentiment-positive { color: #28a745; }
        .sentiment-negative { color: #dc3545; }
        .sentiment-neutral { color: #6c757d; }
        .metric-card { 
            border-radius: 10px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <h1 class="text-center my-4">Fear & Greed Sentiment Dashboard</h1>
            </div>
        </div>
        
        <!-- Entity Selection -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="input-group">
                    <input type="text" id="entityInput" class="form-control" 
                           placeholder="Enter ticker symbol (e.g., AAPL)" value="AAPL">
                    <button class="btn btn-primary" onclick="loadSentimentData()">
                        Load Data
                    </button>
                </div>
            </div>
            <div class="col-md-6">
                <select id="timeframeSelect" class="form-select" onchange="loadChart()">
                    <option value="7">Last 7 days</option>
                    <option value="14">Last 14 days</option>
                    <option value="30">Last 30 days</option>
                </select>
            </div>
        </div>
        
        <!-- Metrics Cards -->
        <div class="row" id="metricsRow">
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h5 class="card-title">Current Sentiment</h5>
                        <h2 id="currentSentiment" class="sentiment-neutral">--</h2>
                        <small id="sentimentLabel" class="text-muted">--</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h5 class="card-title">Total Posts</h5>
                        <h2 id="totalPosts">--</h2>
                        <small class="text-muted">Last 24h</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h5 class="card-title">Positive</h5>
                        <h2 id="positiveCount" class="sentiment-positive">--</h2>
                        <small class="text-muted">posts</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h5 class="card-title">Negative</h5>
                        <h2 id="negativeCount" class="sentiment-negative">--</h2>
                        <small class="text-muted">posts</small>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Sentiment Chart -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5>Sentiment Trend</h5>
                    </div>
                    <div class="card-body">
                        <div id="sentimentChart" style="height: 400px;"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Real-time Analysis -->
        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5>Real-time Text Analysis</h5>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <textarea id="analysisText" class="form-control" rows="3" 
                                    placeholder="Enter text to analyze sentiment..."></textarea>
                        </div>
                        <button class="btn btn-success" onclick="analyzeText()">
                            Analyze Sentiment
                        </button>
                        <div id="analysisResult" class="mt-3"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentEntity = 'AAPL';
        
        function loadSentimentData() {
            const entity = document.getElementById('entityInput').value.toUpperCase();
            currentEntity = entity;
            
            // Update metrics
            fetch(`/api/sentiment/${entity}`)
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        updateMetrics(data);
                    }
                })
                .catch(error => console.error('Error:', error));
            
            // Update chart
            loadChart();
        }
        
        function updateMetrics(data) {
            const sentiment = data.sentiment;
            const sentimentElement = document.getElementById('currentSentiment');
            const labelElement = document.getElementById('sentimentLabel');
            
            sentimentElement.textContent = sentiment.toFixed(3);
            
            if (sentiment > 0.1) {
                sentimentElement.className = 'sentiment-positive';
                labelElement.textContent = 'Positive';
            } else if (sentiment < -0.1) {
                sentimentElement.className = 'sentiment-negative';
                labelElement.textContent = 'Negative';
            } else {
                sentimentElement.className = 'sentiment-neutral';
                labelElement.textContent = 'Neutral';
            }
            
            document.getElementById('totalPosts').textContent = data.total_posts.toLocaleString();
            document.getElementById('positiveCount').textContent = data.distribution.positive.toLocaleString();
            document.getElementById('negativeCount').textContent = data.distribution.negative.toLocaleString();
        }
        
        function loadChart() {
            const days = document.getElementById('timeframeSelect').value;
            
            fetch(`/api/chart/${currentEntity}?days=${days}`)
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const chartData = JSON.parse(data.chart);
                        Plotly.newPlot('sentimentChart', chartData.data, chartData.layout);
                    }
                })
                .catch(error => console.error('Error:', error));
        }
        
        function analyzeText() {
            const text = document.getElementById('analysisText').value;
            if (!text.trim()) return;
            
            fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    entity: currentEntity
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    displayAnalysisResult(data);
                }
            })
            .catch(error => console.error('Error:', error));
        }
        
        function displayAnalysisResult(data) {
            const sentiment = data.sentiment;
            const resultDiv = document.getElementById('analysisResult');
            
            let sentimentClass = 'sentiment-neutral';
            if (sentiment.score > 0.1) sentimentClass = 'sentiment-positive';
            else if (sentiment.score < -0.1) sentimentClass = 'sentiment-negative';
            
            resultDiv.innerHTML = `
                <div class="alert alert-info">
                    <strong>Sentiment Analysis Result:</strong><br>
                    <span class="${sentimentClass}">
                        <strong>${sentiment.label.toUpperCase()}</strong> 
                        (Score: ${sentiment.score.toFixed(3)}, 
                         Confidence: ${sentiment.confidence.toFixed(3)})
                    </span>
                </div>
            `;
        }
        
        // Load initial data
        document.addEventListener('DOMContentLoaded', function() {
            loadSentimentData();
        });
    </script>
</body>
</html>
```

This comprehensive integration guide provides developers with practical examples for integrating the Fear & Greed Sentiment Engine across various platforms, from trading systems to web applications, enabling them to build sophisticated sentiment-driven financial applications.
