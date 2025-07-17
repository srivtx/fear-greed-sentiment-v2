# Chapter 4: Understanding APIs & Data Sources 🌐

## Welcome to the Data World!

Now that you understand the Python basics, let's explore how our system actually gets its data. We'll learn about APIs (don't worry, they're simpler than they sound!) and how we collect information from social media and news sources.

## 🤔 What is an API?

**API = Application Programming Interface**

Think of an API like a **digital waiter** at a restaurant:

### The Restaurant Analogy

**You (our system)** want data
**↓**  
**Waiter (API)** takes your request
**↓**  
**Kitchen (Twitter/Reddit/News)** prepares the data
**↓**  
**Waiter (API)** brings you the data
**↓**  
**You** use the data for analysis

### Real Example: Twitter API

```python
# Instead of going to twitter.com and copying tweets manually...
# We can ask the Twitter API for tweets:

request = "Give me 100 recent tweets about Bitcoin"
twitter_api_response = [
    {"text": "Bitcoin is amazing!", "timestamp": "2024-07-16 10:30"},
    {"text": "BTC going to the moon", "timestamp": "2024-07-16 10:31"},
    # ... 98 more tweets
]
```

**Why APIs are amazing:**
- **Fast:** Get 1000s of tweets in seconds
- **Automated:** No manual copying and pasting
- **Real-time:** Get data as it happens
- **Structured:** Data comes in organized format

## 🔑 API Authentication (Getting Permission)

APIs need to know who you are before giving you data. It's like showing your ID to enter a club.

### API Keys

```python
# Your API credentials (like a membership card)
TWITTER_API_KEY = "abc123def456"
TWITTER_API_SECRET = "secret789xyz"

# Using credentials to get data
headers = {"Authorization": f"Bearer {TWITTER_API_KEY}"}
response = requests.get("https://api.twitter.com/tweets", headers=headers)
```

**In our system:**
```python
# config/config.py
class Config:
    def _load_api_keys_from_env(self):
        # Twitter API credentials
        if os.environ.get("TWITTER_BEARER_TOKEN"):
            self.config["twitter"]["bearer_token"] = os.environ.get("TWITTER_BEARER_TOKEN")
        
        # Reddit API credentials  
        if os.environ.get("REDDIT_CLIENT_ID"):
            self.config["reddit"]["client_id"] = os.environ.get("REDDIT_CLIENT_ID")
```

**Security note:** We store API keys as environment variables (not in code) for security!

## 📱 Twitter: Our Primary Data Source

Twitter is perfect for sentiment analysis because:
- **Real-time:** People tweet reactions instantly
- **Volume:** Millions of tweets per day
- **Financial focus:** Lots of discussion about stocks/crypto
- **Emotional:** People express raw feelings

### What We Collect from Twitter

```python
# Example tweet data we collect
tweet_data = {
    "id": "1234567890",
    "text": "Just bought more $BTC! This dip won't last long! 🚀",
    "created_at": "2024-07-16T10:30:00.000Z",
    "author_id": "987654321",
    "public_metrics": {
        "retweet_count": 5,
        "like_count": 23,
        "reply_count": 3
    },
    "entities": {
        "hashtags": ["HODL", "Bitcoin"],
        "cashtags": ["BTC"]
    }
}
```

### Our Twitter Collection Process

```python
# data_collection/twitter/twitter_collector.py
class TwitterCollector:
    def collect_tweets(self):
        # 1. Connect to Twitter API
        self._authenticate()
        
        # 2. Search for financial keywords
        keywords = ["Bitcoin", "$BTC", "crypto", "stocks", "market"]
        
        # 3. Collect recent tweets
        for keyword in keywords:
            tweets = self._search_tweets(keyword, count=100)
            
            # 4. Save to file
            self._save_tweets(tweets, keyword)
```

**Our search strategy:**
- **Cryptocurrency terms:** Bitcoin, Ethereum, crypto, HODL
- **Stock symbols:** $AAPL, $TSLA, $MSFT
- **Market terms:** bull market, bear market, crash, moon
- **Emotional words:** fear, greed, panic, FOMO

### Twitter API Limits

APIs have limits to prevent abuse:

