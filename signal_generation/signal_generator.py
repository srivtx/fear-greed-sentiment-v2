import logging
import json
from pathlib import Path
import datetime
import pandas as pd
import numpy as np
import os

from config.config import Config
from signal_generation.correlation_engine import CorrelationEngine

logger = logging.getLogger(__name__)


class SignalGenerator:
    """Generates trading signals from sentiment analysis"""

    def __init__(self):
        self.config = Config()
        self.correlation_engine = CorrelationEngine()
        self.data_path = Path(self.config.get("data_storage.path", "data"))
        self.signals_dir = self.data_path / "signals"
        self.signals_dir.mkdir(parents=True, exist_ok=True)

        # Configuration thresholds
        self.sentiment_threshold = self.config.get("signals.sentiment_threshold", 0.25)
        self.confidence_threshold = self.config.get("signals.confidence_threshold", 0.5)
        self.minimum_mentions = self.config.get("signals.minimum_mentions", 3)

    def generate_signals(self, sentiment_dir=None, collection_dir=None):
        """
        Generate trading signals based on sentiment analysis

        Args:
            sentiment_dir (str, optional): Path to sentiment analysis directory
            collection_dir (str, optional): Path to data collection directory

        Returns:
            str: Path to generated signals file
        """
        # Find the most recent sentiment directory if not specified
        if sentiment_dir is None:
            # Find all sentiment directories
            sentiment_dirs = sorted(list(self.data_path.glob("sentiment_*")))
            if not sentiment_dirs:
                logger.error("No sentiment analysis directories found")
                return None
            sentiment_dir = sentiment_dirs[-1]  # Use the most recent
        else:
            sentiment_dir = Path(sentiment_dir)

        # Find the most recent collection directory if not specified
        if collection_dir is None:
            # Find all collection directories
            collection_dirs = sorted(list(self.data_path.glob("collection_*")))
            if not collection_dirs:
                logger.error("No data collection directories found")
                collection_dir = None
            else:
                collection_dir = collection_dirs[-1]  # Use the most recent

        logger.info(f"Generating signals from sentiment data in {sentiment_dir}")

        # Calculate market correlations
        try:
            correlations = self.correlation_engine.calculate_correlations(
                sentiment_dir=sentiment_dir,
                collection_dir=collection_dir
            )
        except Exception as e:
            logger.error(f"Error calculating correlations: {e}")
            correlations = None

        # Generate signals from sentiment
        signals = self._generate_signals_from_sentiment(sentiment_dir, correlations)

        if not signals:
            logger.warning("No signals generated")
            signals = {"signals": []}  # Empty signals object

        # Save signals
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        signals_file = self.signals_dir / f"signals_{timestamp}.json"

        with open(signals_file, "w") as f:
            json.dump(signals, f, indent=2)

        logger.info(f"Generated {len(signals.get('signals', []))} trading signals")
        logger.info(f"Signals saved to {signals_file}")

        return str(signals_file)

    def _generate_signals_from_sentiment(self, sentiment_dir, correlations=None):
        """Generate signals from sentiment analysis data"""
        try:
            # Check required files exist
            entity_sentiment_path = Path(sentiment_dir) / "entity_sentiment.json"
            fear_greed_path = Path(sentiment_dir) / "fear_greed_index.json"

            if not entity_sentiment_path.exists() or not fear_greed_path.exists():
                logger.error(f"Required sentiment files not found in {sentiment_dir}")
                return None

            # Load sentiment data
            with open(entity_sentiment_path, "r") as f:
                entity_sentiment = json.load(f)

            with open(fear_greed_path, "r") as f:
                fear_greed_data = json.load(f)

            # Extract market sentiment
            market_sentiment = fear_greed_data.get("market_sentiment", "Neutral")
            fear_greed_index = fear_greed_data.get("fear_greed_index", 50)

            # Initialize signals
            signals = {
                "timestamp": datetime.datetime.now().isoformat(),
                "market_sentiment": market_sentiment,
                "fear_greed_index": fear_greed_index,
                "signals": []
            }

            # Process each entity type
            for entity_type in ["cryptos", "stocks", "indices"]:
                if entity_type in entity_sentiment:
                    entities = entity_sentiment[entity_type]

                    for symbol, data in entities.items():
                        # Get mentions count
                        mentions = data.get("mentions", 0)

                        # Check if entity has enough mentions
                        if mentions < self.minimum_mentions:
                            continue

                        # Get sentiment score - handle different possible keys
                        sentiment_score = None
                        if "compound" in data:
                            sentiment_score = data["compound"]
                        elif "sentiment_score" in data:
                            sentiment_score = data["sentiment_score"]

                        if sentiment_score is None:
                            continue

                        sentiment_magnitude = abs(sentiment_score)

                        # Skip if sentiment is not strong enough
                        if sentiment_magnitude < self.sentiment_threshold:
                            continue

                        # Determine signal type
                        signal_type = "BUY" if sentiment_score > 0 else "SELL"

                        # Calculate confidence based on sentiment and mentions
                        # Improved formula: gives more weight to mentions and higher base confidence
                        sentiment_component = sentiment_magnitude * 0.5  # Reduced from 0.7
                        mentions_component = min(mentions, 30) / 30 * 0.4  # Increased from 0.3
                        base_confidence = 0.2  # Base confidence for any qualifying signal
                        
                        confidence = min(0.9, base_confidence + sentiment_component + mentions_component)

                        # Skip if confidence is too low
                        if confidence < self.confidence_threshold:
                            continue

                        # Create signal
                        signal = {
                            "symbol": symbol,
                            "type": signal_type,
                            "confidence": round(confidence, 2),
                            "sentiment": round(sentiment_score, 2),
                            "mentions": mentions,
                            "entity_type": entity_type[:-1]  # Remove trailing 's'
                        }

                        # Add correlation data if available
                        if correlations and entity_type in correlations and symbol in correlations[entity_type]:
                            signal["correlation"] = round(correlations[entity_type][symbol], 2)

                        signals["signals"].append(signal)

            return signals

        except Exception as e:
            logger.error(f"Error generating signals: {e}")
            return None