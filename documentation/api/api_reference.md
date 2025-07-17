# API Reference Documentation

## What This API Does

Think of this API as your **direct line to market sentiment intelligence**. Instead of manually reading hundreds of news articles and social media posts to gauge market mood, you can simply make API calls to get:

- **Instant sentiment scores** for any stock or market
- **Real-time fear/greed indicators** 
- **Trading signals** based on sentiment analysis
- **Historical sentiment trends** for backtesting strategies

### Who Should Use This API

- **Traders**: Get sentiment-based entry/exit signals
- **Portfolio Managers**: Incorporate sentiment into risk models  
- **Developers**: Build sentiment-aware trading applications
- **Researchers**: Access sentiment data for academic studies
- **Financial Apps**: Add sentiment features to existing platforms

### Simple Example: Getting Tesla Sentiment

```bash
# Get current sentiment for Tesla
curl -X GET "https://api.feargreed-sentiment.com/v1/sentiment/TSLA" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Response: {"symbol": "TSLA", "sentiment_score": 0.65, "fear_greed": "moderate_greed"}
```

## Overview

The Fear & Greed Sentiment Engine provides a comprehensive RESTful API for sentiment analysis, signal generation, and data collection. This documentation covers all available endpoints, request/response formats, authentication, rate limiting, and integration examples.

## Base URL and Versioning

```
Base URL: https://api.feargreed-sentiment.com/v1/
Development: http://localhost:8000/v1/
```

**API Version**: v1  
**Authentication**: API Key or OAuth 2.0  
**Content Type**: `application/json`  
**Rate Limiting**: 1000 requests/hour (standard tier)

## Authentication

### API Key Authentication

```http
GET /v1/sentiment/analyze
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

### OAuth 2.0 Flow

```python
# Python example
import requests

# Get access token
auth_response = requests.post('https://api.feargreed-sentiment.com/oauth/token', {
    'grant_type': 'client_credentials',
    'client_id': 'your_client_id',
    'client_secret': 'your_client_secret',
    'scope': 'sentiment:read signal:read'
})

access_token = auth_response.json()['access_token']

