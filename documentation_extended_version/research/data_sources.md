# Data Sources and Collection Methodology

## What Data We Use and Why

Think of this system as having **multiple ears listening to different conversations** about the market:

### The Data Sources (Our "Ears")

1. **Twitter/X** → Real-time retail investor sentiment
2. **Reddit** → Deep retail investor discussions and analysis  
3. **Financial News** → Professional/institutional sentiment
4. **Earnings Calls** → Executive confidence and guidance
5. **Market Data** → Actual price and volume movements
6. **Options Data** → Fear indicators (VIX, put/call ratios)

### Why We Need Multiple Sources

**Each source tells a different part of the story:**

- **Twitter**: Fast, emotional, retail-driven (great for momentum)
- **Reddit**: Thoughtful, research-heavy (great for conviction)
- **News**: Professional, fact-based (great for fundamentals)
- **Earnings**: Direct from companies (great for guidance)
- **Options**: Fear/greed levels (great for contrarian signals)

### Data Quality: Garbage In = Garbage Out

We spend 60% of our effort on data quality because:
- **Bad data** = Bad predictions = Lost money
- **Missing data** = Missed opportunities
- **Biased data** = Systematic errors

### Real Numbers: What We Collect Daily

- **~50,000 tweets** mentioning stocks
- **~5,000 Reddit posts** from financial subreddits  
- **~1,200 news articles** from financial sources
- **~100 earnings transcripts** during earnings season
- **Real-time market data** for 3,000+ stocks

## Overview

This document provides comprehensive details on the data sources used in the Fear & Greed Sentiment Engine, collection methodologies, data quality assurance procedures, and integration approaches. Our multi-modal approach combines traditional financial data with modern sentiment sources to create a robust analytical framework.

## Data Source Taxonomy

### 1. Primary Financial Data

#### Market Data Sources

```python
class MarketDataConfiguration:
    """Configuration for market data collection"""
    
    def __init__(self):
        self.primary_sources = {
            'real_time': {
                'alpha_vantage': {
                    'api_endpoint': 'https://www.alphavantage.co/query',
                    'data_types': ['TIME_SERIES_INTRADAY', 'TIME_SERIES_DAILY', 'GLOBAL_QUOTE'],
                    'rate_limit': '5 calls/minute (free), 500 calls/minute (premium)',
                    'latency': '15-60 seconds',
                    'coverage': 'Global equities, forex, commodities',
                    'historical_depth': '20+ years daily, 2 years intraday'
                },
                'yahoo_finance': {
                    'api_endpoint': 'https://query1.finance.yahoo.com/v8/finance/chart/',
                    'data_types': ['OHLCV', 'splits', 'dividends', 'fundamentals'],
                    'rate_limit': '2000 requests/hour',
                    'latency': '5-15 seconds',
                    'coverage': 'Global markets, comprehensive',
                    'historical_depth': '25+ years'
                },
                'quandl': {
                    'api_endpoint': 'https://www.quandl.com/api/v3/',
                    'data_types': ['economic_indicators', 'alternative_data', 'futures'],
                    'rate_limit': '50 calls/day (free), unlimited (premium)',
                    'latency': '1-5 minutes',
                    'coverage': 'Economic data, specialized datasets',
                    'historical_depth': 'Varies by dataset'
                }
            },
            'fundamental': {
                'sec_edgar': {
                    'data_types': ['10-K', '10-Q', '8-K', '13F'],
                    'update_frequency': 'Real-time filing',
                    'format': 'XBRL, HTML, TXT',
                    'coverage': 'All US public companies',
                    'api_access': 'Free, rate limited'
                },
                'financial_modeling_prep': {
                    'data_types': ['income_statement', 'balance_sheet', 'cash_flow', 'ratios'],
                    'update_frequency': 'Quarterly + annual',
                    'format': 'JSON, CSV',
                    'coverage': '15,000+ companies globally',
                    'historical_depth': '10+ years'
                }
            }
        }
    
    def get_data_collection_schedule(self):
        """Define data collection schedule for different sources"""
        
        schedule = {
            'high_frequency': {
                'interval': '1 minute',
                'sources': ['alpha_vantage_intraday', 'yahoo_finance_quotes'],
                'active_hours': 'Market hours + 1 hour post-close',
                'data_retention': '90 days full resolution, then downsampled'
            },
            'daily': {
                'interval': '1 day',
                'sources': ['all_market_sources', 'fundamental_updates'],
                'execution_time': '6:00 PM ET (after market close)',
                'data_retention': 'Permanent'
            },
            'weekly': {
                'interval': '7 days',
                'sources': ['sec_filings', 'economic_indicators'],
                'execution_time': 'Sunday 12:00 AM ET',
                'data_retention': 'Permanent'
            }
        }
        
        return schedule
```

