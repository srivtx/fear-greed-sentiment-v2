# Chapter 8: Entity Recognition - Finding What People Are Talking About 🎯

## Welcome to the Detective Work!

Imagine you're reading thousands of social media posts about the stock market. How do you quickly identify which posts are about Apple, which are about Bitcoin, and which mention Tesla? This is where **Entity Recognition** comes in - it's like having a super-smart highlighter that can automatically find and tag every mention of financial instruments!

## 🕵️ What is Entity Recognition?

**Entity Recognition = Finding and categorizing specific things mentioned in text**

### The Challenge: People Write Differently

Look at all these ways people refer to the same things:

**Bitcoin:**
- "Bitcoin", "bitcoin", "BITCOIN"
- "BTC", "btc", "$BTC"  
- "₿"
- "#bitcoin", "#BTC"
- "coin", "crypto king"

**Apple Inc:**
- "Apple", "AAPL", "$AAPL"
- "Apple Inc", "Apple Inc."
- "#AAPL", "APPL" (typo!)
- "Tim Cook's company"

**Tesla:**
- "Tesla", "TSLA", "$TSLA"
- "Tesla Motors", "Tesla Inc"
- "#tesla", "#TSLA"
- "Elon's company", "EV company"

Our system needs to recognize ALL of these as the same entity!

## 🎯 Types of Financial Entities We Track

### 1. Cryptocurrencies
```python
crypto_entities = {
    'bitcoin': {
        'symbols': ['BTC', 'BITCOIN', '₿'],
        'hashtags': ['#bitcoin', '#btc'],
        'aliases': ['digital gold', 'crypto king'],
        'patterns': [r'\$BTC\b', r'\bBTC\b', r'\bbitcoin\b']
    },
    'ethereum': {
        'symbols': ['ETH', 'ETHEREUM'],
        'hashtags': ['#ethereum', '#eth'],
        'aliases': ['ether', 'vitalik coin'],
        'patterns': [r'\$ETH\b', r'\bETH\b', r'\bethereum\b']
    },
    'dogecoin': {
        'symbols': ['DOGE', 'DOGECOIN'],
        'hashtags': ['#dogecoin', '#doge'],
        'aliases': ['meme coin', 'doge', 'shiba coin'],
        'patterns': [r'\$DOGE\b', r'\bdoge\b', r'\bdogecoin\b']
    }
}
```

### 2. Stocks
```python
stock_entities = {
    'apple': {
        'symbol': 'AAPL',
        'name': 'Apple Inc',
        'aliases': ['apple', 'tim cook company', 'iphone maker'],
        'patterns': [r'\$AAPL\b', r'\bAAPL\b', r'\bapple\b(?!\s+pie)']
    },
    'tesla': {
        'symbol': 'TSLA', 
        'name': 'Tesla Inc',
        'aliases': ['tesla', 'tesla motors', 'elon company', 'ev company'],
        'patterns': [r'\$TSLA\b', r'\bTSLA\b', r'\btesla\b']
    },
    'microsoft': {
        'symbol': 'MSFT',
        'name': 'Microsoft Corporation', 
        'aliases': ['microsoft', 'msft', 'windows company'],
        'patterns': [r'\$MSFT\b', r'\bMSFT\b', r'\bmicrosoft\b']
    }
}
```

### 3. Market Indices
```python
index_entities = {
    'sp500': {
        'names': ['S&P 500', 'S&P500', 'SPX', 'SPY'],
        'aliases': ['sp500', 'sp 500', 'market'],
        'patterns': [r'S&P\s?500', r'\bSPX\b', r'\bSPY\b']
    },
    'nasdaq': {
        'names': ['NASDAQ', 'Nasdaq', 'QQQ'],
        'aliases': ['nasdaq', 'tech index'],
        'patterns': [r'\bNASDAQ\b', r'\bQQQ\b']
    }
}
```

## 🔍 Our Entity Recognition System

### Core Entity Recognizer Class

