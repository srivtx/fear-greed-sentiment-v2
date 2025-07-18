# Chapter 6: Text Processing Deep Dive 🔬

## Welcome to Advanced Text Processing!

In Chapter 5, you learned the basics of NLP and text preprocessing. Now let's dive deeper into the sophisticated techniques our system uses to handle complex, real-world social media text.

## 🎯 The Reality of Social Media Text

Social media text is messy, creative, and constantly evolving. Our system needs to handle:

### The Wild West of Text
```
Real examples from financial social media:
- "BTC 🚀🚀🚀 LETS GOOOOO!!! 💎🙌 #DiamondHands #HODL $100k incoming!!!"
- "rekt again... shoulda sold at 69k 😭😭😭 #FOMO #bearmarket"
- "TSLA looking sus ngl... might dump b4 earnings 📉"
- "gm frens! ETH 2.0 szn is here 🌙 wagmi 💪"
- "📢 BREAKING: Fed raises rates by 0.75% - RIP my portfolio 💀"
```

**Challenges:**
- Multiple languages mixed together
- Intentional misspellings and abbreviations
- Emoji overload
- Technical jargon mixed with slang
- Context-dependent meanings

## 🔤 Advanced Regex Patterns

**Regex = Regular Expressions = Pattern matching for text**

Think of regex like creating search patterns. Instead of looking for exact words, we create rules to find types of content.

### Basic Regex Concepts

```python
import re

# Find exact word
pattern = "bitcoin"
text = "I love bitcoin and Bitcoin!"
matches = re.findall(pattern, text, re.IGNORECASE)
# Result: ['bitcoin', 'Bitcoin']

# Find word boundaries (complete words only)
pattern = r'\bbitcoin\b'
text = "bitcoin vs bitcoins vs mybitcoin"
matches = re.findall(pattern, text, re.IGNORECASE)
# Result: ['bitcoin'] (doesn't match 'bitcoins' or 'mybitcoin')
```

### Our Financial Text Regex Patterns

```python
class AdvancedTextProcessor:
    def __init__(self):
        # Compile regex patterns for efficiency
        self.patterns = {
            # Cashtags: $BTC, $AAPL, $TSLA123
            'cashtag': re.compile(r'\$([A-Z]{1,5})', re.IGNORECASE),
            
            # Hashtags: #HODL, #ToTheMoon
            'hashtag': re.compile(r'#([a-zA-Z][a-zA-Z0-9_]*)', re.IGNORECASE),
            
            # URLs: http://, https://, www.
            'url': re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'),
            
            # User mentions: @username
            'mention': re.compile(r'@([a-zA-Z0-9_]+)'),
            
            # Crypto addresses (simplified)
            'crypto_address': re.compile(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b|\b0x[a-fA-F0-9]{40}\b'),
            
            # Price patterns: $42,000, $1.5K, $2.5M  
            'price': re.compile(r'\$([0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?[KMB]?)'),
            
            # Percentage: +5.5%, -12.3%
            'percentage': re.compile(r'[+-]?([0-9]+(?:\.[0-9]+)?)\s*%'),
            
            # Repeated characters: amazingggg, noooo
            'repeated_chars': re.compile(r'(.)\1{2,}'),
            
            # Emoji ranges (simplified)
            'emoji': re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]')
        }
```

### Pattern Extraction Examples

```python
def extract_all_patterns(text):
    """Extract all relevant patterns from text"""
    
    text = "Just bought $BTC at $42,000! 🚀 #HODL @elonmusk +15.5% gains!!! https://example.com"
    
    results = {}
    
    # Extract cashtags
    results['cashtags'] = self.patterns['cashtag'].findall(text)
    # Result: ['BTC']
    
    # Extract hashtags  
    results['hashtags'] = self.patterns['hashtag'].findall(text)
    # Result: ['HODL']
    
    # Extract prices
    results['prices'] = self.patterns['price'].findall(text)
    # Result: ['42,000']
    
    # Extract percentages
    results['percentages'] = self.patterns['percentage'].findall(text)
    # Result: ['15.5']
    
    # Extract mentions
    results['mentions'] = self.patterns['mention'].findall(text)
    # Result: ['elonmusk']
    
    # Count emojis
    results['emoji_count'] = len(self.patterns['emoji'].findall(text))
    # Result: 1
    
    return results
```

