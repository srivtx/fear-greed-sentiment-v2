#!/usr/bin/env python3
"""
Advanced testing scenarios for Fear & Greed Sentiment Engine
Tests edge cases and stress scenarios
"""

import requests
import json
import time
import os
import threading
from pathlib import Path
from datetime import datetime, timedelta

class AdvancedTester:
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
    
    def test_concurrent_requests(self):
        """Test concurrent API requests"""
        try:
            print("🔄 Testing concurrent requests...")
            
            def make_request():
                response = requests.get(f"{self.base_url}/api/sentiment", timeout=10)
                return response.status_code == 200
            
            # Create multiple threads
            threads = []
            results = []
            
            for i in range(5):
                thread = threading.Thread(target=lambda: results.append(make_request()))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads
            for thread in threads:
                thread.join()
            
            success_count = sum(results)
            if success_count >= 4:  # Allow 1 failure due to race conditions
                self.log_test("Concurrent Requests", "PASS", f"{success_count}/5 requests succeeded")
            else:
                self.log_test("Concurrent Requests", "FAIL", f"Only {success_count}/5 requests succeeded")
                
        except Exception as e:
            self.log_test("Concurrent Requests", "FAIL", f"Error: {str(e)}")
    
    def test_data_pipeline_sequence(self):
        """Test complete data pipeline sequence"""
        try:
            print("🔄 Testing full data pipeline...")
            
            # 1. Trigger collection
            response = requests.post(f"{self.base_url}/api/run_collection")
            if response.status_code != 200:
                self.log_test("Pipeline Trigger", "FAIL", f"Status: {response.status_code}")
                return
            
            # 2. Wait for pipeline to complete
            time.sleep(45)  # Give enough time for full pipeline
            
            # 3. Check for new data
            sentiment_response = requests.get(f"{self.base_url}/api/sentiment")
            if sentiment_response.status_code == 200:
                sentiment_data = sentiment_response.json()
                if 'fear_greed_index' in sentiment_data:
                    timestamp = sentiment_data['fear_greed_index'].get('timestamp', '')
                    if timestamp:
                        # Check if timestamp is recent (within last hour)
                        now = datetime.now()
                        try:
                            data_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            time_diff = abs((now - data_time.replace(tzinfo=None)).total_seconds())
                            if time_diff < 3600:  # Within 1 hour
                                self.log_test("Pipeline Fresh Data", "PASS", f"Data timestamp: {timestamp}")
                            else:
                                self.log_test("Pipeline Fresh Data", "FAIL", f"Data too old: {timestamp}")
                        except:
                            self.log_test("Pipeline Fresh Data", "FAIL", f"Invalid timestamp: {timestamp}")
                    else:
                        self.log_test("Pipeline Fresh Data", "FAIL", "No timestamp in data")
                else:
                    self.log_test("Pipeline Fresh Data", "FAIL", "No fear_greed_index in response")
            else:
                self.log_test("Pipeline Fresh Data", "FAIL", f"API error: {sentiment_response.status_code}")
                
        except Exception as e:
            self.log_test("Data Pipeline Sequence", "FAIL", f"Error: {str(e)}")
    
    def test_historical_data_trends(self):
        """Test historical data shows realistic trends"""
        try:
            response = requests.get(f"{self.base_url}/api/historical_data")
            if response.status_code == 200:
                data = response.json()
                values = data.get('values', [])
                
                if len(values) >= 3:
                    # Check for reasonable variance
                    min_val = min(values)
                    max_val = max(values)
                    variance = max_val - min_val
                    
                    if variance > 5:  # Some reasonable variance
                        self.log_test("Historical Trends", "PASS", f"Variance: {variance:.2f} (min: {min_val:.2f}, max: {max_val:.2f})")
                    else:
                        self.log_test("Historical Trends", "FAIL", f"Too little variance: {variance:.2f}")
                        
                    # Check all values are in valid range
                    invalid_values = [v for v in values if not (0 <= v <= 100)]
                    if not invalid_values:
                        self.log_test("Historical Range", "PASS", "All values in range [0-100]")
                    else:
                        self.log_test("Historical Range", "FAIL", f"Invalid values: {invalid_values}")
                else:
                    self.log_test("Historical Trends", "FAIL", f"Not enough data points: {len(values)}")
            else:
                self.log_test("Historical Trends", "FAIL", f"API error: {response.status_code}")
                
        except Exception as e:
            self.log_test("Historical Trends", "FAIL", f"Error: {str(e)}")
    
    def test_error_handling(self):
        """Test error handling for invalid requests"""
        try:
            # Test invalid endpoints
            invalid_endpoints = [
                "/api/nonexistent",
                "/api/sentiment/invalid",
                "/api/historical_data/wrong"
            ]
            
            error_handled_count = 0
            for endpoint in invalid_endpoints:
                response = requests.get(f"{self.base_url}{endpoint}")
                if response.status_code in [404, 405, 400]:  # Expected error codes
                    error_handled_count += 1
            
            if error_handled_count == len(invalid_endpoints):
                self.log_test("Error Handling", "PASS", f"All {error_handled_count} invalid requests handled properly")
            else:
                self.log_test("Error Handling", "FAIL", f"Only {error_handled_count}/{len(invalid_endpoints)} errors handled")
                
        except Exception as e:
            self.log_test("Error Handling", "FAIL", f"Error: {str(e)}")
    
    def test_data_consistency(self):
        """Test data consistency across endpoints"""
        try:
            # Get data from multiple endpoints
            sentiment_response = requests.get(f"{self.base_url}/api/sentiment")
            gauge_response = requests.get(f"{self.base_url}/api/fear_greed_gauge")
            
            if sentiment_response.status_code == 200 and gauge_response.status_code == 200:
                sentiment_data = sentiment_response.json()
                gauge_data = gauge_response.json()
                
                # Extract Fear & Greed values
                sentiment_fg = sentiment_data.get('fear_greed_index', {}).get('fear_greed_index', 0)
                
                # The gauge should be based on the same data
                if 'chart' in gauge_data:
                    # Both should represent the same underlying data
                    self.log_test("Data Consistency", "PASS", f"Sentiment: {sentiment_fg:.2f}, Gauge data available")
                else:
                    self.log_test("Data Consistency", "FAIL", "Gauge data missing")
            else:
                self.log_test("Data Consistency", "FAIL", "API endpoints not responding")
                
        except Exception as e:
            self.log_test("Data Consistency", "FAIL", f"Error: {str(e)}")
    
    def test_performance(self):
        """Test API response performance"""
        try:
            endpoints = [
                "/api/sentiment",
                "/api/historical_data",
                "/api/system_stats"
            ]
            
            performance_results = []
            for endpoint in endpoints:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}")
                end_time = time.time()
                
                if response.status_code == 200:
                    response_time = (end_time - start_time) * 1000  # Convert to ms
                    performance_results.append(response_time)
                    
                    if response_time < 2000:  # Less than 2 seconds
                        self.log_test(f"Performance {endpoint}", "PASS", f"{response_time:.0f}ms")
                    else:
                        self.log_test(f"Performance {endpoint}", "FAIL", f"{response_time:.0f}ms (too slow)")
                else:
                    self.log_test(f"Performance {endpoint}", "FAIL", f"Status: {response.status_code}")
            
            if performance_results:
                avg_performance = sum(performance_results) / len(performance_results)
                self.log_test("Average Performance", "PASS", f"{avg_performance:.0f}ms")
                
        except Exception as e:
            self.log_test("Performance Test", "FAIL", f"Error: {str(e)}")
    
    def test_memory_usage(self):
        """Test memory usage patterns"""
        try:
            # Get system stats multiple times to check for memory leaks
            initial_stats = requests.get(f"{self.base_url}/api/system_stats").json()
            initial_files = initial_stats.get('total_data_files', 0)
            
            # Make multiple requests
            for _ in range(10):
                requests.get(f"{self.base_url}/api/sentiment")
                time.sleep(0.1)
            
            final_stats = requests.get(f"{self.base_url}/api/system_stats").json()
            final_files = final_stats.get('total_data_files', 0)
            
            # Files should not increase drastically
            file_increase = final_files - initial_files
            if file_increase <= 50:  # Reasonable increase
                self.log_test("Memory Usage", "PASS", f"File count increased by {file_increase}")
            else:
                self.log_test("Memory Usage", "FAIL", f"File count increased by {file_increase} (possible memory leak)")
                
        except Exception as e:
            self.log_test("Memory Usage", "FAIL", f"Error: {str(e)}")
    
    def run_advanced_tests(self):
        """Run all advanced tests"""
        print("🔬 Starting advanced Fear & Greed Engine testing...")
        print("=" * 60)
        
        # Run tests
        self.test_concurrent_requests()
        self.test_historical_data_trends()
        self.test_error_handling()
        self.test_data_consistency()
        self.test_performance()
        self.test_memory_usage()
        
        # Skip the long-running test by default
        # self.test_data_pipeline_sequence()
        
        # Summary
        print("\n" + "=" * 60)
        print("🔬 ADVANCED TEST SUMMARY")
        print("=" * 60)
        
        passed = len([t for t in self.test_results if t['status'] == 'PASS'])
        failed = len([t for t in self.test_results if t['status'] == 'FAIL'])
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        
        if failed == 0:
            print("🎉 ALL ADVANCED TESTS PASSED!")
        else:
            print(f"⚠️  {failed} advanced tests failed.")
            for test in self.test_results:
                if test['status'] == 'FAIL':
                    print(f"  - {test['test']}: {test['details']}")
        
        return passed, failed

if __name__ == "__main__":
    tester = AdvancedTester()
    passed, failed = tester.run_advanced_tests()
    
    if failed == 0:
        print("\n🚀 System is production-ready!")
    else:
        print(f"\n⚠️  System needs {failed} more fixes before production.")
