import logging
import json
import pandas as pd
from pathlib import Path
import numpy as np

logger = logging.getLogger(__name__)


class CorrelationEngine:
    """Calculates correlations between sentiment and market data"""

    def __init__(self):
        pass

    def calculate_correlations(self, sentiment_dir, collection_dir=None):
        """
        Calculate correlations between sentiment and market data

        Args:
            sentiment_dir (str/Path): Path to sentiment directory
            collection_dir (str/Path, optional): Path to collection directory

        Returns:
            dict: Correlation coefficients by entity type and symbol
        """
        # Check if collection_dir is a placeholder or None
        if collection_dir is None or (isinstance(collection_dir, str) and "YYYYMMDD_HHMMSS" in collection_dir):
            # Find most recent collection directory
            collection_dirs = sorted(list(Path("data").glob("collection_*")))
            if collection_dirs:
                collection_dir = collection_dirs[-1]
                logger.info(f"Using most recent collection directory: {collection_dir}")
            else:
                logger.error("No collection directories found")
                return None

        logger.info(f"Calculating correlations between sentiment ({sentiment_dir}) and market data ({collection_dir})")

        # Find market data files
        try:
            market_files = list(Path(collection_dir).glob("market_data_*.csv"))
            if not market_files:
                logger.error(f"No market data found in {collection_dir}")
                return None

            # Load market data
            market_df = pd.read_csv(market_files[0])

            # Load sentiment data
            entity_sentiment_path = Path(sentiment_dir) / "entity_sentiment.json"
            if not entity_sentiment_path.exists():
                logger.error(f"Entity sentiment file not found in {sentiment_dir}")
                return None

            with open(entity_sentiment_path, "r") as f:
                entity_sentiment = json.load(f)

            # Calculate correlations
            correlations = {}

            # For each entity type
            for entity_type in ["cryptos", "stocks", "indices"]:
                if entity_type not in entity_sentiment:
                    continue

                correlations[entity_type] = {}

                for symbol, sentiment_data in entity_sentiment[entity_type].items():
                    try:
                        # Get sentiment score (handle different key names)
                        if "compound" in sentiment_data:
                            sentiment_score = sentiment_data["compound"]
                        elif "sentiment_score" in sentiment_data:
                            sentiment_score = sentiment_data["sentiment_score"]
                        else:
                            logger.warning(f"No sentiment score found for {symbol}")
                            continue

                        # Filter market data for this symbol
                        symbol_data = market_df[market_df["Symbol"] == symbol]

                        if symbol_data.empty:
                            # Try different format for crypto symbols
                            if entity_type == "cryptos":
                                symbol_data = market_df[market_df["Symbol"] == f"{symbol}-USD"]

                        if symbol_data.empty:
                            logger.warning(f"No market data found for {symbol}")
                            continue

                        # Get close price and price change
                        close_price = symbol_data["Close"].values[0]
                        price_change = symbol_data["Change"].values[0] if "Change" in symbol_data.columns else 0

                        # Calculate simple correlation (1 = perfect correlation, -1 = perfect inverse)
                        # This is simplified since we have limited data points
                        if price_change > 0 and sentiment_score > 0:
                            corr = min(1.0, 0.5 + 0.5 * min(price_change / 10, 1.0) * sentiment_score)
                        elif price_change < 0 and sentiment_score < 0:
                            corr = min(1.0, 0.5 + 0.5 * min(abs(price_change) / 10, 1.0) * abs(sentiment_score))
                        elif price_change > 0 and sentiment_score < 0:
                            corr = max(-1.0, -0.5 - 0.5 * min(price_change / 10, 1.0) * abs(sentiment_score))
                        elif price_change < 0 and sentiment_score > 0:
                            corr = max(-1.0, -0.5 - 0.5 * min(abs(price_change) / 10, 1.0) * sentiment_score)
                        else:
                            corr = 0

                        correlations[entity_type][symbol] = round(corr, 2)

                    except Exception as e:
                        logger.error(f"Error calculating correlation for {symbol}: {e}")
                        continue

            return correlations

        except Exception as e:
            logger.error(f"Error calculating correlations: {e}")
            return None

    def calculate_sentiment_market_matrix(self, sentiment_dir, collection_dir=None, days=30):
        """
        Calculate correlation matrix between sentiment and market data over time

        Args:
            sentiment_dir (str/Path): Path to sentiment directory
            collection_dir (str/Path, optional): Path to collection directory
            days (int): Number of days to analyze

        Returns:
            dict: Correlation matrix
        """
        try:
            # Find all sentiment directories sorted by date (newest first)
            data_path = Path("data")
            sentiment_dirs = sorted(list(data_path.glob("sentiment_*")), reverse=True)

            # Limit to the requested number of days
            sentiment_dirs = sentiment_dirs[:days]

            if not sentiment_dirs:
                logger.warning("No sentiment data found for correlation matrix")
                return None

            # Find all collection directories
            collection_dirs = sorted(list(data_path.glob("collection_*")))
            if not collection_dirs:
                logger.warning("No collection data found for correlation matrix")
                return None

            # Create date mapping from sentiment directories to collection directories
            date_mapping = {}
            for sent_dir in sentiment_dirs:
                sent_date = sent_dir.name.split("_")[1][:8]  # Extract date part YYYYMMDD

                # Find matching collection directory
                matching_dirs = [d for d in collection_dirs if sent_date in d.name]
                if matching_dirs:
                    date_mapping[sent_dir] = matching_dirs[0]

            # Calculate correlations for each day
            daily_correlations = {}

            for sent_dir, coll_dir in date_mapping.items():
                try:
                    # Calculate correlation for this day
                    corr = self.calculate_correlations(sent_dir, coll_dir)
                    if corr:
                        # Get date string
                        date_str = sent_dir.name.split("_")[1][:8]
                        daily_correlations[date_str] = corr
                except Exception as e:
                    logger.error(f"Error calculating correlation for {sent_dir}: {e}")
                    continue

            return daily_correlations

        except Exception as e:
            logger.error(f"Error calculating sentiment-market matrix: {e}")
            return None

    def identify_correlation_trends(self, days=7):
        """
        Identify trends in sentiment-market correlations

        Args:
            days (int): Number of days to analyze

        Returns:
            dict: Correlation trends
        """
        try:
            # Calculate correlation matrix
            matrix = self.calculate_sentiment_market_matrix(None, None, days)

            if not matrix:
                return None

            # Track correlation trends by entity
            trends = {
                "strengthening": [],  # Correlation getting stronger (abs value increasing)
                "weakening": [],  # Correlation getting weaker (abs value decreasing)
                "reversal": [],  # Correlation changing sign
                "stable_positive": [],  # Consistently positive correlation
                "stable_negative": []  # Consistently negative correlation
            }

            # Flatten the correlation data
            flat_data = {}
            for date, entity_types in matrix.items():
                for entity_type, symbols in entity_types.items():
                    for symbol, corr in symbols.items():
                        key = f"{entity_type}.{symbol}"
                        if key not in flat_data:
                            flat_data[key] = []
                        flat_data[key].append((date, corr))

            # Analyze trends for each entity
            for key, values in flat_data.items():
                # Sort by date
                values.sort(key=lambda x: x[0])

                # Need at least 3 data points for trend analysis
                if len(values) < 3:
                    continue

                # Calculate trend metrics
                entity_type, symbol = key.split(".")

                # Check for sign changes
                signs = [1 if corr >= 0 else -1 for _, corr in values]
                sign_changes = sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1])

                # Calculate average absolute correlation
                avg_abs_corr = sum(abs(corr) for _, corr in values) / len(values)

                # Calculate correlation trend (slope)
                abs_corrs = [abs(corr) for _, corr in values]
                if len(abs_corrs) >= 2:
                    trend = (abs_corrs[-1] - abs_corrs[0]) / (len(abs_corrs) - 1)
                else:
                    trend = 0

                # Determine trend category
                if sign_changes > 0:
                    trends["reversal"].append({
                        "entity_type": entity_type,
                        "symbol": symbol,
                        "sign_changes": sign_changes,
                        "values": values
                    })
                elif trend > 0.05:  # Strengthening correlation
                    trends["strengthening"].append({
                        "entity_type": entity_type,
                        "symbol": symbol,
                        "trend": trend,
                        "avg_correlation": avg_abs_corr,
                        "values": values
                    })
                elif trend < -0.05:  # Weakening correlation
                    trends["weakening"].append({
                        "entity_type": entity_type,
                        "symbol": symbol,
                        "trend": trend,
                        "avg_correlation": avg_abs_corr,
                        "values": values
                    })
                elif all(corr > 0.3 for _, corr in values):  # Consistently positive
                    trends["stable_positive"].append({
                        "entity_type": entity_type,
                        "symbol": symbol,
                        "avg_correlation": avg_abs_corr,
                        "values": values
                    })
                elif all(corr < -0.3 for _, corr in values):  # Consistently negative
                    trends["stable_negative"].append({
                        "entity_type": entity_type,
                        "symbol": symbol,
                        "avg_correlation": avg_abs_corr,
                        "values": values
                    })

            return trends

        except Exception as e:
            logger.error(f"Error identifying correlation trends: {e}")
            return None