## 😀 Advanced Emoji Handling

Emojis carry significant emotional information in financial social media:

### Emoji Categories and Meanings

```python
class EmojiProcessor:
    def __init__(self):
        self.emoji_categories = {
            # Extremely positive
            'moon_rockets': ['🚀', '🌙', '💎', '🙌', '💪', '🔥'],
            
            # Positive
            'positive': ['😀', '😃', '😄', '😁', '😊', '🥳', '💚', '📈', '💰'],
            
            # Negative  
            'negative': ['😭', '😢', '😞', '😔', '💔', '📉', '💀', '🩸'],
            
            # Extremely negative
            'panic': ['😱', '😰', '🤮', '💸', '⚰️', '🔴'],
            
            # Neutral/thinking
            'neutral': ['🤔', '😐', '😑', '🤷', '💭'],
            
            # Warning/caution
            'warning': ['⚠️', '🚨', '⛔', '🛑', '🔻']
        }
        
        # Create emoji-to-sentiment mapping
        self.emoji_sentiment = {}
        for category, emojis in self.emoji_categories.items():
            sentiment_score = {
                'moon_rockets': 1.0,
                'positive': 0.6,
                'negative': -0.6,
                'panic': -1.0,
                'neutral': 0.0,
                'warning': -0.3
            }[category]
            
            for emoji in emojis:
                self.emoji_sentiment[emoji] = sentiment_score
    
    def analyze_emoji_sentiment(self, text):
        """Calculate sentiment contribution from emojis"""
        
        emoji_scores = []
        for char in text:
            if char in self.emoji_sentiment:
                emoji_scores.append(self.emoji_sentiment[char])
        
        if not emoji_scores:
            return 0.0
        
        # Average emoji sentiment, weighted by count
        return sum(emoji_scores) / len(emoji_scores)
```

### Emoji Replacement Strategy

```python
def replace_emojis_with_words(text):
    """Replace emojis with equivalent words for better sentiment analysis"""
    
    emoji_to_words = {
        '🚀': ' rocket moon ',
        '💎': ' diamond hands ',
        '🙌': ' diamond hands ',
        '📈': ' chart up ',
        '📉': ' chart down ',
        '💰': ' money profits ',
        '💸': ' money lost ',
        '😭': ' crying sad ',
        '🤑': ' money face greed ',
        '💀': ' dead rekt ',
        '🔥': ' fire hot ',
        '❤️': ' love ',
        '💚': ' love green ',
        '💔': ' heartbreak sad '
    }
    
    for emoji, words in emoji_to_words.items():
        text = text.replace(emoji, words)
    
    return text
```

## 🏦 Financial Entity Recognition

Identifying mentions of financial instruments is crucial for our analysis:

### Multi-Pattern Entity Recognition

