# Integration Guide

## Overview

This guide provides comprehensive instructions for integrating the Fear & Greed Sentiment Engine into various platforms, applications, and trading systems. It covers everything from simple API integrations to complex real-time trading bot implementations.

## Quick Start Integration

### Basic Setup

#### 1. API Key Generation

First, obtain your API credentials:

```bash
# Register for API access
curl -X POST https://api.feargreed-sentiment.com/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "company": "Your Company",
    "use_case": "Trading bot development"
  }'
```

#### 2. Environment Setup

```bash
# Install required packages
pip install feargreed-sentiment requests pandas numpy

# Set environment variables
export FEARGREED_API_KEY="your_api_key_here"
export FEARGREED_BASE_URL="https://api.feargreed-sentiment.com/v1"
```

#### 3. Basic Integration Test

```python
import os
import requests

# Test API connection
def test_api_connection():
    headers = {
        'Authorization': f'Bearer {os.getenv("FEARGREED_API_KEY")}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(
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
