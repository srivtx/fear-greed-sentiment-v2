import re
import logging
from typing import Dict, List, Set, Tuple
import pandas as pd
from pathlib import Path
import json

from config.config import Config

logger = logging.getLogger(__name__)


class EntityRecognizer:
    """Recognizes financial entities in text data"""

    def __init__(self):
        self.config = Config()
        self.data_path = Path(self.config.get("data_storage.path", "data"))

        # Load entity lists
        self.entities = {
            "cryptos": self.config.get("targets.cryptocurrencies", []),
            "stocks": self.config.get("targets.stocks", []),
            "indices": self.config.get("targets.indices", [])
        }

        # Add alternative names and symbols for entities
        self.entity_alternatives = self._build_entity_alternatives()

        # Compile regex patterns for faster matching
        self.patterns = self._compile_patterns()

    def _build_entity_alternatives(self):
        """Build a dictionary of alternative names for financial entities"""
        alternatives = {}

        # Add cryptocurrency alternatives
        crypto_alternatives = {
            "BTC": ["bitcoin", "btc", "xbt", "btcusd", "bitcoin core"],
            "ETH": ["ethereum", "eth", "ether", "ethusd"],
            "XRP": ["ripple", "xrp", "xrpusd"],
            "ADA": ["cardano", "ada", "adausd"],
            "SOL": ["solana", "sol", "solusd"],
            "BNB": ["binance", "bnb", "binance coin", "bnbusd"],
            "DOGE": ["dogecoin", "doge", "dogeusd"],
            "DOT": ["polkadot", "dot", "dotusd"],
            "AVAX": ["avalanche", "avax", "avaxusd"],
            "MATIC": ["polygon", "matic", "maticusd"]
        }

        # Add stock alternatives
        stock_alternatives = {
            "AAPL": ["apple", "aapl", "apple inc"],
            "MSFT": ["microsoft", "msft", "microsoft corp"],
            "GOOGL": ["google", "googl", "alphabet", "google inc"],
            "AMZN": ["amazon", "amzn", "amazon.com"],
            "TSLA": ["tesla", "tsla", "tesla motors", "tesla inc"],
            "FB": ["facebook", "fb", "meta", "meta platforms"],
            "NVDA": ["nvidia", "nvda", "nvidia corp"],
            "JPM": ["jpmorgan", "jpm", "jp morgan", "jpmorgan chase"],
            "V": ["visa", "v"],
            "JNJ": ["johnson", "jnj", "johnson & johnson"]
        }

        # Add index alternatives
        index_alternatives = {
            "SPY": ["s&p", "s&p 500", "spy", "spx", "sp500", "standard & poor"],
            "QQQ": ["nasdaq", "qqq", "nasdaq 100", "nasdaq composite"],
            "DIA": ["dow", "dia", "dow jones", "djia", "dow 30"],
            "IWM": ["russell", "iwm", "russell 2000"],
            "VIX": ["vix", "volatility index", "fear index"]
        }

        # Merge all alternatives
        alternatives["cryptos"] = crypto_alternatives
        alternatives["stocks"] = stock_alternatives
        alternatives["indices"] = index_alternatives

        return alternatives

    def _compile_patterns(self):
        """Compile regex patterns for entity recognition"""
        patterns = {
            "cashtag": re.compile(r'\$([a-zA-Z]{1,5})'),
            "hashtag": re.compile(r'#([a-zA-Z]{1,30})'),
            "crypto_names": {},
            "stock_names": {},
            "index_names": {}
        }

        # Compile patterns for alternative names
        for entity_type, alternatives_dict in self.entity_alternatives.items():
            patterns[f"{entity_type}_names"] = {}

            for entity, names in alternatives_dict.items():
                for name in names:
                    pattern = re.compile(r'\b' + re.escape(name) + r'\b', re.IGNORECASE)
                    patterns[f"{entity_type}_names"][name] = {"pattern": pattern, "entity": entity}

        return patterns

    def extract_entities(self, text):
        """
        Extract financial entities from text

        Args:
            text (str): Input text

        Returns:
            dict: Extracted entities by category
        """
        if not text or not isinstance(text, str):
            return {"cryptos": [], "stocks": [], "indices": []}

        text = text.lower()
        entities = {"cryptos": [], "stocks": [], "indices": []}

        # Extract cashtags ($BTC, $AAPL)
        cashtags = self.patterns["cashtag"].findall(text)
        for tag in cashtags:
            tag = tag.upper()
            if tag in self.entities["cryptos"]:
                entities["cryptos"].append(tag)
            elif tag in self.entities["stocks"]:
                entities["stocks"].append(tag)
            elif tag in self.entities["indices"]:
                entities["indices"].append(tag)

        # Extract entities from text using name patterns
        for entity_type in ["cryptos", "stocks", "indices"]:
            pattern_dict = self.patterns[f"{entity_type}_names"]

            for name, data in pattern_dict.items():
                if data["pattern"].search(text):
                    entity = data["entity"]
                    if entity not in entities[entity_type]:
                        entities[entity_type].append(entity)

        # Remove duplicates
        for entity_type in entities:
            entities[entity_type] = list(set(entities[entity_type]))

        return entities

    def analyze_entity_mentions(self, text_data):
        """
        Analyze entity mentions in a collection of text data

        Args:
            text_data (list): List of text data items

        Returns:
            dict: Entity mention statistics
        """
        entity_mentions = {
            "cryptos": {},
            "stocks": {},
            "indices": {}
        }

        # Initialize counters for all known entities
        for entity_type, entity_list in self.entities.items():
            for entity in entity_list:
                entity_mentions[entity_type][entity] = {
                    "mention_count": 0,
                    "sources": {},
                    "sentiment_scores": []
                }

        # Analyze text data
        for item in text_data:
            text = item.get("text", "")
            source = item.get("source", "unknown")
            sentiment_score = item.get("sentiment_score", 0)

            # Skip empty text
            if not text:
                continue

            # Extract entities
            entities = self.extract_entities(text)

            # Update entity mentions
            for entity_type, entity_list in entities.items():
                for entity in entity_list:
                    if entity not in entity_mentions[entity_type]:
                        entity_mentions[entity_type][entity] = {
                            "mention_count": 0,
                            "sources": {},
                            "sentiment_scores": []
                        }

                    entity_mentions[entity_type][entity]["mention_count"] += 1

                    # Track sources
                    if source not in entity_mentions[entity_type][entity]["sources"]:
                        entity_mentions[entity_type][entity]["sources"][source] = 0
                    entity_mentions[entity_type][entity]["sources"][source] += 1

                    # Track sentiment scores
                    entity_mentions[entity_type][entity]["sentiment_scores"].append(sentiment_score)

        # Calculate average sentiment scores
        for entity_type in entity_mentions:
            for entity, data in entity_mentions[entity_type].items():
                scores = data["sentiment_scores"]
                if scores:
                    data["avg_sentiment"] = sum(scores) / len(scores)
                    data["sentiment_variance"] = pd.Series(scores).var() if len(scores) > 1 else 0
                else:
                    data["avg_sentiment"] = 0
                    data["sentiment_variance"] = 0

        return entity_mentions