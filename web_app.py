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
            
        signal_files = [f for f in os.listdir(signals_dir) if f.endswith('.json') and f != '.gitkeep']
        if not signal_files:
            return None
            
        # Sort files by timestamp (newest first) and find one with actual signals
        signal_files = sorted(signal_files, reverse=True)
        
        for signal_file in signal_files:
            try:
                with open(f'{signals_dir}/{signal_file}', 'r') as f:
                    signals_data = json.load(f)
                
                # Check if this file has actual signals (not empty)
                if signals_data and 'signals' in signals_data and len(signals_data['signals']) > 0:
                    return signals_data
                    
            except Exception as e:
                print(f"Error loading signal file {signal_file}: {e}")
                continue
        
        # If no files with signals found, return empty structure
        return {"signals": [], "timestamp": "", "message": "No trading signals generated yet"}
    
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
        # Return empty signals structure instead of error
        return jsonify({
            "signals": [],
            "timestamp": "",
            "message": "No trading signals available - run data collection to generate signals"
        })

@app.route('/api/fear_greed_gauge')
def api_fear_greed_gauge():
    """API endpoint for Fear & Greed gauge chart"""
    
    sentiment_data = dashboard.get_latest_sentiment_data()
    if sentiment_data and 'fear_greed_index' in sentiment_data:
        # The fear_greed_index is the actual value, not nested under 'index'
        fear_greed_data = sentiment_data['fear_greed_index']
        if isinstance(fear_greed_data, dict):
            value = fear_greed_data.get('fear_greed_index', 50)
        else:
            value = fear_greed_data  # It might be a direct number
        
        print(f"🎯 Fear & Greed Index from data: {value}")
        gauge_json = dashboard.create_fear_greed_gauge(value)
        return jsonify({'chart': gauge_json})
    else:
        print("❌ No sentiment data available for gauge")
        return jsonify({'error': 'No data available'}), 404

@app.route('/api/run_collection', methods=['GET', 'POST'])
def api_run_collection():
    """API endpoint to trigger data collection"""
    
    def run_collection():
        try:
            print("🔄 Starting data collection...")
            
            # Run data collection
            result1 = subprocess.run(['python', 'main.py', '--mode', 'collect'], 
                         capture_output=True, text=True, check=True)
            print("✅ Data collection completed")
            
            # Run sentiment analysis  
            result2 = subprocess.run(['python', 'main.py', '--mode', 'analyze'], 
                         capture_output=True, text=True, check=True)
            print("✅ Sentiment analysis completed")
            
            # Generate trading signals
            result3 = subprocess.run(['python', 'main.py', '--mode', 'signal'], 
                         capture_output=True, text=True, check=True)
            print("✅ Signal generation completed")
            
            print("🎉 Full pipeline completed successfully!")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running collection: {e}")
            print(f"Command output: {e.stdout}")
            print(f"Command error: {e.stderr}")
    
    # Run in background thread
    thread = threading.Thread(target=run_collection)
    thread.start()
    
    return jsonify({'status': 'started', 'message': 'Full data pipeline started! Check console for progress.'})

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
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Historical Data - Fear & Greed Engine</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/">📊 Fear & Greed Engine</a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/">Dashboard</a>
                    <a class="nav-link active" href="/historical">Historical</a>
                    <a class="nav-link" href="/settings">Settings</a>
                </div>
            </div>
        </nav>
        <div class="container mt-4">
            <h2>Historical Sentiment Trends</h2>
            <div class="card">
                <div class="card-body">
                    <canvas id="historicalChart" height="100"></canvas>
                </div>
            </div>
            <div class="mt-4">
                <div class="row">
                    <div class="col-md-6">
                        <h5>Historical Data Files</h5>
                        <div id="dataFiles" class="list-group">
                            <div class="list-group-item">Loading historical data...</div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <h5>Analysis Summary</h5>
                        <div class="card">
                            <div class="card-body">
                                <p><strong>Total Collections:</strong> <span id="totalCollections">-</span></p>
                                <p><strong>Date Range:</strong> <span id="dateRange">-</span></p>
                                <p><strong>Avg Fear/Greed:</strong> <span id="avgFearGreed">-</span></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <script>
            // Load historical chart
            fetch('/api/historical_data')
                .then(response => response.json())
                .then(data => {
                    const ctx = document.getElementById('historicalChart').getContext('2d');
                    new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: data.dates,
                            datasets: [{
                                label: 'Fear & Greed Index',
                                data: data.values,
                                borderColor: 'rgb(75, 192, 192)',
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                tension: 0.1
                            }]
                        },
                        options: {
                            responsive: true,
                            scales: {
                                y: { beginAtZero: true, max: 100 }
                            }
                        }
                    });
                });
        </script>
    </body>
    </html>
    """

@app.route('/settings')
def settings():
    """Settings and configuration page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Settings - Fear & Greed Engine</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/">📊 Fear & Greed Engine</a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/">Dashboard</a>
                    <a class="nav-link" href="/historical">Historical</a>
                    <a class="nav-link active" href="/settings">Settings</a>
                </div>
            </div>
        </nav>
        <div class="container mt-4">
            <h2>System Settings</h2>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>Data Collection Settings</h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <label class="form-label">Collection Frequency</label>
                                <select class="form-select">
                                    <option>Every 5 minutes</option>
                                    <option>Every 15 minutes</option>
                                    <option>Every 30 minutes</option>
                                    <option>Every hour</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Data Sources</label>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" checked>
                                    <label class="form-check-label">Reddit</label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" checked>
                                    <label class="form-check-label">News APIs</label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" checked>
                                    <label class="form-check-label">Market Data</label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox">
                                    <label class="form-check-label">Twitter (Rate Limited)</label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>Signal Generation</h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <label class="form-label">Confidence Threshold</label>
                                <input type="range" class="form-range" min="0" max="100" value="30">
                                <small class="form-text text-muted">Minimum confidence for signals (30%)</small>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Asset Types</label>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" checked>
                                    <label class="form-check-label">Stocks</label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" checked>
                                    <label class="form-check-label">Cryptocurrencies</label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" checked>
                                    <label class="form-check-label">Indices</label>
                                </div>
                            </div>
                            <button class="btn btn-primary">Save Settings</button>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5>System Information</h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3">
                                    <strong>Version:</strong><br>
                                    Fear & Greed Engine v2.0
                                </div>
                                <div class="col-md-3">
                                    <strong>Uptime:</strong><br>
                                    <span id="uptime">Calculating...</span>
                                </div>
                                <div class="col-md-3">
                                    <strong>Data Storage:</strong><br>
                                    Local Files + Cache
                                </div>
                                <div class="col-md-3">
                                    <strong>Performance:</strong><br>
                                    304K texts/min processed
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/api/historical_data')
def api_historical_data():
    """API endpoint for historical sentiment trends"""
    
    # Try to get real historical data first
    try:
        dates = []
        values = []
        
        # Look for all sentiment directories
        if os.path.exists('data'):
            sentiment_dirs = [d for d in os.listdir('data') if d.startswith('sentiment_')]
            
            if sentiment_dirs:
                # Sort by timestamp and get real data
                sorted_dirs = sorted(sentiment_dirs)
                
                for sentiment_dir in sorted_dirs[-30:]:  # Last 30 collections
                    try:
                        # Extract date from directory name
                        date_part = sentiment_dir.split('_')[1]  # YYYYMMDD
                        formatted_date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}"
                        
                        # Load fear/greed index
                        with open(f'data/{sentiment_dir}/fear_greed_index.json', 'r') as f:
                            fear_greed_data = json.load(f)
                            fear_greed_value = fear_greed_data.get('fear_greed_index', 50)
                        
                        dates.append(formatted_date)
                        values.append(fear_greed_value)
                        
                    except Exception as e:
                        print(f"Error reading {sentiment_dir}: {e}")
                        continue
                
                if dates and values:
                    return jsonify({
                        'dates': dates,
                        'values': values,
                        'data_source': 'real_data',
                        'data_points': len(dates)
                    })
        
        # Fallback to sample data if no real data available
        print("No real historical data found, generating sample data")
        
    except Exception as e:
        print(f"Error loading historical data: {e}")
    
    # Generate sample data as fallback
    dates = []
    values = []
    
    for i in range(30):
        date = datetime.now() - timedelta(days=i)
        dates.append(date.strftime('%Y-%m-%d'))
        # Sample data - in real system, this comes from database
        values.append(50 + (i % 7 - 3) * 10)
    
    return jsonify({
        'dates': dates[::-1],  # Reverse to chronological order
        'values': values[::-1],
        'data_source': 'sample_data',
        'data_points': len(dates)
    })

