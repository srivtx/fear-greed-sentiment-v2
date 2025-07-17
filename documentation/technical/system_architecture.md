# System Architecture & NLP Pipeline Design

## What This System Does

The Fear & Greed Sentiment Engine is essentially a **smart financial radar** that monitors market sentiment in real-time. Imagine having thousands of financial analysts reading every news article, social media post, and market report simultaneously - that's what this system does automatically.

### Why Sentiment Analysis Matters for Trading

Markets aren't just driven by numbers - they're driven by emotions:
- When people are **fearful**, they sell (creating buying opportunities)
- When people are **greedy**, they buy at any price (creating selling opportunities)
- When uncertainty is high, volatility spikes
- When confidence returns, trends emerge

Our system captures these emotions as they happen and converts them into actionable trading signals.

### Quick Architecture Overview

**Want to see the system in action?**
```bash
# Start the system
python goquant_main.py --mode real-time

# View the web dashboard
open http://localhost:5000

# Check system architecture
curl http://localhost:5000/api/system_stats
```

## Overview

The Fear & Greed Sentiment Engine is a comprehensive real-time sentiment analysis system designed for financial markets. The architecture follows a modular, scalable design pattern that enables efficient processing of multiple data sources and real-time signal generation.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Fear & Greed Sentiment Engine                │
└─────────────────────────────────────────────────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
┌───────▼────────┐    ┌────────────▼──────────┐    ┌─────────▼──────┐
│  Data Sources  │    │    Processing Core    │    │  Output Layer  │
│                │    │                       │    │                │
│ • Twitter API  │    │ • NLP Pipeline        │    │ • Signals      │
│ • Reddit API   │    │ • Sentiment Analysis  │    │ • Dashboards   │
│ • News APIs    │    │ • Entity Recognition  │    │ • Alerts       │
│ • Market Data  │    │ • Signal Generation   │    │ • APIs         │
└────────────────┘    └───────────────────────┘    └────────────────┘
```

## Core Components

### 1. Data Collection Layer

#### Architecture Pattern: Producer-Consumer with Rate Limiting

```python
# Data Collection Architecture
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Client    │───▶│  Rate Limiter   │───▶│  Data Queue     │
│  (Twitter/etc)  │    │  (TokenBucket)  │    │  (Redis/Memory) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                               ┌────────▼────────┐
                                               │  Data Validator │
                                               │   & Sanitizer   │
                                               └─────────────────┘
```

**Key Features:**
- **Asynchronous Collection**: Non-blocking I/O for multiple data sources
- **Rate Limiting**: Token bucket algorithm prevents API throttling
- **Data Validation**: Schema validation and sanitization
- **Error Recovery**: Exponential backoff and circuit breaker patterns

#### Data Source Specifications

| Source | Rate Limit | Data Format | Update Frequency |
|--------|------------|-------------|------------------|
| Twitter API v2 | 300 req/15min | JSON | Real-time |
| Reddit API | 60 req/min | JSON | 5-minute intervals |
| News API | 1000 req/day | JSON | 15-minute intervals |
| Yahoo Finance | 2000 req/hour | CSV/JSON | 1-minute intervals |

### 2. NLP Pipeline Architecture

#### Multi-Stage Processing Pipeline

```
Raw Text Input
      │
      ▼
┌─────────────────┐
│ Text Cleaning   │  ── Remove URLs, mentions, hashtags
│ & Preprocessing │     Normalize whitespace, convert case
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Tokenization   │  ── Split into tokens
│  & Stop Words   │     Remove common stop words
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Entity Recog.   │  ── Extract financial entities
│ & Tagging       │     Tag named entities (companies, tickers)
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Sentiment       │  ── VADER + Custom Financial Lexicon
│ Classification  │     Multi-model ensemble approach
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Confidence      │  ── Calculate prediction confidence
│ Scoring         │     Apply temporal weighting
└─────────────────┘
```

#### NLP Components Detail

##### 1. Text Preprocessing
- **Regex-based cleaning**: Remove noise while preserving sentiment-bearing elements
- **Financial symbol preservation**: Maintain ticker symbols ($AAPL, $BTC)
- **Emoji handling**: Convert emojis to sentiment-bearing text
- **Normalization**: Handle abbreviations and financial jargon

##### 2. Tokenization Strategy
```python
# Custom tokenization for financial text
tokenizer_config = {
    'preserve_case': True,  # Preserve ticker symbols
    'split_hashtags': False,  # Keep hashtags intact
    'handle_negation': True,  # Track negation scope
    'preserve_punctuation': ['!', '?', '$']  # Sentiment indicators
}
```

##### 3. Entity Recognition Pipeline
- **Financial Entity Extraction**: Companies, tickers, currencies
- **Pattern Matching**: Regex patterns for financial terms
- **Context Validation**: Verify entities in financial context
- **Fuzzy Matching**: Handle variations and misspellings

#### Machine Learning Model Architecture

##### Ensemble Sentiment Classification

```
Input Text
    │
    ├─────────────────┬─────────────────┬─────────────────┐
    │                 │                 │                 │
    ▼                 ▼                 ▼                 ▼
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ VADER   │    │Financial│    │ TextBlob│    │ Custom  │
│Lexicon  │    │Lexicon  │    │ Model   │    │ FinBERT │
└────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘
     │              │              │              │
     └──────────────┼──────────────┼──────────────┘
                    │              │
                    ▼              ▼
            ┌─────────────────────────┐
            │    Ensemble Combiner    │
            │   (Weighted Average)    │
            └───────────┬─────────────┘
                        │
                        ▼
            ┌─────────────────────────┐
            │   Final Sentiment       │
            │   Score & Confidence    │
            └─────────────────────────┘