```python
# Twitter API v2 limits (per 15 minutes)
RATE_LIMITS = {
    "search_tweets": 300,      # 300 requests per 15 mins
    "user_tweets": 300,        # 300 requests per 15 mins  
    "tweet_lookup": 300        # 300 requests per 15 mins
}

# Our handling:
def collect_with_rate_limiting():
    tweets_collected = 0
    
    while tweets_collected < target_count:
        try:
            batch = collect_tweet_batch()
            tweets_collected += len(batch)
        except RateLimitError:
            print("Rate limit hit, waiting 15 minutes...")
            time.sleep(15 * 60)  # Wait 15 minutes
```

## 🔴 Reddit: The Discussion Hub

Reddit provides different insights than Twitter:
- **Longer discussions:** Detailed opinions and analysis
- **Community sentiment:** Subreddit-specific emotions
- **Quality content:** Upvoting system filters good content

### Key Subreddits We Monitor

```python
# Financial subreddits we collect from
SUBREDDITS = [
    "CryptoCurrency",      # General crypto discussion
    "Bitcoin",             # Bitcoin-specific
    "ethereum",            # Ethereum community
    "wallstreetbets",      # High-risk stock trading
    "investing",           # General investing
    "stocks",              # Stock market discussion
    "SecurityAnalysis",    # Fundamental analysis
    "ValueInvesting"       # Long-term investing
]
```

### What We Collect from Reddit

```python
# Example Reddit post data
post_data = {
    "id": "abc123",
    "title": "Why Bitcoin will hit $100K this year",
    "selftext": "Here's my analysis of why BTC is going to moon...",
    "score": 245,          # Upvotes minus downvotes
    "upvote_ratio": 0.87,  # 87% upvoted
    "num_comments": 156,
    "created_utc": 1642345678,
    "subreddit": "Bitcoin",
    "author": "crypto_analyst_2024"
}

# Comments on the post
comment_data = {
    "id": "def456", 
    "body": "Totally agree! Just bought more BTC!",
    "score": 23,
    "created_utc": 1642345800,
    "parent_id": "abc123"
}
```

### Our Reddit Collection Process

```python
# data_collection/reddit/reddit_collector.py
class RedditCollector:
    def collect_posts(self):
        # 1. Connect to Reddit API (PRAW)
        reddit = praw.Reddit(
            client_id=self.config["reddit"]["client_id"],
            client_secret=self.config["reddit"]["client_secret"],
            user_agent="fear_greed_engine v0.1.0"
        )
        
        # 2. Collect from each subreddit
        for subreddit_name in self.subreddits:
            subreddit = reddit.subreddit(subreddit_name)
            
            # Get hot posts (trending discussions)
            hot_posts = subreddit.hot(limit=50)
            
            # Get new posts (latest content)
            new_posts = subreddit.new(limit=50)
            
            # 3. Save posts and comments
            self._save_posts_and_comments(hot_posts, new_posts)
```

**Why Reddit is valuable:**
- **Quality filtering:** Upvoted content tends to be better
- **Community consensus:** Subreddit sentiment reflects group thinking
- **Detailed analysis:** People write longer, more thoughtful posts

## 📰 News Sources: The Information Flow

News provides different perspective than social media:
- **Professional analysis:** Journalist and expert opinions
- **Breaking news:** Major events that impact markets
- **Regulatory updates:** Government and policy changes

### News APIs We Use

```python
# News sources and their focus
NEWS_SOURCES = {
    "NewsAPI": {
        "url": "https://newsapi.org/v2/everything",
        "sources": ["reuters", "bloomberg", "cnbc", "marketwatch"],
        "keywords": ["bitcoin", "cryptocurrency", "stock market", "economy"]
    },
    
    "Financial_APIs": {
        "alpha_vantage": "Market data and news",
        "finnhub": "Real-time financial news", 
        "yahoo_finance": "Market news and analysis"
    }
}
```

### What We Collect from News

```python
# Example news article data
article_data = {
    "title": "Bitcoin Reaches New All-Time High Amid Institutional Interest",
    "description": "Major corporations continue to add Bitcoin to their balance sheets...",
    "content": "Full article text here...",
    "url": "https://reuters.com/bitcoin-ath-2024",
    "source": "Reuters",
    "publishedAt": "2024-07-16T09:15:00Z",
    "author": "Financial Reporter"
}
```

### Our News Collection Process

