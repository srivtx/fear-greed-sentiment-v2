import logging
import time
import json
from datetime import datetime
from pathlib import Path
import traceback

from data_collection.collector import DataCollector
from sentiment_analysis.analyzer import SentimentAnalysisEngine
from signal_generation.signal_generator import SignalGenerator
from utils.visualization import SentimentVisualizer
from config.config import Config

logger = logging.getLogger(__name__)


class FearGreedEngine:
    """Main engine for the Fear & Greed sentiment analysis system"""

    def __init__(self):
        self.config = Config()
        self.collector = DataCollector()
        self.analyzer = SentimentAnalysisEngine()
        self.signal_generator = SignalGenerator()
        self.visualizer = SentimentVisualizer()
        self.running = False

        # Set up scheduling intervals (in seconds)
        self.collection_interval = self.config.get("engine.collection_interval_minutes", 60) * 60
        self.analysis_interval = self.config.get("engine.sentiment_analysis_interval_minutes", 120) * 60
        self.signal_interval = self.config.get("engine.signal_generation_interval_minutes", 240) * 60

    def start(self, skip_twitter=False):
        """Start the engine in continuous mode"""
        logger.info("Starting Fear & Greed Engine")
        self.running = True

        # Run initial cycle
        self.run_once(skip_twitter=skip_twitter)

        # Continue running until stopped
        last_collection = datetime.now()
        last_analysis = datetime.now()
        last_signal = datetime.now()

        while self.running:
            now = datetime.now()

            # Check if it's time to collect data
            if (now - last_collection).total_seconds() >= self.collection_interval:
                logger.info("Running scheduled data collection")
                collection_dir = self.collector.run_collection_cycle(skip_twitter=skip_twitter)
                last_collection = datetime.now()

                # Immediately run analysis on newly collected data
                logger.info("Running sentiment analysis on newly collected data")
                sentiment_dir = self.analyzer.run(collection_dir)
                last_analysis = datetime.now()

                # Generate visualizations
                if sentiment_dir:
                    self._run_visualization(sentiment_dir)

                # Generate signals
                if sentiment_dir:
                    self.signal_generator.generate_signals(sentiment_dir=sentiment_dir,
                                                           collection_dir=collection_dir)

            # Check if it's time to run analysis (uses most recent collection)
            elif (now - last_analysis).total_seconds() >= self.analysis_interval:
                logger.info("Running scheduled sentiment analysis")
                collection_dirs = sorted(Path("data").glob("collection_*"))
                if collection_dirs:
                    sentiment_dir = self.analyzer.run(collection_dirs[-1])
                    last_analysis = datetime.now()

                    # Generate visualizations
                    if sentiment_dir:
                        self._run_visualization(sentiment_dir)

            # Check if it's time to generate signals
            if (now - last_signal).total_seconds() >= self.signal_interval:
                logger.info("Running scheduled signal generation")
                sentiment_dirs = sorted(Path("data").glob("sentiment_*"))
                if sentiment_dirs:
                    self.signal_generator.generate_signals(sentiment_dir=sentiment_dirs[-1])
                last_signal = datetime.now()

            # Sleep to avoid high CPU usage
            time.sleep(10)
            
            # Log status every minute to show it's alive
            if int(now.timestamp()) % 60 == 0:
                logger.info(f"Engine running... Next collection in {int(self.collection_interval - (now - last_collection).total_seconds())}s")

    def stop(self):
        """Stop the engine"""
        logger.info("Stopping Fear & Greed Engine")
        self.running = False

    def run_once(self, skip_twitter=False):
        """Run one complete cycle of the engine"""
        try:
            logger.info("Running one complete cycle of the Fear & Greed Engine")

            # Step 1: Data Collection
            logger.info("Starting data collection")
            collection_dir = self.collector.run_collection_cycle(skip_twitter=skip_twitter)

            # Step 2: Sentiment Analysis
            logger.info("Starting sentiment analysis")
            sentiment_dir = self.analyzer.run(collection_dir)

            # Step 3: Generate visualizations
            if sentiment_dir:
                logger.info("Generating visualizations")
                self._run_visualization(sentiment_dir)

            # Step 4: Generate signals
            if sentiment_dir:
                logger.info("Starting signal generation")
                signals_file = self.signal_generator.generate_signals(sentiment_dir=sentiment_dir)
            else:
                signals_file = None

            return {
                "collection_dir": str(collection_dir),
                "sentiment_dir": str(sentiment_dir) if sentiment_dir else None,
                "signals_file": signals_file
            }

        except Exception as e:
            logger.error(f"Error in engine cycle: {e}")
            logger.debug(traceback.format_exc())
            return {"error": str(e)}

    def _run_visualization(self, sentiment_dir):
        """Generate visualizations from sentiment analysis"""
        try:
            # Handle different return types from sentiment analyzer
            if isinstance(sentiment_dir, dict) and 'results_dir' in sentiment_dir:
                # Extract the actual directory path from the results dictionary
                sentiment_path = sentiment_dir['results_dir']
            else:
                sentiment_path = sentiment_dir

            # Convert to Path object if it's a string
            sentiment_path = Path(sentiment_path)

            if not sentiment_path.exists():
                logger.error(f"Sentiment directory not found: {sentiment_path}")
                return None

            # Load fear & greed data
            fear_greed_path = sentiment_path / "fear_greed_index.json"
            if not fear_greed_path.exists():
                logger.error(f"Fear & Greed index file not found in {sentiment_path}")
                return None

            with open(fear_greed_path, "r") as f:
                fear_greed_data = json.load(f)

            fear_greed_index = fear_greed_data.get("fear_greed_index", 50)
            sentiment_label = fear_greed_data.get("market_sentiment", "Neutral")

            # Create gauge chart
            gauge_file = self.visualizer.plot_fear_greed_gauge(fear_greed_index, sentiment_label)
            logger.info(f"Generated Fear & Greed gauge: {gauge_file}")

            # Create sentiment trend chart
            trend_file = self.visualizer.plot_sentiment_trends(days=7)
            if trend_file:
                logger.info(f"Generated sentiment trend chart: {trend_file}")

            # Create entity sentiment charts
            entity_sentiment_path = sentiment_path / "entity_sentiment.json"
            if entity_sentiment_path.exists():
                for entity_type in ["cryptos", "stocks", "indices"]:
                    entity_file = self.visualizer.plot_entity_sentiment(
                        sentiment_path, entity_type=entity_type
                    )
                    if entity_file:
                        logger.info(f"Generated {entity_type} sentiment chart: {entity_file}")

            return True

        except Exception as e:
            logger.error(f"Error generating visualizations: {e}")
            logger.debug(traceback.format_exc())
            return None