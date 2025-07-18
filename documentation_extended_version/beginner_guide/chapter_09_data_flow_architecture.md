# Chapter 9: Data Flow and Architecture - How Everything Works Together 🏗️

## Welcome to the Big Picture!

You've learned about collecting data, cleaning text, analyzing sentiment, and finding entities. Now let's see how all these pieces fit together like a well-orchestrated symphony! Think of this chapter as getting the blueprint of our entire system.

## 🌊 The Complete Data Flow Journey

Imagine following a single tweet from the moment someone posts it until it becomes a Fear & Greed signal. Here's that incredible journey:

### The Data Journey: From Tweet to Trading Signal

```
📱 Tweet Posted: "Bitcoin is AMAZING! 🚀"
                    ⬇️
🔄 Data Collection: Twitter API captures the tweet
                    ⬇️
🧹 Text Preprocessing: Clean and normalize the text
                    ⬇️
🎯 Entity Recognition: Identifies "Bitcoin" 
                    ⬇️
😊 Sentiment Analysis: Calculates positive sentiment (0.8)
                    ⬇️
📊 Signal Generation: Combines with other data
                    ⬇️
📈 Fear & Greed Index: Updates the overall market sentiment
                    ⬇️
💹 Trading Signal: "Bullish sentiment detected for Bitcoin"
```

This happens thousands of times per minute for different posts!

## 🏗️ System Architecture Overview

Our system is like a factory with different specialized departments:

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FEAR & GREED SENTIMENT ENGINE                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐     │
│  │   DATA      │    │  PROCESSING  │    │    ANALYSIS     │     │
│  │ COLLECTION  │───▶│    LAYER     │───▶│     LAYER       │     │
│  └─────────────┘    └──────────────┘    └─────────────────┘     │
│         │                   │                      │            │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐     │
│  │  EXTERNAL   │    │   STORAGE    │    │     OUTPUT      │     │
│  │    APIs     │    │   & CACHE    │    │   & SIGNALS     │     │
│  └─────────────┘    └──────────────┘    └─────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Each Layer Explained

**1. Data Collection Layer**
- Twitter API client
- Reddit API client  
- News API client
- Market data collector

**2. Processing Layer**
- Text preprocessor
- Entity recognizer
- Sentiment analyzer
- Data validator

**3. Analysis Layer**
- Signal generator
- Correlation analyzer
- Fear & Greed calculator
- Trend detector

**4. Storage & Cache**
- Raw data storage
- Processed data cache
- Historical signals
- Configuration

**5. Output Layer**
- Real-time signals
- Visualization data
- API endpoints
- Alerts/notifications

## 🎯 Detailed Component Architecture

### Core Engine Structure

```python
class FearGreedSentimentEngine:
    """Main orchestrator that coordinates all components"""
    
    def __init__(self, config_path: str):
        # Initialize all components
        self.config = self._load_config(config_path)
        
        # Data Collection Components
        self.twitter_collector = TwitterCollector(self.config)
        self.reddit_collector = RedditCollector(self.config)
        self.news_collector = NewsCollector(self.config)
        self.market_collector = MarketDataCollector(self.config)
        
        # Processing Components
        self.text_preprocessor = TextPreprocessor()
        self.entity_recognizer = FinancialEntityRecognizer()
        self.sentiment_analyzer = FinancialSentimentAnalyzer()
        
        # Analysis Components
        self.signal_generator = SignalGenerator(self.config)
        self.fear_greed_calculator = FearGreedCalculator()
        
        # Storage Components
        self.data_storage = DataStorage(self.config)
        self.cache_manager = CacheManager()
        
        # Output Components
        self.visualizer = DataVisualizer()
        self.alert_manager = AlertManager(self.config)
        
        self.logger = logging.getLogger(__name__)
    
    def run_analysis_cycle(self):
        """Execute one complete analysis cycle"""
        
        self.logger.info("Starting analysis cycle")
        
        try:
            # Step 1: Collect fresh data
            raw_data = self._collect_all_data()
            
            # Step 2: Process the data
            processed_data = self._process_raw_data(raw_data)
            
            # Step 3: Generate signals
            signals = self._generate_signals(processed_data)
            
            # Step 4: Calculate Fear & Greed Index
            fear_greed_score = self._calculate_fear_greed(signals)
            
            # Step 5: Store results and send alerts
            self._store_and_notify(signals, fear_greed_score)
            
            self.logger.info(f"Analysis cycle completed. F&G Score: {fear_greed_score}")
            
        except Exception as e:
            self.logger.error(f"Analysis cycle failed: {e}")
            raise
```

