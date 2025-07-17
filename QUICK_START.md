# 🚀 GoQuant Quick Start Guide

**Just downloaded the code? Get running in 5 minutes!**

## 📦 Step 1: Installation (2 minutes)

### Prerequisites
- Python 3.8+ installed
- Git installed

### Quick Setup
```bash
# 1. Clone the repository (if not already done)
git clone https://github.com/srivtx/fear-greed-sentiment-v2.git
cd fear-greed-sentiment-v2

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download NLTK data (required)
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('wordnet')"
```

**✅ Installation Complete!** You're ready to run the system.

---

## 🎯 Step 2: Choose Your Mode (30 seconds)

| I want to... | Use this command | Time needed |
|--------------|------------------|-------------|
| **Quick Fear & Greed analysis** | `python main.py` | 1-2 minutes |
| **See live trading signals** | `real-time` mode | 1-5 minutes |
| **Get a complete analysis report** | `batch` mode | 2-5 minutes |
| **Test system performance** | `performance-test` mode | 2-10 minutes |
| **Try the original engine** | `legacy` mode | 1-2 minutes |

---

## 🏃‍♂️ Step 3: Run Your Chosen Mode

### 🎯 Option 1: Simple Fear & Greed Analysis (Recommended for Beginners)

**What it does**: Quick sentiment analysis with Fear & Greed Index calculation

```bash
# Simple one-click run
python main.py
```

**Expected output:**
```
Fear & Greed Sentiment Analysis Engine
=====================================
Collecting data from social media and news...
✓ Collected 173 Reddit posts
✓ Collected 34 news articles
✓ Collected market data for 13 symbols

Analyzing sentiment...
✓ Processed 207 texts with VADER sentiment analysis
✓ Applied financial lexicons and entity recognition

Results:
Fear & Greed Index: 70.87 (Greed)
Overall Sentiment: 0.142 (Positive)
Market Sentiment: Bullish

Generated 3 trading signals:
✓ BTC: STRONG_BUY (confidence: 0.85)
✓ ETH: HOLD (confidence: 0.72)  
✓ Overall Market: BUY (confidence: 0.78)

✓ Created 5 visualizations in data/visualizations/
✓ Analysis complete!
```

**Files created:**
- `data/collection/` - Raw collected data
- `data/sentiment/` - Sentiment analysis results  
- `data/signals/` - Trading signals
- `data/visualizations/` - Charts and graphs

**Perfect for:** First-time users, quick analysis, simple trading signals

---

### 🔄 Option 2: Real-Time Mode (Live Trading Signals)

**What it does**: Continuously monitors Reddit, news, and markets to generate live trading signals

```bash
# Quick 2-minute test
python goquant_main.py --mode=real-time --duration=2 --no-twitter

# Run for 5 minutes (recommended for first try)
python goquant_main.py --mode=real-time --duration=5 --no-twitter

# Run indefinitely (Ctrl+C to stop)
python goquant_main.py --mode=real-time --no-twitter
```

**Expected output:**
```
Starting GoQuant Fear & Greed Engine in REAL-TIME mode
============================================================
Real-time engine started successfully
Processing social media and market data streams...
Generating sentiment analysis and trading signals...

=== PERFORMANCE METRICS ===
Texts processed: 175 (174.0/min)
Signals generated: 7 (7.0/min)
```

**Perfect for:** Live trading, production systems, continuous monitoring

---

### 📊 Option 3: Batch Mode (Complete Analysis Report)

**What it does**: Collects data, analyzes sentiment, generates signals, and creates visualizations

```bash
# Full analysis (recommended for first try)
python goquant_main.py --mode=batch --no-twitter

# Quick Reddit-only analysis
python goquant_main.py --mode=batch --source=reddit --no-twitter

# Analyze only existing data (faster)
python goquant_main.py --mode=batch --analyze-only --no-twitter
```

**Expected output:**
```
Starting GoQuant Fear & Greed Engine in BATCH mode
============================================================
Phase 1: Data Collection
Phase 2: Advanced Sentiment Analysis
Phase 3: Advanced Signal Generation
Phase 4: Visualization Generation
BATCH PROCESSING COMPLETED
```

**Files created:**
- `data/collection/` - Raw data
- `data/sentiment/` - Analysis results
- `data/signals/` - Trading signals
- `data/visualizations/` - Charts and graphs

**Perfect for:** Research, backtesting, detailed analysis reports

---

### ⚡ Option 4: Performance Test (System Benchmark)

**What it does**: Tests if the system meets high-frequency trading requirements

```bash
# Quick 2-minute test
python goquant_main.py --mode=performance-test --duration=2 --no-twitter

# Standard 5-minute test (recommended)
python goquant_main.py --mode=performance-test --duration=5 --no-twitter

# Extended 10-minute test
python goquant_main.py --mode=performance-test --duration=10 --no-twitter
```