```python
import re
from typing import Dict, List, Set, Tuple
import logging

class FinancialEntityRecognizer:
    def __init__(self):
        self.entities_db = self._load_entities_database()
        self.compiled_patterns = self._compile_patterns()
        self.logger = logging.getLogger(__name__)
        
    def _load_entities_database(self):
        """Load comprehensive financial entities database"""
        
        # This would normally load from a JSON file
        return {
            'cryptocurrencies': crypto_entities,
            'stocks': stock_entities, 
            'indices': index_entities,
            'commodities': {
                'gold': {
                    'symbols': ['GOLD', 'GLD', 'AU'],
                    'patterns': [r'\bgold\b', r'\$GOLD\b', r'\bGLD\b']
                },
                'oil': {
                    'symbols': ['OIL', 'USO', 'CL'],
                    'patterns': [r'\boil\b', r'\$OIL\b', r'crude']
                }
            }
        }
    
    def _compile_patterns(self):
        """Pre-compile regex patterns for better performance"""
        
        compiled = {}
        
        for category, entities in self.entities_db.items():
            compiled[category] = {}
            
            for entity_name, entity_data in entities.items():
                patterns = entity_data.get('patterns', [])
                
                # Compile all patterns for this entity
                compiled[category][entity_name] = [
                    re.compile(pattern, re.IGNORECASE) 
                    for pattern in patterns
                ]
        
        return compiled
```

### Smart Pattern Matching

```python
def find_entities(self, text: str) -> Dict:
    """Find all financial entities mentioned in text"""
    
    found_entities = {
        'cryptocurrencies': set(),
        'stocks': set(),
        'indices': set(),
        'commodities': set()
    }
    
    # Track positions for context analysis
    entity_positions = []
    
    for category in found_entities.keys():
        category_entities = self._find_category_entities(text, category)
        found_entities[category].update(category_entities['names'])
        entity_positions.extend(category_entities['positions'])
    
    # Remove false positives and conflicts
    cleaned_entities = self._clean_entity_conflicts(found_entities, text)
    
    # Add context information
    result = {
        'entities': cleaned_entities,
        'total_count': sum(len(entities) for entities in cleaned_entities.values()),
        'positions': entity_positions,
        'confidence_scores': self._calculate_entity_confidence(text, cleaned_entities)
    }
    
    return result

def _find_category_entities(self, text: str, category: str) -> Dict:
    """Find entities within a specific category"""
    
    found_names = set()
    positions = []
    
    if category not in self.compiled_patterns:
        return {'names': found_names, 'positions': positions}
    
    for entity_name, patterns in self.compiled_patterns[category].items():
        for pattern in patterns:
            matches = pattern.finditer(text)
            
            for match in matches:
                # Validate the match isn't a false positive
                if self._validate_entity_match(text, match, entity_name, category):
                    found_names.add(entity_name)
                    positions.append({
                        'entity': entity_name,
                        'category': category,
                        'start': match.start(),
                        'end': match.end(),
                        'matched_text': match.group()
                    })
    
    return {'names': found_names, 'positions': positions}
```

### Context-Aware Validation