### Data Collection Orchestration

```python
def _collect_all_data(self) -> Dict:
    """Coordinate data collection from all sources"""
    
    self.logger.info("Collecting data from all sources")
    
    # Define what to collect
    collection_tasks = {
        'twitter_posts': self._collect_twitter_data,
        'reddit_posts': self._collect_reddit_data,
        'news_articles': self._collect_news_data,
        'market_data': self._collect_market_data
    }
    
    collected_data = {}
    collection_stats = {}
    
    for source_name, collection_func in collection_tasks.items():
        try:
            start_time = time.time()
            
            # Collect data from this source
            source_data = collection_func()
            
            # Store results
            collected_data[source_name] = source_data
            collection_stats[source_name] = {
                'count': len(source_data) if isinstance(source_data, list) else 1,
                'duration': time.time() - start_time,
                'status': 'success'
            }
            
            self.logger.info(f"Collected {collection_stats[source_name]['count']} items from {source_name}")
            
        except Exception as e:
            collection_stats[source_name] = {
                'count': 0,
                'duration': time.time() - start_time,
                'status': 'failed',
                'error': str(e)
            }
            
            self.logger.warning(f"Failed to collect from {source_name}: {e}")
            collected_data[source_name] = []
    
    # Add collection metadata
    collected_data['_metadata'] = {
        'collection_time': datetime.now(),
        'stats': collection_stats,
        'total_items': sum(stats.get('count', 0) for stats in collection_stats.values())
    }
    
    return collected_data

def _collect_twitter_data(self) -> List[Dict]:
    """Collect Twitter data with rate limiting and error handling"""
    
    # Define search terms based on config
    search_terms = self.config.get('twitter_search_terms', [
        'Bitcoin', 'BTC', '$BTC',
        'Tesla', 'TSLA', '$TSLA',
        'Apple', 'AAPL', '$AAPL'
    ])
    
    all_tweets = []
    
    for term in search_terms:
        try:
            # Respect rate limits
            tweets = self.twitter_collector.search_tweets(
                query=term,
                count=self.config.get('twitter_batch_size', 100),
                since_id=self.cache_manager.get_last_twitter_id(term)
            )
            
            all_tweets.extend(tweets)
            
            # Update cache with latest ID
            if tweets:
                latest_id = max(tweet['id'] for tweet in tweets)
                self.cache_manager.set_last_twitter_id(term, latest_id)
            
        except Exception as e:
            self.logger.warning(f"Failed to collect tweets for '{term}': {e}")
            continue
    
    return all_tweets
```

### Data Processing Pipeline

