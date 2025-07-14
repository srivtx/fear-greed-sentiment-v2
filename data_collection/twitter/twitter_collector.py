import tweepy
import pandas as pd
import logging
import time
from datetime import datetime, timedelta
import re

from config.config import Config

logger = logging.getLogger(__name__)


class TwitterCollector:
    """Collects tweets related to financial markets using Twitter API v2"""

    def __init__(self):
        self.config = Config()
        self._setup_api()
        self.search_queries = self._build_search_queries()

    def _setup_api(self):
        """Set up Twitter API connection using Bearer Token"""
        try:
            twitter_config = self.config.get("twitter", {})
            bearer_token = twitter_config.get("bearer_token")

            if bearer_token:
                self.client = tweepy.Client(
                    bearer_token=bearer_token,
                    wait_on_rate_limit=False  # Don't auto-wait on rate limits
                )
                logger.info("Twitter API connected using Bearer Token")
                self.api_ready = True
            else:
                logger.error("No Twitter Bearer Token provided in config")
                self.client = None
                self.api_ready = False

        except Exception as e:
            logger.error(f"Failed to connect to Twitter API: {e}")
            self.client = None
            self.api_ready = False

    def _build_search_queries(self):
        """Build search queries that work with Twitter API v2 free tier"""
        queries = []

        # Get crypto targets
        cryptos = self.config.get("targets.cryptocurrencies", [])
        if not cryptos:
            # If not in targets, check for coins in root config
            coins = self.config.get("coins", ["bitcoin", "ethereum"])
            # Ensure we have both ticker symbols and names
            cryptos = []
            coin_to_symbol = {
                "bitcoin": "BTC",
                "ethereum": "ETH",
                "cardano": "ADA",
                "solana": "SOL",
                "ripple": "XRP",
                "binance": "BNB",
                "dogecoin": "DOGE"
            }

            for coin in coins:
                cryptos.append(coin_to_symbol.get(coin.lower(), coin.upper()))

        # Create crypto-specific search queries
        for crypto in cryptos:
            # For Bitcoin
            if crypto.upper() == "BTC":
                queries.append("bitcoin OR btc crypto")

            # For Ethereum
            elif crypto.upper() == "ETH":
                queries.append("ethereum OR eth crypto")

            # For other cryptos
            else:
                # Try to get the name from the symbol
                symbol_to_name = {
                    "ADA": "cardano",
                    "SOL": "solana",
                    "XRP": "ripple OR xrp",
                    "BNB": "binance",
                    "DOGE": "dogecoin"
                }

                if crypto.upper() in symbol_to_name:
                    name = symbol_to_name[crypto.upper()]
                    queries.append(f"{name} crypto")
                else:
                    queries.append(f"{crypto} crypto")

        # Add general crypto queries
        queries.append("cryptocurrency OR crypto market")
        queries.append("crypto trading OR crypto investing")

        # Add stock market queries
        queries.append("stock market OR investing")
        queries.append("bull market OR bear market")
        queries.append("market sentiment")

        # Add financial terms
        queries.append("financial markets OR trading")

        return queries

    def collect_tweets(self, max_tweets_per_query=30):
        """
        Collect tweets related to financial markets

        Args:
            max_tweets_per_query (int): Maximum tweets to collect per query

        Returns:
            pd.DataFrame: Collected tweets with metadata
        """
        if not self.api_ready:
            logger.error("Twitter API not ready. Check your Bearer Token.")
            return pd.DataFrame()

        all_tweets = []

        # Collect tweets using API v2 search
        for query in self.search_queries:
            try:
                logger.debug(f"Searching for tweets with query: {query}")

                # Use Twitter API v2 with Bearer Token
                response = self.client.search_recent_tweets(
                    query=query,
                    max_results=min(max_tweets_per_query, 100),  # API v2 limits to 100
                    tweet_fields=["created_at", "public_metrics", "author_id", "text"],
                    user_fields=["username", "public_metrics", "description"],
                    expansions=["author_id"]
                )

                if response and hasattr(response, 'data') and response.data:
                    # Create a user lookup dictionary
                    users = {user.id: user for user in
                             response.includes["users"]} if "users" in response.includes else {}

                    for tweet in response.data:
                        # Get user info
                        user = users.get(tweet.author_id, None)
                        followers_count = user.public_metrics["followers_count"] if user and hasattr(user,
                                                                                                     'public_metrics') else 0

                        # Extract tweet data
                        tweet_data = {
                            "id": tweet.id,
                            "text": tweet.text,
                            "created_at": tweet.created_at.isoformat() if tweet.created_at else datetime.now().isoformat(),
                            "user": user.username if user else "unknown",
                            "followers_count": followers_count,
                            "retweet_count": tweet.public_metrics["retweet_count"] if hasattr(tweet,
                                                                                              'public_metrics') else 0,
                            "favorite_count": tweet.public_metrics["like_count"] if hasattr(tweet,
                                                                                            'public_metrics') else 0,
                            "source": "twitter",
                            "search_query": query,
                            "collected_at": datetime.now().isoformat()
                        }

                        # Only add if tweet not already in the collection
                        if not any(t.get('id') == tweet.id for t in all_tweets):
                            all_tweets.append(tweet_data)

                    logger.debug(f"Found {len(response.data)} tweets for query: {query}")
                else:
                    logger.debug(f"No tweets found for query: {query}")

                # Small sleep between queries to be polite
                time.sleep(1)

            except tweepy.TooManyRequests as e:
                logger.warning(f"Twitter API rate limit reached. Skipping remaining queries.")
                # Don't wait - just return what we have so far
                break

            except Exception as e:
                logger.error(f"Error collecting tweets for query '{query}': {e}")
                # Continue with next query
                continue

        logger.info(f"Total tweets collected: {len(all_tweets)}")

        # Handle empty results
        if not all_tweets:
            return pd.DataFrame()

        return pd.DataFrame(all_tweets)

    def extract_entities_from_tweets(self, tweets_df):
        """
        Extract financial entities from tweets

        Args:
            tweets_df (pd.DataFrame): DataFrame of tweets

        Returns:
            dict: Extracted entities and their counts
        """
        entities = {
            "cryptos": {},
            "stocks": {},
            "indices": {}
        }

        if tweets_df.empty:
            return entities

        # Define entity patterns
        crypto_patterns = {
            "BTC": r'\b(bitcoin|btc|xbt)\b',
            "ETH": r'\b(ethereum|eth|ether)\b',
            "XRP": r'\b(ripple|xrp)\b',
            "ADA": r'\b(cardano|ada)\b',
            "SOL": r'\b(solana|sol)\b',
            "BNB": r'\b(binance|bnb)\b',
            "DOGE": r'\b(dogecoin|doge)\b'
        }

        stock_patterns = {
            "AAPL": r'\b(apple|aapl)\b',
            "MSFT": r'\b(microsoft|msft)\b',
            "GOOGL": r'\b(google|alphabet|googl)\b',
            "AMZN": r'\b(amazon|amzn)\b',
            "TSLA": r'\b(tesla|tsla)\b'
        }

        index_patterns = {
            "SPY": r'\b(s&p|spy|sp500|s&p 500)\b',
            "QQQ": r'\b(nasdaq|qqq)\b',
            "DIA": r'\b(dow|dow jones|djia)\b'
        }

        # Analyze each tweet
        for _, tweet in tweets_df.iterrows():
            text = tweet['text'].lower()

            # Check for cryptos
            for crypto, pattern in crypto_patterns.items():
                if re.search(pattern, text):
                    if crypto not in entities["cryptos"]:
                        entities["cryptos"][crypto] = 0
                    entities["cryptos"][crypto] += 1

            # Check for stocks
            for stock, pattern in stock_patterns.items():
                if re.search(pattern, text):
                    if stock not in entities["stocks"]:
                        entities["stocks"][stock] = 0
                    entities["stocks"][stock] += 1

            # Check for indices
            for index, pattern in index_patterns.items():
                if re.search(pattern, text):
                    if index not in entities["indices"]:
                        entities["indices"][index] = 0
                    entities["indices"][index] += 1

        return entities