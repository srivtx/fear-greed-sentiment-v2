import requests
import logging
import json
import time
from datetime import datetime, timedelta
import random

from config.config import Config

logger = logging.getLogger(__name__)


class NewsCollector:
    """Collects news articles from financial news sources"""

    def __init__(self):
        self.config = Config()
        self._setup_api()
        self.search_terms = self._get_search_terms()
        self.sources = ["bloomberg", "financial-times", "business-insider", "cnbc", "wall-street-journal",
                        "the-economist", "reuters", "fortune"]

    def _setup_api(self):
        """Set up News API connection"""
        try:
            news_config = self.config.get("news", {})
            self.api_key = news_config.get("api_key")

            if self.api_key:
                self.api_ready = True
                logger.info("News API connection successful")
            else:
                logger.warning("No News API key provided in config")
                self.api_ready = False

        except Exception as e:
            logger.error(f"Failed to set up News API: {e}")
            self.api_ready = False

    def _get_search_terms(self):
        """Get search terms for news queries"""
        search_terms = []

        # Add crypto-specific terms
        cryptos = self.config.get("targets.cryptocurrencies", ["BTC", "ETH"])
        for crypto in cryptos:
            if crypto == "BTC":
                search_terms.append("bitcoin OR btc")
            elif crypto == "ETH":
                search_terms.append("ethereum OR eth")
            else:
                search_terms.append(crypto)

        # Add stock-specific terms
        stocks = self.config.get("targets.stocks", ["AAPL", "MSFT"])
        for stock in stocks:
            search_terms.append(stock)

        # Add general financial terms
        general_terms = [
            "market sentiment",
            "crypto market",
            "stock market",
            "financial markets",
            "bull market",
            "bear market",
            "market volatility"
        ]

        search_terms.extend(general_terms)
        return search_terms

    def collect_news(self):
        """
        Collect news articles related to financial markets

        Returns:
            list: Collected news articles
        """
        if not self.api_ready:
            logger.warning("News API not ready, returning sample data")
            return self._generate_sample_news()

        all_articles = []

        # Use News API to collect articles
        for term in self.search_terms:
            try:
                # Build API request
                url = "https://newsapi.org/v2/everything"
                params = {
                    "q": term,
                    "language": "en",
                    "sortBy": "publishedAt",
                    "pageSize": 10,
                    "from": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
                    "apiKey": self.api_key
                }

                # Optional: Add sources parameter if available
                if self.sources:
                    params["sources"] = ",".join(self.sources)

                # Make API request
                response = requests.get(url, params=params)

                if response.status_code == 200:
                    data = response.json()

                    if data.get("status") == "ok" and data.get("totalResults", 0) > 0:
                        articles = data.get("articles", [])

                        for article in articles:
                            # Format article data
                            article_data = {
                                "title": article.get("title", ""),
                                "description": article.get("description", ""),
                                "url": article.get("url", ""),
                                "source": article.get("source", {}).get("name", ""),
                                "published_at": article.get("publishedAt", ""),
                                "search_term": term,
                                "collected_at": datetime.now().isoformat()
                            }

                            # Only add if not already in the collection (avoid duplicates)
                            if not any(a.get("url") == article_data["url"] for a in all_articles):
                                all_articles.append(article_data)

                        logger.debug(f"Found {len(articles)} articles for term: {term}")
                    else:
                        logger.debug(f"No articles found for term: {term}")

                else:
                    logger.warning(f"News API returned status code {response.status_code} for term: {term}")

                # Sleep to avoid rate limits
                time.sleep(0.5)

            except Exception as e:
                logger.error(f"Error collecting news for term '{term}': {e}")
                continue

        logger.info(f"Total news articles collected: {len(all_articles)}")

        # If no articles collected, return sample data
        if not all_articles:
            logger.warning("No news articles collected, returning sample data")
            return self._generate_sample_news()

        return all_articles

    def _generate_sample_news(self):
        """Generate sample news data when API is unavailable"""
        sample_articles = [
            {
                "title": "Bitcoin Price Surges Past $50,000 as Institutional Adoption Grows",
                "description": "Bitcoin has surged past $50,000 as institutional adoption continues to grow, with major companies adding the cryptocurrency to their balance sheets.",
                "url": "https://example.com/bitcoin-price-surge",
                "source": "Sample Financial News",
                "published_at": datetime.now().isoformat(),
                "search_term": "bitcoin",
                "collected_at": datetime.now().isoformat()
            },
            {
                "title": "Stock Market Reaches New Highs Amid Economic Recovery",
                "description": "Major indices have reached new all-time highs as economic data signals strong recovery from the pandemic.",
                "url": "https://example.com/stock-market-highs",
                "source": "Sample Business News",
                "published_at": (datetime.now() - timedelta(hours=5)).isoformat(),
                "search_term": "stock market",
                "collected_at": datetime.now().isoformat()
            },
            {
                "title": "Ethereum 2.0 Launch Date Announced, ETH Price Reacts",
                "description": "Developers have announced the launch date for Ethereum 2.0, causing a significant price movement for ETH.",
                "url": "https://example.com/ethereum-2-launch",
                "source": "Sample Crypto News",
                "published_at": (datetime.now() - timedelta(hours=12)).isoformat(),
                "search_term": "ethereum",
                "collected_at": datetime.now().isoformat()
            },
            {
                "title": "Apple Reports Record Quarterly Revenue, Beats Expectations",
                "description": "Apple Inc. has reported record quarterly revenue, beating analyst expectations with strong iPhone and services sales.",
                "url": "https://example.com/apple-record-revenue",
                "source": "Sample Tech News",
                "published_at": (datetime.now() - timedelta(days=1)).isoformat(),
                "search_term": "AAPL",
                "collected_at": datetime.now().isoformat()
            },
            {
                "title": "Market Sentiment Turns Bullish as Economic Indicators Improve",
                "description": "Market sentiment has turned bullish as key economic indicators show improvement, with investors showing increased risk appetite.",
                "url": "https://example.com/market-sentiment-bullish",
                "source": "Sample Market Analysis",
                "published_at": (datetime.now() - timedelta(hours=18)).isoformat(),
                "search_term": "market sentiment",
                "collected_at": datetime.now().isoformat()
            }
        ]

        # Add some randomness to the sample data
        for article in sample_articles:
            # Add random sentiment indicators to titles
            sentiments = ["bullish", "bearish", "positive", "negative", "neutral", "optimistic", "pessimistic"]
            if random.random() > 0.7:
                article["title"] += f" - Analysts {random.choice(sentiments).title()}"

        return sample_articles