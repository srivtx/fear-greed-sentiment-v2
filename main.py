import argparse
import logging
from datetime import datetime
import sys
import time
from pathlib import Path
import json

from engine import FearGreedEngine
from data_collection.collector import DataCollector
from sentiment_analysis.analyzer import SentimentAnalysisEngine
from signal_generation.signal_generator import SignalGenerator
from utils.visualization import SentimentVisualizer

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("FearGreedEngine")


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Fear & Greed Sentiment Engine")
    parser.add_argument("--mode", type=str, default="run",
                        choices=["run", "collect", "analyze", "signal", "visualize"],
                        help="Mode to run the engine in")
    parser.add_argument("--continuous", action="store_true", help="Run in continuous mode")
    parser.add_argument("--data-dir", type=str, help="Data directory to use for analysis or signal generation")
    parser.add_argument("--source", type=str, choices=["twitter", "reddit", "news", "market", "all"], default="all",
                        help="Specific data source to collect (only in collect mode)")
    parser.add_argument("--no-twitter", action="store_true", help="Skip Twitter data collection")
    args = parser.parse_args()

    # Initialize engine
    engine = FearGreedEngine()

    # Run in specified mode
    if args.mode == "run":
        if args.continuous:
            logger.info("Starting Fear & Greed Engine in continuous mode")
            engine.start(skip_twitter=args.no_twitter)

            # Keep running until interrupted
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received. Stopping engine...")
                engine.stop()
        else:
            logger.info("Running one cycle of Fear & Greed Engine")
            result = engine.run_once(skip_twitter=args.no_twitter)
            logger.info(f"Engine run completed successfully")

    elif args.mode == "collect":
        logger.info("Running data collection only")
        collector = DataCollector()

        if args.source != "all":
            logger.info(f"Collecting data from {args.source} only")
            # Create a collection directory
            collection_dir = Path("data") / f"collection_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            collection_dir.mkdir(parents=True, exist_ok=True)

            # Call source-specific collection method
            if args.source == "twitter" and not args.no_twitter:
                collector._collect_twitter_data(collection_dir)
            elif args.source == "reddit":
                collector._collect_reddit_data(collection_dir)
            elif args.source == "news":
                collector._collect_news_data(collection_dir)
            elif args.source == "market":
                collector._collect_market_data(collection_dir)
        else:
            # Run full collection cycle
            collection_dir = collector.run_collection_cycle(skip_twitter=args.no_twitter)
            logger.info(f"Data collection completed: {collection_dir}")

    elif args.mode == "analyze":
        logger.info("Running sentiment analysis only")
        analyzer = SentimentAnalysisEngine()

        # Use specified data directory or find most recent
        collection_dir = None
        if args.data_dir:
            collection_dir = Path(args.data_dir)
        else:
            # Find most recent collection directory
            data_path = Path("data")
            collection_dirs = sorted([d for d in data_path.glob("collection_*")])
            if collection_dirs:
                collection_dir = collection_dirs[-1]
            else:
                logger.error("No collection directories found")
                return

        logger.info(f"Using collection directory: {collection_dir}")
        sentiment_dir = analyzer.run(collection_dir)

        # Generate visualizations if sentiment analysis succeeded
        if sentiment_dir:
            visualizer = SentimentVisualizer()
            try:
                # Load fear & greed data
                fear_greed_path = Path(sentiment_dir) / "fear_greed_index.json"
                if fear_greed_path.exists():
                    with open(fear_greed_path, "r") as f:
                        fear_greed_data = json.load(f)

                    fear_greed_index = fear_greed_data.get("fear_greed_index", 50)
                    sentiment_label = fear_greed_data.get("market_sentiment", "Neutral")

                    # Create visualizations
                    gauge_file = visualizer.plot_fear_greed_gauge(fear_greed_index, sentiment_label)
                    logger.info(f"Created Fear & Greed gauge: {gauge_file}")

                    trend_file = visualizer.plot_sentiment_trends()
                    if trend_file:
                        logger.info(f"Created sentiment trend chart: {trend_file}")

                    # Create entity sentiment charts
                    for entity_type in ["cryptos", "stocks", "indices"]:
                        entity_file = visualizer.plot_entity_sentiment(sentiment_dir, entity_type=entity_type)
                        if entity_file:
                            logger.info(f"Created {entity_type} sentiment chart: {entity_file}")
            except Exception as e:
                logger.error(f"Error generating visualizations: {e}")

        logger.info(f"Sentiment analysis completed: {sentiment_dir}")

    elif args.mode == "signal":
        logger.info("Running signal generation only")
        signal_generator = SignalGenerator()

        # Use specified sentiment directory or find most recent
        sentiment_dir = None
        if args.data_dir:
            sentiment_dir = Path(args.data_dir)
        else:
            # Find most recent sentiment directory
            data_path = Path("data")
            sentiment_dirs = sorted([d for d in data_path.glob("sentiment_*")])
            if sentiment_dirs:
                sentiment_dir = sentiment_dirs[-1]
            else:
                logger.error("No sentiment directories found")
                return

        logger.info(f"Using sentiment directory: {sentiment_dir}")

        # Find most recent collection directory for market data
        collection_dir = None
        data_path = Path("data")
        collection_dirs = sorted([d for d in data_path.glob("collection_*")])
        if collection_dirs:
            collection_dir = collection_dirs[-1]

        result = signal_generator.generate_signals(sentiment_dir=sentiment_dir)
        logger.info(f"Signal generation completed: {result}")

    elif args.mode == "visualize":
        logger.info("Generating visualizations")
        visualizer = SentimentVisualizer()

        # Use specified sentiment directory or find most recent
        sentiment_dir = None
        if args.data_dir:
            sentiment_dir = Path(args.data_dir)
        else:
            # Find most recent sentiment directory
            data_path = Path("data")
            sentiment_dirs = sorted([d for d in data_path.glob("sentiment_*")])
            if sentiment_dirs:
                sentiment_dir = sentiment_dirs[-1]
            else:
                logger.error("No sentiment directories found")
                return

        logger.info(f"Using sentiment directory: {sentiment_dir}")

        try:
            # Load fear & greed data
            fear_greed_path = Path(sentiment_dir) / "fear_greed_index.json"
            if fear_greed_path.exists():
                with open(fear_greed_path, "r") as f:
                    fear_greed_data = json.load(f)

                fear_greed_index = fear_greed_data.get("fear_greed_index", 50)
                sentiment_label = fear_greed_data.get("market_sentiment", "Neutral")

                # Create visualizations
                gauge_file = visualizer.plot_fear_greed_gauge(fear_greed_index, sentiment_label)
                logger.info(f"Created Fear & Greed gauge: {gauge_file}")

                trend_file = visualizer.plot_sentiment_trends()
                if trend_file:
                    logger.info(f"Created sentiment trend chart: {trend_file}")

                # Create entity sentiment charts
                for entity_type in ["cryptos", "stocks", "indices"]:
                    entity_file = visualizer.plot_entity_sentiment(sentiment_dir, entity_type=entity_type)
                    if entity_file:
                        logger.info(f"Created {entity_type} sentiment chart: {entity_file}")
        except Exception as e:
            logger.error(f"Error generating visualizations: {e}")


if __name__ == "__main__":
    main()