# Use access token
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}
```

## Sentiment Analysis Endpoints

### Analyze Single Text

**Endpoint**: `POST /v1/sentiment/analyze`

Analyze sentiment for a single piece of text.

#### Request

```json
{
    "text": "AAPL is showing strong bullish momentum. Great buying opportunity!",
    "entity": "AAPL",
    "source": "twitter",
    "options": {
        "include_confidence": true,
        "include_breakdown": true,
        "language": "en"
    }
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | Yes | Text to analyze (max 10,000 characters) |
| `entity` | string | No | Financial entity/ticker symbol |
| `source` | string | No | Source platform (twitter, reddit, news, etc.) |
| `options.include_confidence` | boolean | No | Include confidence scores (default: false) |
| `options.include_breakdown` | boolean | No | Include model breakdown (default: false) |
| `options.language` | string | No | Text language (default: "en") |

#### Response

```json
{
    "status": "success",
    "data": {
        "sentiment": {
            "score": 0.75,
            "label": "positive",
            "confidence": 0.89
        },
        "entity": "AAPL",
        "source": "twitter",
        "processed_at": "2024-01-15T10:30:00Z",
        "breakdown": {
            "vader": {
                "score": 0.72,
                "confidence": 0.85
            },
            "financial_lexicon": {
                "score": 0.80,
                "confidence": 0.92
            },
            "textblob": {
                "score": 0.68,
                "confidence": 0.78
            },
            "finbert": {
                "score": 0.81,
                "confidence": 0.94
            }
        },
        "features": {
            "keywords": ["bullish", "momentum", "buying", "opportunity"],
            "entities": ["AAPL"],
            "emotions": ["optimism", "excitement"]
        }
    },
    "metadata": {
        "processing_time_ms": 45,
        "model_version": "v2.1.0",
        "request_id": "req_12345"
    }
}
```

### Batch Sentiment Analysis

**Endpoint**: `POST /v1/sentiment/batch`

Analyze sentiment for multiple texts in a single request.

#### Request

```json
{
    "texts": [
        {
            "id": "text_1",
            "text": "Market is crashing! Sell everything!",
            "entity": "SPY"
        },
        {
            "id": "text_2", 
            "text": "Great earnings report from Apple. Stock should rally.",
            "entity": "AAPL"
        }
    ],
    "options": {
        "include_confidence": true,
        "parallel_processing": true
    }
}
```

#### Response

```json
{
    "status": "success",
    "data": {
        "results": [
            {
                "id": "text_1",
                "sentiment": {
                    "score": -0.85,
                    "label": "negative",
                    "confidence": 0.92
                },
                "entity": "SPY"
            },
            {
                "id": "text_2",
                "sentiment": {
                    "score": 0.78,
                    "label": "positive", 
                    "confidence": 0.87
                },
                "entity": "AAPL"
            }
        ],
        "summary": {
            "total_processed": 2,
            "average_sentiment": -0.035,
            "sentiment_distribution": {
                "positive": 1,
                "negative": 1,
                "neutral": 0
            }
        }
    },
    "metadata": {
        "batch_processing_time_ms": 78,
        "parallel_workers": 4
    }
}
```

### Stream Sentiment Analysis

**Endpoint**: `WebSocket /v1/sentiment/stream`

Real-time sentiment analysis via WebSocket connection.

#### Connection

```javascript
// JavaScript WebSocket example
const ws = new WebSocket('wss://api.feargreed-sentiment.com/v1/sentiment/stream?auth=YOUR_API_KEY');

ws.onopen = function() {
    console.log('Connected to sentiment stream');
    
    // Send text for analysis
    ws.send(JSON.stringify({
        "action": "analyze",
        "data": {
            "text": "Breaking: Fed raises interest rates by 0.5%",
            "entity": "SPY",
            "source": "news"
        }
    }));
};

ws.onmessage = function(event) {
    const response = JSON.parse(event.data);
    console.log('Sentiment result:', response);
};
```

#### WebSocket Messages

**Send Message**:
```json
{
    "action": "analyze",
    "data": {
        "text": "Tesla stock is mooning! 🚀",
        "entity": "TSLA",
        "request_id": "custom_id_123"
    }
}
```

**Receive Message**:
```json
{
    "action": "result",
    "data": {
        "sentiment": {
            "score": 0.82,
            "label": "positive",
            "confidence": 0.91
        },
        "entity": "TSLA",
        "request_id": "custom_id_123",
        "processed_at": "2024-01-15T10:30:00Z"
    }
}
```

## Signal Generation Endpoints

### Generate Trading Signals

**Endpoint**: `POST /v1/signals/generate`

Generate trading signals based on sentiment analysis.

#### Request

```json
{
    "entity": "AAPL",
    "timeframe": "1h",
    "signal_types": ["sentiment", "momentum", "correlation"],
    "lookback_hours": 24,
    "options": {
        "include_confidence": true,
        "include_analysis": true
    }
}
```

#### Response

```json
{
    "status": "success",
    "data": {
        "entity": "AAPL",
        "signals": [
            {
                "type": "sentiment",
                "signal": "buy",
                "strength": 0.75,
                "confidence": 0.82,
                "timestamp": "2024-01-15T10:30:00Z",
                "reasoning": "Strong positive sentiment increase over 4-hour window"
            },
            {
                "type": "momentum",
                "signal": "hold", 
                "strength": 0.45,
                "confidence": 0.67,
                "timestamp": "2024-01-15T10:30:00Z",
                "reasoning": "Sentiment momentum slowing but still positive"
            }
        ],
        "overall_signal": {
            "recommendation": "buy",
            "confidence": 0.74,
            "risk_level": "medium"
        },
        "analysis": {
            "sentiment_trend": "improving",
            "volume_analysis": "above_average",
            "correlation_signals": ["tech_sector_positive", "market_bullish"]
        }
    }
}
```

### Historical Signals

**Endpoint**: `GET /v1/signals/history`

Retrieve historical trading signals for backtesting and analysis.

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `entity` | string | Yes | Ticker symbol or entity |
| `start_date` | string | Yes | Start date (ISO 8601) |
| `end_date` | string | Yes | End date (ISO 8601) |
| `signal_types` | array | No | Filter by signal types |
| `limit` | integer | No | Maximum results (default: 100, max: 1000) |

#### Example Request

```http
GET /v1/signals/history?entity=AAPL&start_date=2024-01-01T00:00:00Z&end_date=2024-01-15T23:59:59Z&limit=50
Authorization: Bearer YOUR_API_KEY
```

#### Response

```json
{
    "status": "success",
    "data": {
        "entity": "AAPL",
        "period": {
            "start": "2024-01-01T00:00:00Z",
            "end": "2024-01-15T23:59:59Z"
        },
        "signals": [
            {
                "timestamp": "2024-01-15T09:00:00Z",
                "signal": "buy",
                "strength": 0.78,
                "confidence": 0.85,
                "type": "sentiment",
                "price_at_signal": 185.23
            }
        ],
        "statistics": {
            "total_signals": 42,
            "buy_signals": 18,
            "sell_signals": 12,
            "hold_signals": 12,
            "average_confidence": 0.76
        }
    },
    "pagination": {
        "current_page": 1,
        "total_pages": 1,
        "total_results": 42
    }
}
```

## Data Collection Endpoints

### Market Data

**Endpoint**: `GET /v1/data/market`

Retrieve market data with sentiment overlay.

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbols` | string | Yes | Comma-separated ticker symbols |
| `interval` | string | No | Data interval (1m, 5m, 1h, 1d) |
| `period` | string | No | Time period (1d, 5d, 1mo, 3mo, 1y) |
| `include_sentiment` | boolean | No | Include sentiment data overlay |

#### Example Request

```http
GET /v1/data/market?symbols=AAPL,TSLA,MSFT&interval=1h&period=1d&include_sentiment=true
Authorization: Bearer YOUR_API_KEY
```

#### Response

```json
{
    "status": "success",
    "data": {
        "symbols": ["AAPL", "TSLA", "MSFT"],
        "interval": "1h",
        "market_data": [
            {
                "symbol": "AAPL",
                "timestamp": "2024-01-15T10:00:00Z",
                "price": 185.23,
                "volume": 125000,
                "sentiment": {
                    "score": 0.75,
                    "sources_count": 142,
                    "trending_topics": ["earnings", "iPhone", "growth"]
                }
            }
        ]
    }
}
```

### Social Media Data

**Endpoint**: `GET /v1/data/social`

Retrieve aggregated social media sentiment data.

#### Request

```http
GET /v1/data/social?entity=AAPL&sources=twitter,reddit&timeframe=24h&sentiment_filter=positive
Authorization: Bearer YOUR_API_KEY
```

#### Response

```json
{
    "status": "success",
    "data": {
        "entity": "AAPL",
        "timeframe": "24h",
        "sources": ["twitter", "reddit"],
        "posts": [
            {
                "id": "post_12345",
                "text": "AAPL earnings beat expectations! 🚀",
                "source": "twitter",
                "timestamp": "2024-01-15T10:15:00Z",
                "sentiment": {
                    "score": 0.82,
                    "confidence": 0.89
                },
                "engagement": {
                    "likes": 245,
                    "shares": 67,
                    "comments": 34
                }
            }
        ],
        "summary": {
            "total_posts": 1247,
            "average_sentiment": 0.68,
            "sentiment_distribution": {
                "positive": 743,
                "neutral": 342,
                "negative": 162
            },
            "trending_keywords": ["earnings", "beat", "growth", "bullish"]
        }
    }
}
```

## Utility Endpoints

### Entity Recognition

**Endpoint**: `POST /v1/entities/extract`

Extract financial entities from text.

#### Request

```json
{
    "text": "Apple and Microsoft are outperforming the S&P 500 this quarter",
    "entity_types": ["stock", "index", "company"]
}
```

#### Response

```json
{
    "status": "success",
    "data": {
        "entities": [
            {
                "text": "Apple",
                "type": "company",
                "symbol": "AAPL",
                "confidence": 0.95,
                "start_pos": 0,
                "end_pos": 5
            },
            {
                "text": "Microsoft", 
                "type": "company",
                "symbol": "MSFT",
                "confidence": 0.92,
                "start_pos": 10,
                "end_pos": 19
            },
            {
                "text": "S&P 500",
                "type": "index",
                "symbol": "SPY",
                "confidence": 0.98,
                "start_pos": 49,
                "end_pos": 56
            }
        ]
    }
}
```

### Health Check

**Endpoint**: `GET /v1/health`

Check API health and system status.

#### Response

```json
{
    "status": "healthy",
    "version": "v1.2.0",
    "timestamp": "2024-01-15T10:30:00Z",
    "services": {
        "sentiment_engine": "healthy",
        "database": "healthy",
        "redis_cache": "healthy",
        "external_apis": "healthy"
    },
    "performance": {
        "avg_response_time_ms": 45,
        "requests_per_minute": 120,
        "error_rate_percent": 0.02
    }
}
```

## Error Handling

### Error Response Format

```json
{
    "status": "error",
    "error": {
        "code": "INVALID_REQUEST",
        "message": "The request text exceeds the maximum length of 10,000 characters",
        "details": {
            "field": "text",
            "provided_length": 15000,
            "max_length": 10000
        }
    },
    "request_id": "req_12345",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Request format or parameters invalid |
| `UNAUTHORIZED` | 401 | Invalid or missing authentication |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMITED` | 429 | Rate limit exceeded |
| `INTERNAL_ERROR` | 500 | Internal server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

## Rate Limiting

### Rate Limit Headers

All API responses include rate limiting headers:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 995
X-RateLimit-Reset: 1642248600
X-RateLimit-Window: 3600
```

### Rate Limit Tiers

| Tier | Requests/Hour | Batch Size | WebSocket Connections |
|------|---------------|------------|----------------------|
| Free | 100 | 10 | 1 |
| Standard | 1,000 | 50 | 5 |
| Premium | 10,000 | 200 | 20 |
| Enterprise | Unlimited | 1,000 | 100 |

## SDK Examples

### Python SDK

```python
from feargreed_sentiment import SentimentAPI

# Initialize client
client = SentimentAPI(api_key="your_api_key")

# Analyze single text
result = client.analyze_sentiment(
    text="AAPL is showing strong bullish momentum",
    entity="AAPL",
    include_confidence=True
)

print(f"Sentiment: {result.sentiment.label} ({result.sentiment.score})")
print(f"Confidence: {result.sentiment.confidence}")

# Batch analysis
texts = [
    {"id": "1", "text": "Market is crashing!", "entity": "SPY"},
    {"id": "2", "text": "Buy the dip on AAPL", "entity": "AAPL"}
]

batch_results = client.analyze_batch(texts)
for result in batch_results.results:
    print(f"{result.id}: {result.sentiment.label}")

# Generate signals
signals = client.generate_signals(
    entity="AAPL",
    timeframe="1h",
    signal_types=["sentiment", "momentum"]
)

print(f"Overall recommendation: {signals.overall_signal.recommendation}")
```

### JavaScript SDK

```javascript
import { SentimentAPI } from 'feargreed-sentiment';

// Initialize client
const client = new SentimentAPI({
    apiKey: 'your_api_key',
    baseURL: 'https://api.feargreed-sentiment.com/v1'
});

// Analyze sentiment
async function analyzeSentiment() {
    try {
        const result = await client.analyzeSentiment({
            text: "Tesla stock is mooning! 🚀",
            entity: "TSLA",
            options: {
                includeConfidence: true,
                includeBreakdown: true
            }
        });
        
        console.log('Sentiment:', result.sentiment.label);
        console.log('Score:', result.sentiment.score);
        console.log('Confidence:', result.sentiment.confidence);
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Real-time streaming
const stream = client.createSentimentStream();

stream.on('connected', () => {
    console.log('Connected to sentiment stream');
});

stream.on('result', (result) => {
    console.log('Real-time sentiment:', result);
});

stream.on('error', (error) => {
    console.error('Stream error:', error);
});

// Send text for analysis
stream.analyze({
    text: "Breaking news: Apple reports record earnings",
    entity: "AAPL"
});
```

### cURL Examples

#### Single Sentiment Analysis

```bash
curl -X POST "https://api.feargreed-sentiment.com/v1/sentiment/analyze" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "AAPL showing strong bullish momentum",
    "entity": "AAPL",
    "options": {
      "include_confidence": true
    }
  }'
```

#### Generate Trading Signals

```bash
curl -X POST "https://api.feargreed-sentiment.com/v1/signals/generate" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "entity": "AAPL",
    "timeframe": "1h",
    "signal_types": ["sentiment", "momentum"],
    "lookback_hours": 24
  }'
```

#### Get Market Data

```bash
curl -X GET "https://api.feargreed-sentiment.com/v1/data/market?symbols=AAPL,TSLA&interval=1h&include_sentiment=true" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Webhooks

### Webhook Configuration

Configure webhooks to receive real-time notifications when sentiment changes significantly.

#### Setup Webhook

```json
{
    "url": "https://your-app.com/webhooks/sentiment",
    "events": ["sentiment_alert", "signal_generated"],
    "filters": {
        "entities": ["AAPL", "TSLA", "MSFT"],
        "sentiment_threshold": 0.7,
        "confidence_threshold": 0.8
    },
    "secret": "your_webhook_secret"
}
```

#### Webhook Payload

```json
{
    "event": "sentiment_alert",
    "timestamp": "2024-01-15T10:30:00Z",
    "data": {
        "entity": "AAPL",
        "sentiment": {
            "score": 0.85,
            "label": "positive",
            "confidence": 0.91
        },
        "trigger": {
            "type": "threshold_exceeded",
            "threshold": 0.7,
            "previous_score": 0.65
        },
        "source_summary": {
            "total_sources": 156,
            "twitter": 89,
            "reddit": 45,
            "news": 22
        }
    },
    "signature": "sha256=abcd1234..."
}
```

This comprehensive API documentation provides developers with all the necessary information to integrate with the Fear & Greed Sentiment Engine, from basic sentiment analysis to advanced trading signal generation and real-time data streaming.
