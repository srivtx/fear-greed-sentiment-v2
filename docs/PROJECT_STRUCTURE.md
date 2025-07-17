# 📁 Fear & Greed Sentiment Engine - Project Structure Guide

## 🏗️ Project Overview

This document provides a comprehensive overview of the Fear & Greed Sentiment Engine project structure, file organization, and component relationships.

---

## 📊 Directory Structure

```
fear-greed-sentiment-v2/
├── 📁 Root Files
│   ├── quick_start.sh              # Main entry point with GoQuant integration
│   ├── main.py                     # Basic sentiment analysis engine
│   ├── goquant_main.py             # Advanced GoQuant engine (real-time, batch, performance)
│   ├── web_app.py                  # Flask web dashboard
│   ├── real_time_engine.py         # Real-time processing engine
│   ├── engine.py                   # Core Fear & Greed engine
│   ├── advanced_sentiment_analyzer.py   # Advanced NLP analysis
│   ├── advanced_signal_generator.py     # Advanced trading signals
│   ├── setup.py                    # Python package setup
│   └── requirements.txt            # Python dependencies
│
├── 📁 config/                      # Configuration files
│   ├── __init__.py
│   ├── config.py                   # Configuration management
│   ├── config.json                 # Main configuration
│   └── config.json.example         # Example configuration
│
├── 📁 data/                        # Data storage (auto-generated)
│   ├── collection_*/               # Raw data collections
│   ├── sentiment_*/                # Sentiment analysis results
│   ├── signals/                    # Trading signals
│   ├── visualizations/             # Generated charts
│   ├── market_cache/               # Market data cache
│   └── temp/                       # Temporary files
│
├── 📁 data_collection/             # Data collection modules
│   ├── __init__.py
│   ├── collector.py                # Main data collector
│   ├── financial/                  # Financial data collectors
│   ├── news/                       # News data collectors
│   ├── reddit/                     # Reddit data collectors
│   └── twitter/                    # Twitter data collectors
│
├── 📁 sentiment_analysis/          # Sentiment analysis modules
│   ├── __init__.py
│   ├── analyzer.py                 # Main sentiment analyzer
│   ├── sentiment_analyzer.py       # VADER sentiment analysis
│   ├── preprocessor.py             # Text preprocessing
│   └── entitiy_recognition.py      # Entity recognition
│
├── 📁 signal_generation/           # Trading signal generation
│   ├── __init__.py
│   ├── signal_generator.py         # Main signal generator
│   └── correlation_engine.py       # Correlation analysis
│
├── 📁 utils/                       # Utility modules
│   ├── __init__.py
│   └── visualization.py            # Chart and graph generation
│
├── 📁 backtesting/                 # Backtesting framework
│   ├── __init__.py
│   └── backtester.py               # Backtesting engine
│
├── 📁 templates/                   # HTML templates for web dashboard
│   └── dashboard.html              # Main dashboard template
│
├── 📁 scripts/                     # Utility scripts
│   ├── setup/                      # Setup scripts
│   │   ├── quick_setup.sh          # Quick setup script
│   │   ├── setup.sh                # Standard setup script
│   │   └── setup_production.sh     # Production setup script
│   ├── testing/                    # Testing scripts
│   │   ├── run_tests.sh            # Test runner with menu
│   │   └── run_tests_demo.sh       # Demo test runner
│   ├── download_nltk_data.py       # NLTK data downloader
│   └── real_world_demo.py          # Real-world demonstration
│
├── 📁 tests/                       # Test files
│   ├── test_comprehensive_suite.py # Complete system testing
│   ├── validate_signals.py         # Signal validation
│   └── dashboard_validation.py     # Dashboard validation
│
├── 📁 docs/                        # Documentation
│   ├── EXTENDED_GUIDE.md           # Comprehensive user guide
│   ├── TESTING_GUIDE.md            # Testing and validation guide
│   ├── GOQUANT_MODES_GUIDE.md      # GoQuant modes explanation
│   ├── PROJECT_STRUCTURE.md        # This file
│   ├── SYSTEM_OVERVIEW.md          # System architecture overview
│   ├── REALTIME_ENGINE_EXPLAINED.md # Real-time engine deep dive
│   ├── IMPROVEMENTS.md             # Feature improvements
│   └── README_old.md               # Previous README version
│
├── 📁 logs/                        # Log files
│   └── fear_greed_engine_*.log     # System logs
│
├── 📁 documentation/               # Additional documentation
│   ├── README.md                   # Documentation index
│   ├── api/                        # API documentation
│   ├── assignment/                 # Assignment requirements
│   ├── beginner_guide/             # Beginner tutorials
│   ├── deployment/                 # Deployment guides
│   ├── development/                # Development guidelines
│   ├── financial/                  # Financial analysis docs
│   ├── research/                   # Research papers
│   └── technical/                  # Technical documentation
│
└── 📁 Additional Files
    ├── .gitignore                  # Git ignore rules
    ├── .venv/                      # Virtual environment
    ├── README.md                   # Main project README
    ├── QUICK_START.md              # Quick start guide
    └── __pycache__/                # Python cache files
```