```python
class FinancialEntityRecognizer:
    def __init__(self):
        # Different ways people refer to the same asset
        self.entity_patterns = {
            'BTC': [
                r'\bbitcoin\b', r'\bbtc\b', r'\$btc\b', r'\bxbt\b',
                r'\bbtcusd\b', r'\bbitcoin core\b'
            ],
            'ETH': [
                r'\bethereum\b', r'\beth\b', r'\$eth\b', r'\bether\b',
                r'\bethusd\b'
            ],
            'TSLA': [
                r'\btesla\b', r'\btsla\b', r'\$tsla\b', r'\btesla motors\b',
                r'\btesla inc\b'
            ],
            'AAPL': [
                r'\bapple\b', r'\baapl\b', r'\$aapl\b', r'\bapple inc\b'
            ]
        }
        
        # Compile all patterns
        self.compiled_patterns = {}
        for entity, patterns in self.entity_patterns.items():
            self.compiled_patterns[entity] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]
    
    def extract_entities(self, text):
        """Extract all financial entities from text"""
        
        entities_found = {
            'cryptos': [],
            'stocks': [],
            'indices': []
        }
        
        # Convert to lowercase for matching
        text_lower = text.lower()
        
        # Check each entity pattern
        for entity, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(text_lower):
                    # Categorize the entity
                    if entity in ['BTC', 'ETH', 'XRP', 'ADA', 'SOL']:
                        entities_found['cryptos'].append(entity)
                    elif entity in ['AAPL', 'TSLA', 'MSFT', 'GOOGL']:
                        entities_found['stocks'].append(entity)
                    break  # Found this entity, no need to check other patterns
        
        # Remove duplicates
        for category in entities_found:
            entities_found[category] = list(set(entities_found[category]))
        
        return entities_found
```

### Context-Aware Entity Recognition

```python
def extract_entities_with_context(text):
    """Extract entities and their surrounding context"""
    
    entities_with_context = []
    
    # Find all cashtags with surrounding words
    cashtag_pattern = r'(\w+\s+)?(\$[A-Z]{1,5})(\s+\w+)?'
    matches = re.finditer(cashtag_pattern, text, re.IGNORECASE)
    
    for match in matches:
        before = match.group(1) or ""
        entity = match.group(2)
        after = match.group(3) or ""
        
        entities_with_context.append({
            'entity': entity,
            'context_before': before.strip(),
            'context_after': after.strip(),
            'full_context': f"{before}{entity}{after}".strip()
        })
    
    return entities_with_context

# Example usage
text = "Love $BTC, hate $TSLA, neutral on $ETH today"
contexts = extract_entities_with_context(text)

# Result:
# [
#   {'entity': '$BTC', 'context_before': 'Love', 'context_after': '', 'full_context': 'Love $BTC'},
#   {'entity': '$TSLA', 'context_before': 'hate', 'context_after': '', 'full_context': 'hate $TSLA'},
#   {'entity': '$ETH', 'context_before': 'on', 'context_after': 'today', 'full_context': 'on $ETH today'}
# ]
```

## 🔄 Handling Intentional Misspellings

Social media users often misspell words intentionally:

### Common Financial Misspellings

```python
class SpellingNormalizer:
    def __init__(self):
        self.financial_spellings = {
            # Intentional misspellings
            'hodl': 'hold',
            'stonks': 'stocks', 
            'tendies': 'profits',
            'gainz': 'gains',
            'loosing': 'losing',
            'loosers': 'losers',
            
            # Elongated words
            'amazinggggg': 'amazing',
            'noooooo': 'no',
            'yesssss': 'yes',
            
            # Common typos
            'recieve': 'receive',
            'seperate': 'separate',
            'definately': 'definitely',
            
            # Crypto slang
            'shitcoin': 'altcoin',
            'moonboi': 'optimist',
            'rekt': 'wrecked',
            'fud': 'fear uncertainty doubt',
            'fomo': 'fear missing out',
            'btfd': 'buy the dip',
            'wagmi': 'will make it',
            'ngmi': 'not going to make it'
        }
    
    def normalize_spellings(self, text):
        """Fix common misspellings and expand abbreviations"""
        
        words = text.split()
        normalized_words = []
        
        for word in words:
            # Check for exact matches first
            if word.lower() in self.financial_spellings:
                normalized_words.append(self.financial_spellings[word.lower()])
            else:
                # Check for repeated characters (amazingggg -> amazing)
                normalized_word = self._fix_repeated_chars(word)
                normalized_words.append(normalized_word)
        
        return ' '.join(normalized_words)
    
    def _fix_repeated_chars(self, word):
        """Fix words with repeated characters"""
        # Replace 3+ repeated characters with just 2
        # "amazinggggg" -> "amazing"
        return re.sub(r'(.)\1{2,}', r'\1\1', word)
```