#### Options and Derivatives Data

```python
class OptionsDataCollection:
    """Options and derivatives data collection framework"""
    
    def __init__(self):
        self.options_sources = {
            'cboe': {
                'data_types': ['options_chains', 'volatility_indices', 'put_call_ratios'],
                'symbols': ['VIX', 'VVIX', 'SKEW', 'GVZ', 'OVX'],
                'frequency': 'Real-time during market hours',
                'historical_availability': '2006-present'
            },
            'iex_cloud': {
                'data_types': ['options_chains', 'implied_volatility', 'greeks'],
                'coverage': 'US equities and ETFs',
                'latency': '15-60 seconds',
                'cost_structure': 'Per-symbol pricing'
            }
        }
    
    def calculate_fear_greed_indicators(self, options_data):
        """Calculate fear/greed indicators from options data"""
        
        indicators = {}
        
        # VIX-based fear indicator
        if 'VIX' in options_data:
            vix_current = options_data['VIX']['current_value']
            vix_50d_avg = options_data['VIX']['50_day_average']
            
            indicators['vix_fear_level'] = {
                'current_vix': vix_current,
                'relative_to_average': (vix_current - vix_50d_avg) / vix_50d_avg,
                'fear_score': min(max((vix_current - 15) / 20, 0), 1),  # Normalized 0-1
                'interpretation': self.interpret_vix_level(vix_current)
            }
        
        # Put/Call Ratio
        if 'put_call_ratio' in options_data:
            pc_ratio = options_data['put_call_ratio']['equity_only']
            pc_10d_avg = options_data['put_call_ratio']['10_day_average']
            
            indicators['put_call_sentiment'] = {
                'current_ratio': pc_ratio,
                'vs_average': (pc_ratio - pc_10d_avg) / pc_10d_avg,
                'sentiment_score': self.pc_ratio_to_sentiment(pc_ratio),
                'extreme_reading': pc_ratio > 1.2 or pc_ratio < 0.6
            }
        
        # SKEW Index (tail risk)
        if 'SKEW' in options_data:
            skew_current = options_data['SKEW']['current_value']
            skew_avg = options_data['SKEW']['historical_average']
            
            indicators['tail_risk'] = {
                'current_skew': skew_current,
                'vs_historical': (skew_current - skew_avg) / skew_avg,
                'tail_risk_score': (skew_current - 100) / 50,  # Normalized
                'black_swan_probability': self.skew_to_tail_probability(skew_current)
            }
        
        return indicators
    
    def interpret_vix_level(self, vix_value):
        """Interpret VIX level for fear/greed assessment"""
        
        if vix_value < 15:
            return "Extreme Greed - Very low fear"
        elif vix_value < 20:
            return "Greed - Low fear"
        elif vix_value < 25:
            return "Neutral - Moderate fear"
        elif vix_value < 35:
            return "Fear - High volatility expected"
        else:
            return "Extreme Fear - Panic conditions"
```

### 2. News and Media Sources

#### Traditional Financial News

