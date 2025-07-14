import praw
import pandas as pd
import logging
import time
from datetime import datetime, timedelta
import re

from config.config import Config

logger = logging.getLogger(__name__)


class RedditCollector:
    """Collects Reddit posts and comments from financial subreddits"""

    def __init__(self):
        self.config = Config()
        self._setup_api()
        self.subreddits = self._get_subreddits()

    def _setup_api(self):
        """Set up Reddit API connection"""
        try:
            reddit_config = self.config.get("reddit", {})

            # Set up with password authentication if username and password are provided
            if "username" in reddit_config and "password" in reddit_config:
                self.reddit = praw.Reddit(
                    client_id=reddit_config.get("client_id"),
                    client_secret=reddit_config.get("client_secret"),
                    username=reddit_config.get("username"),
                    password=reddit_config.get("password"),
                    user_agent=reddit_config.get("user_agent", "fear_greed_engine v0.1.0")
                )
            else:
                # Set up with script-only authentication (no username/password)
                self.reddit = praw.Reddit(
                    client_id=reddit_config.get("client_id"),
                    client_secret=reddit_config.get("client_secret"),
                    user_agent=reddit_config.get("user_agent", "fear_greed_engine v0.1.0")
                )

            logger.info("Reddit API connection successful")
        except Exception as e:
            logger.error(f"Failed to connect to Reddit API: {e}")
            self.reddit = None

    def _get_subreddits(self):
        """Get list of subreddits to monitor"""
        # First check for subreddits in root config
        subreddits = self.config.get("subreddits")

        if not subreddits:
            # Fall back to reddit.subreddits config
            subreddits = self.config.get("reddit.subreddits")

        # Use defaults if still not found
        if not subreddits:
            subreddits = [
                "wallstreetbets", "investing", "stocks", "cryptocurrency",
                "Bitcoin", "finance", "CryptoMarkets", "StockMarket"
            ]

        return subreddits
    def collect_posts(self, limit=25, timeframe="day"):
        """
        Collect posts from financial subreddits

        Args:
            limit (int): Number of posts to collect per subreddit
            timeframe (str): Time filter ('hour', 'day', 'week', 'month', 'year', 'all')

        Returns:
            list: Collected posts with metadata
        """
        if not self.reddit:
            logger.error("Reddit API not connected")
            return []

        all_posts = []

        for subreddit_name in self.subreddits:
            try:
                logger.info(f"Collecting posts from r/{subreddit_name}")
                subreddit = self.reddit.subreddit(subreddit_name)

                # Get top posts
                top_posts = subreddit.top(time_filter=timeframe, limit=limit)
                for post in top_posts:
                    post_data = self._extract_post_data(post, subreddit_name)
                    all_posts.append(post_data)

                # Get hot posts
                hot_posts = subreddit.hot(limit=limit)
                for post in hot_posts:
                    # Skip duplicates
                    if any(p.get("id") == post.id for p in all_posts):
                        continue

                    post_data = self._extract_post_data(post, subreddit_name)
                    all_posts.append(post_data)

                # Get new posts
                new_posts = subreddit.new(limit=limit)
                for post in new_posts:
                    # Skip duplicates
                    if any(p.get("id") == post.id for p in all_posts):
                        continue

                    post_data = self._extract_post_data(post, subreddit_name)
                    all_posts.append(post_data)

                logger.info(f"Collected {len(all_posts)} posts from r/{subreddit_name}")

                # Sleep to avoid rate limiting
                time.sleep(1)

            except Exception as e:
                logger.error(f"Error collecting posts from r/{subreddit_name}: {e}")

        logger.info(f"Total Reddit posts collected: {len(all_posts)}")
        return all_posts

    def _extract_post_data(self, post, subreddit_name):
        """Extract relevant data from a Reddit post"""
        # Combine title and selftext for analysis
        text = f"{post.title} {post.selftext}"

        # Extract financial symbols ($AAPL, BTC, etc.)
        cashtags = re.findall(r'\$([a-zA-Z]{1,5})', text)
        symbols = [symbol.upper() for symbol in cashtags]

        # Extract creation time
        created_at = datetime.fromtimestamp(post.created_utc)

        return {
            "id": post.id,
            "text": text,
            "title": post.title,
            "selftext": post.selftext,
            "created_at": created_at.isoformat(),
            "subreddit": subreddit_name,
            "author": str(post.author),
            "upvotes": post.score,
            "upvote_ratio": post.upvote_ratio,
            "num_comments": post.num_comments,
            "url": post.url,
            "is_self": post.is_self,
            "extracted_symbols": symbols,
            "collected_at": datetime.now().isoformat()
        }