**Expected output:**
```
PERFORMANCE TEST RESULTS
============================================================
GoQuant Requirements Analysis:
✅ Sentiment Analysis: PASSED (0.13ms < 100ms target)
✅ Signal Generation: PASSED (245ms < 500ms target)
❌ Throughput: FAILED (174/min < 10,000/min target)
⚠️ MOST GOQUANT REQUIREMENTS MET
Pass rate: 66.7% (2/3)
```

**Perfect for:** System validation, performance optimization, compliance testing

---

### 🔙 Option 5: Legacy Mode (Original Engine)

**What it does**: Runs the original simple engine for comparison

```bash
# Basic run
python goquant_main.py --mode=legacy --no-twitter
```

**Expected output:**
```
Fear & Greed Index: 70.87 (Greed)
Generated 3 trading signals
Created 5 visualizations
```

**Perfect for:** Compatibility testing, simple debugging, comparison with new system

---

## 🛠️ Step 4: Troubleshooting

### ❌ Common Issues & Solutions

**Issue**: `ModuleNotFoundError: No module named 'nltk'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue**: `LookupError: Resource vader_lexicon not found`
```bash
# Solution: Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('punkt_tab')"
```

**Issue**: Twitter rate limiting errors
```bash
# Solution: Always use --no-twitter flag
python goquant_main.py --mode=real-time --no-twitter
```

**Issue**: Slow performance or high memory usage
```bash
# Solution: Limit duration
python goquant_main.py --mode=real-time --duration=5 --no-twitter
```

**Issue**: Permission errors on Windows
```bash
# Solution: Run as administrator or use different directory
```

---

## 📋 Step 5: Understanding the Output

### Real-Time Mode Output
```
Texts processed: 175 (174.0/min)     # Social media posts analyzed
Signals generated: 7 (7.0/min)       # Trading signals created
Queue sizes: Data=0, Sentiment=0     # System health (0 = good)
```

### Batch Mode Files
```
data/
├── collection/          # Raw data from Reddit, news, markets
├── sentiment/          # Sentiment analysis results
├── signals/           # Trading signals with reasoning
└── visualizations/    # Charts and graphs (.png files)
```

### Performance Test Results
```
✅ PASSED = Meets requirements
❌ FAILED = Needs optimization  
⚠️ PARTIAL = Most requirements met
```

---

## 🎯 Step 6: Next Steps

### For Beginners (Start Here!)
```bash
# Simple Fear & Greed analysis
python main.py
```

### For Traders
```bash
# Start with real-time mode for live signals
python goquant_main.py --mode=real-time --duration=10 --no-twitter
```

### For Researchers
```bash
# Use batch mode for comprehensive analysis
python goquant_main.py --mode=batch --no-twitter
```

### For Developers
```bash
# Test system performance first
python goquant_main.py --mode=performance-test --duration=5 --no-twitter

# Then try real-time development
python goquant_main.py --mode=real-time --duration=2 --no-twitter --log-level=DEBUG
```

---

## 🔧 Advanced Options

### Debug Mode
```bash
# See detailed logs
python goquant_main.py --mode=real-time --duration=2 --log-level=DEBUG
```

### Specific Data Sources
```bash
# Reddit only
python goquant_main.py --mode=batch --source=reddit --no-twitter

# News only  
python goquant_main.py --mode=batch --source=news --no-twitter

# Market data only
python goquant_main.py --mode=batch --source=market --no-twitter
```

### Custom Duration
```bash
# 30 seconds (very quick test)
python goquant_main.py --mode=real-time --duration=0.5 --no-twitter

# 1 hour (extended analysis)
python goquant_main.py --mode=real-time --duration=60 --no-twitter
```

---

## 🆘 Getting Help

### Check Logs
```bash
# Logs are saved to: fear_greed_engine_YYYYMMDD.log
tail -f fear_greed_engine_*.log
```

### Test Individual Components
```bash
# Test basic functionality (simple Fear & Greed analysis)
python main.py

# Test web interface
python web_app.py
```

### Verify Installation
```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip list | grep -E "(nltk|pandas|numpy|requests)"
```

---

## 🎉 Success Checklist

- [ ] ✅ **Installation completed** without errors
- [ ] ✅ **Simple mode** (`python main.py`) runs successfully
- [ ] ✅ **Real-time mode** runs and shows metrics
- [ ] ✅ **Batch mode** creates files in `data/` directory
- [ ] ✅ **Performance test** shows results
- [ ] ✅ **No critical errors** in logs

**🎊 Congratulations! You're running the GoQuant Fear & Greed Sentiment Engine!**

---

## 📚 What's Next?

1. **Read the full guide**: `GOQUANT_MODES_GUIDE.md`
2. **Explore the code**: Start with `goquant_main.py`
3. **Customize settings**: Edit `config/config.json`
4. **Add your APIs**: Set up Reddit/News API keys for more data
5. **Build your strategy**: Modify signal generation logic

**Happy Trading! 📈🚀**
