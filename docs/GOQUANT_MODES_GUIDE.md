# GoQuant Fear & Greed Sentiment Engine - Modes Guide

## 📋 Overview

The GoQuant Fear & Greed Sentiment Engine is an advanced financial sentiment analysis system with multiple operation modes designed for different use cases. This guide explains all available modes, their purposes, and how to use them effectively.

## 🏗️ System Architecture

```
GoQuantFearGreedEngine (Main Orchestrator)
├── RealTimeFearGreedEngine (Live Processing)
├── AdvancedFinancialSentimentAnalyzer (NLP Engine)
├── AdvancedSignalGenerator (Trading Signals)
├── FearGreedEngine (Legacy Compatibility)
├── DataCollector (Multi-source Data)
└── SentimentVisualizer (Charts & Graphs)
```

## 🚀 Operation Modes

### 1. 🔄 Real-Time Mode (Default)

**Purpose**: Live trading system with continuous processing

```bash
python goquant_main.py --mode=real-time [OPTIONS]
```

#### Features:
- ✅ **Continuous data streaming** from Reddit, News, Market APIs
- ✅ **11+ worker threads** running in parallel
- ✅ **Live signal generation** every few seconds
- ✅ **Real-time performance monitoring**
- ✅ **Queue-based processing** for high throughput
- ✅ **Runs indefinitely** (or until duration limit)

#### Architecture:
```
Data Sources → Queues → Sentiment Analysis → Signal Generation → Live Output
    ↓           ↓           ↓                    ↓                ↓
Reddit      Data Queue   4 Parallel         Signal Queue     Trading
News        ────────→    Processors         ────────→        Signals
Market                   (Multi-threaded)                    (Real-time)
```

#### Performance Metrics:
- **Throughput**: 174+ texts/minute
- **Processing**: <100ms per text
- **Signals**: Generated every few seconds
- **Threads**: 11+ parallel workers

#### Example Commands:
```bash
# Run indefinitely
python goquant_main.py --mode=real-time

# Run for 10 minutes
python goquant_main.py --mode=real-time --duration=10

# Skip Twitter (recommended)
python goquant_main.py --mode=real-time --no-twitter --duration=5
```

#### Best For:
- Live trading applications
- Production systems
- Real-time market monitoring
- Automated trading bots

---

### 2. 📊 Batch Mode

**Purpose**: One-time comprehensive analysis with detailed reporting

```bash
python goquant_main.py --mode=batch [OPTIONS]
```

#### Features:
- 📈 **4-Phase Processing Pipeline**
- 🔍 **Advanced NLP analysis**
- 📊 **Comprehensive visualizations**
- 💾 **Detailed file outputs**
- 🎯 **Entity sentiment recognition**
- 📋 **Performance reports**

#### Processing Phases:

**Phase 1: Data Collection**
```
Reddit Posts → News Articles → Market Data → Raw Dataset
```

**Phase 2: Advanced Sentiment Analysis**
```
Raw Text → NLP Processing → Entity Recognition → Sentiment Scores
```

**Phase 3: Signal Generation**
```
Sentiment Data → Trading Logic → Risk Assessment → Trading Signals
```

**Phase 4: Visualization**
```
All Data → Charts → Graphs → Reports → Saved Files
```

#### Output Files:
- `data/collection/` - Raw collected data
- `data/sentiment/` - Sentiment analysis results
- `data/signals/` - Trading signals with reasoning
- `data/visualizations/` - Charts and graphs

#### Example Commands:
```bash
# Full analysis
python goquant_main.py --mode=batch

# Reddit only
python goquant_main.py --mode=batch --source=reddit

# Analyze existing data
python goquant_main.py --mode=batch --analyze-only

# News and market data
python goquant_main.py --mode=batch --source=news
```

#### Best For:
- Research and backtesting
- Detailed analysis reports
- Strategy development
- Historical analysis

---

### 3. ⚡ Performance Test Mode

**Purpose**: Benchmark system against GoQuant requirements

```bash
python goquant_main.py --mode=performance-test [OPTIONS]
```

#### Features:
- 🎯 **GoQuant compliance testing**
- 📊 **Detailed performance metrics**
- ✅ **Pass/Fail assessment**
- 🔥 **Stress testing capabilities**
- 📈 **Benchmark reporting**

#### GoQuant Requirements Testing:

| Requirement | Target | Test Method |
|-------------|--------|-------------|
| **Sentiment Analysis** | <100ms per text | Real-time processing |
| **Signal Generation** | <500ms per signal | Live signal timing |
| **Throughput** | >10,000 texts/min | Volume stress test |

#### Sample Output:
```
PERFORMANCE TEST RESULTS
============================================================
GoQuant Requirements Analysis:
-----------------------------------
✅ Sentiment Analysis: PASSED
   Average: 0.13ms (target: <100ms)
   P95: 0.23ms

✅ Signal Generation: PASSED
   Average: 245ms (target: <500ms)

❌ Throughput: FAILED
   Achieved: 174.0 texts/min (target: >10,000/min)

Overall Assessment:
--------------------
⚠️ MOST GOQUANT REQUIREMENTS MET
Pass rate: 66.7% (2/3)
```

#### Example Commands:
```bash
# 5-minute test (default)
python goquant_main.py --mode=performance-test

# 2-minute quick test
python goquant_main.py --mode=performance-test --duration=2

# Extended 10-minute test
python goquant_main.py --mode=performance-test --duration=10
```

#### Best For:
- System validation
- Performance optimization
- Compliance testing
- Benchmarking

---

### 4. 🔙 Legacy Mode

**Purpose**: Original engine for compatibility and debugging