---

## 🚀 Component Overview

### **Core Engine Files**

| File | Purpose | Key Features |
|------|---------|--------------|
| `main.py` | Basic sentiment analysis | Simple one-time analysis |
| `goquant_main.py` | Advanced GoQuant engine | Real-time, batch, performance modes |
| `engine.py` | Core Fear & Greed engine | Main processing logic |
| `web_app.py` | Flask web dashboard | Interactive web interface |
| `real_time_engine.py` | Real-time processing | Continuous data processing |

### **Advanced Components**

| File | Purpose | Key Features |
|------|---------|--------------|
| `advanced_sentiment_analyzer.py` | Advanced NLP | Entity recognition, emotion analysis |
| `advanced_signal_generator.py` | Advanced signals | Risk assessment, correlation analysis |

### **GoQuant Modes**

| Mode | Command | Purpose |
|------|---------|---------|
| **Real-time** | `--mode=real-time` | Live trading with continuous processing |
| **Batch** | `--mode=batch` | Comprehensive analysis with reports |
| **Performance** | `--mode=performance-test` | System benchmarking |
| **Legacy** | `--mode=legacy` | Simple backward compatibility |

---

## 🛠️ Setup and Usage

### **Quick Start Options**

```bash
# Run the interactive quick start
./quick_start.sh

# Available options:
# 1. Basic data collection and analysis
# 2. Start web dashboard
# 3. Run system tests
# 4. GoQuant real-time engine
# 5. GoQuant batch analysis
# 6. GoQuant performance test
# 7. Complete setup and dashboard
# 8. GoQuant full pipeline
```

### **Direct GoQuant Usage**

```bash
# Real-time trading mode
python goquant_main.py --mode=real-time --duration=60

# Batch analysis mode
python goquant_main.py --mode=batch --source=reddit

# Performance testing
python goquant_main.py --mode=performance-test --duration=10
```

### **Testing Options**

```bash
# Run all tests
./scripts/testing/run_tests.sh

# Run specific test
python tests/test_comprehensive_suite.py
python tests/validate_signals.py
python tests/dashboard_validation.py
```

---

## 📊 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Data Collection Layer                        │
├─────────────────────────────────────────────────────────────────┤
│  Reddit API → News API → Twitter API → Market Data → Raw Data   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Data Processing Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  Text Preprocessing → Entity Recognition → Sentiment Analysis   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Analysis Layer                                │
├─────────────────────────────────────────────────────────────────┤
│  Fear & Greed Calculation → Signal Generation → Risk Assessment │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Output Layer                                 │
├─────────────────────────────────────────────────────────────────┤
│  Web Dashboard → API Endpoints → Trading Signals → Reports      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Configuration Management

### **Configuration Files**

- `config/config.json` - Main configuration
- `config/config.json.example` - Example configuration
- `config/config.py` - Configuration management class

### **Environment Variables**

```bash
# API Keys (recommended for production)
export REDDIT_CLIENT_ID="your_reddit_client_id"
export REDDIT_CLIENT_SECRET="your_reddit_client_secret"
export TWITTER_BEARER_TOKEN="your_twitter_bearer_token"
export NEWSAPI_KEY="your_newsapi_key"

# System Configuration
export PYTHONPATH="$(pwd)"
```

---

## 📈 Performance Monitoring

### **Key Metrics**

- **Throughput**: Texts processed per minute
- **Latency**: Response time for sentiment analysis
- **Accuracy**: Sentiment classification quality
- **Resource Usage**: CPU, memory, network utilization

### **Monitoring Tools**

- `tests/test_comprehensive_suite.py` - System health checks
- `tests/validate_signals.py` - Signal quality validation
- `tests/dashboard_validation.py` - Dashboard data validation

---

## 🚀 Deployment Options

### **Development Mode**

```bash
# Quick development setup
./quick_start.sh
# Select option 1 or 2 for development
```

### **Production Mode**

