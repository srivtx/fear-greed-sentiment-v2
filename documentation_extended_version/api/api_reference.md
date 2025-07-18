# Fear & Greed Sentiment Engine - API Reference

## 📋 Overview

The Fear & Greed Sentiment Engine provides a RESTful API for accessing real-time sentiment analysis, Fear & Greed Index calculations, trading signals, and system metrics.

---

## 🌐 Base URL and Access

```
Development: http://localhost:5000/api/
Production: https://your-domain.com/api/
```

**API Version**: v1  
**Authentication**: None required (development)  
**Content Type**: `application/json`  
**Rate Limiting**: 100 requests/minute (development)

---

## 📊 Core Endpoints

### **1. Sentiment Analysis**

#### `GET /api/sentiment`
Get current sentiment analysis and Fear & Greed Index.

**Example Request:**
```bash
curl -X GET "http://localhost:5000/api/sentiment"
```

**Example Response:**
```json
{
  "fear_greed_index": {
    "fear_greed_index": 67.3,
    "market_sentiment": "Greed",
    "total_mentions": 247,
    "timestamp": "2025-07-17T14:30:22Z"
  },
  "sentiment_breakdown": {
    "positive": 64.2,
    "negative": 15.8,
    "neutral": 20.0
  },
  "data_sources": {
    "reddit": 172,
    "news": 45,
    "market": 30
  },
  "processing_time_ms": 245
}
```

### **2. Trading Signals**

#### `GET /api/signals`
Get current trading signals based on sentiment analysis.

**Example Request:**
```bash
curl -X GET "http://localhost:5000/api/signals"
```

**Example Response:**
```json
{
  "signals": [
    {
      "asset": "Bitcoin",
      "signal": "BUY",
      "confidence": 0.78,
      "reasoning": [
        "Fear & Greed Index: 67.3 (Greed)",
        "Positive sentiment: 64.2%",
        "High engagement: 892 interactions"
      ],
      "risk_level": "Medium",
      "timestamp": "2025-07-17T14:30:22Z"
    },
    {
      "asset": "Ethereum",
      "signal": "HOLD",
      "confidence": 0.62,
      "reasoning": [
        "Neutral sentiment: 55.1%",
        "Mixed signals from sources"
      ],
      "risk_level": "Low",
      "timestamp": "2025-07-17T14:30:22Z"
    }
  ],
  "total_signals": 2,
  "last_updated": "2025-07-17T14:30:22Z"
}
```

### **3. Historical Data**

#### `GET /api/historical_data`
Get historical sentiment and Fear & Greed Index data.

**Example Request:**
```bash
curl -X GET "http://localhost:5000/api/historical_data"
```

**Example Response:**
```json
{
  "historical_data": [
    {
      "timestamp": "2025-07-17T14:00:00Z",
      "fear_greed_index": 65.8,
      "sentiment": "Greed",
      "data_points": 198
    },
    {
      "timestamp": "2025-07-17T14:30:00Z",
      "fear_greed_index": 67.3,
      "sentiment": "Greed",
      "data_points": 247
    }
  ],
  "period": "24_hours",
  "total_records": 48
}
```

### **4. System Statistics**

#### `GET /api/system_stats`
Get system performance metrics and health status.

**Example Request:**
```bash
curl -X GET "http://localhost:5000/api/system_stats"
```

**Example Response:**
```json
{
  "system_health": {
    "status": "healthy",
    "uptime_seconds": 3600,
    "threads_active": 11,
    "memory_usage_mb": 52.3
  },
  "performance_metrics": {
    "texts_processed": 1247,
    "processing_speed": "174.2 texts/minute",
    "average_latency_ms": 87,
    "api_calls_made": 45
  },
  "data_collection": {
    "reddit_posts": 172,
    "news_articles": 45,
    "market_updates": 30,
    "last_collection": "2025-07-17T14:29:45Z"
  },
  "signal_generation": {
    "signals_generated": 7,
    "buy_signals": 3,
    "sell_signals": 1,
    "hold_signals": 3
  }
}
```

### **5. Data Collection Trigger**

#### `POST /api/run_collection`
Manually trigger a new data collection cycle.

**Example Request:**
```bash
curl -X POST "http://localhost:5000/api/run_collection"
```

**Example Response:**
```json
{
  "status": "success",
  "message": "Data collection initiated",
  "collection_id": "collection_20250717_143022",
  "estimated_completion": "2025-07-17T14:32:00Z"
}
```

---

## 🔧 Integration Examples