```python
class NewsDataCollection:
    """Financial news data collection and processing"""
    
    def __init__(self):
        self.news_sources = {
            'premium_apis': {
                'bloomberg_api': {
                    'coverage': 'Global financial news, analysis',
                    'update_frequency': 'Real-time',
                    'data_format': 'JSON with metadata',
                    'sentiment_tags': 'Available',
                    'cost': 'Enterprise pricing',
                    'rate_limit': 'Negotiable'
                },
                'reuters_news_api': {
                    'coverage': 'Global news, financial markets',
                    'update_frequency': 'Real-time',
                    'languages': '16 languages',
                    'categories': 'Business, markets, politics, economics',
                    'historical_depth': '2 years'
                },
                'dow_jones_newswires': {
                    'coverage': 'Breaking news, analysis',
                    'specialization': 'Real-time market-moving news',
                    'latency': '< 1 second',
                    'metadata': 'Company tags, relevance scores'
                }
            },
            'free_sources': {
                'newsapi': {
                    'endpoint': 'https://newsapi.org/v2/',
                    'sources': '70+ financial news sources',
                    'rate_limit': '1000 requests/day (free)',
                    'data_retention': '1 month',
                    'search_capabilities': 'Keywords, sources, date ranges'
                },
                'alpha_vantage_news': {
                    'endpoint': 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT',
                    'integration': 'Part of market data API',
                    'sentiment_analysis': 'Built-in sentiment scores',
                    'symbols': 'Linked to stock symbols'
                },
                'rss_feeds': {
                    'sources': ['CNBC', 'MarketWatch', 'Yahoo Finance', 'Seeking Alpha'],
                    'update_frequency': '15-60 minutes',
                    'format': 'XML/RSS',
                    'processing': 'Custom parsing required'
                }
            }
        }
    
    def news_collection_pipeline(self, symbols_list, lookback_hours=24):
        """News collection pipeline for specified symbols"""
        
        collection_results = {
            'articles_collected': 0,
            'sources_queried': [],
            'processing_errors': [],
            'sentiment_distribution': {},
            'entity_mentions': {}
        }
        
        for symbol in symbols_list:
            # Query each news source
            for source_type, sources in self.news_sources.items():
                for source_name, source_config in sources.items():
                    try:
                        articles = self.query_news_source(
                            source_name, 
                            symbol, 
                            lookback_hours
                        )
                        
                        # Process articles
                        processed_articles = self.process_news_articles(articles, symbol)
                        
                        # Update collection results
                        collection_results['articles_collected'] += len(processed_articles)
                        collection_results['sources_queried'].append(source_name)
                        
                        # Aggregate sentiment
                        for article in processed_articles:
                            sentiment = article.get('sentiment', 'neutral')
                            collection_results['sentiment_distribution'][sentiment] = \
                                collection_results['sentiment_distribution'].get(sentiment, 0) + 1
                    
                    except Exception as e:
                        collection_results['processing_errors'].append({
                            'source': source_name,
                            'symbol': symbol,
                            'error': str(e)
                        })
        
        return collection_results
    
    def process_news_articles(self, articles, symbol):
        """Process and enrich news articles with metadata"""
        
        processed = []
        
        for article in articles:
            # Extract metadata
            metadata = {
                'title': article.get('title', ''),
                'content': article.get('description', '') + ' ' + article.get('content', ''),
                'published_at': article.get('publishedAt'),
                'source': article.get('source', {}).get('name', 'unknown'),
                'url': article.get('url', ''),
                'symbol': symbol
            }
            
            # Add processing timestamps
            metadata['collected_at'] = datetime.utcnow().isoformat()
            
            # Calculate article metrics
            metadata['word_count'] = len(metadata['content'].split())
            metadata['title_sentiment'] = self.quick_sentiment_analysis(metadata['title'])
            metadata['content_sentiment'] = self.quick_sentiment_analysis(metadata['content'])
            
            # Extract entities and keywords
            metadata['entities'] = self.extract_entities(metadata['content'])
            metadata['keywords'] = self.extract_keywords(metadata['content'])
            
            # Relevance scoring
            metadata['relevance_score'] = self.calculate_relevance_score(
                metadata['content'], 
                symbol
            )
            
            processed.append(metadata)
        
        return processed
```

#### Alternative News Sources

