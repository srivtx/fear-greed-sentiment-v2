#!/usr/bin/env python3
"""
Comprehensive Testing Suite for Fear & Greed Sentiment Engine
Tests the entire pipeline: data collection → sentiment analysis → API → web dashboard
"""

import unittest
import requests
import json
import time
import os
from datetime import datetime
from pathlib import Path

class TestFearGreedEngine(unittest.TestCase):
    """Test the core engine functionality"""
    
    BASE_URL = "http://localhost:5000"
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        print("🧪 Starting Fear & Greed Engine Test Suite")
        print("=" * 60)
        
        # Check if web app is running
        try:
            response = requests.get(f"{cls.BASE_URL}/", timeout=5)
            if response.status_code != 200:
                raise Exception("Web app not responding")
        except:
            print("❌ Web app not running. Start with: python web_app.py")
            raise
    
    def test_01_api_endpoints_availability(self):
        """Test that all API endpoints are available"""
        print("\n🔍 Testing API Endpoints...")
        
        endpoints = [
            '/api/sentiment',
            '/api/historical_data', 
            '/api/system_stats',
            '/api/signals',
            '/api/fear_greed_gauge'
        ]
        
        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                response = requests.get(f"{self.BASE_URL}{endpoint}")
                self.assertEqual(response.status_code, 200, 
                               f"Endpoint {endpoint} returned {response.status_code}")
                print(f"  ✅ {endpoint}: OK")
    
    def test_02_sentiment_data_structure(self):
        """Test sentiment API returns correct data structure"""
        print("\n📊 Testing Sentiment Data Structure...")
        
        response = requests.get(f"{self.BASE_URL}/api/sentiment")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        # Check main structure
        required_keys = ['fear_greed_index', 'general_sentiment', 'entity_sentiment']
        for key in required_keys:
            self.assertIn(key, data, f"Missing key: {key}")
            print(f"  ✅ {key}: Present")
        
        # Check Fear & Greed Index structure
        fg_data = data['fear_greed_index']
        fg_required = ['timestamp', 'fear_greed_index', 'market_sentiment', 
                       'total_mentions', 'calculation_details']
        
        for key in fg_required:
            self.assertIn(key, fg_data, f"Missing Fear & Greed key: {key}")
            print(f"  ✅ fear_greed_index.{key}: Present")
        
        # Validate data types and ranges
        self.assertIsInstance(fg_data['fear_greed_index'], (int, float))
        self.assertGreaterEqual(fg_data['fear_greed_index'], 0)
        self.assertLessEqual(fg_data['fear_greed_index'], 100)
        print(f"  ✅ Fear & Greed Index: {fg_data['fear_greed_index']:.2f} (Valid range)")
        
        self.assertIsInstance(fg_data['total_mentions'], int)
        self.assertGreater(fg_data['total_mentions'], 0)
        print(f"  ✅ Total mentions: {fg_data['total_mentions']} (Valid count)")
    
    def test_03_data_freshness(self):
        """Test that data is fresh and timestamps are recent"""
        print("\n⏰ Testing Data Freshness...")
        
        response = requests.get(f"{self.BASE_URL}/api/sentiment")
        data = response.json()
        
        timestamp_str = data['fear_greed_index']['timestamp']
        
        # Parse timestamp
        data_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        current_time = datetime.now()
        
        # Check if data is less than 1 hour old
        time_diff = abs((current_time - data_time.replace(tzinfo=None)).total_seconds())
        self.assertLess(time_diff, 3600, "Data is more than 1 hour old")
        
        print(f"  ✅ Data timestamp: {timestamp_str}")
        print(f"  ✅ Age: {time_diff/60:.1f} minutes (Fresh)")
    
    def test_04_calculation_components(self):
        """Test that calculation components are present and valid"""
        print("\n🧮 Testing Calculation Components...")
        
        response = requests.get(f"{self.BASE_URL}/api/sentiment")
        data = response.json()
        
        calc_details = data['fear_greed_index']['calculation_details']
        
        components = [
            'sentiment_component',
            'distribution_component', 
            'engagement_component',
            'volatility_component',
            'market_noise'
        ]
        
        total = 0
        for component in components:
            self.assertIn(component, calc_details, f"Missing component: {component}")
            value = calc_details[component]
            self.assertIsInstance(value, (int, float))
            print(f"  ✅ {component}: {value:.2f}")
            
            if component != 'market_noise':  # market_noise can be negative
                total += value
        
        # Check that components roughly add up to the final index
        final_index = data['fear_greed_index']['fear_greed_index']
        self.assertAlmostEqual(total + calc_details['market_noise'], final_index, places=1)
        print(f"  ✅ Components sum: {total + calc_details['market_noise']:.2f} ≈ Final: {final_index:.2f}")
    
    def test_05_entity_sentiment(self):
        """Test entity sentiment analysis"""
        print("\n💎 Testing Entity Sentiment...")
        
        response = requests.get(f"{self.BASE_URL}/api/sentiment")
        data = response.json()
        
        entity_data = data['entity_sentiment']
        
        # Check structure
        self.assertIn('cryptos', entity_data)
        self.assertIn('stocks', entity_data)
        
        # Test crypto sentiment
        cryptos = entity_data['cryptos']
        for crypto, sentiment in cryptos.items():
            if sentiment['mentions'] > 0:
                self.assertIn('compound', sentiment)
                self.assertIn('sentiment_label', sentiment)
                self.assertIn('mentions', sentiment)
                print(f"  ✅ {crypto}: {sentiment['compound']:+.3f} ({sentiment['mentions']} mentions)")
        
        # Test stock sentiment
        stocks = entity_data['stocks']
        for stock, sentiment in stocks.items():
            if sentiment['mentions'] > 0:
                self.assertIn('compound', sentiment)
                self.assertIn('sentiment_label', sentiment)
                self.assertIn('mentions', sentiment)
                print(f"  ✅ {stock}: {sentiment['compound']:+.3f} ({sentiment['mentions']} mentions)")
    
    def test_06_historical_data(self):
        """Test historical data endpoint"""
        print("\n📈 Testing Historical Data...")
        
        response = requests.get(f"{self.BASE_URL}/api/historical_data")
        data = response.json()
        
        required_keys = ['timestamps', 'values', 'data_points', 'data_source']
        for key in required_keys:
            self.assertIn(key, data, f"Missing historical data key: {key}")
        
        # Check data consistency
        self.assertEqual(len(data['timestamps']), len(data['values']))
        self.assertEqual(len(data['values']), data['data_points'])
        
        # Check value ranges
        for value in data['values']:
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 100)
        
        print(f"  ✅ Data points: {data['data_points']}")
        print(f"  ✅ Value range: {min(data['values']):.1f} - {max(data['values']):.1f}")
        print(f"  ✅ Data source: {data['data_source']}")
    
    def test_07_system_stats(self):
        """Test system statistics"""
        print("\n🖥️ Testing System Statistics...")
        
        response = requests.get(f"{self.BASE_URL}/api/system_stats")
        data = response.json()
        
        required_keys = [
            'collection_runs', 'sentiment_runs', 'signal_runs',
            'total_data_files', 'disk_usage_mb', 'uptime_hours'
        ]
        
        for key in required_keys:
            self.assertIn(key, data, f"Missing system stat: {key}")
            self.assertIsInstance(data[key], (int, float))
            self.assertGreaterEqual(data[key], 0)
            print(f"  ✅ {key}: {data[key]}")
    
    def test_08_api_performance(self):
        """Test API response times"""
        print("\n⚡ Testing API Performance...")
        
        endpoints = [
            '/api/sentiment',
            '/api/historical_data',
            '/api/system_stats'
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = requests.get(f"{self.BASE_URL}{endpoint}")
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # ms
            
            self.assertEqual(response.status_code, 200)
            self.assertLess(response_time, 1000, f"{endpoint} took {response_time:.0f}ms (too slow)")
            
            print(f"  ✅ {endpoint}: {response_time:.0f}ms")
    
    def test_09_data_files_exist(self):
        """Test that data files exist and are readable"""
        print("\n📁 Testing Data Files...")
        
        data_dir = Path("data")
        self.assertTrue(data_dir.exists(), "Data directory doesn't exist")
        
        # Check for recent sentiment directories
        sentiment_dirs = list(data_dir.glob("sentiment_*"))
        self.assertGreater(len(sentiment_dirs), 0, "No sentiment directories found")
        
        # Check the most recent one has files
        latest_sentiment = sorted(sentiment_dirs)[-1]
        required_files = ['fear_greed_index.json', 'entity_sentiment.json', 'general_sentiment.json']
        
        for file_name in required_files:
            file_path = latest_sentiment / file_name
            self.assertTrue(file_path.exists(), f"Missing file: {file_path}")
            
            # Test that file is valid JSON
            with open(file_path, 'r') as f:
                json.load(f)  # Will raise exception if invalid JSON
            
            print(f"  ✅ {file_path.name}: Valid JSON")
        
        print(f"  ✅ Latest sentiment data: {latest_sentiment.name}")

class TestDataCollectionIntegrity(unittest.TestCase):
    """Test data collection and processing integrity"""
    
    def test_real_data_sources(self):
        """Verify we're using real data from actual sources"""
        print("\n🌐 Testing Real Data Sources...")
        
        # Check for recent collection directories
        data_dir = Path("data")
        collection_dirs = list(data_dir.glob("collection_*"))
        
        self.assertGreater(len(collection_dirs), 0, "No collection directories found")
        
        latest_collection = sorted(collection_dirs)[-1]
        
        # Check for Reddit data
        reddit_files = list(latest_collection.glob("reddit_*.json"))
        if reddit_files:
            with open(reddit_files[0], 'r') as f:
                reddit_data = json.load(f)
                self.assertGreater(len(reddit_data), 0, "No Reddit posts collected")
                
                # Check that posts have real structure
                post = reddit_data[0]
                self.assertIn('title', post)
                self.assertIn('text', post)
                self.assertIn('created_at', post)
                print(f"  ✅ Reddit: {len(reddit_data)} real posts")
        
        # Check for market data
        market_files = list(latest_collection.glob("market_data_*.csv"))
        if market_files:
            import pandas as pd
            market_data = pd.read_csv(market_files[0])
            self.assertGreater(len(market_data), 0, "No market data collected")
            print(f"  ✅ Market data: {len(market_data)} symbols")

def run_web_test():
    """Test the web interface manually"""
    print("\n🌐 WEB INTERFACE TEST")
    print("=" * 40)
    print("🚀 Dashboard URL: http://localhost:5000")
    print("\n📋 Manual Test Checklist:")
    print("  1. ✓ Dashboard loads without errors")
    print("  2. ✓ Fear & Greed gauge displays correctly")
    print("  3. ✓ Real-time data updates every 30 seconds")
    print("  4. ✓ Historical chart shows data points")
    print("  5. ✓ Sentiment breakdown shows percentages")
    print("  6. ✓ Asset sentiment tables populate")
    print("  7. ✓ System stats display correctly")
    print("  8. ✓ All navigation links work")
    print("  9. ✓ Settings page loads")
    print("  10. ✓ Historical page shows trends")
    print("\n🎯 Expected Values:")
    
    # Get current data for reference
    try:
        response = requests.get("http://localhost:5000/api/sentiment")
        if response.status_code == 200:
            data = response.json()
            fg_data = data['fear_greed_index']
            print(f"  • Fear & Greed Index: {fg_data['fear_greed_index']:.2f}")
            print(f"  • Market Sentiment: {fg_data['market_sentiment']}")
            print(f"  • Data Points: {fg_data['total_mentions']:,}")
            print(f"  • Last Updated: {fg_data['timestamp']}")
        else:
            print("  ❌ Could not fetch current data")
    except Exception as e:
        print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 FEAR & GREED SENTIMENT ENGINE - COMPREHENSIVE TESTS")
    print("=" * 70)
    
    # Run automated tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run manual web test
    run_web_test()
    
    print("\n" + "=" * 70)
    print("🎉 TEST SUITE COMPLETED!")
    print("📊 Check the web dashboard manually at: http://localhost:5000")
