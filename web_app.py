#!/usr/bin/env python3
"""
Fear & Greed Sentiment Engine - Web Interface
A Flask-based web dashboard for real-time sentiment analysis and trading signals
"""

from flask import Flask, render_template, jsonify, request, send_file
import json
import os
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
from pathlib import Path
import subprocess
import threading
import time

# Import our existing modules
from engine import FearGreedEngine
from data_collection.collector import DataCollector
from sentiment_analysis.analyzer import SentimentAnalysisEngine

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

class WebDashboard:
    """Web dashboard for the Fear & Greed Sentiment Engine"""
    
    def __init__(self):
        self.engine = FearGreedEngine()
        self.latest_data = {}
        self.is_running = False
        
    def get_latest_sentiment_data(self):
        """Get the most recent sentiment analysis results"""
        
        # Find the most recent sentiment directory
        sentiment_dirs = []
        if os.path.exists('data'):
            for item in os.listdir('data'):
                if item.startswith('sentiment_'):
                    sentiment_dirs.append(item)
        
        if not sentiment_dirs:
            return None
            
        latest_dir = sorted(sentiment_dirs)[-1]
        sentiment_path = f'data/{latest_dir}'
        
        # Load sentiment data
        try:
            # Load fear/greed index
            with open(f'{sentiment_path}/fear_greed_index.json', 'r') as f:
                fear_greed_data = json.load(f)
            
            # Load general sentiment
            with open(f'{sentiment_path}/general_sentiment.json', 'r') as f:
                general_sentiment = json.load(f)
            
            # Load entity sentiment
            with open(f'{sentiment_path}/entity_sentiment.json', 'r') as f:
                entity_sentiment = json.load(f)
                
            return {
                'fear_greed_index': fear_greed_data,
                'general_sentiment': general_sentiment,
                'entity_sentiment': entity_sentiment,
                'timestamp': latest_dir.split('_')[1] + '_' + latest_dir.split('_')[2]
            }
            
        except Exception as e:
            print(f"Error loading sentiment data: {e}")
            return None
    
    def get_latest_signals(self):
        """Get the most recent trading signals"""
        
        signals_dir = 'data/signals'
        if not os.path.exists(signals_dir):
            return None
            
        signal_files = [f for f in os.listdir(signals_dir) if f.endswith('.json')]
        if not signal_files:
            return None
            
        latest_file = sorted(signal_files)[-1]
        
        try:
            with open(f'{signals_dir}/{latest_file}', 'r') as f:
                signals_data = json.load(f)
            return signals_data
        except Exception as e:
            print(f"Error loading signals: {e}")
            return None
    
    def create_fear_greed_gauge(self, value):
        """Create a Plotly gauge chart for Fear & Greed Index"""
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Fear & Greed Index"},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 25], 'color': "red"},
                    {'range': [25, 45], 'color': "orange"},
                    {'range': [45, 55], 'color': "yellow"},
                    {'range': [55, 75], 'color': "lightgreen"},
                    {'range': [75, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            font={'color': "darkblue", 'family': "Arial"},
            height=400
        )
        
        return plotly.utils.PlotlyJSONEncoder().encode(fig)

dashboard = WebDashboard()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/sentiment')
def api_sentiment():
    """API endpoint for current sentiment data"""
    
    sentiment_data = dashboard.get_latest_sentiment_data()
    if sentiment_data:
        return jsonify(sentiment_data)
    else:
        return jsonify({'error': 'No sentiment data available'}), 404

@app.route('/api/signals')
def api_signals():
    """API endpoint for current trading signals"""
    
    signals_data = dashboard.get_latest_signals()
    if signals_data:
        return jsonify(signals_data)
    else:
        return jsonify({'error': 'No signals data available'}), 404

@app.route('/api/fear_greed_gauge')
def api_fear_greed_gauge():
    """API endpoint for Fear & Greed gauge chart"""
    
    sentiment_data = dashboard.get_latest_sentiment_data()
    if sentiment_data and 'fear_greed_index' in sentiment_data:
        value = sentiment_data['fear_greed_index'].get('index', 50)
        gauge_json = dashboard.create_fear_greed_gauge(value)
        return jsonify({'chart': gauge_json})
    else:
        return jsonify({'error': 'No data available'}), 404

@app.route('/api/run_collection')
def api_run_collection():
    """API endpoint to trigger data collection"""
    
    def run_collection():
        try:
            subprocess.run(['python', 'main.py', '--mode', 'collect'], 
                         capture_output=True, text=True, check=True)
            subprocess.run(['python', 'main.py', '--mode', 'analyze'], 
                         capture_output=True, text=True, check=True)
            subprocess.run(['python', 'main.py', '--mode', 'signal'], 
                         capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running collection: {e}")
    
    # Run in background thread
    thread = threading.Thread(target=run_collection)
    thread.start()
    
    return jsonify({'status': 'started', 'message': 'Data collection started in background'})

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    
    status = {
        'timestamp': datetime.now().isoformat(),
        'system_running': True,
        'last_collection': None,
        'last_analysis': None,
        'data_sources': {
            'reddit': True,
            'news': True,
            'market_data': True,
            'twitter': False  # Rate limited in demo
        }
    }
    
    # Check for recent data
    if os.path.exists('data'):
        collections = [d for d in os.listdir('data') if d.startswith('collection_')]
        if collections:
            status['last_collection'] = sorted(collections)[-1]
        
        sentiments = [d for d in os.listdir('data') if d.startswith('sentiment_')]
        if sentiments:
            status['last_analysis'] = sorted(sentiments)[-1]
    
    return jsonify(status)

@app.route('/historical')
def historical():
    """Historical data and trends page"""
    return render_template('historical.html')

@app.route('/settings')
def settings():
    """Settings and configuration page"""
    return render_template('settings.html')

@app.route('/api/historical_data')
def api_historical_data():
    """API endpoint for historical sentiment trends"""
    
    # This would normally query a database
    # For demo, we'll create sample data
    dates = []
    values = []
    
    for i in range(30):
        date = datetime.now() - timedelta(days=i)
        dates.append(date.strftime('%Y-%m-%d'))
        # Sample data - in real system, this comes from database
        values.append(50 + (i % 7 - 3) * 10)
    
    return jsonify({
        'dates': dates[::-1],  # Reverse to chronological order
        'values': values[::-1]
    })

if __name__ == '__main__':
    print("🚀 Starting Fear & Greed Sentiment Engine Web Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("💡 Real-time sentiment analysis and trading signals")
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