## ⚡ Performance Optimization

Processing thousands of texts requires efficient code:

### Batch Processing

```python
class BatchTextProcessor:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.entity_recognizer = FinancialEntityRecognizer()
        
    def process_batch(self, texts, batch_size=1000):
        """Process texts in batches for better performance"""
        
        results = []
        total_texts = len(texts)
        
        for i in range(0, total_texts, batch_size):
            batch = texts[i:i+batch_size]
            batch_results = []
            
            for text in batch:
                try:
                    # Process single text
                    processed = self._process_single_text(text)
                    batch_results.append(processed)
                except Exception as e:
                    logger.warning(f"Error processing text: {e}")
                    batch_results.append(None)
            
            results.extend(batch_results)
            
            # Log progress
            processed_count = min(i + batch_size, total_texts)
            logger.info(f"Processed {processed_count}/{total_texts} texts")
        
        return results
    
    def _process_single_text(self, text):
        """Process a single text through complete pipeline"""
        
        if not text or len(text.strip()) == 0:
            return None
        
        # Extract metadata before cleaning
        entities = self.entity_recognizer.extract_entities(text)
        emoji_sentiment = self._analyze_emoji_sentiment(text)
        
        # Clean text for sentiment analysis
        cleaned_text = self.preprocessor.preprocess(text)
        
        return {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'entities': entities,
            'emoji_sentiment': emoji_sentiment,
            'text_length': len(text),
            'cleaned_length': len(cleaned_text)
        }
```

### Caching for Repeated Content

```python
from functools import lru_cache
import hashlib

class CachedTextProcessor:
    def __init__(self):
        self.processor = BatchTextProcessor()
        
    @lru_cache(maxsize=10000)
    def process_text_cached(self, text_hash, text):
        """Cache processed results for identical texts"""
        return self.processor._process_single_text(text)
    
    def process_with_caching(self, texts):
        """Process texts with caching for duplicates"""
        
        results = []
        cache_hits = 0
        
        for text in texts:
            # Create hash of text for caching
            text_hash = hashlib.md5(text.encode()).hexdigest()
            
            # Check cache first
            try:
                result = self.process_text_cached(text_hash, text)
                if text_hash in self.process_text_cached.cache_info():
                    cache_hits += 1
                results.append(result)
            except Exception as e:
                logger.warning(f"Error processing text: {e}")
                results.append(None)
        
        logger.info(f"Cache hits: {cache_hits}/{len(texts)} ({cache_hits/len(texts)*100:.1f}%)")
        return results
```

## 🧪 Quality Control and Validation

Ensuring processed text quality:

### Text Quality Metrics

```python
def calculate_text_quality(original, cleaned):
    """Calculate quality metrics for processed text"""
    
    metrics = {
        'original_length': len(original),
        'cleaned_length': len(cleaned),
        'compression_ratio': len(cleaned) / len(original) if len(original) > 0 else 0,
        'word_count_original': len(original.split()),
        'word_count_cleaned': len(cleaned.split()),
        'meaningful_words_ratio': len(cleaned.split()) / len(original.split()) if len(original.split()) > 0 else 0
    }
    
    # Quality flags
    quality_flags = {
        'too_short': len(cleaned.split()) < 3,
        'over_compressed': metrics['compression_ratio'] < 0.3,
        'no_meaningful_content': len(cleaned.strip()) == 0,
        'mostly_noise': metrics['meaningful_words_ratio'] < 0.2
    }
    
    # Overall quality score (0-1)
    quality_score = 1.0
    for flag, is_problematic in quality_flags.items():
        if is_problematic:
            quality_score -= 0.2
    
    return {
        'metrics': metrics,
        'flags': quality_flags,
        'quality_score': max(0, quality_score)
    }
```

