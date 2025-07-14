import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import logging

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Analyzes sentiment of text using VADER sentiment analyzer"""

    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        self._apply_financial_lexicon()
        logger.info("Financial lexicon loaded and applied to VADER")

    def _apply_financial_lexicon(self):
        """Apply financial-specific lexicon to improve VADER"""
        # Financial terms with positive sentiment
        financial_positives = {
            'bull': 2.0,
            'bullish': 2.5,
            'long': 0.5,
            'buy': 1.0,
            'bought': 1.0,
            'buying': 1.0,
            'moon': 2.0,
            'mooning': 2.5,
            'hodl': 1.5,
            'rally': 1.5,
            'rallying': 1.5,
            'surge': 2.0,
            'surging': 2.0,
            'gain': 1.0,
            'gains': 1.0,
            'profit': 1.5,
            'profitable': 1.5,
            'profited': 1.5,
            'breakout': 2.0,
            'outperform': 1.5,
            'outperformed': 1.5,
            'support': 0.5,
            'backed': 0.5,
            'upgrade': 1.0,
            'upgraded': 1.0,
            'green': 0.8,
            'recover': 1.0,
            'recovery': 1.0,
            'recovered': 1.0,
            'ath': 1.5  # All-Time High
        }

        # Financial terms with negative sentiment
        financial_negatives = {
            'bear': -2.0,
            'bearish': -2.5,
            'short': -0.5,
            'sell': -1.0,
            'selling': -1.0,
            'sold': -1.0,
            'dump': -2.0,
            'dumping': -2.5,
            'crash': -3.0,
            'crashing': -3.0,
            'dip': -1.0,
            'correction': -1.5,
            'loss': -1.0,
            'losses': -1.5,
            'lose': -1.0,
            'losing': -1.5,
            'lost': -1.5,
            'drop': -1.5,
            'dropping': -1.5,
            'fell': -1.5,
            'fallen': -1.5,
            'plunge': -2.0,
            'plunging': -2.0,
            'resistance': -0.5,
            'downgrade': -1.0,
            'downgraded': -1.0,
            'red': -0.8,
            'fud': -1.5,  # Fear, Uncertainty, Doubt
            'scam': -2.5,
            'bubble': -1.5,
            'atl': -1.5  # All-Time Low
        }

        # Update VADER lexicon
        self.vader.lexicon.update(financial_positives)
        self.vader.lexicon.update(financial_negatives)

    def analyze(self, text):
        """
        Analyze sentiment of text

        Args:
            text (str): Text to analyze

        Returns:
            dict: Sentiment scores
        """
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            return {
                'compound': 0.0,
                'pos': 0.0,
                'neg': 0.0,
                'neu': 1.0
            }

        try:
            # Get sentiment scores from VADER
            sentiment_scores = self.vader.polarity_scores(text)
            return sentiment_scores

        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                'compound': 0.0,
                'pos': 0.0,
                'neg': 0.0,
                'neu': 1.0
            }