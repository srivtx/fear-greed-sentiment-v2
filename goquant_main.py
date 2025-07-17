#!/usr/bin/env python3
"""
Enhanced Fear & Greed Sentiment Engine for GoQuant
Main application with real-time processing, performance monitoring, and advanced features
"""

import argparse
import logging
import signal
import sys
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
import threading
from typing import Dict, List

# Import our enhanced components
from real_time_engine import RealTimeFearGreedEngine
from advanced_sentiment_analyzer import AdvancedFinancialSentimentAnalyzer
from advanced_signal_generator import AdvancedSignalGenerator

# Import existing components
from engine import FearGreedEngine
from data_collection.collector import DataCollector
from utils.visualization import SentimentVisualizer

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(threadName)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f'fear_greed_engine_{datetime.now().strftime("%Y%m%d")}.log')
    ]
)

logger = logging.getLogger("GoQuantFearGreedEngine")

class GoQuantFearGreedEngine:
    """
    Enhanced Fear & Greed Engine for GoQuant requirements
    Features: Real-time processing, advanced NLP, sophisticated signal generation
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.real_time_engine = RealTimeFearGreedEngine()
        self.advanced_sentiment = AdvancedFinancialSentimentAnalyzer()
        self.advanced_signals = AdvancedSignalGenerator()
        self.legacy_engine = FearGreedEngine()
        self.data_collector = DataCollector()
        self.visualizer = SentimentVisualizer()
        
        # Performance tracking
        self.start_time = time.time()
        self.session_stats = {
            'texts_processed': 0,
            'signals_generated': 0,
            'api_calls': 0,
            'errors': 0,
            'uptime_seconds': 0
        }
        
        # Control flags
        self.running = False
        self.shutdown_requested = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info("GoQuant Fear & Greed Engine initialized")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.shutdown_requested = True
        
        if self.running:
            self.stop()
    
    def run_real_time_mode(self, skip_twitter: bool = True, duration_minutes: int = None):
        """
        Run the engine in real-time mode with advanced processing
        
        Args:
            skip_twitter: Skip Twitter data collection
            duration_minutes: Run for specified duration (None = indefinite)
        """
        self.logger.info("Starting GoQuant Fear & Greed Engine in REAL-TIME mode")
        self.logger.info("=" * 60)
        
        self.running = True
        
        # Start the real-time engine
        threads = self.real_time_engine.start(skip_twitter=skip_twitter)
        
        # Performance monitoring thread
        monitor_thread = threading.Thread(
            target=self._monitor_performance,
            name="PerformanceMonitor",
            daemon=True
        )
        monitor_thread.start()
        threads.append(monitor_thread)
        
        # Main execution loop
        start_time = time.time()
        try:
            self.logger.info("Real-time engine started successfully")
            self.logger.info("Processing social media and market data streams...")
            self.logger.info("Generating sentiment analysis and trading signals...")
            self.logger.info("Press Ctrl+C to stop\n")
            
            while self.running and not self.shutdown_requested:
                # Check if duration limit reached
                if duration_minutes:
                    elapsed_minutes = (time.time() - start_time) / 60
                    if elapsed_minutes >= duration_minutes:
                        self.logger.info(f"Duration limit ({duration_minutes} minutes) reached")
                        break
                
                # Display recent signals periodically
                if int(time.time()) % 30 == 0:  # Every 30 seconds
                    self._display_recent_signals()
                
                time.sleep(1)
        
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received")
        except Exception as e:
            self.logger.error(f"Error in real-time mode: {e}")
        finally:
            self.stop()
    
    def run_batch_mode(self, source: str = "all", analyze_only: bool = False):
        """
        Run the engine in batch mode for data collection and analysis
        
        Args:
            source: Data source to collect ('all', 'reddit', 'news', 'market')
            analyze_only: Only perform analysis on existing data
        """
        self.logger.info("Starting GoQuant Fear & Greed Engine in BATCH mode")
        self.logger.info("=" * 60)
        
        try:
            if not analyze_only:
                # Data Collection Phase
                self.logger.info("Phase 1: Data Collection")
                self.logger.info("-" * 30)
                
                collection_start = time.time()
                
                # Run full collection cycle using the proper method
                self.logger.info(f"Running data collection cycle for: {source}")
                collection_dir = self.data_collector.run_collection_cycle(skip_twitter=True)
                self.logger.info(f"Data collection completed: {collection_dir}")
                
                # Store the collection directory for analysis
                self.collection_dir = collection_dir
                
                collection_time = time.time() - collection_start
                self.logger.info(f"Data collection completed in {collection_time:.2f} seconds")
            
            # Advanced Sentiment Analysis Phase
            self.logger.info("\nPhase 2: Advanced Sentiment Analysis")
            self.logger.info("-" * 40)
            
            analysis_start = time.time()
            
            # Use the proper method to run sentiment analysis
            if hasattr(self, 'collection_dir') and self.collection_dir:
                # Analyze the newly collected data
                sentiment_dir = self.legacy_engine.analyzer.run(self.collection_dir)
                self.sentiment_dir = sentiment_dir
                self.logger.info(f"Sentiment analysis completed: {sentiment_dir}")
            else:
                # Use the most recent sentiment data
                sentiment_dir = self.legacy_engine.analyzer.run()
                self.sentiment_dir = sentiment_dir
                self.logger.info(f"Using existing sentiment analysis: {sentiment_dir}")
            
            # Load sentiment results for advanced processing
            sentiment_results = {}
            try:
                # Load sentiment data files
                sentiment_files = list(Path(sentiment_dir).glob("*.json"))
                all_texts = []
                for file_path in sentiment_files:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            all_texts.extend([item.get('text', '') for item in data if 'text' in item])
                        elif isinstance(data, dict) and 'texts' in data:
                            all_texts.extend(data['texts'])
                
                self.logger.info(f"Loaded {len(all_texts)} texts for advanced analysis")
            except Exception as e:
                self.logger.warning(f"Could not load sentiment texts: {e}")
                all_texts = []
            
            # Extract texts for advanced analysis
            all_texts = []
            if 'reddit' in sentiment_results:
                reddit_texts = [post.get('title', '') + ' ' + post.get('body', '') 
                              for post in sentiment_results['reddit'].get('posts', [])]
                all_texts.extend(reddit_texts)
            
            if 'news' in sentiment_results:
                news_texts = [article.get('title', '') + ' ' + article.get('description', '')
                            for article in sentiment_results['news'].get('articles', [])]
                all_texts.extend(news_texts)
            
            # Run advanced sentiment analysis
            if all_texts:
                self.logger.info(f"Analyzing {len(all_texts)} texts with advanced NLP...")
                advanced_sentiment = self.advanced_sentiment.analyze_advanced_sentiment(all_texts)
                
                # Log advanced metrics
                self.logger.info(f"Advanced sentiment score: {advanced_sentiment['overall_sentiment']:.3f}")
                self.logger.info(f"Confidence: {advanced_sentiment['confidence']:.3f}")
                self.logger.info(f"Financial relevance: {advanced_sentiment['text_analysis']['financial_relevance_score']:.3f}")
                self.logger.info(f"Processing speed: {advanced_sentiment['processing_metrics']['texts_per_second']:.1f} texts/sec")
                
                # Display entity sentiments
                if advanced_sentiment['entity_sentiment']:
                    self.logger.info("\nEntity Sentiments:")
                    for entity, data in advanced_sentiment['entity_sentiment'].items():
                        self.logger.info(f"  {entity}: {data['sentiment']:.3f} (confidence: {data['confidence']:.2f}, mentions: {data['mention_count']})")
            
            analysis_time = time.time() - analysis_start
            self.logger.info(f"\nSentiment analysis completed in {analysis_time:.2f} seconds")
            
            # Advanced Signal Generation Phase
            self.logger.info("\nPhase 3: Advanced Signal Generation")
            self.logger.info("-" * 40)
            
            signal_start = time.time()
            
            # Generate legacy signals first
            if hasattr(self, 'sentiment_dir') and self.sentiment_dir:
                legacy_signals_file = self.legacy_engine.signal_generator.generate_signals(
                    sentiment_dir=self.sentiment_dir,
                    collection_dir=getattr(self, 'collection_dir', None)
                )
                self.logger.info(f"Legacy signals generated: {legacy_signals_file}")
            
            # Generate advanced signals
            if 'all_texts' in locals() and all_texts:
                advanced_sentiment = self.advanced_sentiment.analyze_advanced_sentiment(all_texts)
                
                signals = self.advanced_signals.generate_signals(
                    advanced_sentiment,
                    market_data={},  # Will be populated by advanced signal generator
                    historical_data=None  # Could add historical data collection
                )
                
                signal_time = time.time() - signal_start
                self.logger.info(f"Generated {len(signals)} trading signals in {signal_time:.2f} seconds")
                
                # Display signals
                if signals:
                    self.logger.info("\nGenerated Trading Signals:")
                    for signal in signals[:10]:  # Show top 10
                        self.logger.info(f"  {signal.symbol}: {signal.signal_type} "
                                       f"(confidence: {signal.confidence:.2f}, "
                                       f"strength: {signal.strength:.2f}, "
                                       f"risk: {signal.risk_score:.2f})")
                        self.logger.info(f"    Reasoning: {signal.reasoning}")
                        if signal.price_target:
                            self.logger.info(f"    Target: ${signal.price_target:.2f}, "
                                           f"Stop: ${signal.stop_loss:.2f}")
                
                # Save signals
                self._save_signals(signals)
            
            # Visualization Phase
            self.logger.info("\nPhase 4: Visualization Generation")
            self.logger.info("-" * 35)
            
            viz_start = time.time()
            if hasattr(self, 'sentiment_dir') and self.sentiment_dir:
                self.legacy_engine._run_visualization(self.sentiment_dir)
            viz_time = time.time() - viz_start
            
            self.logger.info(f"Visualizations created in {viz_time:.2f} seconds")
            
            # Final Summary
            total_time = time.time() - (collection_start if not analyze_only else analysis_start)
            self.logger.info(f"\n{'='*60}")
            self.logger.info("BATCH PROCESSING COMPLETED")
            self.logger.info(f"Total execution time: {total_time:.2f} seconds")
            self.logger.info(f"{'='*60}")
            
        except Exception as e:
            self.logger.error(f"Error in batch mode: {e}")
            raise
    
    def run_performance_test(self, duration_minutes: int = 5):
        """
        Run performance test to validate GoQuant requirements
        
        Args:
            duration_minutes: Duration to run the test
        """
        self.logger.info("Starting PERFORMANCE TEST for GoQuant requirements")
        self.logger.info("=" * 60)
        self.logger.info(f"Test duration: {duration_minutes} minutes")
        self.logger.info("Target metrics:")
        self.logger.info("  - Sentiment analysis: <100ms per text")
        self.logger.info("  - Signal generation: <500ms per signal")
        self.logger.info("  - Throughput: >10,000 texts/minute")
        self.logger.info("")
        
        # Run real-time mode for specified duration
        self.run_real_time_mode(skip_twitter=True, duration_minutes=duration_minutes)
        
        # Analyze performance results
        self._analyze_performance_results()
    
    def _display_recent_signals(self):
        """Display recent trading signals"""
        try:
            signals = self.real_time_engine.get_recent_signals(limit=5)
            if signals:
                self.logger.info(f"\nRecent Signals ({len(signals)}):")
                for signal in signals:
                    self.logger.info(f"  {signal.symbol}: {signal.signal} "
                                   f"(confidence: {signal.confidence:.2f})")
        except Exception as e:
            self.logger.debug(f"Error displaying signals: {e}")
    
    def _monitor_performance(self):
        """Monitor and log performance metrics"""
        while self.running and not self.shutdown_requested:
            try:
                time.sleep(60)  # Report every minute
                
                # Get real-time engine metrics
                rt_metrics = self.real_time_engine.get_performance_metrics()
                
                # Get advanced analyzer metrics
                analyzer_metrics = self.advanced_sentiment.get_performance_metrics()
                
                # Get signal generator metrics
                signal_metrics = self.advanced_signals.get_performance_metrics()
                
                # Log consolidated metrics
                self.logger.info("=== PERFORMANCE METRICS ===")
                self.logger.info(f"Runtime: {rt_metrics['runtime_seconds']:.1f}s")
                self.logger.info(f"Texts processed: {rt_metrics['texts_processed']} "
                               f"({rt_metrics['texts_per_minute']:.1f}/min)")
                self.logger.info(f"Signals generated: {rt_metrics['signals_generated']} "
                               f"({rt_metrics['signals_per_minute']:.1f}/min)")
                self.logger.info(f"Avg processing time: {analyzer_metrics.get('avg_processing_time_ms', 0):.2f}ms")
                self.logger.info(f"Queue sizes: Data={rt_metrics['queue_sizes']['data']}, "
                               f"Sentiment={rt_metrics['queue_sizes']['sentiment']}, "
                               f"Signals={rt_metrics['queue_sizes']['signals']}")
                
                # Performance warnings (adjusted for real-time vs batch processing)
                if rt_metrics['texts_per_minute'] < 500:  # Realistic real-time target
                    self.logger.warning("⚠️  Throughput below real-time target (500 texts/min)")
                else:
                    self.logger.info("✅ Throughput meets real-time target")
                
                if analyzer_metrics.get('avg_processing_time_ms', 0) > 100:
                    self.logger.warning("⚠️  Sentiment processing time above target (100ms)")
                
                self.logger.info("=" * 30)
                
            except Exception as e:
                self.logger.error(f"Error in performance monitoring: {e}")
    
    def _save_signals(self, signals):
        """Save trading signals to file"""
        try:
            signals_dir = Path("data/signals")
            signals_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = signals_dir / f"signals_{timestamp}.json"
            
            # Convert signals to JSON-serializable format
            signals_data = []
            for signal in signals:
                signals_data.append({
                    'symbol': signal.symbol,
                    'signal_type': signal.signal_type,
                    'confidence': signal.confidence,
                    'strength': signal.strength,
                    'sentiment_score': signal.sentiment_score,
                    'price_target': signal.price_target,
                    'stop_loss': signal.stop_loss,
                    'position_size': signal.position_size,
                    'risk_score': signal.risk_score,
                    'time_horizon': signal.time_horizon,
                    'reasoning': signal.reasoning,
                    'generated_at': signal.generated_at.isoformat(),
                    'expires_at': signal.expires_at.isoformat(),
                    'metadata': signal.metadata
                })
            
            with open(filename, 'w') as f:
                json.dump(signals_data, f, indent=2)
            
            self.logger.info(f"Signals saved to {filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving signals: {e}")
    
    def _analyze_performance_results(self):
        """Analyze and report performance test results"""
        self.logger.info("\n" + "="*60)
        self.logger.info("PERFORMANCE TEST RESULTS")
        self.logger.info("="*60)
        
        # Get final metrics
        rt_metrics = self.real_time_engine.get_performance_metrics()
        analyzer_metrics = self.advanced_sentiment.get_performance_metrics()
        signal_metrics = self.advanced_signals.get_performance_metrics()
        
        # GoQuant requirement analysis
        self.logger.info("GoQuant Requirements Analysis:")
        self.logger.info("-" * 35)
        
        # Requirement 1: Sentiment analysis <100ms
        avg_sentiment_time = analyzer_metrics.get('avg_processing_time_ms', 0)
        p95_sentiment_time = analyzer_metrics.get('p95_processing_time_ms', 0)
        
        if avg_sentiment_time <= 100:
            self.logger.info("✅ Sentiment Analysis: PASSED")
        else:
            self.logger.info("❌ Sentiment Analysis: FAILED")
        
        self.logger.info(f"   Average: {avg_sentiment_time:.2f}ms (target: <100ms)")
        self.logger.info(f"   P95: {p95_sentiment_time:.2f}ms")
        
        # Requirement 2: Signal generation <500ms
        avg_signal_time = signal_metrics.get('avg_generation_time_ms', 0)
        
        if avg_signal_time <= 500:
            self.logger.info("✅ Signal Generation: PASSED")
        else:
            self.logger.info("❌ Signal Generation: FAILED")
        
        self.logger.info(f"   Average: {avg_signal_time:.2f}ms (target: <500ms)")
        
        # Requirement 3: Throughput >10,000 texts/minute
        throughput = rt_metrics['texts_per_minute']
        
        if throughput >= 10000:
            self.logger.info("✅ Throughput: PASSED")
        else:
            self.logger.info("❌ Throughput: FAILED")
        
        self.logger.info(f"   Achieved: {throughput:.1f} texts/min (target: >10,000/min)")
        
        # Overall assessment
        self.logger.info("\nOverall Assessment:")
        self.logger.info("-" * 20)
        
        requirements_met = 0
        total_requirements = 3
        
        if avg_sentiment_time <= 100:
            requirements_met += 1
        if avg_signal_time <= 500:
            requirements_met += 1
        if throughput >= 10000:
            requirements_met += 1
        
        pass_rate = (requirements_met / total_requirements) * 100
        
        if pass_rate >= 100:
            self.logger.info("🎉 ALL GOQUANT REQUIREMENTS MET!")
        elif pass_rate >= 67:
            self.logger.info("⚠️  MOST GOQUANT REQUIREMENTS MET")
        else:
            self.logger.info("❌ GOQUANT REQUIREMENTS NOT MET")
        
        self.logger.info(f"Pass rate: {pass_rate:.1f}% ({requirements_met}/{total_requirements})")
        
        # Additional metrics
        self.logger.info(f"\nAdditional Metrics:")
        self.logger.info(f"  Total runtime: {rt_metrics['runtime_seconds']:.1f} seconds")
        self.logger.info(f"  Total texts processed: {rt_metrics['texts_processed']}")
        self.logger.info(f"  Total signals generated: {rt_metrics['signals_generated']}")
        self.logger.info(f"  Error rate: {self.session_stats['errors']}")
        self.logger.info(f"  Active threads: {rt_metrics['threads_active']}")
        
        self.logger.info("="*60)
    
    def stop(self):
        """Stop the engine gracefully"""
        self.logger.info("Stopping GoQuant Fear & Greed Engine...")
        self.running = False
        
        # Stop real-time engine and get final metrics
        final_metrics = self.real_time_engine.stop()
        
        # Update session stats with real-time engine metrics
        if final_metrics:
            self.session_stats['texts_processed'] = final_metrics.get('texts_processed', 0)
            self.session_stats['signals_generated'] = final_metrics.get('signals_generated', 0)
            self.session_stats['api_calls'] = final_metrics.get('api_calls', 0)
        
        # Final session stats
        self.session_stats['uptime_seconds'] = time.time() - self.start_time
        
        self.logger.info("Engine stopped successfully")
        self.logger.info(f"Session statistics: {json.dumps(self.session_stats, indent=2)}")

def main():
    """Main entry point with enhanced argument parsing"""
    parser = argparse.ArgumentParser(
        description="GoQuant Fear & Greed Sentiment Engine - Advanced Version"
    )
    
    parser.add_argument(
        "--mode", 
        type=str, 
        default="real-time",
        choices=["real-time", "batch", "performance-test", "legacy"],
        help="Engine operation mode"
    )
    
    parser.add_argument(
        "--source", 
        type=str, 
        choices=["twitter", "reddit", "news", "market", "all"], 
        default="all",
        help="Data source for collection (batch mode only)"
    )
    
    parser.add_argument(
        "--duration", 
        type=int, 
        help="Duration in minutes (real-time and performance-test modes)"
    )
    
    parser.add_argument(
        "--no-twitter", 
        action="store_true", 
        help="Skip Twitter data collection"
    )
    
    parser.add_argument(
        "--analyze-only", 
        action="store_true", 
        help="Only analyze existing data (batch mode)"
    )
    
    parser.add_argument(
        "--log-level", 
        type=str, 
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )
    
    args = parser.parse_args()
    
    # Set logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Initialize engine
    engine = GoQuantFearGreedEngine()
    
    try:
        if args.mode == "real-time":
            engine.run_real_time_mode(
                skip_twitter=args.no_twitter,
                duration_minutes=args.duration
            )
        
        elif args.mode == "batch":
            engine.run_batch_mode(
                source=args.source,
                analyze_only=args.analyze_only
            )
        
        elif args.mode == "performance-test":
            duration = args.duration or 5
            engine.run_performance_test(duration_minutes=duration)
        
        elif args.mode == "legacy":
            # Run original engine for compatibility
            legacy_engine = FearGreedEngine()
            legacy_engine.run_full_cycle()
        
    except KeyboardInterrupt:
        logger.info("Operation interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        if hasattr(engine, 'stop'):
            engine.stop()

if __name__ == "__main__":
    main()
