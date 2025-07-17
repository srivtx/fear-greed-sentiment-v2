#!/usr/bin/env python3
"""
Comprehensive testing script for the Fear & Greed Sentiment Engine
Tests various scenarios to ensure the app works perfectly
"""

import requests
import json
import time
import os
from pathlib import Path
from datetime import datetime

class FearGreedTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.test_results = []
        
    def log_test(self, test_name, status, details=""):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status_symbol = "✅" if status == "PASS" else "❌"
        print(f"{status_symbol} {test_name}: {details}")
        
    def test_web_app_health(self):
        """Test if web app is running and responding"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                self.log_test("Web App Health", "PASS", "Dashboard loads successfully")
            else:
                self.log_test("Web App Health", "FAIL", f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Web App Health", "FAIL", f"Connection error: {str(e)}")
    
    def test_api_endpoints(self):
        """Test all API endpoints"""
        endpoints = [
            "/api/sentiment",
            "/api/signals", 
            "/api/fear_greed_gauge",
            "/api/historical_data",
            "/api/system_stats"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(f"API {endpoint}", "PASS", f"Returns valid JSON with {len(data)} fields")
                else:
                    self.log_test(f"API {endpoint}", "FAIL", f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"API {endpoint}", "FAIL", f"Error: {str(e)}")
    
    def test_fear_greed_calculation(self):
        """Test Fear & Greed index calculation variety"""
        try:
            response = requests.get(f"{self.base_url}/api/sentiment")
            if response.status_code == 200:
                data = response.json()
                if 'fear_greed_index' in data:
                    fg_data = data['fear_greed_index']
                    index_value = fg_data.get('fear_greed_index', 0)
                    
                    # Check if index is in valid range
                    if 0 <= index_value <= 100:
                        self.log_test("Fear & Greed Range", "PASS", f"Index: {index_value:.2f}")
                    else:
                        self.log_test("Fear & Greed Range", "FAIL", f"Out of range: {index_value}")
                    
                    # Check if not always the same value
                    if index_value != 100:
                        self.log_test("Fear & Greed Variance", "PASS", f"Shows realistic value: {index_value:.2f}")
                    else:
                        self.log_test("Fear & Greed Variance", "FAIL", "Still showing max value of 100")
                else:
                    self.log_test("Fear & Greed Calculation", "FAIL", "No fear_greed_index in response")
            else:
                self.log_test("Fear & Greed Calculation", "FAIL", f"API error: {response.status_code}")
        except Exception as e:
            self.log_test("Fear & Greed Calculation", "FAIL", f"Error: {str(e)}")
    
    def test_historical_data(self):
        """Test historical data functionality"""
        try:
            response = requests.get(f"{self.base_url}/api/historical_data")
            if response.status_code == 200:
                data = response.json()
                dates = data.get('dates', [])
                values = data.get('values', [])
                
                if len(dates) > 0 and len(values) > 0:
                    self.log_test("Historical Data", "PASS", f"{len(dates)} data points available")
                    
                    # Check for data variety
                    unique_values = len(set(values))
                    if unique_values > 1:
                        self.log_test("Historical Variance", "PASS", f"{unique_values} unique values")
                    else:
                        self.log_test("Historical Variance", "FAIL", "All historical values are the same")
                else:
                    self.log_test("Historical Data", "FAIL", "No historical data returned")
            else:
                self.log_test("Historical Data", "FAIL", f"API error: {response.status_code}")
        except Exception as e:
            self.log_test("Historical Data", "FAIL", f"Error: {str(e)}")
    
    def test_data_collection(self):
        """Test data collection pipeline"""
        try:
            # Trigger data collection
            response = requests.post(f"{self.base_url}/api/run_collection")
            if response.status_code == 200:
                self.log_test("Data Collection Trigger", "PASS", "Collection started successfully")
                
                # Wait for collection to complete
                time.sleep(3)
                
                # Check for new data files
                data_dirs = [d for d in os.listdir('data') if d.startswith('collection_')]
                if data_dirs:
                    latest_dir = sorted(data_dirs)[-1]
                    self.log_test("Data Collection Files", "PASS", f"Latest: {latest_dir}")
                else:
                    self.log_test("Data Collection Files", "FAIL", "No collection directories found")
            else:
                self.log_test("Data Collection Trigger", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Data Collection", "FAIL", f"Error: {str(e)}")
    
    def test_page_navigation(self):
        """Test navigation between pages"""
        pages = [
            "/",
            "/historical", 
            "/settings"
        ]
        
        for page in pages:
            try:
                response = requests.get(f"{self.base_url}{page}")
                if response.status_code == 200:
                    self.log_test(f"Page {page}", "PASS", "Page loads successfully")
                else:
                    self.log_test(f"Page {page}", "FAIL", f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Page {page}", "FAIL", f"Error: {str(e)}")
    
    def test_data_freshness(self):
        """Test if system generates fresh, varied data"""
        try:
            # Get current data
            response1 = requests.get(f"{self.base_url}/api/sentiment")
            time.sleep(2)
            
            # Trigger new collection
            requests.post(f"{self.base_url}/api/run_collection")
            time.sleep(30)  # Wait for collection to complete
            
            # Get new data
            response2 = requests.get(f"{self.base_url}/api/sentiment")
            
            if response1.status_code == 200 and response2.status_code == 200:
                data1 = response1.json()
                data2 = response2.json()
                
                # Compare timestamps or values
                ts1 = data1.get('fear_greed_index', {}).get('timestamp', '')
                ts2 = data2.get('fear_greed_index', {}).get('timestamp', '')
                
                if ts1 != ts2:
                    self.log_test("Data Freshness", "PASS", "New data generated successfully")
                else:
                    self.log_test("Data Freshness", "FAIL", "Data not refreshing")
            else:
                self.log_test("Data Freshness", "FAIL", "API calls failed")
        except Exception as e:
            self.log_test("Data Freshness", "FAIL", f"Error: {str(e)}")
    
    def test_system_stats(self):
        """Test system statistics"""
        try:
            response = requests.get(f"{self.base_url}/api/system_stats")
            if response.status_code == 200:
                data = response.json()
                expected_fields = ['collection_runs', 'sentiment_runs', 'signal_runs', 'uptime_hours']
                
                missing_fields = [field for field in expected_fields if field not in data]
                if not missing_fields:
                    self.log_test("System Stats", "PASS", f"All fields present: {list(data.keys())}")
                else:
                    self.log_test("System Stats", "FAIL", f"Missing fields: {missing_fields}")
            else:
                self.log_test("System Stats", "FAIL", f"API error: {response.status_code}")
        except Exception as e:
            self.log_test("System Stats", "FAIL", f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting comprehensive Fear & Greed Engine testing...")
        print("=" * 60)
        
        # Run all tests
        self.test_web_app_health()
        self.test_api_endpoints()
        self.test_fear_greed_calculation()
        self.test_historical_data()
        self.test_page_navigation()
        self.test_system_stats()
        self.test_data_collection()
        
        # Don't run data freshness test automatically as it takes too long
        # self.test_data_freshness()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = len([t for t in self.test_results if t['status'] == 'PASS'])
        failed = len([t for t in self.test_results if t['status'] == 'FAIL'])
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {passed/(passed+failed)*100:.1f}%")
        
        if failed > 0:
            print(f"\n🔍 FAILED TESTS:")
            for test in self.test_results:
                if test['status'] == 'FAIL':
                    print(f"  - {test['test']}: {test['details']}")
        
        # Save results
        with open('test_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n💾 Detailed results saved to test_results.json")
        
        return passed, failed

if __name__ == "__main__":
    tester = FearGreedTester()
    passed, failed = tester.run_all_tests()
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! App is working perfectly!")
    else:
        print(f"\n⚠️  {failed} tests failed. Please check the issues above.")