```python
# data_collection/news/news_collector.py
class NewsCollector:
    def collect_news(self):
        # 1. Define search terms
        financial_keywords = [
            "bitcoin cryptocurrency",
            "stock market crash", 
            "federal reserve interest rates",
            "inflation economic indicators"
        ]
        
        # 2. Collect from multiple sources
        for keyword in financial_keywords:
            articles = self._search_news(keyword, days_back=1)
            
            # 3. Filter for relevant content
            relevant_articles = self._filter_financial_news(articles)
            
            # 4. Save articles
            self._save_articles(relevant_articles, keyword)
```

## 💹 Market Data: The Reality Check

We also collect actual market data to compare sentiment with reality:

### Financial Data Sources

```python
# Market data we collect
MARKET_DATA = {
    "yfinance": {
        "stocks": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
        "crypto": ["BTC-USD", "ETH-USD", "XRP-USD"],
        "indices": ["^GSPC", "^IXIC", "^DJI"]  # S&P 500, NASDAQ, Dow
    },
    
    "crypto_exchanges": {
        "binance": "Real-time crypto prices",
        "coinbase": "US crypto market data"
    }
}
```

### What We Track

```python
# Example market data
market_data = {
    "symbol": "BTC-USD",
    "price": 65432.50,
    "change": +1234.50,
    "change_percent": +1.92,
    "volume": 28500000000,
    "market_cap": 1280000000000,
    "timestamp": "2024-07-16T10:30:00Z"
}
```

## 🔄 How We Coordinate Data Collection

Our system collects data from all sources in a coordinated way:

```python
# data_collection/collector.py  
class DataCollector:
    def run_collection_cycle(self, skip_twitter=False):
        """Run one complete data collection cycle"""
        
        # Create timestamped directory
        collection_dir = Path(f"data/collection_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        collection_dir.mkdir(parents=True, exist_ok=True)
        
        # Collect from all sources
        if not skip_twitter:
            logger.info("Collecting Twitter data...")
            self._collect_twitter_data(collection_dir)
        
        logger.info("Collecting Reddit data...")
        self._collect_reddit_data(collection_dir)
        
        logger.info("Collecting news data...")
        self._collect_news_data(collection_dir)
        
        logger.info("Collecting market data...")
        self._collect_market_data(collection_dir)
        
        return collection_dir
```

### Collection Schedule

```python
# How often we collect data
COLLECTION_SCHEDULE = {
    "twitter": "Every 15 minutes",    # High frequency for real-time sentiment
    "reddit": "Every 30 minutes",    # Moderate frequency for discussions
    "news": "Every 60 minutes",      # Lower frequency for breaking news
    "market_data": "Every 5 minutes" # High frequency for price tracking
}
```

## 📁 How We Store Collected Data

Our system organizes data in a logical structure:

```
data/
├── collection_20240716_103000/    # Timestamped collection
│   ├── twitter_data.json          # Twitter posts
│   ├── twitter_entities.json      # Extracted entities from Twitter
│   ├── reddit_posts.json          # Reddit posts
│   ├── reddit_comments.json       # Reddit comments  
│   ├── news_articles.json         # News articles
│   └── market_data.json           # Price and volume data
├── collection_20240716_104500/    # Next collection
└── collection_20240716_110000/    # And so on...
```

### Data Format Example

```python
# twitter_data.json format
{
    "collection_timestamp": "2024-07-16T10:30:00Z",
    "source": "twitter",
    "tweet_count": 1247,
    "tweets": [
        {
            "id": "1234567890",
            "text": "Bitcoin is going to the moon! 🚀",
            "created_at": "2024-07-16T10:29:45Z", 
            "author_id": "987654321",
            "metrics": {"likes": 23, "retweets": 5},
            "entities": {"cashtags": ["BTC"], "hashtags": ["HODL"]}
        },
        // ... more tweets
    ]
}
```

## 🚫 Handling API Errors and Limitations

Real-world APIs have problems. Our system handles them gracefully:

### Common Issues and Solutions

```python
def robust_api_call(api_function, max_retries=3):
    """Make API calls with error handling and retries"""
    
    for attempt in range(max_retries):
        try:
            return api_function()
            
        except requests.exceptions.ConnectionError:
            logger.warning(f"Connection error, attempt {attempt + 1}")
            time.sleep(2 ** attempt)  # Exponential backoff
            
        except requests.exceptions.Timeout:
            logger.warning(f"Request timeout, attempt {attempt + 1}")
            time.sleep(1)
            
        except Exception as e:
            if "rate limit" in str(e).lower():
                logger.info("Rate limit hit, waiting...")
                time.sleep(15 * 60)  # Wait 15 minutes
            else:
                logger.error(f"API error: {e}")
                break
    
    logger.error("All API attempts failed")
    return None
```

