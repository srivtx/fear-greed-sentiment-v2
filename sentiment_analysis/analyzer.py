import logging
import json
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

from sentiment_analysis.sentiment_analyzer import SentimentAnalyzer
from sentiment_analysis.preprocessor import TextPreprocessor
from config.config import Config

logger = logging.getLogger(__name__)


class SentimentAnalysisEngine:
    """Runs sentiment analysis on collected data"""

    def __init__(self):
        self.config = Config()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.preprocessor = TextPreprocessor()

    def run(self, data_dir=None):
        """
        Run sentiment analysis on collected data

        Args:
            data_dir (str, optional): Path to data directory

        Returns:
            str: Path to sentiment analysis results directory
        """
        # Use data_dir if specified, otherwise use default pattern
        if data_dir is None:
            data_dir = Path("data") / "collection_YYYYMMDD_HHMMSS"
        else:
            data_dir = Path(data_dir)

        logger.info(f"Running sentiment analysis on data in {data_dir}")

        # Create results directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = Path("data") / f"sentiment_{timestamp}"
        results_dir.mkdir(parents=True, exist_ok=True)

        # Collect text data from various sources
        text_data = self._collect_text_data(data_dir)

        if not text_data:
            logger.error("No text data found to analyze")
            return None

        # Analyze sentiment for text data
        logger.info(f"Analyzing sentiment for {len(text_data)} text items")
        sentiment_results = self._analyze_sentiment(text_data)

        # Extract entities and their sentiment
        entity_sentiment = self._extract_entity_sentiment(text_data, sentiment_results)

        # Calculate general sentiment
        general_sentiment = self._calculate_general_sentiment(sentiment_results)

        # Calculate Fear & Greed Index
        fear_greed_index = self._calculate_fear_greed_index(entity_sentiment, general_sentiment)

        # Save results
        self._save_results(results_dir, entity_sentiment, general_sentiment, fear_greed_index)

        logger.info(f"Sentiment analysis complete. Results saved to {results_dir}")
        logger.info(
            f"Fear & Greed Index: {fear_greed_index['fear_greed_index']:.2f} - {fear_greed_index['market_sentiment']}")

        # Return the path to the results directory
        return str(results_dir)

    def _collect_text_data(self, data_dir):
        """
        Collect text data from various sources

        Args:
            data_dir (Path): Path to data directory

        Returns:
            list: Text data items with metadata
        """
        text_data = []

        # Collect tweets
        twitter_files = list(data_dir.glob("twitter_*.json"))
        for file_path in twitter_files:
            try:
                tweets_df = pd.read_json(file_path)
                for _, tweet in tweets_df.iterrows():
                    text_data.append({
                        "text": tweet.get("text", ""),
                        "source": "twitter",
                        "created_at": tweet.get("created_at", ""),
                        "author": tweet.get("user", "unknown"),
                        "metadata": {
                            "followers": tweet.get("followers_count", 0),
                            "retweets": tweet.get("retweet_count", 0),
                            "favorites": tweet.get("favorite_count", 0)
                        }
                    })
            except Exception as e:
                logger.error(f"Error processing Twitter data from {file_path}: {e}")

        # Collect Reddit posts
        reddit_files = list(data_dir.glob("reddit_*.json"))
        for file_path in reddit_files:
            try:
                with open(file_path, "r") as f:
                    reddit_posts = json.load(f)

                for post in reddit_posts:
                    # Combine title and text for more context
                    full_text = f"{post.get('title', '')} {post.get('text', '')}"
                    text_data.append({
                        "text": full_text,
                        "source": "reddit",
                        "created_at": post.get("created_at", ""),
                        "author": post.get("author", "unknown"),
                        "subreddit": post.get("subreddit", ""),
                        "metadata": {
                            "score": post.get("score", 0),
                            "comments": post.get("num_comments", 0),
                            "awards": post.get("total_awards", 0)
                        }
                    })
            except Exception as e:
                logger.error(f"Error processing Reddit data from {file_path}: {e}")

        # Collect news articles
        news_files = list(data_dir.glob("news_*.json"))
        for file_path in news_files:
            try:
                with open(file_path, "r") as f:
                    news_articles = json.load(f)

                for article in news_articles:
                    # Combine title and description for more context
                    full_text = f"{article.get('title', '')} {article.get('description', '')}"
                    text_data.append({
                        "text": full_text,
                        "source": "news",
                        "created_at": article.get("published_at", ""),
                        "author": article.get("source", "unknown"),
                        "metadata": {
                            "url": article.get("url", ""),
                            "search_term": article.get("search_term", "")
                        }
                    })
            except Exception as e:
                logger.error(f"Error processing News data from {file_path}: {e}")

        return text_data

    def _analyze_sentiment(self, text_data):
        """
        Analyze sentiment for text data

        Args:
            text_data (list): Text data items

        Returns:
            list: Sentiment results
        """
        sentiment_results = []

        for item in text_data:
            try:
                # Preprocess text
                text = item.get("text", "")
                clean_text = self.preprocessor.preprocess(text)

                # Skip if text is too short after preprocessing
                if len(clean_text.split()) < 3:
                    continue

                # Analyze sentiment
                sentiment = self.sentiment_analyzer.analyze(clean_text)

                # Add to results
                result = {
                    "text": text,
                    "clean_text": clean_text,
                    "source": item.get("source", "unknown"),
                    "created_at": item.get("created_at", ""),
                    "author": item.get("author", "unknown"),
                    "sentiment": sentiment
                }

                # Add additional metadata if available
                for key, value in item.items():
                    if key not in result and key != "text":
                        result[key] = value

                sentiment_results.append(result)

            except Exception as e:
                logger.error(f"Error analyzing sentiment for text: {e}")
                continue

        return sentiment_results

    def _extract_entity_sentiment(self, text_data, sentiment_results):
        """
        Extract entities and their sentiment

        Args:
            text_data (list): Text data items
            sentiment_results (list): Sentiment results

        Returns:
            dict: Entity sentiment data
        """
        # Define entities to track
        cryptos = self.config.get("targets.cryptocurrencies", ["BTC", "ETH", "XRP", "ADA", "SOL"])
        stocks = self.config.get("targets.stocks", ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"])
        indices = self.config.get("targets.indices", ["SPY", "QQQ", "DIA"])

        # Extract entity mentions from Twitter entities
        twitter_entity_files = list(Path("data").glob("collection_*/twitter_entities_*.json"))
        twitter_entities = {}

        for file_path in twitter_entity_files:
            try:
                with open(file_path, "r") as f:
                    entities = json.load(f)

                # Merge entities
                for category, items in entities.items():
                    if category not in twitter_entities:
                        twitter_entities[category] = {}

                    for symbol, count in items.items():
                        if symbol not in twitter_entities[category]:
                            twitter_entities[category][symbol] = count
                        else:
                            twitter_entities[category][symbol] += count
            except Exception as e:
                logger.error(f"Error processing Twitter entities from {file_path}: {e}")

        # Initialize entity sentiment
        entity_sentiment = {
            "cryptos": {},
            "stocks": {},
            "indices": {}
        }

        # Extract entities from text data
        for crypto in cryptos:
            entity_sentiment["cryptos"][crypto] = self._get_entity_sentiment(crypto, sentiment_results)

        for stock in stocks:
            entity_sentiment["stocks"][stock] = self._get_entity_sentiment(stock, sentiment_results)

        for index in indices:
            entity_sentiment["indices"][index] = self._get_entity_sentiment(index, sentiment_results)

        # Add Twitter entity counts
        if twitter_entities:
            for category, items in twitter_entities.items():
                if category == "cryptos":
                    for symbol, count in items.items():
                        if symbol in entity_sentiment["cryptos"]:
                            entity_sentiment["cryptos"][symbol]["mentions"] += count

                elif category == "stocks":
                    for symbol, count in items.items():
                        if symbol in entity_sentiment["stocks"]:
                            entity_sentiment["stocks"][symbol]["mentions"] += count

                elif category == "indices":
                    for symbol, count in items.items():
                        if symbol in entity_sentiment["indices"]:
                            entity_sentiment["indices"][symbol]["mentions"] += count

        return entity_sentiment

    def _get_entity_sentiment(self, entity, sentiment_results):
        """
        Get sentiment for a specific entity

        Args:
            entity (str): Entity symbol
            sentiment_results (list): Sentiment results

        Returns:
            dict: Entity sentiment data
        """
        # Initialize counters
        total_pos = 0.0
        total_neg = 0.0
        total_neu = 0.0
        count = 0
        pos_count = 0
        neg_count = 0
        neu_count = 0
        sources = {}

        # Check for entity mentions in text
        for result in sentiment_results:
            text = result.get("text", "").lower()

            # Simple check for entity mention (could be improved with NLP)
            if entity.lower() in text:
                sentiment = result.get("sentiment", {})
                pos = sentiment.get("pos", 0.0)
                neg = sentiment.get("neg", 0.0)
                neu = sentiment.get("neu", 0.0)
                compound = sentiment.get("compound", 0.0)

                # Add to totals
                total_pos += pos
                total_neg += neg
                total_neu += neu
                count += 1

                # Count by sentiment type
                if compound > 0.05:
                    pos_count += 1
                elif compound < -0.05:
                    neg_count += 1
                else:
                    neu_count += 1

                # Track sources
                source = result.get("source", "unknown")
                if source not in sources:
                    sources[source] = 0
                sources[source] += 1

        # Calculate averages
        if count > 0:
            avg_pos = total_pos / count
            avg_neg = total_neg / count
            avg_neu = total_neu / count

            # Calculate compound sentiment
            compound = avg_pos - avg_neg

            # Determine sentiment label
            if compound > 0.05:
                sentiment_label = "positive"
            elif compound < -0.05:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"

            # Calculate confidence based on number of mentions
            confidence = min(0.9, (count / 30) * 0.5 + 0.4)

            return {
                "compound": compound,
                "positive": avg_pos,
                "negative": avg_neg,
                "neutral": avg_neu,
                "sentiment_label": sentiment_label,
                "mentions": count,
                "positive_count": pos_count,
                "neutral_count": neu_count,
                "negative_count": neg_count,
                "sources": sources,
                "confidence": confidence
            }
        else:
            # No mentions found
            return {
                "compound": 0.0,
                "positive": 0.0,
                "negative": 0.0,
                "neutral": 0.0,
                "sentiment_label": "neutral",
                "mentions": 0,
                "positive_count": 0,
                "neutral_count": 0,
                "negative_count": 0,
                "sources": {},
                "confidence": 0.0
            }

    def _calculate_general_sentiment(self, sentiment_results):
        """
        Calculate general market sentiment

        Args:
            sentiment_results (list): Sentiment results

        Returns:
            dict: General sentiment metrics
        """
        # Count sentiment categories
        positive_count = 0
        neutral_count = 0
        negative_count = 0
        total_sentiment = 0.0

        for result in sentiment_results:
            sentiment = result.get("sentiment", {})
            compound = sentiment.get("compound", 0.0)

            # Add to total
            total_sentiment += compound

            # Count by category
            if compound > 0.05:
                positive_count += 1
            elif compound < -0.05:
                negative_count += 1
            else:
                neutral_count += 1

        # Calculate average sentiment
        total_count = len(sentiment_results)
        avg_sentiment = total_sentiment / total_count if total_count > 0 else 0.0

        return {
            "positive": positive_count,
            "neutral": neutral_count,
            "negative": negative_count,
            "total": total_count,
            "avg_sentiment": avg_sentiment
        }

    def _calculate_fear_greed_index(self, entity_sentiment, general_sentiment):
        """
        Calculate Fear & Greed Index

        Args:
            entity_sentiment (dict): Entity sentiment data
            general_sentiment (dict): General sentiment metrics

        Returns:
            dict: Fear & Greed Index data
        """
        # Extract metrics for calculation
        avg_sentiment = general_sentiment.get("avg_sentiment", 0.0)
        positive_count = general_sentiment.get("positive", 0)
        negative_count = general_sentiment.get("negative", 0)
        neutral_count = general_sentiment.get("neutral", 0)
        total_count = general_sentiment.get("total", 0)

        # Calculate sentiment ratios
        if total_count == 0:
            return {"timestamp": datetime.now().isoformat(), "fear_greed_index": 50, "market_sentiment": "Neutral", 
                    "base_sentiment": 0, "general_positive": 0, "general_neutral": 0, "general_negative": 0, "total_mentions": 0}
        
        # Calculate percentages
        positive_pct = (positive_count / total_count) * 100
        negative_pct = (negative_count / total_count) * 100
        neutral_pct = (neutral_count / total_count) * 100
        
        # Enhanced sentiment analysis with market context
        # 1. Base sentiment component (30% weight) - from VADER scores
        base_sentiment_score = ((avg_sentiment + 1) / 2) * 100  # Convert [-1,1] to [0,100]
        sentiment_component = base_sentiment_score * 0.3
        
        # 2. Sentiment distribution component (35% weight)
        # Consider the ratio and intensity of sentiment
        if negative_count > 0:
            pos_neg_ratio = positive_count / negative_count
            distribution_score = min(100, (pos_neg_ratio - 0.5) * 20 + 50)  # More sensitive scaling
        else:
            distribution_score = 85 if positive_count > 0 else 50
        distribution_component = distribution_score * 0.35
        
        # 3. Market engagement component (20% weight)
        # High engagement (more posts) can indicate volatility
        engagement_factor = min(1.0, total_count / 200)  # Normalize around 200 posts
        if engagement_factor > 0.8:
            # High engagement can indicate market stress
            engagement_adjustment = -5
        elif engagement_factor < 0.3:
            # Low engagement might indicate complacency
            engagement_adjustment = -3
        else:
            engagement_adjustment = 0
        engagement_component = (50 + engagement_adjustment) * 0.2
        
        # 4. Volatility indicator (15% weight) 
        # Based on sentiment distribution - extreme distributions indicate strong emotions
        sentiment_spread = max(positive_pct, negative_pct) - min(positive_pct, negative_pct)
        if sentiment_spread > 60:  # Very polarized sentiment
            volatility_score = 30 if negative_pct > positive_pct else 70
        else:
            volatility_score = 50  # Balanced sentiment
        volatility_component = volatility_score * 0.15
        
        # Add small market noise for natural variation (±2 points max)
        import random
        market_noise = random.uniform(-2, 2)
        
        # Calculate final index
        fear_greed_index = sentiment_component + distribution_component + engagement_component + volatility_component + market_noise
        
        # Ensure bounds
        fear_greed_index = min(100, max(0, fear_greed_index))

        # Determine market sentiment with more nuanced thresholds
        if fear_greed_index >= 85:
            market_sentiment = "Extreme Greed"
        elif fear_greed_index >= 70:
            market_sentiment = "Greed"
        elif fear_greed_index >= 55:
            market_sentiment = "Optimism"
        elif fear_greed_index >= 45:
            market_sentiment = "Neutral"
        elif fear_greed_index >= 30:
            market_sentiment = "Concern"
        elif fear_greed_index >= 15:
            market_sentiment = "Fear"
        else:
            market_sentiment = "Extreme Fear"

        return {
            "timestamp": datetime.now().isoformat(),
            "fear_greed_index": fear_greed_index,
            "market_sentiment": market_sentiment,
            "base_sentiment": avg_sentiment,
            "general_positive": positive_count,
            "general_neutral": neutral_count,
            "general_negative": negative_count,
            "total_mentions": total_count,
            "calculation_details": {
                "sentiment_component": round(sentiment_component, 2),
                "distribution_component": round(distribution_component, 2),
                "engagement_component": round(engagement_component, 2),
                "volatility_component": round(volatility_component, 2),
                "market_noise": round(market_noise, 2),
                "positive_pct": round(positive_pct, 1),
                "negative_pct": round(negative_pct, 1),
                "neutral_pct": round(neutral_pct, 1)
            }
        }

    def _save_results(self, results_dir, entity_sentiment, general_sentiment, fear_greed_index):
        """
        Save sentiment analysis results

        Args:
            results_dir (Path): Results directory path
            entity_sentiment (dict): Entity sentiment data
            general_sentiment (dict): General sentiment metrics
            fear_greed_index (dict): Fear & Greed Index data
        """
        # Save entity sentiment
        entity_sentiment_path = results_dir / "entity_sentiment.json"
        with open(entity_sentiment_path, "w") as f:
            json.dump(entity_sentiment, f, indent=2)

        # Save general sentiment
        general_sentiment_path = results_dir / "general_sentiment.json"
        with open(general_sentiment_path, "w") as f:
            json.dump(general_sentiment, f, indent=2)

        # Save Fear & Greed Index
        fear_greed_path = results_dir / "fear_greed_index.json"
        with open(fear_greed_path, "w") as f:
            json.dump(fear_greed_index, f, indent=2)