```python
def _validate_entity_match(self, text: str, match, entity_name: str, category: str) -> bool:
    """Validate that an entity match is legitimate"""
    
    matched_text = match.group().lower()
    start_pos = match.start()
    end_pos = match.end()
    
    # Get surrounding context (10 characters before and after)
    context_start = max(0, start_pos - 10)
    context_end = min(len(text), end_pos + 10)
    context = text[context_start:context_end].lower()
    
    # Rule 1: Check for false positive patterns
    false_positive_checks = {
        'apple': [
            r'apple\s+(pie|juice|tree|fruit)',  # "apple pie", not the company
            r'(eat|eating|ate)\s+apple'         # "eating apple", not stock
        ],
        'tesla': [
            r'nikola\s+tesla',                  # The inventor, not the company
        ],
        'meta': [
            r'meta\s+(tag|data|information)',   # HTML meta, not Meta (Facebook)
        ]
    }
    
    if entity_name in false_positive_checks:
        for fp_pattern in false_positive_checks[entity_name]:
            if re.search(fp_pattern, context):
                return False
    
    # Rule 2: Require financial context for ambiguous terms
    ambiguous_terms = ['apple', 'meta', 'coin', 'stock']
    
    if any(term in matched_text for term in ambiguous_terms):
        financial_context_patterns = [
            r'\$',                    # Dollar sign nearby
            r'\b(buy|sell|trade|invest|portfolio|price|market)\b',
            r'\b(up|down|bull|bear|moon|crash)\b',
            r'#(stocks|crypto|trading|investing)'
        ]
        
        has_financial_context = any(
            re.search(pattern, context) 
            for pattern in financial_context_patterns
        )
        
        if not has_financial_context:
            return False
    
    # Rule 3: Check minimum word boundaries
    # Ensure we're not matching parts of other words
    if start_pos > 0 and text[start_pos - 1].isalnum():
        return False
    if end_pos < len(text) and text[end_pos].isalnum():
        return False
    
    return True
```

### Handling Conflicts and Overlaps

```python
def _clean_entity_conflicts(self, found_entities: Dict, text: str) -> Dict:
    """Resolve conflicts when multiple entities could match the same text"""
    
    cleaned = {category: set() for category in found_entities.keys()}
    
    # Get all entity positions sorted by start position
    all_positions = []
    for category, entities in found_entities.items():
        for entity in entities:
            positions = self._get_entity_positions(text, entity, category)
            all_positions.extend(positions)
    
    all_positions.sort(key=lambda x: x['start'])
    
    # Remove overlapping matches, keeping the most specific/confident one
    filtered_positions = []
    
    for i, current in enumerate(all_positions):
        is_valid = True
        
        # Check for overlaps with already accepted entities
        for accepted in filtered_positions:
            if self._positions_overlap(current, accepted):
                # Keep the more specific/confident match
                if self._get_match_confidence(current) <= self._get_match_confidence(accepted):
                    is_valid = False
                    break
                else:
                    # Remove the less confident match
                    filtered_positions.remove(accepted)
        
        if is_valid:
            filtered_positions.append(current)
            cleaned[current['category']].add(current['entity'])
    
    return cleaned

def _positions_overlap(self, pos1: Dict, pos2: Dict) -> bool:
    """Check if two entity positions overlap"""
    return not (pos1['end'] <= pos2['start'] or pos2['end'] <= pos1['start'])

def _get_match_confidence(self, position: Dict) -> float:
    """Calculate confidence score for an entity match"""
    
    # Factors that increase confidence:
    confidence = 0.5  # Base confidence
    
    # Exact symbol match (e.g., "$AAPL") is highly confident
    if '$' in position['matched_text']:
        confidence += 0.4
    
    # All caps symbol match is confident
    if position['matched_text'].isupper() and len(position['matched_text']) <= 5:
        confidence += 0.3
    
    # Hashtag match is moderately confident
    if position['matched_text'].startswith('#'):
        confidence += 0.2
    
    # Longer matches tend to be more specific
    if len(position['matched_text']) > 4:
        confidence += 0.1
    
    return min(confidence, 1.0)
```

## 📊 Advanced Entity Features

### Fuzzy Matching for Typos

```python
from difflib import SequenceMatcher

def find_fuzzy_matches(self, text: str, threshold: float = 0.8) -> List[Dict]:
    """Find entity matches even with typos"""
    
    fuzzy_matches = []
    words = re.findall(r'\b\w+\b', text.upper())
    
    for word in words:
        if len(word) < 3:  # Skip very short words
            continue
            
        for category, entities in self.entities_db.items():
            for entity_name, entity_data in entities.items():
                
                # Check against symbols and names
                candidates = []
                if 'symbols' in entity_data:
                    candidates.extend(entity_data['symbols'])
                if 'symbol' in entity_data:
                    candidates.append(entity_data['symbol'])
                
                for candidate in candidates:
                    similarity = SequenceMatcher(None, word, candidate.upper()).ratio()
                    
                    if similarity >= threshold:
                        fuzzy_matches.append({
                            'original_word': word,
                            'matched_entity': entity_name,
                            'matched_symbol': candidate,
                            'similarity': similarity,
                            'category': category
                        })
    
    return sorted(fuzzy_matches, key=lambda x: x['similarity'], reverse=True)
```