@app.route('/api/system_stats')
def api_system_stats():
    """API endpoint for system statistics"""
    
    stats = {
        'timestamp': datetime.now().isoformat(),
        'collection_runs': 0,
        'sentiment_runs': 0,
        'signal_runs': 0,
        'uptime_hours': 24,  # Approximate uptime
        'collections_count': 0,
        'sentiment_analyses_count': 0,
        'signals_generated_count': 0,
        'total_data_files': 0,
        'disk_usage_mb': 0,
        'last_activity': None
    }
    
    try:
        if os.path.exists('data'):
            # Count different types of data
            for item in os.listdir('data'):
                if item.startswith('collection_'):
                    stats['collections_count'] += 1
                    stats['collection_runs'] += 1
                elif item.startswith('sentiment_'):
                    stats['sentiment_analyses_count'] += 1
                    stats['sentiment_runs'] += 1
            
            # Count signal files
            signals_dir = 'data/signals'
            if os.path.exists(signals_dir):
                signal_files = [f for f in os.listdir(signals_dir) if f.endswith('.json')]
                stats['signals_generated_count'] = len(signal_files)
                stats['signal_runs'] = len(signal_files)
            
            # Calculate total files
            for root, dirs, files in os.walk('data'):
                stats['total_data_files'] += len(files)
            
            # Calculate disk usage (rough estimate)
            total_size = 0
            for root, dirs, files in os.walk('data'):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        total_size += os.path.getsize(file_path)
                    except:
                        pass
            stats['disk_usage_mb'] = round(total_size / (1024 * 1024), 2)
            
            # Get last activity
            all_dirs = [d for d in os.listdir('data') if d.startswith(('collection_', 'sentiment_'))]
            if all_dirs:
                latest_dir = sorted(all_dirs)[-1]
                stats['last_activity'] = latest_dir
                
    except Exception as e:
        print(f"Error calculating system stats: {e}")
    
    return jsonify(stats)

if __name__ == '__main__':
    print("🚀 Starting Fear & Greed Sentiment Engine Web Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("💡 Real-time sentiment analysis and trading signals")
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
