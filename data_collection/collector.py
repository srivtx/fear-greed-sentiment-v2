import logging
import json
from pathlib import Path
from datetime import datetime
import pandas as pd

from data_collection.twitter.twitter_collector import TwitterCollector
from data_collection.reddit.reddit_collector import RedditCollector
from data_collection.news.news_collector import NewsCollector
from data_collection.financial.market_data_collector import MarketDataCollector

logger = logging.getLogger(__name__)


class DataCollector:
    """Collects data from various sources"""

    def __init__(self):
        self.twitter_collector = TwitterCollector()
        self.reddit_collector = RedditCollector()
        self.news_collector = NewsCollector()
        self.market_collector = MarketDataCollector()

    def run_collection_cycle(self, skip_twitter=False):
        """
        Run a full data collection cycle

        Args:
            skip_twitter (bool): Whether to skip Twitter collection

        Returns:
            Path: Path to collection directory
        """
        logger.info("Starting data collection cycle")

        # Create collection directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        collection_dir = Path("data") / f"collection_{timestamp}"
        collection_dir.mkdir(parents=True, exist_ok=True)

        # Collect Twitter data (if not skipped)
        if not skip_twitter:
            try:
                logger.info("Collecting Twitter data")
                twitter_file = self._collect_twitter_data(collection_dir)
                if twitter_file:
                    logger.info(f"Twitter data collection succeeded: {twitter_file}")
                else:
                    logger.warning("Twitter data collection produced no results, continuing with other sources")
            except Exception as e:
                logger.error(f"Twitter data collection failed: {e}")
                logger.info("Continuing with other data sources")
        else:
            logger.info("Twitter data collection skipped")

        # Collect Reddit data
        try:
            logger.info("Collecting Reddit data")
            reddit_file = self._collect_reddit_data(collection_dir)
            if reddit_file:
                logger.info(f"Reddit data collection succeeded: {reddit_file}")
        except Exception as e:
            logger.error(f"Reddit data collection failed: {e}")

        # Collect news data
        try:
            logger.info("Collecting News data")
            news_file = self._collect_news_data(collection_dir)
            if news_file:
                logger.info(f"News data collection succeeded: {news_file}")
        except Exception as e:
            logger.error(f"News data collection failed: {e}")

        # Collect market data
        try:
            logger.info("Collecting Market data")
            market_file = self._collect_market_data(collection_dir)
            if market_file:
                logger.info(f"Market data collection succeeded: {market_file}")
        except Exception as e:
            logger.error(f"Market data collection failed: {e}")

        # Collect historical market data once a week
        try:
            logger.info("Collecting historical market data")
            hist_file = self._collect_historical_market_data(collection_dir)
            if hist_file:
                logger.info(f"Historical market data collection succeeded: {hist_file}")
        except Exception as e:
            logger.error(f"Historical market data collection failed: {e}")

        return collection_dir

    def _collect_twitter_data(self, collection_dir):
        """Collect Twitter data"""
        tweets_df = self.twitter_collector.collect_tweets(max_tweets_per_query=30)

        if not tweets_df.empty:
            # Extract entities from tweets
            entities = self.twitter_collector.extract_entities_from_tweets(tweets_df)

            # Save data
            twitter_file = collection_dir / f"twitter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            tweets_df.to_json(twitter_file, orient="records")

            # Save entities
            entities_file = collection_dir / f"twitter_entities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(entities_file, "w") as f:
                json.dump(entities, f)

            logger.info(f"Saved {len(tweets_df)} tweets to {twitter_file}")
            return twitter_file
        else:
            logger.warning("No tweets collected")
            return None

    def _collect_reddit_data(self, collection_dir):
        """Collect Reddit data"""
        reddit_posts = self.reddit_collector.collect_posts()

        if reddit_posts:
            # Save data
            reddit_file = collection_dir / f"reddit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(reddit_file, "w") as f:
                json.dump(reddit_posts, f)

            logger.info(f"Saved {len(reddit_posts)} Reddit posts to {reddit_file}")
            return reddit_file
        else:
            logger.warning("No Reddit posts collected")
            return None

    def _collect_news_data(self, collection_dir):
        """Collect news data"""
        news_articles = self.news_collector.collect_news()

        if news_articles:
            # Save data
            news_file = collection_dir / f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(news_file, "w") as f:
                json.dump(news_articles, f)

            logger.info(f"Saved {len(news_articles)} news articles to {news_file}")
            return news_file
        else:
            logger.warning("No news articles collected")
            return None

    def _collect_market_data(self, collection_dir):
        """Collect current market data"""
        market_data = self.market_collector.collect_current_data()

        if market_data:
            # Combine data frames
            combined_data = []
            for symbol, df in market_data.items():
                if not df.empty:
                    records = df.to_dict('records')
                    combined_data.extend(records)

            # Save to CSV
            market_file = collection_dir / f"market_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            pd.DataFrame(combined_data).to_csv(market_file, index=False)

            logger.info(f"Saved market data for {len(market_data)} symbols")
            return market_file
        else:
            logger.warning("No market data collected")
            return None

    def _collect_historical_market_data(self, collection_dir):
        """Collect historical market data"""
        historical_data = self.market_collector.collect_historical_data(period="1y")

        if historical_data:
            # Combine data frames
            combined_data = []
            for symbol, df in historical_data.items():
                if not df.empty:
                    records = df.to_dict('records')
                    combined_data.extend(records)

            # Save to CSV
            hist_file = collection_dir / f"market_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            pd.DataFrame(combined_data).to_csv(hist_file, index=False)

            logger.info(f"Saved historical data for {len(historical_data)} symbols")
            return hist_file
        else:
            logger.warning("No historical market data collected")
            return None