```bash
python goquant_main.py --mode=legacy [OPTIONS]
```

#### Features:
- 🔄 **Single-threaded processing**
- 📝 **Simple batch collection**
- ⚙️ **Basic sentiment analysis**
- 🔧 **Compatible with old workflows**
- 🐛 **Debugging and comparison**

#### Architecture:
```
Sequential Processing: Collect → Analyze → Generate → Visualize
```

#### Example Commands:
```bash
# Basic legacy run
python goquant_main.py --mode=legacy

# Skip Twitter
python goquant_main.py --mode=legacy --no-twitter
```

#### Best For:
- Debugging issues
- Comparing with new system
- Simple one-off analysis
- Backward compatibility

---

## 🎯 Mode Comparison Matrix

| Feature | real-time | batch | performance-test | legacy |
|---------|-----------|-------|------------------|--------|
| **Processing Style** | Continuous streaming | One-time complete | Benchmark testing | Simple batch |
| **Threading** | 11+ parallel | Mixed threading | 11+ parallel | Single thread |
| **Duration** | Indefinite/timed | Complete cycle | Timed test | One execution |
| **Output Format** | Live signals | Reports + files | Performance metrics | Basic results |
| **Data Sources** | All (streaming) | All (batch) | All (streaming) | All (simple) |
| **Complexity** | High | Very High | High | Low |
| **Resource Usage** | High | Medium | High | Low |
| **Use Case** | Live trading | Research | Validation | Compatibility |

## 🛠️ Command Line Options

### Global Options (All Modes)
```bash
--mode           # Operation mode: real-time, batch, performance-test, legacy
--no-twitter     # Skip Twitter data collection (recommended)
--log-level      # Logging level: DEBUG, INFO, WARNING, ERROR
```

### Mode-Specific Options

#### Real-Time & Performance-Test
```bash
--duration       # Duration in minutes (default: indefinite for real-time, 5 for performance-test)
```

#### Batch Mode
```bash
--source         # Data source: twitter, reddit, news, market, all
--analyze-only   # Only analyze existing data, skip collection
```

## 📊 Performance Metrics

### Real-Time Engine Metrics
- **Texts processed**: Total and per-minute rates
- **Signals generated**: Count and frequency
- **Processing time**: Average, P95, P99 percentiles
- **Queue sizes**: Data, sentiment, signal queue depths
- **Thread status**: Active worker threads
- **API calls**: Rate limiting and success rates

### Advanced Analyzer Metrics
- **Sentiment scores**: Overall sentiment with confidence
- **Entity recognition**: Named entities with sentiment
- **Financial relevance**: Text relevance to financial markets
- **Processing speed**: Texts per second throughput

### Signal Generator Metrics
- **Signal quality**: Confidence and strength scores
- **Risk assessment**: Risk scores and position sizing
- **Time horizons**: Short, medium, long-term signals
- **Reasoning**: Detailed explanations for each signal

## 🎛️ Configuration

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure APIs (optional)
export REDDIT_CLIENT_ID="your_reddit_client_id"
export REDDIT_CLIENT_SECRET="your_reddit_client_secret"
export NEWS_API_KEY="your_news_api_key"
```

### Data Sources Configuration
- **Reddit**: 4 subreddits (Bitcoin, CryptoCurrency, wallstreetbets, investing)
- **News**: Financial news APIs
- **Market Data**: CoinGecko (crypto) + Yahoo Finance (stocks)
- **Twitter**: Optional (rate-limited)

## 🚨 Troubleshooting

### Common Issues

**Issue**: Low throughput in performance tests
```bash
# Solution: Increase duration for better measurement
python goquant_main.py --mode=performance-test --duration=10
```

**Issue**: Twitter rate limiting
```bash
# Solution: Skip Twitter data
python goquant_main.py --mode=real-time --no-twitter
```

**Issue**: Memory usage in real-time mode
```bash
# Solution: Set duration limit
python goquant_main.py --mode=real-time --duration=30
```

### Debug Mode
```bash
# Enable debug logging
python goquant_main.py --mode=batch --log-level=DEBUG
```

## 📈 Example Workflows

### Production Trading Setup
```bash
# 1. Validate system
python goquant_main.py --mode=performance-test --duration=5

# 2. Run live trading
python goquant_main.py --mode=real-time --no-twitter
```

### Research Analysis
```bash
# 1. Collect comprehensive data
python goquant_main.py --mode=batch --source=all

# 2. Analyze specific source
python goquant_main.py --mode=batch --source=reddit

# 3. Re-analyze existing data
python goquant_main.py --mode=batch --analyze-only
```

### System Development
```bash
# 1. Test with legacy
python goquant_main.py --mode=legacy

# 2. Compare with new system
python goquant_main.py --mode=batch --source=reddit

# 3. Validate performance
python goquant_main.py --mode=performance-test
```

## 🔮 Future Enhancements

- **Multi-asset support**: Forex, commodities, bonds
- **Custom signal strategies**: User-defined trading logic
- **Real-time visualizations**: Live dashboards
- **Historical backtesting**: Strategy validation
- **API endpoints**: REST API for external systems
- **Machine learning**: Adaptive sentiment models

## 🤝 Contributing

To contribute to the GoQuant engine:

1. Fork the repository
2. Create a feature branch
3. Test with all modes
4. Submit a pull request

## 📞 Support

For issues or questions:
- Check the logs in `fear_greed_engine_YYYYMMDD.log`
- Run with `--log-level=DEBUG` for detailed output
- Use `--mode=legacy` for simple debugging

---

*GoQuant Fear & Greed Sentiment Engine - Advanced Financial Analysis System*