```

**Model Weights:**
- VADER: 30% (general sentiment)
- Financial Lexicon: 40% (domain-specific)
- TextBlob: 15% (linguistic features)
- Custom FinBERT: 15% (context understanding)

### 3. Signal Generation Architecture

#### Multi-Factor Signal Model

```
Sentiment Scores
       │
       ▼
┌─────────────────┐
│ Temporal        │ ── Time-based weighting
│ Aggregation     │    Volume-weighted averaging
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Factor          │ ── • Momentum Factor
│ Calculation     │    • Volume Factor
│                 │    • Market Correlation
└─────────┬───────┘    • Entity Influence
          │
          ▼
┌─────────────────┐
│ Risk            │ ── Volatility assessment
│ Assessment      │    Confidence intervals
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Signal          │ ── Buy/Sell/Hold signals
│ Generation      │    Position sizing
└─────────────────┘    Risk-adjusted returns
```

#### Signal Calculation Formula

```python
# Composite Signal Score
signal_score = (
    sentiment_score * 0.4 +           # Base sentiment
    momentum_factor * 0.25 +          # Trend momentum
    volume_factor * 0.2 +             # Discussion volume
    market_correlation * 0.15         # Market alignment
)

# Risk-Adjusted Signal
final_signal = signal_score * confidence_multiplier * (1 - risk_penalty)
```

### 4. Data Storage Architecture

#### Multi-Tier Storage Strategy

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Hot Storage   │    │  Warm Storage   │    │  Cold Storage   │
│   (Redis)       │    │  (PostgreSQL)   │    │  (File System)  │
│                 │    │                 │    │                 │
│ • Real-time     │    │ • Historical    │    │ • Archive data  │
│   data cache    │    │   sentiment     │    │ • Backups       │
│ • Session data  │    │ • Market data   │    │ • Logs          │
│ • Temp results  │    │ • User configs  │    │ • Raw data      │
│                 │    │                 │    │                 │
│ TTL: 1 hour     │    │ TTL: 90 days    │    │ TTL: Unlimited  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### Data Models

##### Sentiment Data Model
```python
@dataclass
class SentimentRecord:
    id: str
    timestamp: datetime
    entity: str
    platform: str
    text: str
    sentiment_score: float
    confidence: float
    factors: Dict[str, float]
    metadata: Dict[str, Any]
```

##### Signal Data Model
```python
@dataclass
class TradingSignal:
    id: str
    timestamp: datetime
    entity: str
    signal_type: str  # BUY, SELL, HOLD
    strength: float   # 0.0 to 1.0
    confidence: float
    risk_level: str
    factors: Dict[str, float]
    expiry: datetime
```

### 5. Performance Optimization

#### Caching Strategy
- **L1 Cache**: In-memory results cache (60 seconds TTL)
- **L2 Cache**: Redis distributed cache (15 minutes TTL)
- **L3 Cache**: Preprocessed data cache (1 hour TTL)

#### Parallel Processing
```python
# Asynchronous processing pipeline
async def process_sentiment_batch(texts: List[str]) -> List[SentimentResult]:
    tasks = [
        asyncio.create_task(process_single_text(text))
        for text in texts
    ]
    return await asyncio.gather(*tasks)
```

#### Performance Metrics
- **Throughput**: 1000+ texts/second
- **Latency**: <100ms for single text analysis
- **Memory Usage**: <2GB for full pipeline
- **CPU Utilization**: <80% under peak load

### 6. Monitoring & Observability

#### System Metrics
```python
# Key Performance Indicators
metrics = {
    'processing_rate': 'texts/second',
    'api_response_time': 'milliseconds',
    'sentiment_accuracy': 'percentage',
    'signal_precision': 'percentage',
    'system_uptime': 'percentage',
    'error_rate': 'errors/hour'
}
```

#### Logging Architecture
- **Structured Logging**: JSON format with correlation IDs
- **Log Levels**: DEBUG, INFO, WARN, ERROR, CRITICAL
- **Log Rotation**: Daily rotation with 30-day retention
- **Centralized Collection**: ELK stack integration ready

### 7. Scalability Considerations

#### Horizontal Scaling
- **Microservices**: Each component can scale independently
- **Load Balancing**: Round-robin for stateless components
- **Database Sharding**: Time-based partitioning for historical data

#### Vertical Scaling
- **Memory Optimization**: Efficient data structures and caching
- **CPU Optimization**: Vectorized operations and parallel processing
- **I/O Optimization**: Asynchronous operations and connection pooling

## Configuration Management

### Environment-Specific Configs
```yaml
# Production Configuration
production:
  api_limits:
    twitter: 300
    reddit: 60
    news: 1000
  cache:
    ttl: 900  # 15 minutes
    size: 10000
  processing:
    batch_size: 100
    max_workers: 8
  monitoring:
    metrics_enabled: true
    log_level: "INFO"
```

## Security Architecture

### Data Protection
- **API Key Management**: Environment variables and secrets management
- **Data Encryption**: AES-256 for sensitive data at rest
- **Access Control**: Role-based access control (RBAC)
- **Rate Limiting**: DDoS protection and fair usage

### Compliance
- **Data Privacy**: GDPR-compliant data handling
- **Financial Regulations**: SOX compliance for financial data
- **Audit Logging**: Comprehensive audit trail

## Deployment Architecture

### Container Strategy
```dockerfile
# Multi-stage build for optimization
FROM python:3.11-slim as base
FROM base as dependencies
FROM dependencies as application
```

### Infrastructure as Code
```yaml
# Docker Compose for local development
# Kubernetes manifests for production
# Terraform for cloud infrastructure
```

This architecture ensures scalability, maintainability, and high performance while providing robust sentiment analysis capabilities for financial markets.