```bash
# Production setup
./scripts/setup/setup_production.sh

# Start production services
python goquant_main.py --mode=real-time &
python web_app.py &
```

### **Testing Mode**

```bash
# Comprehensive testing
./scripts/testing/run_tests.sh

# Performance benchmarking
python goquant_main.py --mode=performance-test --duration=10
```

---

## 📚 Documentation Guide

### **For New Users**

1. **README.md** - Start here for project overview
2. **QUICK_START.md** - Quick setup instructions
3. **docs/EXTENDED_GUIDE.md** - Comprehensive user guide

### **For Developers**

1. **docs/SYSTEM_OVERVIEW.md** - System architecture
2. **docs/TESTING_GUIDE.md** - Testing procedures
3. **docs/GOQUANT_MODES_GUIDE.md** - GoQuant engine details

### **For Traders**

1. **docs/EXTENDED_GUIDE.md** - Trading signal interpretation
2. **tests/validate_signals.py** - Signal validation
3. **Web Dashboard** - Real-time monitoring

---

## 🔄 Maintenance and Updates

### **Regular Tasks**

- **Daily**: Run `tests/dashboard_validation.py`
- **Weekly**: Run `tests/test_comprehensive_suite.py`
- **Monthly**: Review and update configuration
- **Quarterly**: Performance optimization review

### **File Cleanup**

- **Logs**: `logs/` directory (automatically rotated)
- **Data**: `data/temp/` directory (cleared on restart)
- **Cache**: `__pycache__/` directories (auto-generated)

---

## 🎯 Key Features by Component

### **GoQuant Engine (`goquant_main.py`)**

- ✅ Real-time processing with multi-threading
- ✅ Batch analysis with comprehensive reports
- ✅ Performance testing and benchmarking
- ✅ Legacy mode for backward compatibility

### **Web Dashboard (`web_app.py`)**

- ✅ Real-time Fear & Greed gauge
- ✅ Interactive charts and visualizations
- ✅ Trading signals display
- ✅ API endpoints for integration

### **Sentiment Analysis (`sentiment_analysis/`)**

- ✅ VADER sentiment analysis
- ✅ Entity recognition and extraction
- ✅ Financial keyword detection
- ✅ Multi-source data processing

### **Signal Generation (`signal_generation/`)**

- ✅ BUY/SELL/HOLD signal generation
- ✅ Confidence scoring
- ✅ Risk assessment
- ✅ Correlation analysis

---

## 🏆 Project Highlights

- **🎯 Production Ready**: Full GoQuant integration with real-time processing
- **📊 Comprehensive**: Complete sentiment analysis pipeline
- **🚀 Scalable**: Multi-threaded architecture for high performance
- **🔧 Configurable**: Flexible configuration management
- **📈 Monitored**: Comprehensive testing and validation suite
- **🌐 Interactive**: Modern web dashboard with real-time updates
- **📚 Documented**: Extensive documentation and guides

---

## 🛠️ File Organization Best Practices

### **Directory Purpose**

| Directory | Purpose | Auto-generated |
|-----------|---------|----------------|
| `config/` | Configuration files | No |
| `data/` | Data storage | Yes |
| `data_collection/` | Data collection modules | No |
| `sentiment_analysis/` | NLP and sentiment modules | No |
| `signal_generation/` | Trading signal modules | No |
| `utils/` | Utility functions | No |
| `backtesting/` | Backtesting framework | No |
| `templates/` | HTML templates | No |
| `scripts/` | Utility scripts | No |
| `tests/` | Test files | No |
| `docs/` | Documentation | No |
| `logs/` | Log files | Yes |

### **File Naming Conventions**

- **Snake_case**: Python files (`main.py`, `goquant_main.py`)
- **Kebab-case**: Documentation (`EXTENDED_GUIDE.md`)
- **Timestamps**: Data files (`collection_20250717_130520/`)
- **Descriptive**: Clear purpose indication

---

## 🔍 Troubleshooting Guide

### **Common Issues**

1. **Missing Dependencies**: Check `requirements.txt`
2. **API Key Issues**: Verify `config/config.json`
3. **Permission Errors**: Check file permissions
4. **Port Conflicts**: Web dashboard port 5000

### **Debug Commands**

```bash
# Check system health
python tests/test_comprehensive_suite.py

# Validate configuration
python -c "from config.config import Config; print('Config OK')"

# Test web dashboard
curl http://localhost:5000/api/sentiment
```

---

**🎉 This project structure provides a professional, maintainable, and scalable Fear & Greed Sentiment Engine suitable for both development and production environments!**