```python
def _process_raw_data(self, raw_data: Dict) -> Dict:
    """Process all collected data through analysis pipeline"""
    
    self.logger.info("Processing raw data")
    
    processed_data = {
        'posts': [],           # All processed social media posts
        'news': [],            # All processed news articles
        'market_data': {},     # Market price/volume data
        'entities_found': {},  # Summary of entities found
        'processing_stats': {}
    }
    
    processing_stats = {}
    
    # Process Twitter posts
    if 'twitter_posts' in raw_data:
        start_time = time.time()
        processed_tweets = self._process_social_media_posts(
            raw_data['twitter_posts'], 
            source='twitter'
        )
        processed_data['posts'].extend(processed_tweets)
        
        processing_stats['twitter'] = {
            'raw_count': len(raw_data['twitter_posts']),
            'processed_count': len(processed_tweets),
            'duration': time.time() - start_time
        }
    
    # Process Reddit posts
    if 'reddit_posts' in raw_data:
        start_time = time.time()
        processed_reddit = self._process_social_media_posts(
            raw_data['reddit_posts'],
            source='reddit'
        )
        processed_data['posts'].extend(processed_reddit)
        
        processing_stats['reddit'] = {
            'raw_count': len(raw_data['reddit_posts']),
            'processed_count': len(processed_reddit),
            'duration': time.time() - start_time
        }
    
    # Process news articles
    if 'news_articles' in raw_data:
        start_time = time.time()
        processed_news = self._process_news_articles(raw_data['news_articles'])
        processed_data['news'].extend(processed_news)
        
        processing_stats['news'] = {
            'raw_count': len(raw_data['news_articles']),
            'processed_count': len(processed_news),
            'duration': time.time() - start_time
        }
    
    # Process market data
    if 'market_data' in raw_data:
        processed_data['market_data'] = raw_data['market_data']
    
    # Generate entity summary
    processed_data['entities_found'] = self._summarize_entities(processed_data['posts'])
    processed_data['processing_stats'] = processing_stats
    
    self.logger.info(f"Processed {len(processed_data['posts'])} posts and {len(processed_data['news'])} articles")
    
    return processed_data

def _process_social_media_posts(self, posts: List[Dict], source: str) -> List[Dict]:
    """Process social media posts through the full pipeline"""
    
    processed_posts = []
    
    for post in posts:
        try:
            # Extract text content
            text = self._extract_text_content(post, source)
            
            if not text or len(text.strip()) < 10:  # Skip very short posts
                continue
            
            # Step 1: Preprocess text
            preprocessed_text = self.text_preprocessor.preprocess(text)
            
            # Step 2: Find entities
            entities = self.entity_recognizer.find_entities(text)
            
            # Step 3: Analyze sentiment
            sentiment = self.sentiment_analyzer.analyze_complete_sentiment(preprocessed_text)
            
            # Step 4: Extract metadata
            metadata = self._extract_post_metadata(post, source)
            
            # Step 5: Create processed post record
            processed_post = {
                'id': post.get('id'),
                'source': source,
                'original_text': text,
                'preprocessed_text': preprocessed_text,
                'entities': entities,
                'sentiment': sentiment,
                'metadata': metadata,
                'timestamp': metadata.get('created_at'),
                'author': metadata.get('author'),
                'engagement': metadata.get('engagement', {})
            }
            
            processed_posts.append(processed_post)
            
        except Exception as e:
            self.logger.warning(f"Failed to process post {post.get('id', 'unknown')}: {e}")
            continue
    
    return processed_posts
```

### Signal Generation and Aggregation

```python
def _generate_signals(self, processed_data: Dict) -> Dict:
    """Generate trading signals from processed data"""
    
    self.logger.info("Generating signals")
    
    # Group posts by entities mentioned
    entity_posts = self._group_posts_by_entity(processed_data['posts'])
    
    signals = {}
    
    for entity, posts in entity_posts.items():
        if len(posts) < self.config.get('min_posts_for_signal', 5):
            continue  # Not enough data for reliable signal
        
        try:
            # Calculate entity-specific signal
            entity_signal = self.signal_generator.generate_entity_signal(
                entity=entity,
                posts=posts,
                market_data=processed_data.get('market_data'),
                news_articles=processed_data.get('news', [])
            )
            
            if entity_signal:
                signals[entity] = entity_signal
                
        except Exception as e:
            self.logger.warning(f"Failed to generate signal for {entity}: {e}")
    
    # Add overall market sentiment signal
    if processed_data['posts']:
        overall_signal = self.signal_generator.generate_overall_market_signal(
            all_posts=processed_data['posts'],
            market_data=processed_data.get('market_data')
        )
        
        if overall_signal:
            signals['overall_market'] = overall_signal
    
    self.logger.info(f"Generated {len(signals)} signals")
    return signals

def _group_posts_by_entity(self, posts: List[Dict]) -> Dict[str, List[Dict]]:
    """Group posts by the financial entities they mention"""
    
    entity_posts = {}
    
    for post in posts:
        entities_found = post.get('entities', {})
        
        # Add post to each entity it mentions
        for category, entity_names in entities_found.get('entities', {}).items():
            for entity_name in entity_names:
                if entity_name not in entity_posts:
                    entity_posts[entity_name] = []
                
                entity_posts[entity_name].append(post)
    
    return entity_posts
```

### Fear & Greed Index Calculation

