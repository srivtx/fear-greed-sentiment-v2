# Chapter 3: Python & Programming Basics 🐍

## Welcome to the Technical Side!

Now that you understand **what** our system does, let's learn **how** it does it. Don't worry if you're new to programming - we'll start with the basics and focus only on what you need to understand our Fear & Greed Engine!

## 🤷‍♀️ "But I Don't Know How to Code!"

**That's perfectly fine!** This chapter will teach you:
- Only the Python concepts you need for our project
- How to read and understand our code (even if you don't write it yourself)
- What each library does and why we use it
- Basic patterns used throughout our system

**Think of this as learning to read a foreign language, not necessarily speak it fluently.**

## 🐍 What is Python?

Python is a programming language that's:
- **Easy to read** (looks almost like English)
- **Popular for data analysis** (perfect for our sentiment analysis)
- **Has lots of libraries** (pre-built tools we can use)
- **Great for beginners** (you'll see why!)

### Python vs. Other Languages

```python
# Python (easy to read)
if sentiment_score > 0.5:
    print("This is positive sentiment!")

# Compare to other languages (harder to read)
// Java
if (sentimentScore > 0.5) {
    System.out.println("This is positive sentiment!");
}
```

See how Python looks more like English? That's why we chose it!

## 🔧 Essential Python Concepts for Our Project

### 1. Variables (Storing Information)

Think of variables like labeled boxes that hold information:

```python
# Storing different types of information
tweet_text = "I love Bitcoin! 🚀"  # Text (string)
sentiment_score = 0.8              # Number (float)
total_tweets = 1000               # Whole number (integer)
is_positive = True                # True/False (boolean)
```

**In our system:**
- `tweet_text` stores the actual tweet we're analyzing
- `sentiment_score` stores how positive/negative it is (-1 to +1)
- `total_tweets` counts how many we've processed
- `is_positive` tracks if sentiment is good or bad

### 2. Lists (Collections of Things)

Lists hold multiple items, like a shopping list:

```python
# A list of tweets to analyze
tweets = [
    "Bitcoin is amazing!",
    "I hate this market crash",
    "Ethereum looks promising",
    "Selling all my stocks"
]

# A list of sentiment scores
scores = [0.8, -0.6, 0.4, -0.7]

# Access individual items
first_tweet = tweets[0]  # "Bitcoin is amazing!"
first_score = scores[0]  # 0.8
```

**In our system:**
- We store hundreds of tweets in lists
- We store their sentiment scores in matching lists
- We process them one by one

### 3. Dictionaries (Labeled Information)

Dictionaries store information with labels, like a phone book:

```python
# Information about a single tweet
tweet_data = {
    "text": "Bitcoin is going to the moon! 🚀",
    "sentiment_score": 0.9,
    "source": "twitter",
    "timestamp": "2024-07-16 10:30:00",
    "mentions": ["Bitcoin"]
}

# Access specific information
text = tweet_data["text"]           # "Bitcoin is going to the moon! 🚀"
score = tweet_data["sentiment_score"]  # 0.9
```

**In our system:**
- Each tweet is stored as a dictionary with all its information
- We can easily find specific data we need
- Makes the code organized and readable

### 4. Functions (Reusable Code Blocks)

Functions are like recipes - you define them once and use them many times:

```python
# Define a function to analyze sentiment
def analyze_sentiment(text):
    """
    This function takes text and returns a sentiment score
    """
    # ... analysis code here ...
    return sentiment_score

# Use the function
tweet = "I love this stock!"
score = analyze_sentiment(tweet)  # Returns 0.8
```

**In our system:**
- `analyze_sentiment()` processes text and returns scores
- `collect_tweets()` gathers data from Twitter
- `calculate_fear_greed_index()` computes our final index

### 5. Classes (Blueprints for Objects)

Classes are like blueprints for creating objects with specific capabilities:

```python
# Define a class (blueprint)
class SentimentAnalyzer:
    def __init__(self):
        """Set up the analyzer when created"""
        self.positive_words = ["love", "amazing", "great"]
        self.negative_words = ["hate", "terrible", "awful"]
    
    def analyze(self, text):
        """Analyze text and return sentiment score"""
        # ... analysis logic here ...
        return score

# Create an analyzer object (from the blueprint)
analyzer = SentimentAnalyzer()

# Use it to analyze text
score = analyzer.analyze("I love Bitcoin!")  # Returns positive score
```

**In our system:**
- `SentimentAnalyzer` class handles all sentiment analysis
- `DataCollector` class handles gathering data from APIs
- `FearGreedEngine` class coordinates everything

## 📚 Key Libraries We Use

Our system uses pre-built libraries (tools) that others have created. Think of them as specialized toolboxes:

### 1. **pandas** 📊 (Data Manipulation)

**What it does:** Handles spreadsheet-like data (tables of information)

```python
import pandas as pd

# Create a table of tweet data
data = {
    'tweet': ['Bitcoin rocks!', 'Market is crashing'],
    'sentiment': [0.8, -0.6],
    'source': ['twitter', 'reddit']
}
df = pd.DataFrame(data)

# Now we can easily:
positive_tweets = df[df['sentiment'] > 0]  # Filter positive tweets
average_sentiment = df['sentiment'].mean()  # Calculate average
```

**Why we use it:**
- Perfect for handling thousands of tweets and scores
- Easy filtering, sorting, and calculations
- Can save/load data from files

### 2. **numpy** 🔢 (Math Operations)

**What it does:** Handles mathematical operations on large amounts of numbers

```python
import numpy as np

# List of sentiment scores
scores = [0.8, -0.3, 0.5, -0.1, 0.9]

# Calculate statistics quickly
average = np.mean(scores)      # 0.36
std_dev = np.std(scores)       # 0.49
maximum = np.max(scores)       # 0.9
```

**Why we use it:**
- Super fast mathematical calculations
- Statistical functions we need for analysis
- Works great with pandas

### 3. **requests** 🌐 (Web Requests)

**What it does:** Fetches data from websites and APIs

```python
import requests

# Get data from Twitter API
response = requests.get("https://api.twitter.com/tweets", 
                       headers={"Authorization": "Bearer token"})
tweets = response.json()  # Convert response to Python data
```

**Why we use it:**
- Communicates with Twitter, Reddit, News APIs
- Downloads web content for analysis
- Handles authentication and errors

### 4. **NLTK** 📝 (Natural Language Processing)

**What it does:** Provides tools for processing human language

```python
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Create sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Analyze text
scores = analyzer.polarity_scores("I love this stock!")
# Returns: {'neg': 0.0, 'neu': 0.323, 'pos': 0.677, 'compound': 0.6369}
```

**Why we use it:**
- VADER sentiment analyzer (specifically designed for social media)
- Text preprocessing tools
- Language processing utilities

### 5. **matplotlib/seaborn** 📈 (Visualization)

**What it does:** Creates charts and graphs

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Create a simple chart
sentiment_scores = [0.8, -0.3, 0.5, -0.1, 0.9]
plt.plot(sentiment_scores)
plt.title("Sentiment Over Time")
plt.show()
```

**Why we use it:**
- Creates our Fear & Greed gauge
- Generates sentiment trend charts
- Visualizes results for easy understanding

## 🏗️ How Our Code is Organized

Our project follows a logical structure. Think of it like organizing a house:

```
fear-greed-sentiment-v2/
├── 🏠 main.py                 # Front door (main entry point)
├── 🏠 engine.py               # Control center (coordinates everything)
├── 📁 config/                 # Settings and configuration
├── 📁 data_collection/        # Kitchen (where we gather ingredients)
│   ├── twitter/
│   ├── reddit/
│   └── news/
├── 📁 sentiment_analysis/     # Workshop (where we process data)
│   ├── analyzer.py
│   ├── preprocessor.py
│   └── sentiment_analyzer.py
├── 📁 signal_generation/      # Office (where we make decisions)
└── 📁 utils/                  # Garage (tools and utilities)
```

### 1. **main.py** - The Front Door
This is where everything starts:

```python
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    
    # Create the main engine
    engine = FearGreedEngine()
    
    # Run the system
    if args.mode == "run":
        engine.run_once()
```

**What it does:**
- Handles command-line options
- Creates the main engine
- Starts the analysis process

### 2. **engine.py** - The Control Center
This coordinates all components:

```python
class FearGreedEngine:
    def __init__(self):
        self.collector = DataCollector()
        self.analyzer = SentimentAnalysisEngine()
        self.signal_generator = SignalGenerator()
    
    def run_once(self):
        # Step 1: Collect data
        collection_dir = self.collector.run_collection_cycle()
        
        # Step 2: Analyze sentiment
        sentiment_dir = self.analyzer.run(collection_dir)
        
        # Step 3: Generate signals
        signals = self.signal_generator.generate_signals(sentiment_dir)
```

**What it does:**
- Manages the entire pipeline
- Coordinates data collection, analysis, and signal generation
- Handles errors and scheduling

### 3. **Data Collection Modules**
These gather information from various sources:

```python
class TwitterCollector:
    def collect_tweets(self):
        # Connect to Twitter API
        # Search for relevant tweets
        # Save tweets to files
        
class RedditCollector:
    def collect_posts(self):
        # Connect to Reddit API
        # Get posts from financial subreddits
        # Save posts to files
```

### 4. **Sentiment Analysis Modules**
These process and analyze the collected text:

```python
class SentimentAnalysisEngine:
    def run(self, data_dir):
        # Load collected text data
        # Analyze sentiment of each piece
        # Calculate Fear & Greed Index
        # Save results
```

## 🔄 How Data Flows Through Our System

Think of our system like a factory assembly line:

```
📱 Social Media Posts
    ↓
🔍 Data Collection (APIs)
    ↓ 
🧹 Text Preprocessing (Clean & Prepare)
    ↓
🧠 Sentiment Analysis (VADER)
    ↓
🎯 Entity Recognition (Find Bitcoin, Apple, etc.)
    ↓
📊 Aggregation (Combine all scores)
    ↓
📈 Fear & Greed Index (0-100 scale)
    ↓
💰 Trading Signals (Buy/Sell recommendations)
    ↓
📋 Results & Visualizations
```

### Example: Processing One Tweet

Let's follow a single tweet through our system:

**1. Input:**
```
Raw tweet: "Just bought more $BTC! This dip won't last long! 🚀📈 #HODL"
```

**2. Data Collection:**
```python
tweet_data = {
    "text": "Just bought more $BTC! This dip won't last long! 🚀📈 #HODL",
    "source": "twitter",
    "timestamp": "2024-07-16 10:30:00",
    "user": "crypto_trader_123"
}
```

**3. Text Preprocessing:**
```python
# Clean the text
cleaned_text = "just bought more btc this dip wont last long hodl"
```

**4. Sentiment Analysis:**
```python
sentiment_scores = {
    'compound': 0.7269,    # Overall positive
    'pos': 0.746,          # 74.6% positive
    'neu': 0.254,          # 25.4% neutral  
    'neg': 0.0             # 0% negative
}
```

**5. Entity Recognition:**
```python
entities = {
    "cryptos": ["BTC"],
    "stocks": [],
    "indices": []
}
```

**6. Result:**
```python
processed_tweet = {
    "original_text": "Just bought more $BTC! This dip won't last long! 🚀📈 #HODL",
    "sentiment_score": 0.7269,
    "sentiment_label": "positive", 
    "entities_mentioned": ["BTC"],
    "source": "twitter",
    "timestamp": "2024-07-16 10:30:00"
}
```

This single tweet now contributes to:
- Overall market sentiment
- Bitcoin-specific sentiment  
- The Fear & Greed Index calculation

## 🎯 Common Programming Patterns in Our Code

### 1. **Error Handling**
Our code gracefully handles problems:

```python
try:
    # Try to collect tweets
    tweets = collect_tweets_from_api()
except ConnectionError:
    # If internet fails, use cached data
    print("Using cached tweets due to connection error")
    tweets = load_cached_tweets()
```

### 2. **Configuration Management**
Settings are stored in one place:

```python
# config/config.py
class Config:
    def __init__(self):
        self.twitter_api_key = "your_api_key"
        self.sentiment_threshold = 0.1
        self.max_tweets_per_hour = 1000
```

### 3. **Logging**
We track what the system is doing:

```python
import logging

logger = logging.getLogger(__name__)

def analyze_sentiment(text):
    logger.info(f"Analyzing sentiment for text: {text[:50]}...")
    # ... analysis code ...
    logger.info(f"Sentiment score: {score}")
```

### 4. **Data Persistence**
We save results to files:

```python
import json

# Save results
with open("sentiment_results.json", "w") as f:
    json.dump(results, f)

# Load results later
with open("sentiment_results.json", "r") as f:
    results = json.load(f)
```

## 🎓 Reading Our Code: A Practical Example

Let's look at a simplified version of our sentiment analysis function:

```python
def analyze_sentiment(text):
    """
    Analyze sentiment of input text
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Sentiment scores and metadata
    """
    # Handle empty input
    if not text or len(text.strip()) == 0:
        return {"sentiment": 0.0, "confidence": 0.0}
    
    # Clean the text
    cleaned_text = preprocess_text(text)
    
    # Analyze sentiment using VADER
    scores = vader_analyzer.polarity_scores(cleaned_text)
    
    # Extract entities (Bitcoin, Apple, etc.)
    entities = extract_entities(cleaned_text)
    
    # Return structured result
    return {
        "original_text": text,
        "cleaned_text": cleaned_text,
        "sentiment_score": scores['compound'],
        "positive": scores['pos'],
        "negative": scores['neg'],
        "neutral": scores['neu'],
        "entities": entities,
        "confidence": calculate_confidence(scores, text)
    }
```

**How to read this:**
1. **Function signature:** `analyze_sentiment(text)` - takes text input
2. **Docstring:** Explains what the function does
3. **Error handling:** Checks for empty input
4. **Processing steps:** Clean → Analyze → Extract → Return
5. **Return value:** Dictionary with all results

You don't need to write this code, but understanding how to read it helps you:
- Understand what each part does
- Modify settings and parameters
- Debug issues when they arise
- Add new features

## 🎯 What You've Learned

You now understand:

✅ **Basic Python concepts** used in our project
✅ **Key libraries** and what each one does
✅ **Code organization** and project structure
✅ **Data flow** through our system
✅ **Common patterns** in our codebase
✅ **How to read** our functions and classes

## 🚀 What's Next?

In **Chapter 4**, we'll explore **APIs & Data Sources** - how our system connects to Twitter, Reddit, and news websites to gather the data we analyze. You'll learn:

- What APIs are and how they work (think of them as digital waiters)
- How we authenticate and connect to different services
- What data we collect and why
- Rate limits and how we handle them

**Ready to learn how we gather our data?** Let's continue to **[Chapter 4: Understanding APIs & Data Sources](chapter_04_apis_data_sources.md)**!

---

## 💡 Quick Code Reading Exercise

Look at this simplified function and see if you can understand what it does:

```python
def calculate_fear_greed_index(sentiment_scores):
    """Calculate Fear & Greed Index from sentiment scores"""
    
    # Count positive and negative scores
    positive_count = sum(1 for score in sentiment_scores if score > 0.1)
    negative_count = sum(1 for score in sentiment_scores if score < -0.1)
    total_count = len(sentiment_scores)
    
    # Calculate percentages
    positive_pct = (positive_count / total_count) * 100
    negative_pct = (negative_count / total_count) * 100
    
    # Convert to 0-100 scale
    if positive_pct > negative_pct:
        index = 50 + (positive_pct - negative_pct) / 2
    else:
        index = 50 - (negative_pct - positive_pct) / 2
    
    return max(0, min(100, index))  # Keep between 0-100
```

**Can you figure out:**
1. What this function takes as input?
2. What it calculates?
3. What it returns?

**Answers:** 
1. A list of sentiment scores
2. The percentage of positive vs negative sentiment
3. A Fear & Greed Index value between 0-100

Great job! You're getting the hang of reading code! 🎉