### **Python Integration**
```python
import requests
import json

class SentimentAPI:
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url
    
    def get_sentiment(self):
        """Get current sentiment analysis"""
        response = requests.get(f"{self.base_url}/sentiment")
        return response.json()
    
    def get_signals(self):
        """Get trading signals"""
        response = requests.get(f"{self.base_url}/signals")
        return response.json()
    
    def get_fear_greed_index(self):
        """Get Fear & Greed Index only"""
        data = self.get_sentiment()
        return data['fear_greed_index']['fear_greed_index']

# Usage example
api = SentimentAPI()
sentiment = api.get_sentiment()
fear_greed = api.get_fear_greed_index()
signals = api.get_signals()

print(f"Fear & Greed Index: {fear_greed}")
print(f"Market Sentiment: {sentiment['fear_greed_index']['market_sentiment']}")
```

### **JavaScript Integration**
```javascript
class SentimentAPI {
    constructor(baseUrl = 'http://localhost:5000/api') {
        this.baseUrl = baseUrl;
    }
    
    async getSentiment() {
        const response = await fetch(`${this.baseUrl}/sentiment`);
        return response.json();
    }
    
    async getSignals() {
        const response = await fetch(`${this.baseUrl}/signals`);
        return response.json();
    }
    
    async getSystemStats() {
        const response = await fetch(`${this.baseUrl}/system_stats`);
        return response.json();
    }
}

// Usage example
const api = new SentimentAPI();

api.getSentiment().then(data => {
    console.log('Fear & Greed Index:', data.fear_greed_index.fear_greed_index);
    console.log('Market Sentiment:', data.fear_greed_index.market_sentiment);
});
```

### **cURL Examples**
```bash
# Get sentiment with formatted output
curl -s "http://localhost:5000/api/sentiment" | jq '.fear_greed_index'

# Get only the Fear & Greed Index number
curl -s "http://localhost:5000/api/sentiment" | jq '.fear_greed_index.fear_greed_index'

# Get trading signals
curl -s "http://localhost:5000/api/signals" | jq '.signals[]'

# Monitor system health
curl -s "http://localhost:5000/api/system_stats" | jq '.system_health'
```

---

## 📊 Error Handling

### **Standard HTTP Status Codes**
- **200**: Success
- **400**: Bad Request
- **404**: Not Found
- **429**: Rate Limit Exceeded
- **500**: Internal Server Error

### **Error Response Format**
```json
{
  "error": "ValidationError",
  "message": "Invalid request parameters",
  "code": 400,
  "timestamp": "2025-07-17T14:30:22Z"
}
```

### **Common Error Scenarios**
```bash
# No sentiment data available
{
  "error": "NoDataError",
  "message": "No sentiment data available. Run data collection first.",
  "code": 404
}

# System overloaded
{
  "error": "SystemOverloadError", 
  "message": "System is processing. Please try again in a few seconds.",
  "code": 503
}
```

---

## 🎯 Rate Limiting

### **Current Limits**
- **Development**: 100 requests/minute
- **Production**: 1000 requests/hour

### **Rate Limit Headers**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642684800
```

### **Handling Rate Limits**
```python
import time
import requests

def api_call_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            # Rate limited, wait and retry
            time.sleep(60)
            continue
        else:
            response.raise_for_status()
    
    raise Exception("Max retries exceeded")
```

---

## 🔍 Testing the API

### **Health Check**
```bash
# Test if API is running
curl -I "http://localhost:5000/api/sentiment"
```

### **Quick Validation**
```bash
# Test all endpoints
curl "http://localhost:5000/api/sentiment" && echo
curl "http://localhost:5000/api/signals" && echo  
curl "http://localhost:5000/api/system_stats" && echo
```

### **Performance Testing**
```bash
# Test response times
time curl -s "http://localhost:5000/api/sentiment" > /dev/null
```

---

## 📚 Additional Resources

### **Related Documentation**
- **[Web Dashboard Guide](../../docs/EXTENDED_GUIDE.md#web-dashboard-guide)** - Dashboard usage
- **[System Overview](../../docs/SYSTEM_OVERVIEW.md)** - Architecture details
- **[Testing Guide](../../docs/TESTING_GUIDE.md)** - API testing procedures

### **Code Examples**
- **Python Examples**: `/scripts/api_examples.py`
- **JavaScript Examples**: `/static/js/api_client.js`
- **Dashboard Source**: `/templates/dashboard.html`

---

**🎉 This API provides real-time access to comprehensive sentiment analysis and trading signals!**
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