```python
def _calculate_fear_greed(self, signals: Dict) -> Dict:
    """Calculate the overall Fear & Greed Index"""
    
    self.logger.info("Calculating Fear & Greed Index")
    
    # Collect all sentiment scores
    sentiment_scores = []
    volume_weights = []
    
    for entity, signal_data in signals.items():
        if entity == 'overall_market':
            continue  # Handle separately
        
        sentiment = signal_data.get('sentiment_score', 0)
        volume = signal_data.get('post_count', 1)
        confidence = signal_data.get('confidence', 0.5)
        
        # Weight by volume and confidence
        weight = volume * confidence
        
        sentiment_scores.append(sentiment)
        volume_weights.append(weight)
    
    if not sentiment_scores:
        return {'score': 50, 'label': 'Neutral', 'confidence': 0}
    
    # Calculate weighted average sentiment
    weighted_sentiment = np.average(sentiment_scores, weights=volume_weights)
    
    # Convert sentiment (-1 to 1) to Fear & Greed scale (0 to 100)
    fg_score = self.fear_greed_calculator.sentiment_to_fear_greed(weighted_sentiment)
    
    # Calculate confidence based on data quality
    confidence = self._calculate_fg_confidence(signals, sentiment_scores, volume_weights)
    
    # Get label for the score
    label = self.fear_greed_calculator.get_fear_greed_label(fg_score)
    
    result = {
        'score': round(fg_score, 1),
        'label': label,
        'confidence': round(confidence, 2),
        'timestamp': datetime.now(),
        'contributing_entities': list(signals.keys()),
        'total_posts_analyzed': sum(s.get('post_count', 0) for s in signals.values()),
        'sentiment_distribution': self._calculate_sentiment_distribution(sentiment_scores)
    }
    
    self.logger.info(f"Fear & Greed Score: {result['score']} ({result['label']})")
    return result
```

## 🔄 Real-Time vs Batch Processing

Our system supports two processing modes:

### Batch Processing (Every 15 minutes)
```python
class BatchProcessor:
    """Handles scheduled batch processing"""
    
    def __init__(self, engine):
        self.engine = engine
        self.scheduler = BlockingScheduler()
        
    def start_batch_processing(self):
        """Start scheduled batch processing"""
        
        # Schedule different tasks at different intervals
        self.scheduler.add_job(
            func=self.engine.run_analysis_cycle,
            trigger="interval",
            minutes=15,  # Main analysis every 15 minutes
            id='main_analysis'
        )
        
        self.scheduler.add_job(
            func=self.engine.collect_market_data,
            trigger="interval", 
            minutes=5,   # Market data every 5 minutes
            id='market_data'
        )
        
        self.scheduler.add_job(
            func=self.engine.cleanup_old_data,
            trigger="interval",
            hours=1,     # Cleanup every hour
            id='cleanup'
        )
        
        self.scheduler.start()
```

### Real-Time Processing (Event-driven)
```python
class RealTimeProcessor:
    """Handles real-time event processing"""
    
    def __init__(self, engine):
        self.engine = engine
        self.tweet_stream = None
        self.processing_queue = queue.Queue()
        
    def start_real_time_processing(self):
        """Start real-time data stream processing"""
        
        # Start Twitter stream
        self.tweet_stream = self.engine.twitter_collector.start_stream(
            callback=self.handle_new_tweet
        )
        
        # Start processing worker
        processing_thread = threading.Thread(target=self.process_queue_worker)
        processing_thread.daemon = True
        processing_thread.start()
        
    def handle_new_tweet(self, tweet):
        """Handle new tweet from stream"""
        
        # Quick filter: does it contain relevant entities?
        if self.engine.entity_recognizer.has_financial_entities(tweet['text']):
            self.processing_queue.put(('tweet', tweet))
    
    def process_queue_worker(self):
        """Worker thread that processes real-time events"""
        
        while True:
            try:
                event_type, data = self.processing_queue.get(timeout=1)
                
                if event_type == 'tweet':
                    self.process_single_tweet(data)
                
                self.processing_queue.task_done()
                
            except queue.Empty:
                continue
    
    def process_single_tweet(self, tweet):
        """Process a single tweet in real-time"""
        
        # Quick processing for real-time updates
        processed = self.engine._process_social_media_posts([tweet], 'twitter')
        
        if processed:
            # Update running sentiment averages
            self.engine.update_running_sentiment(processed[0])
            
            # Check for significant sentiment spikes
            if self.engine.detect_sentiment_spike(processed[0]):
                self.engine.send_real_time_alert(processed[0])
```

## 📊 Data Storage and Caching Strategy

### Multi-Level Storage