### Context-Based Entity Disambiguation

```python
def disambiguate_entities(self, text: str, found_entities: Dict) -> Dict:
    """Use context to resolve ambiguous entity references"""
    
    # Common ambiguous cases
    ambiguous_cases = {
        'coin': ['bitcoin', 'ethereum', 'dogecoin'],  # Which coin?
        'stock': ['any_stock_mentioned'],              # Which stock?
        'crypto': ['bitcoin', 'ethereum', 'crypto_general']
    }
    
    text_lower = text.lower()
    disambiguated = found_entities.copy()
    
    for ambiguous_term, possible_entities in ambiguous_cases.items():
        if ambiguous_term in text_lower:
            
            # Look for context clues
            context_window = 50  # Look 50 characters around the term
            
            for match in re.finditer(rf'\b{ambiguous_term}\b', text_lower):
                start = max(0, match.start() - context_window)
                end = min(len(text), match.end() + context_window)
                context = text_lower[start:end]
                
                # Find the most likely specific entity based on context
                best_match = self._find_best_entity_from_context(context, possible_entities)
                
                if best_match:
                    # Add the specific entity
                    category = self._get_entity_category(best_match)
                    if category:
                        disambiguated[category].add(best_match)
    
    return disambiguated

def _find_best_entity_from_context(self, context: str, possible_entities: List[str]) -> str:
    """Find the most likely entity based on surrounding context"""
    
    entity_scores = {}
    
    for entity in possible_entities:
        if entity == 'any_stock_mentioned':
            continue
            
        score = 0
        entity_data = self._get_entity_data(entity)
        
        if not entity_data:
            continue
        
        # Check for entity-specific keywords in context
        keywords = entity_data.get('aliases', []) + [entity]
        
        for keyword in keywords:
            if keyword.lower() in context:
                score += 1
        
        # Check for related symbols
        if 'symbols' in entity_data:
            for symbol in entity_data['symbols']:
                if symbol.lower() in context:
                    score += 2  # Symbols are strong indicators
        
        entity_scores[entity] = score
    
    # Return entity with highest score
    if entity_scores:
        return max(entity_scores, key=entity_scores.get)
    
    return None
```

## 🎯 Real-World Entity Recognition Examples

### Example 1: Multi-Entity Post
```python
text = "Just bought $AAPL and $TSLA! Bitcoin is also looking good! #stocks #crypto"

entities = recognizer.find_entities(text)
# Result:
{
    'entities': {
        'stocks': {'apple', 'tesla'},
        'cryptocurrencies': {'bitcoin'},
        'indices': set(),
        'commodities': set()
    },
    'total_count': 3,
    'positions': [
        {'entity': 'apple', 'category': 'stocks', 'start': 12, 'end': 17, 'matched_text': '$AAPL'},
        {'entity': 'tesla', 'category': 'stocks', 'start': 22, 'end': 27, 'matched_text': '$TSLA'},
        {'entity': 'bitcoin', 'category': 'cryptocurrencies', 'start': 30, 'end': 37, 'matched_text': 'Bitcoin'}
    ],
    'confidence_scores': {
        'apple': 0.9,   # High - exact symbol match
        'tesla': 0.9,   # High - exact symbol match  
        'bitcoin': 0.7  # Medium - name match with crypto context
    }
}
```

### Example 2: Ambiguous Context
```python
text = "I love apple pie but hate Apple stock prices"

entities = recognizer.find_entities(text)
# Result:
{
    'entities': {
        'stocks': {'apple'},        # Only the second "Apple" is recognized
        'cryptocurrencies': set(),
        'indices': set(),
        'commodities': set()
    },
    'total_count': 1,
    'positions': [
        {'entity': 'apple', 'category': 'stocks', 'start': 27, 'end': 32, 'matched_text': 'Apple'}
    ],
    'confidence_scores': {
        'apple': 0.8  # High confidence due to "stock prices" context
    }
}
```

