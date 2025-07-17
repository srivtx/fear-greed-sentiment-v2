#!/usr/bin/env python3
"""
Advanced Sentiment Analysis Engine for Financial Markets
Optimized for GoQuant requirements with enhanced NLP and financial focus
"""

import re
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, Counter
import logging
import time
import json

# NLP libraries
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.chunk import ne_chunk
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer

# Financial libraries
import yfinance as yf

class AdvancedFinancialSentimentAnalyzer:
    """
    Advanced sentiment analyzer specifically designed for financial markets
    Implements GoQuant requirements for accurate financial sentiment analysis
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize NLP components
        self.vader = SentimentIntensityAnalyzer()
        self.lemmatizer = WordNetLemmatizer()
        
        # Download required NLTK data
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))
        
        # Enhanced financial lexicon with contextual weights
        self.financial_lexicon = self._build_financial_lexicon()
        
        # Entity recognition patterns (crypto, stocks, indices)
        self.entity_patterns = self._build_entity_patterns()
        
        # Sarcasm and irony detection patterns
        self.sarcasm_patterns = self._build_sarcasm_patterns()
        
        # Market psychology indicators
        self.psychology_indicators = self._build_psychology_indicators()
        
        # Performance metrics
        self.analysis_times = []
        
        self.logger.info("AdvancedFinancialSentimentAnalyzer initialized")
    
    def _build_financial_lexicon(self) -> Dict[str, float]:
        """Build comprehensive financial sentiment lexicon"""
        return {
            # Extreme Fear (-0.8 to -1.0)
            'crash': -0.9, 'collapse': -0.9, 'plummet': -0.8, 'dump': -0.8,
            'panic': -0.9, 'disaster': -0.8, 'catastrophe': -0.9, 'bloodbath': -0.8,
            'capitulation': -0.8, 'liquidation': -0.7, 'selloff': -0.7,
            
            # High Fear (-0.5 to -0.7)
            'bear': -0.6, 'bearish': -0.6, 'decline': -0.5, 'fall': -0.5,
            'drop': -0.5, 'down': -0.4, 'negative': -0.4, 'loss': -0.5,
            'worried': -0.5, 'concern': -0.4, 'risk': -0.4, 'danger': -0.6,
            'uncertainty': -0.4, 'volatile': -0.3, 'unstable': -0.5,
            
            # Moderate Fear (-0.2 to -0.4)
            'correction': -0.3, 'pullback': -0.3, 'dip': -0.2, 'retreat': -0.3,
            'weakness': -0.3, 'softness': -0.2, 'caution': -0.2,
            
            # Extreme Greed (0.8 to 1.0)
            'moon': 0.9, 'rocket': 0.9, 'explode': 0.8, 'parabolic': 0.8,
            'euphoria': 0.9, 'frenzy': 0.8, 'bubble': 0.7, 'mania': 0.8,
            'diamond': 0.8, 'hodl': 0.7, 'lambo': 0.8,
            
            # High Greed (0.5 to 0.7)
            'bull': 0.6, 'bullish': 0.6, 'pump': 0.6, 'surge': 0.6,
            'rally': 0.6, 'breakout': 0.5, 'breakthrough': 0.6,
            'optimistic': 0.5, 'confident': 0.5, 'strong': 0.4,
            'buy': 0.5, 'accumulate': 0.5, 'long': 0.4,
            
            # Moderate Greed (0.2 to 0.4)
            'up': 0.3, 'rise': 0.3, 'gain': 0.4, 'profit': 0.4,
            'green': 0.3, 'positive': 0.3, 'growth': 0.4,
            'support': 0.2, 'bounce': 0.3, 'recovery': 0.4,
            
            # Technical Analysis Terms
            'resistance': -0.2, 'support': 0.2, 'breakout': 0.5, 'breakdown': -0.5,
            'oversold': 0.3, 'overbought': -0.3, 'momentum': 0.3,
            'volume': 0.1, 'liquidity': 0.1, 'volatility': -0.1,
            
            # Market Psychology
            'fomo': 0.6, 'fear': -0.6, 'greed': 0.6, 'hope': 0.4,
            'despair': -0.7, 'euphoria': 0.8, 'complacency': -0.2,
            'anxiety': -0.5, 'excitement': 0.5, 'confidence': 0.4,
            
            # News-specific terms
            'announce': 0.2, 'partnership': 0.4, 'adoption': 0.5,
            'regulation': -0.3, 'ban': -0.7, 'approve': 0.5,
            'institutional': 0.4, 'mainstream': 0.3, 'endorsement': 0.5
        }
    
    def _build_entity_patterns(self) -> Dict[str, List[str]]:
        """Build patterns for financial entity recognition"""
        return {
            'crypto': [
                # Major cryptocurrencies
                r'\b(BTC|BITCOIN)\b', r'\b(ETH|ETHEREUM)\b', r'\b(XRP|RIPPLE)\b',
                r'\b(ADA|CARDANO)\b', r'\b(SOL|SOLANA)\b', r'\b(DOGE|DOGECOIN)\b',
                r'\b(MATIC|POLYGON)\b', r'\b(AVAX|AVALANCHE)\b', r'\b(DOT|POLKADOT)\b',
                r'\b(LINK|CHAINLINK)\b', r'\b(UNI|UNISWAP)\b', r'\b(ATOM|COSMOS)\b',
                r'\b(ALGO|ALGORAND)\b', r'\b(VET|VECHAIN)\b', r'\b(FTM|FANTOM)\b',
                # Generic crypto terms
                r'\bcrypto\b', r'\bcryptocurrency\b', r'\bdigital asset\b',
                r'\bdefi\b', r'\bnft\b', r'\bweb3\b', r'\bblockchain\b'
            ],
            'stocks': [
                # Major tech stocks
                r'\b(AAPL|APPLE)\b', r'\b(MSFT|MICROSOFT)\b', r'\b(GOOGL|GOOGLE)\b',
                r'\b(AMZN|AMAZON)\b', r'\b(TSLA|TESLA)\b', r'\b(META|FACEBOOK)\b',
                r'\b(NVDA|NVIDIA)\b', r'\b(NFLX|NETFLIX)\b', r'\b(CRM|SALESFORCE)\b',
                # Financial stocks
                r'\b(JPM|JPMORGAN)\b', r'\b(BAC|BANK OF AMERICA)\b', r'\b(WFC|WELLS FARGO)\b',
                r'\b(GS|GOLDMAN SACHS)\b', r'\b(MS|MORGAN STANLEY)\b',
                # Other major stocks
                r'\b(KO|COCA COLA)\b', r'\b(PFE|PFIZER)\b', r'\b(JNJ|JOHNSON)\b',
                r'\b(WMT|WALMART)\b', r'\b(V|VISA)\b', r'\b(MA|MASTERCARD)\b'
            ],
            'indices': [
                r'\b(SPY|SP500|S&P 500)\b', r'\b(QQQ|NASDAQ)\b', r'\b(DIA|DJIA|DOW)\b',
                r'\b(VIX|VOLATILITY)\b', r'\b(IWM|RUSSELL)\b',
                r'\bmarket\b', r'\bindex\b', r'\bindices\b'
            ]
        }
    
    def _build_sarcasm_patterns(self) -> List[str]:
        """Build patterns for sarcasm detection"""
        return [
            r'yeah right', r'sure thing', r'totally', r'obviously',
            r'what could go wrong', r'this is fine', r'great timing',
            r'perfect', r'wonderful', r'amazing', r'brilliant',
            r'love it when', r'just what we needed', r'exactly what i wanted'
        ]
    
    def _build_psychology_indicators(self) -> Dict[str, Dict[str, float]]:
        """Build market psychology indicators"""
        return {
            'fear_indicators': {
                'market_crash': -0.9, 'recession': -0.8, 'bear_market': -0.7,
                'inflation': -0.5, 'interest_rates': -0.4, 'fed': -0.3,
                'unemployment': -0.6, 'gdp': -0.3, 'earnings': -0.2
            },
            'greed_indicators': {
                'ath': 0.7, 'all_time_high': 0.7, 'record_high': 0.6,
                'bull_market': 0.7, 'rally': 0.6, 'surge': 0.6,
                'institutional_adoption': 0.5, 'mainstream': 0.4
            },
            'uncertainty_indicators': {
                'volatile': -0.3, 'uncertain': -0.4, 'unclear': -0.3,
                'mixed_signals': -0.3, 'conflicting': -0.4, 'unpredictable': -0.5
            }
        }
    
    def analyze_advanced_sentiment(self, texts: List[str], entities: Optional[List[str]] = None) -> Dict:
        """
        Perform advanced sentiment analysis optimized for financial markets
        
        Args:
            texts: List of text strings to analyze
            entities: Optional list of specific entities to focus on
            
        Returns:
            Comprehensive sentiment analysis results
        """
        start_time = time.time()
        
        if not texts:
            return self._empty_result()
        
        # Filter and preprocess texts
        valid_texts = [t for t in texts if t and isinstance(t, str) and len(t.strip()) > 10]
        
        if not valid_texts:
            return self._empty_result()
        
        # Initialize results structure
        results = {
            'overall_sentiment': 0.0,
            'confidence': 0.0,
            'sentiment_distribution': {'fear': 0, 'neutral': 0, 'greed': 0},
            'entity_sentiment': {},
            'market_psychology': {},
            'sentiment_momentum': 0.0,
            'text_analysis': {
                'total_texts': len(valid_texts),
                'avg_length': np.mean([len(t) for t in valid_texts]),
                'financial_relevance_score': 0.0,
                'sarcasm_detected': 0,
                'emotion_scores': {}
            },
            'processing_metrics': {
                'processing_time_ms': 0.0,
                'texts_per_second': 0.0
            }
        }
        
        # Analyze each text
        text_sentiments = []
        entity_mentions = defaultdict(list)
        total_financial_relevance = 0
        
        for text in valid_texts:
            text_result = self._analyze_single_text(text)
            text_sentiments.append(text_result)
            
            # Aggregate entity mentions
            for entity, sentiment in text_result['entity_mentions'].items():
                entity_mentions[entity].append(sentiment)
            
            # Aggregate financial relevance
            total_financial_relevance += text_result['financial_relevance']
            
            # Track sarcasm
            if text_result['sarcasm_probability'] > 0.7:
                results['text_analysis']['sarcasm_detected'] += 1
        
        # Calculate overall metrics
        if text_sentiments:
            # Weighted sentiment calculation
            sentiments = [t['final_sentiment'] for t in text_sentiments]
            confidences = [t['confidence'] for t in text_sentiments]
            weights = [t['financial_relevance'] for t in text_sentiments]
            
            # Overall sentiment (weighted by financial relevance and confidence)
            total_weight = sum(w * c for w, c in zip(weights, confidences))
            if total_weight > 0:
                results['overall_sentiment'] = sum(
                    s * w * c for s, w, c in zip(sentiments, weights, confidences)
                ) / total_weight
            
            # Overall confidence
            results['confidence'] = np.mean(confidences)
            
            # Sentiment distribution
            for sentiment in sentiments:
                if sentiment < -0.1:
                    results['sentiment_distribution']['fear'] += 1
                elif sentiment > 0.1:
                    results['sentiment_distribution']['greed'] += 1
                else:
                    results['sentiment_distribution']['neutral'] += 1
            
            # Normalize distribution
            total_texts = len(sentiments)
            for key in results['sentiment_distribution']:
                results['sentiment_distribution'][key] /= total_texts
            
            # Calculate sentiment momentum (trend)
            if len(sentiments) > 1:
                recent = sentiments[-min(5, len(sentiments)):]  # Last 5 texts
                older = sentiments[:-min(5, len(sentiments))] if len(sentiments) > 5 else [0]
                results['sentiment_momentum'] = np.mean(recent) - np.mean(older)
        
        # Process entity sentiments
        for entity, sentiment_list in entity_mentions.items():
            if len(sentiment_list) >= 1:  # Minimum mentions threshold
                results['entity_sentiment'][entity] = {
                    'sentiment': np.mean(sentiment_list),
                    'confidence': min(1.0, len(sentiment_list) / 10.0),  # More mentions = higher confidence
                    'mention_count': len(sentiment_list),
                    'sentiment_std': np.std(sentiment_list),
                    'trend': sentiment_list[-1] - sentiment_list[0] if len(sentiment_list) > 1 else 0
                }
        
        # Market psychology analysis
        results['market_psychology'] = self._analyze_market_psychology(text_sentiments)
        
        # Text analysis metrics
        results['text_analysis']['financial_relevance_score'] = total_financial_relevance / len(valid_texts)
        results['text_analysis']['emotion_scores'] = self._aggregate_emotions(text_sentiments)
        
        # Performance metrics
        processing_time = (time.time() - start_time) * 1000
        results['processing_metrics']['processing_time_ms'] = processing_time
        results['processing_metrics']['texts_per_second'] = len(valid_texts) / max(0.001, processing_time / 1000)
        
        # Track performance
        self.analysis_times.append(processing_time)
        
        return results
    
    def _analyze_single_text(self, text: str) -> Dict:
        """Analyze a single text with comprehensive techniques"""
        
        # Clean and preprocess
        cleaned_text = self._clean_text(text)
        
        # Basic sentiment analysis
        vader_scores = self.vader.polarity_scores(cleaned_text)
        textblob_sentiment = TextBlob(cleaned_text).sentiment
        
        # Financial lexicon sentiment
        financial_sentiment = self._calculate_financial_sentiment(cleaned_text)
        
        # Entity recognition and sentiment
        entities = self._extract_entities_with_sentiment(cleaned_text)
        
        # Financial relevance score
        financial_relevance = self._calculate_financial_relevance(cleaned_text)
        
        # Sarcasm detection
        sarcasm_prob = self._detect_sarcasm(cleaned_text)
        
        # Emotion analysis
        emotions = self._analyze_emotions(cleaned_text)
        
        # Market psychology indicators
        psychology = self._detect_psychology_indicators(cleaned_text)
        
        # Combine sentiments with sophisticated weighting
        base_sentiment = (
            vader_scores['compound'] * 0.3 +
            textblob_sentiment.polarity * 0.2 +
            financial_sentiment * 0.5  # Higher weight for financial-specific sentiment
        )
        
        # Adjust for sarcasm (reverse sentiment if sarcasm detected)
        if sarcasm_prob > 0.7:
            base_sentiment *= -0.6
        
        # Adjust for financial relevance (boost sentiment for more relevant texts)
        final_sentiment = base_sentiment * (0.5 + 0.5 * financial_relevance)
        
        # Calculate confidence
        confidence = min(1.0, (
            abs(base_sentiment) * 0.4 +
            financial_relevance * 0.3 +
            (1 - sarcasm_prob) * 0.2 +
            textblob_sentiment.subjectivity * 0.1
        ))
        
        return {
            'original_text': text[:200],  # Truncate for storage
            'cleaned_text': cleaned_text[:200],
            'vader_sentiment': vader_scores,
            'textblob_sentiment': {
                'polarity': textblob_sentiment.polarity,
                'subjectivity': textblob_sentiment.subjectivity
            },
            'financial_sentiment': financial_sentiment,
            'final_sentiment': final_sentiment,
            'confidence': confidence,
            'entity_mentions': entities,
            'financial_relevance': financial_relevance,
            'sarcasm_probability': sarcasm_prob,
            'emotions': emotions,
            'psychology_indicators': psychology
        }
    
    def _clean_text(self, text: str) -> str:
        """Advanced text cleaning for financial analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove user mentions and hashtags (keep the content)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#(\w+)', r'\1', text)  # Keep hashtag content
        
        # Remove excessive punctuation
        text = re.sub(r'[!]{3,}', '!', text)
        text = re.sub(r'[?]{3,}', '?', text)
        text = re.sub(r'[.]{3,}', '...', text)
        
        # Remove special characters but keep financial symbols
        text = re.sub(r'[^\w\s$%\-+.,!?]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _calculate_financial_sentiment(self, text: str) -> float:
        """Calculate sentiment using enhanced financial lexicon"""
        words = text.lower().split()
        sentiment_sum = 0
        word_count = 0
        
        # Direct word matching
        for word in words:
            if word in self.financial_lexicon:
                sentiment_sum += self.financial_lexicon[word]
                word_count += 1
        
        # Phrase matching (two-word combinations)
        for i in range(len(words) - 1):
            phrase = f"{words[i]}_{words[i+1]}"
            if phrase in self.financial_lexicon:
                sentiment_sum += self.financial_lexicon[phrase]
                word_count += 1
        
        return sentiment_sum / max(word_count, 1)
    
    def _extract_entities_with_sentiment(self, text: str) -> Dict[str, float]:
        """Extract financial entities and calculate their contextual sentiment"""
        entities = {}
        
        # Check all entity types
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text.upper())
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0]  # Handle regex groups
                    
                    # Get context around the entity
                    context = self._get_entity_context(text, match, window=15)
                    
                    # Calculate sentiment for this context
                    context_sentiment = self._calculate_financial_sentiment(context)
                    
                    # Normalize entity name
                    entity_name = self._normalize_entity_name(match)
                    entities[entity_name] = context_sentiment
        
        return entities
    
    def _get_entity_context(self, text: str, entity: str, window: int = 15) -> str:
        """Get context words around an entity mention"""
        words = text.split()
        entity_indices = []
        
        # Find all occurrences of the entity
        for i, word in enumerate(words):
            if entity.lower() in word.lower():
                entity_indices.append(i)
        
        if not entity_indices:
            return text
        
        # Get context around the first mention
        idx = entity_indices[0]
        start = max(0, idx - window)
        end = min(len(words), idx + window + 1)
        
        return ' '.join(words[start:end])
    
    def _normalize_entity_name(self, entity: str) -> str:
        """Normalize entity names for consistency"""
        entity = entity.upper()
        
        # Cryptocurrency normalization
        crypto_map = {
            'BITCOIN': 'BTC', 'ETHEREUM': 'ETH', 'RIPPLE': 'XRP',
            'CARDANO': 'ADA', 'SOLANA': 'SOL', 'DOGECOIN': 'DOGE',
            'POLYGON': 'MATIC', 'AVALANCHE': 'AVAX', 'POLKADOT': 'DOT'
        }
        
        # Stock normalization
        stock_map = {
            'APPLE': 'AAPL', 'MICROSOFT': 'MSFT', 'GOOGLE': 'GOOGL',
            'AMAZON': 'AMZN', 'TESLA': 'TSLA', 'FACEBOOK': 'META',
            'NVIDIA': 'NVDA', 'NETFLIX': 'NFLX'
        }
        
        return crypto_map.get(entity, stock_map.get(entity, entity))
    
    def _calculate_financial_relevance(self, text: str) -> float:
        """Calculate how relevant the text is to financial markets"""
        words = text.lower().split()
        
        # Financial keywords
        financial_keywords = [
            'price', 'market', 'trading', 'investment', 'portfolio',
            'profit', 'loss', 'gain', 'return', 'yield', 'dividend',
            'stock', 'crypto', 'currency', 'exchange', 'broker',
            'bull', 'bear', 'trend', 'analysis', 'forecast'
        ]
        
        # Count financial keywords
        financial_word_count = sum(1 for word in words if word in financial_keywords)
        
        # Check for entity mentions
        entity_count = 0
        for patterns in self.entity_patterns.values():
            for pattern in patterns:
                entity_count += len(re.findall(pattern, text.upper()))
        
        # Calculate relevance score
        word_ratio = financial_word_count / max(len(words), 1)
        entity_ratio = min(1.0, entity_count / 5.0)  # Cap at 5 entities
        
        return min(1.0, word_ratio * 0.6 + entity_ratio * 0.4)
    
    def _detect_sarcasm(self, text: str) -> float:
        """Detect sarcasm using pattern matching and context analysis"""
        sarcasm_score = 0.0
        
        # Pattern-based detection
        for pattern in self.sarcasm_patterns:
            if re.search(pattern, text.lower()):
                sarcasm_score += 0.3
        
        # Excessive punctuation
        if re.search(r'[!?]{3,}', text):
            sarcasm_score += 0.2
        
        # Contradiction indicators
        contradiction_words = ['but', 'however', 'although', 'despite', 'nevertheless']
        for word in contradiction_words:
            if word in text.lower():
                sarcasm_score += 0.1
        
        # Extreme positive words in negative context
        extreme_positive = ['amazing', 'fantastic', 'wonderful', 'perfect', 'brilliant']
        if any(word in text.lower() for word in extreme_positive):
            # Check if context suggests sarcasm
            if any(neg in text.lower() for neg in ['crash', 'dump', 'down', 'loss']):
                sarcasm_score += 0.4
        
        return min(1.0, sarcasm_score)
    
    def _analyze_emotions(self, text: str) -> Dict[str, float]:
        """Analyze emotions using financial-focused emotion detection"""
        emotions = {
            'fear': 0, 'greed': 0, 'hope': 0, 'despair': 0,
            'excitement': 0, 'anxiety': 0, 'confidence': 0, 'uncertainty': 0
        }
        
        emotion_keywords = {
            'fear': ['scared', 'afraid', 'worried', 'panic', 'nervous', 'terrified', 'fearful'],
            'greed': ['greedy', 'fomo', 'more', 'want', 'need', 'grab', 'hoard'],
            'hope': ['hope', 'optimistic', 'positive', 'believe', 'faith', 'trust'],
            'despair': ['hopeless', 'despair', 'give up', 'surrender', 'defeated'],
            'excitement': ['excited', 'thrilled', 'pumped', 'hyped', 'enthusiastic'],
            'anxiety': ['anxious', 'stressed', 'tense', 'uneasy', 'restless'],
            'confidence': ['confident', 'sure', 'certain', 'strong', 'solid'],
            'uncertainty': ['uncertain', 'unsure', 'confused', 'unclear', 'doubtful']
        }
        
        words = text.lower().split()
        total_words = len(words)
        
        for emotion, keywords in emotion_keywords.items():
            count = sum(1 for word in words if any(kw in word for kw in keywords))
            emotions[emotion] = count / max(total_words, 1)
        
        return emotions
    
    def _detect_psychology_indicators(self, text: str) -> Dict[str, float]:
        """Detect market psychology indicators"""
        psychology = {}
        
        for indicator_type, indicators in self.psychology_indicators.items():
            score = 0
            for indicator, weight in indicators.items():
                if indicator.replace('_', ' ') in text.lower():
                    score += weight
            psychology[indicator_type] = score
        
        return psychology
    
    def _analyze_market_psychology(self, text_sentiments: List[Dict]) -> Dict:
        """Analyze overall market psychology from text sentiments"""
        if not text_sentiments:
            return {}
        
        # Aggregate psychology indicators
        psychology_agg = defaultdict(list)
        for text_result in text_sentiments:
            for psych_type, score in text_result['psychology_indicators'].items():
                if score != 0:  # Only non-zero scores
                    psychology_agg[psych_type].append(score)
        
        # Calculate market psychology metrics
        psychology_summary = {}
        for psych_type, scores in psychology_agg.items():
            if scores:
                psychology_summary[psych_type] = {
                    'average': np.mean(scores),
                    'strength': len(scores) / len(text_sentiments),  # How prevalent this psychology is
                    'intensity': np.std(scores)  # How varied the psychology is
                }
        
        return psychology_summary
    
    def _aggregate_emotions(self, text_sentiments: List[Dict]) -> Dict[str, float]:
        """Aggregate emotions across all texts"""
        if not text_sentiments:
            return {}
        
        emotion_totals = defaultdict(float)
        for text_result in text_sentiments:
            for emotion, score in text_result['emotions'].items():
                emotion_totals[emotion] += score
        
        # Average emotions
        num_texts = len(text_sentiments)
        return {emotion: total / num_texts for emotion, total in emotion_totals.items()}
    
    def _empty_result(self) -> Dict:
        """Return empty result structure"""
        return {
            'overall_sentiment': 0.0,
            'confidence': 0.0,
            'sentiment_distribution': {'fear': 0, 'neutral': 1, 'greed': 0},
            'entity_sentiment': {},
            'market_psychology': {},
            'sentiment_momentum': 0.0,
            'text_analysis': {
                'total_texts': 0,
                'avg_length': 0,
                'financial_relevance_score': 0.0,
                'sarcasm_detected': 0,
                'emotion_scores': {}
            },
            'processing_metrics': {
                'processing_time_ms': 0.0,
                'texts_per_second': 0.0
            }
        }
    
    def get_performance_metrics(self) -> Dict:
        """Get analyzer performance metrics"""
        if not self.analysis_times:
            return {'avg_processing_time_ms': 0, 'total_analyses': 0}
        
        return {
            'avg_processing_time_ms': np.mean(self.analysis_times),
            'p95_processing_time_ms': np.percentile(self.analysis_times, 95),
            'p99_processing_time_ms': np.percentile(self.analysis_times, 99),
            'total_analyses': len(self.analysis_times),
            'fastest_analysis_ms': min(self.analysis_times),
            'slowest_analysis_ms': max(self.analysis_times)
        }