```python
class AlternativeNewsCollection:
    """Collection from alternative and specialized news sources"""
    
    def __init__(self):
        self.alternative_sources = {
            'financial_blogs': {
                'seeking_alpha': {
                    'rss_feeds': ['https://seekingalpha.com/feed.xml'],
                    'content_type': 'Analysis articles, earnings previews',
                    'update_frequency': 'Multiple times daily',
                    'sentiment_bias': 'Generally bullish'
                },
                'motley_fool': {
                    'rss_feeds': ['https://www.fool.com/feeds/index.aspx'],
                    'content_type': 'Investment advice, stock picks',
                    'update_frequency': 'Daily',
                    'sentiment_bias': 'Long-term bullish'
                },
                'zerohedge': {
                    'rss_feeds': ['https://feeds.feedburner.com/zerohedge/feed'],
                    'content_type': 'Contrarian analysis, market commentary',
                    'update_frequency': 'Multiple times daily',
                    'sentiment_bias': 'Generally bearish'
                }
            },
            'earnings_transcripts': {
                'seeking_alpha_transcripts': {
                    'access_method': 'Web scraping',
                    'content_type': 'Earnings call transcripts',
                    'update_frequency': 'Real-time during earnings season',
                    'metadata': 'CEO/CFO quotes, Q&A sections'
                },
                'motley_fool_transcripts': {
                    'access_method': 'RSS + web scraping',
                    'content_type': 'Full earnings transcripts',
                    'special_features': 'Key quotes highlighted'
                }
            },
            'regulatory_filings': {
                'sec_edgar': {
                    'filing_types': ['8-K', '10-K', '10-Q', '13F', 'DEF 14A'],
                    'real_time_alerts': True,
                    'processing_method': 'XBRL + text extraction',
                    'sentiment_sections': ['MD&A', 'Risk Factors', 'Business Overview']
                }
            }
        }
    
    def earnings_transcript_analysis(self, transcript_text, company_symbol):
        """Analyze earnings call transcripts for sentiment and key insights"""
        
        analysis = {
            'overall_sentiment': None,
            'management_tone': None,
            'analyst_sentiment': None,
            'key_topics': [],
            'sentiment_by_section': {},
            'guidance_sentiment': None
        }
        
        # Split transcript into sections
        sections = self.parse_transcript_sections(transcript_text)
        
        for section_name, section_text in sections.items():
            # Section-specific sentiment analysis
            section_sentiment = self.analyze_section_sentiment(section_text, section_name)
            analysis['sentiment_by_section'][section_name] = section_sentiment
            
            # Extract key topics for this section
            topics = self.extract_key_topics(section_text)
            analysis['key_topics'].extend(topics)
        
        # Overall sentiment aggregation
        analysis['overall_sentiment'] = self.aggregate_section_sentiments(
            analysis['sentiment_by_section']
        )
        
        # Management tone analysis (from prepared remarks)
        if 'prepared_remarks' in sections:
            analysis['management_tone'] = self.analyze_management_tone(
                sections['prepared_remarks']
            )
        
        # Analyst sentiment (from Q&A)
        if 'qa_session' in sections:
            analysis['analyst_sentiment'] = self.analyze_analyst_questions(
                sections['qa_session']
            )
        
        # Forward guidance sentiment
        guidance_text = self.extract_guidance_statements(transcript_text)
        if guidance_text:
            analysis['guidance_sentiment'] = self.analyze_guidance_sentiment(guidance_text)
        
        return analysis
    
    def parse_transcript_sections(self, transcript_text):
        """Parse earnings transcript into structured sections"""
        
        sections = {}
        
        # Common section patterns
        section_patterns = {
            'prepared_remarks': [
                r'Prepared Remarks.*?(?=Operator|Questions|Q&A)',
                r'Company participants.*?(?=Operator|Questions)'
            ],
            'qa_session': [
                r'Questions and Answers.*',
                r'Q&A Session.*',
                r'Operator.*Thank you.*(?=Questions)'
            ],
            'operator_intro': [
                r'^.*?(?=Company participants|Prepared Remarks)'
            ]
        }
        
        for section_name, patterns in section_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, transcript_text, re.DOTALL | re.IGNORECASE)
                if match:
                    sections[section_name] = match.group(0)
                    break
        
        return sections
```

### 3. Social Media Data Sources

#### Twitter/X Data Collection

```python
class TwitterDataCollection:
    """Twitter/X data collection using various APIs and methods"""
    
    def __init__(self):
        self.api_configurations = {
            'twitter_api_v2': {
                'endpoint': 'https://api.twitter.com/2/',
                'rate_limits': {
                    'tweet_search': '300 requests/15min',
                    'user_timeline': '300 requests/15min',
                    'filtered_stream': '50 rules active'
                },
                'data_fields': [
                    'text', 'created_at', 'author_id', 'public_metrics',
                    'context_annotations', 'entities', 'geo'
                ],
                'pricing': 'Tiered based on usage'
            },
            'academic_api': {
                'endpoint': 'https://api.twitter.com/2/',
                'rate_limits': {
                    'tweet_search': '10M tweets/month',
                    'historical_access': 'Full archive access'
                },
                'requirements': 'Academic institution affiliation',
                'data_retention': 'Unlimited for research'
            }
        }
    
    def setup_twitter_streams(self, symbols_list):
        """Setup real-time Twitter streams for financial symbols"""
        
        # Build search rules for financial symbols
        rules = []
        
        for symbol in symbols_list:
            # Create comprehensive search rules
            symbol_rules = [
                f"${symbol} lang:en",  # Cashtag
                f"{symbol} (stock OR shares OR equity) lang:en",  # Company mentions
                f"{symbol} (earnings OR revenue OR profit) lang:en",  # Earnings related
                f"{symbol} (bullish OR bearish OR buy OR sell) lang:en"  # Sentiment terms
            ]
            
            rules.extend(symbol_rules)
        
        # Add general market sentiment rules
        market_rules = [
            "(SPY OR QQQ OR VIX) (fear OR greed OR sentiment) lang:en",
            "(market OR stocks) (crash OR rally OR volatility) lang:en",
            "earnings has:cashtags lang:en",
            "(Federal Reserve OR Fed OR interest rates) (stocks OR market) lang:en"
        ]
        
        rules.extend(market_rules)
        
        return {
            'rules': rules,
            'total_rules': len(rules),
            'estimated_volume': self.estimate_tweet_volume(rules),
            'recommended_setup': self.recommend_stream_setup(rules)
        }
    
    def process_tweet_stream(self, tweet_data):
        """Process incoming tweet data for sentiment analysis"""
        
        processed_tweets = []
        
        for tweet in tweet_data:
            processed_tweet = {
                'id': tweet['id'],
                'text': tweet['text'],
                'created_at': tweet['created_at'],
                'author_id': tweet['author_id'],
                'metrics': tweet.get('public_metrics', {}),
                
                # Extract financial entities
                'symbols': self.extract_symbols(tweet['text']),
                'cashtags': self.extract_cashtags(tweet['text']),
                'hashtags': self.extract_hashtags(tweet['text']),
                
                # Sentiment analysis
                'sentiment_score': self.analyze_tweet_sentiment(tweet['text']),
                'emotion_scores': self.analyze_tweet_emotions(tweet['text']),
                
                # Metadata
                'influence_score': self.calculate_user_influence(tweet['author_id']),
                'engagement_rate': self.calculate_engagement_rate(tweet.get('public_metrics', {})),
                'topic_classification': self.classify_tweet_topic(tweet['text']),
                
                # Processing timestamp
                'processed_at': datetime.utcnow().isoformat()
            }
            
            processed_tweets.append(processed_tweet)
        
        return processed_tweets
    
    def calculate_user_influence(self, author_id):
        """Calculate user influence score for weighting tweets"""
        
        # This would typically involve caching user metadata
        # For now, return a placeholder calculation
        
        user_metrics = {
            'followers_count': 1000,  # Would fetch from user object
            'following_count': 500,
            'tweet_count': 5000,
            'listed_count': 50,
            'verified': False
        }
        
        # Simple influence calculation
        follower_score = min(user_metrics['followers_count'] / 10000, 1.0)
        ratio_score = user_metrics['followers_count'] / max(user_metrics['following_count'], 1)
        ratio_score = min(ratio_score / 10, 1.0)
        
        influence = (follower_score * 0.6 + ratio_score * 0.3 + 
                    (0.1 if user_metrics['verified'] else 0))
        
        return influence
```