### Content Filtering

```python
def filter_quality_content(processed_texts, min_quality=0.6):
    """Filter out low-quality processed texts"""
    
    high_quality_texts = []
    filtered_count = 0
    
    for item in processed_texts:
        if item is None:
            filtered_count += 1
            continue
        
        quality = calculate_text_quality(item['original_text'], item['cleaned_text'])
        
        if quality['quality_score'] >= min_quality:
            item['quality_metrics'] = quality
            high_quality_texts.append(item)
        else:
            filtered_count += 1
    
    logger.info(f"Filtered out {filtered_count}/{len(processed_texts)} low-quality texts")
    return high_quality_texts
```

## 🎯 Our Complete Advanced Pipeline

Here's how everything works together:

```python
class AdvancedTextPipeline:
    def __init__(self):
        self.spelling_normalizer = SpellingNormalizer()
        self.entity_recognizer = FinancialEntityRecognizer()
        self.emoji_processor = EmojiProcessor()
        self.cached_processor = CachedTextProcessor()
    
    def process_social_media_texts(self, raw_texts):
        """Complete pipeline for social media text processing"""
        
        logger.info(f"Starting pipeline for {len(raw_texts)} texts")
        
        # Step 1: Normalize spellings and expand abbreviations
        normalized_texts = [
            self.spelling_normalizer.normalize_spellings(text) 
            for text in raw_texts
        ]
        
        # Step 2: Process with caching
        processed_texts = self.cached_processor.process_with_caching(normalized_texts)
        
        # Step 3: Filter for quality
        quality_texts = filter_quality_content(processed_texts, min_quality=0.6)
        
        # Step 4: Add advanced analysis
        for item in quality_texts:
            # Enhanced emoji analysis
            item['emoji_analysis'] = self.emoji_processor.analyze_emoji_sentiment(
                item['original_text']
            )
            
            # Context-aware entity recognition
            item['entity_contexts'] = extract_entities_with_context(
                item['original_text']
            )
        
        logger.info(f"Pipeline complete: {len(quality_texts)} high-quality texts")
        return quality_texts
```

## 🎯 What You've Learned

You now understand:

✅ **Advanced regex patterns** for extracting financial information
✅ **Emoji handling** and sentiment contribution
✅ **Sophisticated entity recognition** with context awareness
✅ **Spelling normalization** for social media text
✅ **Performance optimization** through batching and caching
✅ **Quality control** and content filtering
✅ **Complete advanced pipeline** integration

## 🚀 What's Next?

In **Chapter 7**, we'll explore **How Sentiment Analysis Works** - the core engine that actually determines if text is positive, negative, or neutral. You'll learn:

- How VADER sentiment analyzer works under the hood
- Financial-specific sentiment scoring
- Confidence calculation and uncertainty handling
- Combining multiple sentiment signals

**Ready to understand the heart of sentiment analysis?** Let's continue to **[Chapter 7: How Sentiment Analysis Works](chapter_07_sentiment_analysis_engine.md)**!

---

## 💡 Advanced Practice Exercise

Try to identify what advanced processing would be needed for these challenging texts:

1. **Input:** "TSLA lookin sus ngl... might dump b4 earnings 📉 #ElonMusk wagmi tho 💎🙌"

2. **Input:** "bitcoinnnn is mooooning!!! 🚀🚀🚀 hodl 4ever!!! $100k sooooon"

3. **Input:** "gm crypto fam! ETH 2.0 szn finally here 🌙 time 2 accumulate b4 normies FOMO in 💪"

**For each text, identify:**
- Spelling normalizations needed
- Entities mentioned
- Emoji sentiment contribution
- Context clues for sentiment
- Quality assessment

This helps you think like our advanced processing pipeline! 🔬