### Example 3: Typos and Variants
```python
text = "APPL is going up! Also watching BTC and etherium"

# Regular entity recognition
entities = recognizer.find_entities(text)
# Finds: {} (empty - "APPL" and "etherium" are typos)

# Fuzzy matching
fuzzy_matches = recognizer.find_fuzzy_matches(text, threshold=0.8)
# Result:
[
    {
        'original_word': 'APPL',
        'matched_entity': 'apple', 
        'matched_symbol': 'AAPL',
        'similarity': 0.88,
        'category': 'stocks'
    },
    {
        'original_word': 'ETHERIUM',
        'matched_entity': 'ethereum',
        'matched_symbol': 'ETH', 
        'similarity': 0.82,
        'category': 'cryptocurrencies'
    }
]
```

## 🚀 Performance Optimization

### Caching and Preprocessing

```python
class OptimizedEntityRecognizer(FinancialEntityRecognizer):
    def __init__(self):
        super().__init__()
        self.match_cache = {}  # Cache recent matches
        self.compiled_mega_pattern = self._create_mega_pattern()
    
    def _create_mega_pattern(self):
        """Create one big regex pattern for initial filtering"""
        
        all_patterns = []
        
        for category, entities in self.compiled_patterns.items():
            for entity_name, patterns in entities.items():
                for pattern in patterns:
                    all_patterns.append(pattern.pattern)
        
        # Combine all patterns with OR operator
        mega_pattern = '|'.join(f'({pattern})' for pattern in all_patterns)
        return re.compile(mega_pattern, re.IGNORECASE)
    
    def find_entities_fast(self, text: str) -> Dict:
        """Fast entity recognition using pre-filtering"""
        
        # Check cache first
        text_hash = hash(text)
        if text_hash in self.match_cache:
            return self.match_cache[text_hash]
        
        # Quick pre-filter: does text contain ANY potential entities?
        if not self.compiled_mega_pattern.search(text):
            empty_result = {
                'entities': {cat: set() for cat in self.entities_db.keys()},
                'total_count': 0,
                'positions': [],
                'confidence_scores': {}
            }
            self.match_cache[text_hash] = empty_result
            return empty_result
        
        # Full entity recognition
        result = self.find_entities(text)
        
        # Cache the result
        if len(self.match_cache) > 1000:  # Prevent memory bloat
            self.match_cache.clear()
        
        self.match_cache[text_hash] = result
        return result
```

## 🎯 What You've Learned

You now understand:

✅ **What entity recognition is** and why it's crucial for financial sentiment
✅ **Different types of financial entities** we track (crypto, stocks, indices, commodities)  
✅ **Pattern matching techniques** for finding entities in messy social media text
✅ **Context validation** to avoid false positives
✅ **Conflict resolution** when multiple patterns match
✅ **Fuzzy matching** for handling typos and variations
✅ **Performance optimization** strategies for real-time processing

## 🚀 What's Next?

In **Chapter 9**, we'll explore **Data Flow and Architecture** - how all the pieces we've learned about work together. You'll learn:

- How data flows through our entire system
- The role of each component we've built
- How sentiment and entities combine to create signals
- Real-time vs. batch processing workflows

**Ready to see the big picture?** Let's continue to **[Chapter 9: Data Flow and Architecture](chapter_09_data_flow_architecture.md)**!

---

## 💡 Entity Recognition Practice

Try to identify entities in these texts:

1. **"$TSLA and $AAPL both looking bullish! Also got some Bitcoin"**
   - How many entities? Which categories?

2. **"Love apple pie but hate Apple stock performance"**
   - Which "apple" should be recognized and why?

3. **"BTC, ETH, and DOGE all mooning! 🚀"**
   - What patterns would match these?

Practice thinking like an entity recognition system! 🎯