# Example usage and testing
if __name__ == "__main__":
    analyzer = AdvancedFinancialSentimentAnalyzer()
    
    # Test texts
    test_texts = [
        "Bitcoin is crashing hard! This is a disaster for crypto markets. Panic selling everywhere!",
        "AAPL breaking out to new all-time highs! Very bullish sentiment in tech stocks.",
        "Market looking uncertain with mixed signals from the Fed. Not sure where we're heading.",
        "HODL! Diamond hands! Bitcoin to the moon! 🚀",
        "Yeah right, this 'dip' is totally normal. What could go wrong? 📉"
    ]
    
    print("Testing Advanced Financial Sentiment Analyzer")
    print("=" * 60)
    
    results = analyzer.analyze_advanced_sentiment(test_texts)
    
    print(f"Overall Sentiment: {results['overall_sentiment']:.3f}")
    print(f"Confidence: {results['confidence']:.3f}")
    print(f"Processing Time: {results['processing_metrics']['processing_time_ms']:.2f}ms")
    print(f"Texts per Second: {results['processing_metrics']['texts_per_second']:.1f}")
    print()
    
    print("Entity Sentiments:")
    for entity, data in results['entity_sentiment'].items():
        print(f"  {entity}: {data['sentiment']:.3f} (confidence: {data['confidence']:.2f}, mentions: {data['mention_count']})")
    
    print()
    print("Sentiment Distribution:")
    for sentiment, ratio in results['sentiment_distribution'].items():
        print(f"  {sentiment.capitalize()}: {ratio:.2%}")
    
    print()
    print("Performance Metrics:")
    perf = analyzer.get_performance_metrics()
    for metric, value in perf.items():
        print(f"  {metric}: {value}")