#### Reddit Data Collection

```python
class RedditDataCollection:
    """Reddit data collection for financial sentiment analysis"""
    
    def __init__(self):
        self.target_subreddits = {
            'finance_focused': [
                'investing', 'SecurityAnalysis', 'ValueInvesting',
                'financialindependence', 'StockMarket', 'stocks'
            ],
            'trading_focused': [
                'wallstreetbets', 'options', 'SecurityAnalysis',
                'DayTrading', 'pennystocks', 'forex'
            ],
            'crypto_focused': [
                'cryptocurrency', 'Bitcoin', 'ethereum',
                'CryptoCurrency', 'altcoin'
            ],
            'general_economic': [
                'economics', 'business', 'news',
                'worldnews', 'finance'
            ]
        }
        
        self.api_config = {
            'praw_config': {
                'client_id': 'your_client_id',
                'client_secret': 'your_client_secret',
                'user_agent': 'sentiment_analysis_bot/1.0'
            },
            'rate_limits': {
                'requests_per_minute': 60,
                'posts_per_request': 100,
                'comments_per_request': 500
            }
        }
    
    def collect_subreddit_data(self, subreddit_name, time_filter='day', limit=1000):
        """Collect posts and comments from a specific subreddit"""
        
        import praw
        
        reddit = praw.Reddit(**self.api_config['praw_config'])
        subreddit = reddit.subreddit(subreddit_name)
        
        collected_data = {
            'posts': [],
            'comments': [],
            'submission_count': 0,
            'comment_count': 0,
            'collection_metadata': {
                'subreddit': subreddit_name,
                'time_filter': time_filter,
                'collected_at': datetime.utcnow().isoformat()
            }
        }
        
        # Collect hot posts
        for submission in subreddit.hot(limit=limit):
            post_data = {
                'id': submission.id,
                'title': submission.title,
                'selftext': submission.selftext,
                'score': submission.score,
                'upvote_ratio': submission.upvote_ratio,
                'num_comments': submission.num_comments,
                'created_utc': submission.created_utc,
                'author': str(submission.author) if submission.author else '[deleted]',
                'url': submission.url,
                'permalink': submission.permalink,
                
                # Extract financial mentions
                'symbols_mentioned': self.extract_symbols_from_text(
                    submission.title + ' ' + submission.selftext
                ),
                
                # Sentiment analysis
                'title_sentiment': self.analyze_reddit_sentiment(submission.title),
                'content_sentiment': self.analyze_reddit_sentiment(submission.selftext),
                
                # Classification
                'post_category': self.classify_reddit_post(submission.title, submission.selftext),
                'dd_probability': self.calculate_dd_probability(submission.title, submission.selftext)
            }
            
            collected_data['posts'].append(post_data)
            collected_data['submission_count'] += 1
            
            # Collect top comments for each post
            submission.comments.replace_more(limit=0)  # Remove "more comments"
            
            for comment in submission.comments.list()[:10]:  # Top 10 comments
                if hasattr(comment, 'body') and comment.body != '[deleted]':
                    comment_data = {
                        'id': comment.id,
                        'parent_id': submission.id,
                        'body': comment.body,
                        'score': comment.score,
                        'created_utc': comment.created_utc,
                        'author': str(comment.author) if comment.author else '[deleted]',
                        
                        # Analysis
                        'sentiment': self.analyze_reddit_sentiment(comment.body),
                        'symbols_mentioned': self.extract_symbols_from_text(comment.body),
                        'agreement_with_post': self.calculate_agreement_score(
                            submission.title + submission.selftext,
                            comment.body
                        )
                    }
                    
                    collected_data['comments'].append(comment_data)
                    collected_data['comment_count'] += 1
        
        return collected_data
    
    def analyze_wallstreetbets_sentiment(self, posts_data):
        """Specialized analysis for WallStreetBets posts"""
        
        wsb_analysis = {
            'overall_sentiment': None,
            'top_mentioned_stocks': {},
            'dd_posts': [],
            'yolo_sentiment': None,
            'rocket_emoji_count': 0,
            'diamond_hands_mentions': 0,
            'paper_hands_mentions': 0
        }
        
        sentiment_scores = []
        symbol_mentions = {}
        
        for post in posts_data:
            # Count WSB-specific indicators
            text_content = post['title'] + ' ' + post.get('selftext', '')
            
            wsb_analysis['rocket_emoji_count'] += text_content.count('🚀')
            wsb_analysis['diamond_hands_mentions'] += len(
                re.findall(r'diamond\s+hands|💎\s*🙌|💎🙌', text_content, re.IGNORECASE)
            )
            wsb_analysis['paper_hands_mentions'] += len(
                re.findall(r'paper\s+hands|🧻\s*🙌|🧻🙌', text_content, re.IGNORECASE)
            )
            
            # Aggregate sentiment
            if post.get('title_sentiment'):
                sentiment_scores.append(post['title_sentiment']['compound'])
            
            # Count symbol mentions
            for symbol in post.get('symbols_mentioned', []):
                symbol_mentions[symbol] = symbol_mentions.get(symbol, 0) + 1
            
            # Identify DD posts
            if post.get('dd_probability', 0) > 0.7:
                wsb_analysis['dd_posts'].append({
                    'title': post['title'],
                    'score': post['score'],
                    'symbols': post.get('symbols_mentioned', []),
                    'sentiment': post.get('content_sentiment')
                })
        
        # Calculate aggregated metrics
        wsb_analysis['overall_sentiment'] = np.mean(sentiment_scores) if sentiment_scores else 0
        wsb_analysis['top_mentioned_stocks'] = dict(
            sorted(symbol_mentions.items(), key=lambda x: x[1], reverse=True)[:10]
        )
        
        # Calculate special WSB sentiment indicators
        total_posts = len(posts_data)
        wsb_analysis['bullish_indicators'] = {
            'rocket_density': wsb_analysis['rocket_emoji_count'] / total_posts,
            'diamond_hands_ratio': wsb_analysis['diamond_hands_mentions'] / max(
                wsb_analysis['diamond_hands_mentions'] + wsb_analysis['paper_hands_mentions'], 1
            ),
            'dd_activity': len(wsb_analysis['dd_posts']) / total_posts
        }
        
        return wsb_analysis
```

