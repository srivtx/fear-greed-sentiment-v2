import os
from pathlib import Path
from typing import Dict, Any
import json
import logging

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for the Fear & Greed Engine"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize configuration from environment variables or config file"""
        self.config_path = Path(__file__).parent / "config.json"
        self.config: Dict[str, Any] = {}

        # Load from config file if it exists
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                self.config = json.load(f)

        # Override with environment variables (for security and CI/CD)
        self._load_api_keys_from_env()

        # Set default values if needed
        self._set_defaults()

    def _load_api_keys_from_env(self):
        """Load API keys from environment variables"""
        # Twitter API - Bearer Token
        if os.environ.get("TWITTER_BEARER_TOKEN"):
            self.config.setdefault("twitter", {})
            self.config["twitter"]["bearer_token"] = os.environ.get("TWITTER_BEARER_TOKEN")

        # Twitter API - OAuth (legacy)
        if os.environ.get("TWITTER_API_KEY"):
            self.config.setdefault("twitter", {})
            self.config["twitter"]["api_key"] = os.environ.get("TWITTER_API_KEY")
            self.config["twitter"]["api_secret"] = os.environ.get("TWITTER_API_SECRET")
            self.config["twitter"]["access_token"] = os.environ.get("TWITTER_ACCESS_TOKEN")
            self.config["twitter"]["access_token_secret"] = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

        # Reddit API
        if os.environ.get("REDDIT_CLIENT_ID"):
            self.config.setdefault("reddit", {})
            self.config["reddit"]["client_id"] = os.environ.get("REDDIT_CLIENT_ID")
            self.config["reddit"]["client_secret"] = os.environ.get("REDDIT_CLIENT_SECRET")
            self.config["reddit"]["user_agent"] = os.environ.get("REDDIT_USER_AGENT", "fear_greed_engine v0.1.0")

            # Reddit username/password if provided
            if os.environ.get("REDDIT_USERNAME"):
                self.config["reddit"]["username"] = os.environ.get("REDDIT_USERNAME")
                self.config["reddit"]["password"] = os.environ.get("REDDIT_PASSWORD")

        # News API
        if os.environ.get("NEWS_API_KEY"):
            self.config.setdefault("news", {})
            self.config["news"]["api_key"] = os.environ.get("NEWS_API_KEY")

    def _set_defaults(self):
        """Set default configurations"""
        # Handle both traditional structure and new structure

        # If user provided coins in root, copy to targets.cryptocurrencies
        if "coins" in self.config and not self.config.get("targets", {}).get("cryptocurrencies"):
            self.config.setdefault("targets", {})
            self.config["targets"]["cryptocurrencies"] = self.config["coins"]

        # Sentiment defaults
        self.config.setdefault("sentiment", {})
        self.config["sentiment"].setdefault("model", "vader")

        # Data storage defaults
        self.config.setdefault("data_storage", {})
        self.config["data_storage"].setdefault("path", "data")

        # Targets defaults
        self.config.setdefault("targets", {})
        self.config["targets"].setdefault("cryptocurrencies", ["BTC", "ETH", "XRP", "ADA", "SOL"])
        self.config["targets"].setdefault("stocks", ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"])
        self.config["targets"].setdefault("indices", ["SPY", "QQQ", "DIA"])

    def get(self, key, default=None):
        """Get a configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key, value):
        """Set a configuration value"""
        keys = key.split('.')
        config = self.config
        for i, k in enumerate(keys[:-1]):
            config.setdefault(k, {})
            config = config[k]
        config[keys[-1]] = value

    def save(self):
        """Save configuration to file"""
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)