```python
class DataStorage:
    """Manages data storage across different persistence layers"""
    
    def __init__(self, config):
        self.config = config
        
        # Level 1: In-memory cache (fastest)
        self.memory_cache = {}
        
        # Level 2: Local file cache (fast)
        self.cache_dir = Path(config.get('cache_directory', 'data/cache'))
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Level 3: Long-term storage (persistent)
        self.data_dir = Path(config.get('data_directory', 'data'))
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def store_processed_data(self, data_type: str, data: Dict):
        """Store data with appropriate caching strategy"""
        
        timestamp = datetime.now()
        
        # Level 1: Store in memory for immediate access
        cache_key = f"{data_type}_{timestamp.strftime('%Y%m%d_%H%M')}"
        self.memory_cache[cache_key] = data
        
        # Level 2: Store in local cache files
        cache_file = self.cache_dir / f"{cache_key}.json"
        with open(cache_file, 'w') as f:
            json.dump(data, f, default=str, indent=2)
        
        # Level 3: Store daily aggregates for long-term analysis
        daily_file = self.data_dir / f"{data_type}_{timestamp.strftime('%Y%m%d')}.jsonl"
        with open(daily_file, 'a') as f:
            json.dump({'timestamp': timestamp.isoformat(), 'data': data}, f, default=str)
            f.write('\n')
        
        # Cleanup old memory cache
        self._cleanup_memory_cache()
    
    def _cleanup_memory_cache(self, max_items: int = 100):
        """Keep memory cache from growing too large"""
        
        if len(self.memory_cache) > max_items:
            # Remove oldest items
            sorted_keys = sorted(self.memory_cache.keys())
            for key in sorted_keys[:-max_items]:
                del self.memory_cache[key]
```

## 🚀 Performance Monitoring

```python
class PerformanceMonitor:
    """Monitor system performance and health"""
    
    def __init__(self):
        self.metrics = {
            'processing_times': [],
            'data_collection_rates': {},
            'error_counts': {},
            'memory_usage': [],
            'api_rate_limits': {}
        }
    
    def record_processing_time(self, operation: str, duration: float):
        """Record how long operations take"""
        
        self.metrics['processing_times'].append({
            'operation': operation,
            'duration': duration,
            'timestamp': datetime.now()
        })
        
        # Keep only recent measurements
        cutoff = datetime.now() - timedelta(hours=1)
        self.metrics['processing_times'] = [
            m for m in self.metrics['processing_times'] 
            if m['timestamp'] > cutoff
        ]
    
    def get_performance_summary(self) -> Dict:
        """Get current performance summary"""
        
        recent_times = self.metrics['processing_times']
        
        if not recent_times:
            return {'status': 'No data'}
        
        # Calculate averages by operation
        operation_times = {}
        for record in recent_times:
            op = record['operation']
            if op not in operation_times:
                operation_times[op] = []
            operation_times[op].append(record['duration'])
        
        summary = {
            'total_operations': len(recent_times),
            'average_times': {
                op: np.mean(times) 
                for op, times in operation_times.items()
            },
            'slowest_operations': {
                op: np.max(times)
                for op, times in operation_times.items()
            }
        }
        
        return summary
```

## 🎯 What You've Learned

You now understand:

✅ **The complete data journey** from social media post to trading signal
✅ **System architecture** and how all components work together
✅ **Data collection orchestration** across multiple sources
✅ **Processing pipeline** that transforms raw data into insights
✅ **Signal generation** and aggregation strategies
✅ **Real-time vs batch processing** approaches
✅ **Storage and caching** strategies for performance
✅ **Performance monitoring** and system health

## 🚀 What's Next?

In **Chapter 10**, we'll explore **Signal Generation in Detail** - the sophisticated algorithms that convert sentiment and entity data into actionable trading signals. You'll learn:

- Different types of signals we generate
- How we weight and combine multiple data sources
- Correlation analysis between sentiment and market movements
- Risk management and signal confidence scoring

**Ready to dive into the heart of trading signal generation?** Let's continue to **[Chapter 10: Signal Generation](chapter_10_signal_generation.md)**!

---

## 💡 Architecture Understanding Check

Think about these scenarios:

1. **What happens when Twitter API goes down?**
   - How does our system handle this gracefully?

2. **A tweet mentions both Bitcoin and Tesla**
   - How does it contribute to signals for both entities?

3. **High-volume day with 10,000 posts**
   - How do our caching and processing strategies handle this?

Understanding these scenarios helps you grasp the robustness of our architecture! 🏗️