### 4. Data Quality and Validation

#### Data Quality Framework

```python
class DataQualityAssurance:
    """Comprehensive data quality assurance for sentiment analysis"""
    
    def __init__(self):
        self.quality_metrics = {
            'completeness': ['missing_values', 'null_ratios', 'coverage_gaps'],
            'accuracy': ['duplicate_detection', 'format_validation', 'range_checks'],
            'consistency': ['cross_source_validation', 'temporal_consistency'],
            'timeliness': ['data_latency', 'update_frequency', 'staleness_detection'],
            'validity': ['schema_compliance', 'business_rule_validation']
        }
    
    def validate_market_data(self, market_data_df):
        """Validate market data quality"""
        
        validation_results = {
            'passed_checks': [],
            'failed_checks': [],
            'warnings': [],
            'data_quality_score': 0
        }
        
        # Check for required columns
        required_columns = ['open', 'high', 'low', 'close', 'volume', 'timestamp']
        missing_columns = [col for col in required_columns if col not in market_data_df.columns]
        
        if not missing_columns:
            validation_results['passed_checks'].append('Required columns present')
        else:
            validation_results['failed_checks'].append(f'Missing columns: {missing_columns}')
        
        # Validate OHLC relationships
        ohlc_valid = (
            (market_data_df['high'] >= market_data_df['open']) &
            (market_data_df['high'] >= market_data_df['close']) &
            (market_data_df['low'] <= market_data_df['open']) &
            (market_data_df['low'] <= market_data_df['close']) &
            (market_data_df['high'] >= market_data_df['low'])
        ).all()
        
        if ohlc_valid:
            validation_results['passed_checks'].append('OHLC relationships valid')
        else:
            validation_results['failed_checks'].append('Invalid OHLC relationships detected')
        
        # Check for suspicious price movements
        price_changes = market_data_df['close'].pct_change()
        extreme_moves = (abs(price_changes) > 0.5).sum()  # >50% moves
        
        if extreme_moves == 0:
            validation_results['passed_checks'].append('No extreme price movements')
        elif extreme_moves < 5:
            validation_results['warnings'].append(f'{extreme_moves} extreme price movements detected')
        else:
            validation_results['failed_checks'].append(f'Too many extreme movements: {extreme_moves}')
        
        # Volume validation
        zero_volume_days = (market_data_df['volume'] == 0).sum()
        if zero_volume_days == 0:
            validation_results['passed_checks'].append('No zero volume days')
        else:
            validation_results['warnings'].append(f'{zero_volume_days} zero volume days')
        
        # Calculate overall quality score
        total_checks = len(validation_results['passed_checks']) + len(validation_results['failed_checks'])
        if total_checks > 0:
            validation_results['data_quality_score'] = len(validation_results['passed_checks']) / total_checks
        
        return validation_results
    
    def validate_sentiment_data(self, sentiment_data):
        """Validate sentiment data quality and consistency"""
        
        validation_results = {
            'text_quality': {},
            'sentiment_consistency': {},
            'temporal_distribution': {},
            'source_reliability': {}
        }
        
        # Text quality checks
        if 'text' in sentiment_data.columns:
            text_lengths = sentiment_data['text'].str.len()
            
            validation_results['text_quality'] = {
                'avg_length': text_lengths.mean(),
                'median_length': text_lengths.median(),
                'very_short_texts': (text_lengths < 10).sum(),  # < 10 characters
                'very_long_texts': (text_lengths > 5000).sum(),  # > 5000 characters
                'empty_texts': sentiment_data['text'].isna().sum()
            }
        
        # Sentiment score consistency
        if 'sentiment_score' in sentiment_data.columns:
            sentiment_scores = sentiment_data['sentiment_score']
            
            validation_results['sentiment_consistency'] = {
                'score_range': [sentiment_scores.min(), sentiment_scores.max()],
                'score_distribution': {
                    'mean': sentiment_scores.mean(),
                    'std': sentiment_scores.std(),
                    'skewness': sentiment_scores.skew(),
                    'kurtosis': sentiment_scores.kurtosis()
                },
                'extreme_scores': {
                    'very_positive': (sentiment_scores > 0.8).sum(),
                    'very_negative': (sentiment_scores < -0.8).sum(),
                    'neutral': (abs(sentiment_scores) < 0.1).sum()
                }
            }
        
        # Temporal distribution
        if 'timestamp' in sentiment_data.columns:
            timestamps = pd.to_datetime(sentiment_data['timestamp'])
            time_gaps = timestamps.diff().dt.total_seconds()
            
            validation_results['temporal_distribution'] = {
                'time_span': (timestamps.max() - timestamps.min()).total_seconds() / 3600,  # hours
                'data_points': len(timestamps),
                'avg_gap_minutes': time_gaps.mean() / 60,
                'max_gap_hours': time_gaps.max() / 3600,
                'gaps_over_1hour': (time_gaps > 3600).sum()
            }
        
        return validation_results
```

