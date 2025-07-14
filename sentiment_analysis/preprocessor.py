import re
import nltk
import logging
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

logger = logging.getLogger(__name__)


class TextPreprocessor:
    """Preprocesses text for sentiment analysis"""

    def __init__(self):
        # Download required NLTK resources
        logger.info("Downloading required NLTK resources...")
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')

        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

        # Add financial stop words (words that don't carry sentiment)
        self.financial_stop_words = {
            'stock', 'stocks', 'market', 'markets', 'trading', 'trade', 'traded',
            'invest', 'investment', 'investing', 'investor', 'investors',
            'share', 'shares', 'shareholder', 'shareholders',
            'price', 'prices', 'pricing',
            'crypto', 'cryptocurrency', 'cryptocurrencies', 'token', 'tokens',
            'coin', 'coins', 'blockchain', 'mining', 'mined',
            'exchange', 'exchanges', 'wallet', 'wallets',
            'buy', 'bought', 'sell', 'sold', 'selling', 'buying',
            'dollar', 'dollars', 'cent', 'cents'
        }

        self.stop_words.update(self.financial_stop_words)

    def preprocess(self, text):
        """
        Preprocess text for sentiment analysis

        Args:
            text (str): Raw text

        Returns:
            str: Preprocessed text
        """
        if not text or not isinstance(text, str):
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)

        # Remove mentions and hashtags
        text = re.sub(r'@\w+|\#\w+', '', text)

        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)

        # Tokenize
        tokens = word_tokenize(text)

        # Remove stop words and lemmatize
        cleaned_tokens = [self.lemmatizer.lemmatize(token) for token in tokens if
                          token not in self.stop_words and len(token) > 2]

        # Rejoin tokens
        cleaned_text = ' '.join(cleaned_tokens)

        return cleaned_text

    def clean_for_entity_extraction(self, text):
        """
        Clean text for entity extraction (less aggressive than for sentiment)

        Args:
            text (str): Raw text

        Returns:
            str: Cleaned text
        """
        if not text or not isinstance(text, str):
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)

        # Remove special characters (keep $ for stock/crypto symbols)
        text = re.sub(r'[^a-zA-Z0-9\s\$]', '', text)

        return text