### Fallback Strategies

```python
def collect_data_with_fallbacks():
    """Collect data with multiple fallback options"""
    
    # Try primary data source
    data = collect_from_primary_api()
    if data:
        return data
    
    # Try secondary source
    logger.warning("Primary API failed, trying secondary...")
    data = collect_from_secondary_api()
    if data:
        return data
    
    # Use cached data as last resort
    logger.warning("All APIs failed, using cached data...")
    return load_cached_data()
```

## 🎯 Quality Control and Filtering

Not all data is useful. We filter for quality:

### Text Quality Filters

```python
def is_quality_text(text):
    """Filter out low-quality text"""
    
    # Remove very short texts
    if len(text.split()) < 3:
        return False
    
    # Remove mostly non-English text
    if not is_english(text):
        return False
        
    # Remove spam patterns
    if is_spam(text):
        return False
        
    # Remove bot-like content
    if is_bot_content(text):
        return False
    
    return True
```

### Relevance Filters

```python
def is_financially_relevant(text):
    """Check if text is relevant to financial markets"""
    
    financial_keywords = [
        "bitcoin", "cryptocurrency", "stock", "market", "trading",
        "investment", "portfolio", "bull", "bear", "crash", "moon"
    ]
    
    text_lower = text.lower()
    keyword_count = sum(1 for keyword in financial_keywords if keyword in text_lower)
    
    return keyword_count >= 1  # At least one financial keyword
```

## 🔄 Real-Time vs Batch Processing

Our system handles both approaches:

### Real-Time Processing
```python
def real_time_collection():
    """Continuously collect and process data"""
    
    while True:
        # Collect small batches frequently
        new_tweets = collect_recent_tweets(count=50)
        new_reddit_posts = collect_recent_posts(count=20)
        
        # Process immediately
        if new_tweets or new_reddit_posts:
            quick_sentiment_analysis(new_tweets + new_reddit_posts)
            update_fear_greed_index()
        
        # Wait before next collection
        time.sleep(5 * 60)  # 5 minutes
```

### Batch Processing
```python
def batch_collection():
    """Collect large amounts of data periodically"""
    
    # Collect comprehensive dataset
    all_tweets = collect_tweets(count=5000)
    all_reddit_posts = collect_reddit_posts(count=1000)
    all_news = collect_news_articles(count=500)
    
    # Process everything at once
    comprehensive_analysis(all_tweets + all_reddit_posts + all_news)
    generate_detailed_reports()
```

## 🎯 What You've Learned

You now understand:

✅ **What APIs are** and how they work (digital waiters)
✅ **Authentication** and API keys for access
✅ **Twitter data collection** and why it's valuable
✅ **Reddit data collection** for community sentiment
✅ **News data collection** for professional analysis  
✅ **Market data collection** for reality checks
✅ **Data organization** and storage structure
✅ **Error handling** and fallback strategies
✅ **Quality control** and filtering techniques

## 🚀 What's Next?

In **Chapter 5**, we'll dive into **Natural Language Processing (NLP)** - how our system actually understands and processes human language. You'll learn:

- How computers "read" and understand text
- Text preprocessing and why it's necessary
- Tokenization, stemming, and lemmatization explained simply
- How we prepare text for sentiment analysis

**Ready to learn how computers understand language?** Let's continue to **[Chapter 5: Introduction to NLP](chapter_05_intro_to_nlp.md)**!

---

## 💡 Practice Exercise

Visit these websites and notice how they display data that's probably coming from APIs:

1. **Twitter.com** - Notice how tweets load automatically as you scroll
2. **Reddit.com** - See how posts and comments are organized  
3. **Yahoo Finance** - Look at real-time stock prices updating
4. **CoinMarketCap** - Watch cryptocurrency prices change live

Think about:
- How much manual work it would take to copy all this data by hand
- How APIs make it possible to collect thousands of data points automatically
- Why real-time data is valuable for sentiment analysis

This will help you appreciate the power of APIs in our system! 🌐