## Data Integration and Storage

### Database Architecture

```python
class DataStorageArchitecture:
    """Database architecture for multi-modal sentiment data"""
    
    def __init__(self):
        self.storage_layers = {
            'raw_data': {
                'technology': 'Apache Kafka + S3',
                'purpose': 'Real-time ingestion and raw data storage',
                'retention': '90 days hot, 2 years cold',
                'format': 'JSON, Avro'
            },
            'processed_data': {
                'technology': 'PostgreSQL + TimescaleDB',
                'purpose': 'Structured storage for analysis',
                'retention': 'Permanent',
                'optimization': 'Time-series partitioning'
            },
            'feature_store': {
                'technology': 'Redis + PostgreSQL',
                'purpose': 'Real-time feature serving',
                'retention': '30 days',
                'access_pattern': 'High-frequency reads'
            },
            'model_artifacts': {
                'technology': 'MLflow + S3',
                'purpose': 'Model storage and versioning',
                'retention': 'All versions',
                'metadata': 'Experiment tracking'
            }
        }
    
    def design_database_schema(self):
        """Design optimized database schema for sentiment data"""
        
        schema = {
            'market_data': {
                'table': 'market_ohlcv',
                'columns': {
                    'symbol': 'VARCHAR(10) NOT NULL',
                    'timestamp': 'TIMESTAMPTZ NOT NULL',
                    'open_price': 'DECIMAL(10,4)',
                    'high_price': 'DECIMAL(10,4)',
                    'low_price': 'DECIMAL(10,4)',
                    'close_price': 'DECIMAL(10,4)',
                    'volume': 'BIGINT',
                    'adjusted_close': 'DECIMAL(10,4)'
                },
                'indexes': [
                    'CREATE INDEX idx_market_symbol_time ON market_ohlcv (symbol, timestamp)',
                    'CREATE INDEX idx_market_time ON market_ohlcv (timestamp DESC)'
                ],
                'partitioning': 'PARTITION BY RANGE (timestamp)'
            },
            'news_data': {
                'table': 'news_articles',
                'columns': {
                    'article_id': 'UUID PRIMARY KEY',
                    'title': 'TEXT NOT NULL',
                    'content': 'TEXT',
                    'source': 'VARCHAR(100)',
                    'published_at': 'TIMESTAMPTZ',
                    'collected_at': 'TIMESTAMPTZ DEFAULT NOW()',
                    'symbols': 'TEXT[]',  # Array of mentioned symbols
                    'sentiment_score': 'DECIMAL(5,4)',
                    'sentiment_label': 'VARCHAR(20)',
                    'relevance_score': 'DECIMAL(5,4)',
                    'url': 'TEXT UNIQUE'
                },
                'indexes': [
                    'CREATE INDEX idx_news_published ON news_articles (published_at DESC)',
                    'CREATE INDEX idx_news_symbols ON news_articles USING GIN (symbols)',
                    'CREATE INDEX idx_news_sentiment ON news_articles (sentiment_score)'
                ]
            },
            'social_media': {
                'table': 'social_posts',
                'columns': {
                    'post_id': 'VARCHAR(50) PRIMARY KEY',
                    'platform': 'VARCHAR(20) NOT NULL',  # twitter, reddit, etc.
                    'content': 'TEXT',
                    'author_id': 'VARCHAR(100)',
                    'created_at': 'TIMESTAMPTZ',
                    'metrics': 'JSONB',  # likes, shares, comments, etc.
                    'symbols': 'TEXT[]',
                    'hashtags': 'TEXT[]',
                    'sentiment_scores': 'JSONB',  # Multiple sentiment dimensions
                    'influence_score': 'DECIMAL(5,4)',
                    'topic_category': 'VARCHAR(50)'
                },
                'indexes': [
                    'CREATE INDEX idx_social_platform_time ON social_posts (platform, created_at DESC)',
                    'CREATE INDEX idx_social_symbols ON social_posts USING GIN (symbols)',
                    'CREATE INDEX idx_social_metrics ON social_posts USING GIN (metrics)'
                ]
            },
            'aggregated_sentiment': {
                'table': 'sentiment_aggregates',
                'columns': {
                    'symbol': 'VARCHAR(10) NOT NULL',
                    'timestamp': 'TIMESTAMPTZ NOT NULL',
                    'time_window': 'INTERVAL NOT NULL',  # 1h, 4h, 1d, etc.
                    'news_sentiment': 'DECIMAL(5,4)',
                    'social_sentiment': 'DECIMAL(5,4)',
                    'combined_sentiment': 'DECIMAL(5,4)',
                    'sentiment_volume': 'INTEGER',
                    'sentiment_confidence': 'DECIMAL(5,4)',
                    'fear_greed_score': 'DECIMAL(5,4)',
                    'volatility_expectation': 'DECIMAL(5,4)',
                    'data_sources': 'TEXT[]'
                },
                'indexes': [
                    'CREATE UNIQUE INDEX idx_sentiment_agg_unique ON sentiment_aggregates (symbol, timestamp, time_window)',
                    'CREATE INDEX idx_sentiment_agg_time ON sentiment_aggregates (timestamp DESC)'
                ],
                'partitioning': 'PARTITION BY RANGE (timestamp)'
            }
        }
        
        return schema
```

This comprehensive data collection methodology ensures robust, high-quality data feeds for the Fear & Greed Sentiment Engine. The multi-modal approach, combined with rigorous quality assurance and optimized storage, provides the foundation for accurate sentiment analysis and reliable trading signals.
