# 🚀 Quick Start Guide - Fear & Greed Sentiment Engine

Welcome to the Fear & Greed Sentiment Engine! This guide will help you get started quickly using the interactive `quick_start.sh` script.

## 📋 Prerequisites

Before running the quick start script, ensure you have:

- **Python 3.8+** installed on your system
- **pip** package manager
- **Git** (if cloning the repository)
- **Internet connection** (for downloading dependencies and data)

## 🎯 Quick Start Commands

### 1. Clone and Navigate
```bash
git clone https://github.com/srivtx/fear-greed-sentiment-v2.git
cd fear-greed-sentiment-v2
```

### 2. Run the Quick Start Script
```bash
chmod +x quick_start.sh
./quick_start.sh
```

## 🛠️ What the Script Does Automatically

The `quick_start.sh` script performs the following setup steps:

1. **✅ System Check**: Verifies Python 3.8+ installation
2. **📦 Dependencies**: Installs all required Python packages from `requirements.txt`
3. **🧠 NLTK Data**: Downloads necessary natural language processing data
4. **⚙️ Configuration**: Creates config files from examples if needed
5. **📁 Directories**: Creates necessary data and log directories
6. **🎯 Interactive Menu**: Presents 8 different execution options

## 🎮 Interactive Menu Options

After the setup, you'll see an interactive menu with 8 options:

### Option 1: 🔄 Basic Data Collection and Analysis (Simple Mode)
**Best for**: First-time users, quick testing

**What it does**:
- Collects data from Reddit, news sources, and market APIs
- Performs sentiment analysis on collected data
- Generates a Fear & Greed Index
- Starts the web dashboard automatically

**Usage**:
```
Enter your choice (1-8): 1
```

**Expected output**:
- Creates `data/collection_*` directories with raw data
- Creates `data/sentiment_*` directories with analysis results
- Launches web dashboard at `http://localhost:5000`

---

### Option 2: 🌐 Start Web Dashboard
**Best for**: Viewing existing data, monitoring sentiment

**What it does**:
- Launches the web dashboard interface
- If no data exists, runs a quick analysis first
- Displays Fear & Greed Index and historical trends

**Usage**:
```
Enter your choice (1-8): 2
```

**Access**: Open your browser to `http://localhost:5000`

**Features**:
- Real-time Fear & Greed Index gauge
- Historical sentiment charts
- Asset-specific sentiment breakdown
- System performance metrics
- Auto-refresh every 30 seconds

---

### Option 3: 🧪 Run System Tests
**Best for**: Developers, system validation

**What it does**:
- Starts web dashboard in background
- Runs comprehensive system tests
- Validates API endpoints, data structure, and performance
- Stops the dashboard after testing

**Usage**:
```
Enter your choice (1-8): 3
```

**Expected results**:
- ✅ API Endpoints: All endpoints responding
- ✅ Data Structure: Valid JSON with required fields
- ✅ Data Freshness: Recent timestamps
- ✅ Performance: Response times under 1000ms

---

### Option 4: ⚡ GoQuant Real-time Engine (Trading Mode)
**Best for**: Live trading, continuous monitoring

**What it does**:
- Runs the advanced GoQuant engine in real-time mode
- Processes live data continuously
- Generates trading signals
- Optimized for professional trading environments

**Usage**:
```
Enter your choice (1-8): 4
```

**Sub-options**:
1. **Run for 10 minutes**: Quick real-time session
2. **Run for 1 hour**: Standard trading session
3. **Run indefinitely**: Continuous operation until stopped

**Example**:
```
Select duration:
1. Run for 10 minutes
2. Run for 1 hour  
3. Run indefinitely (until stopped)
Enter choice (1-3): 2
```

---

### Option 5: 📊 GoQuant Batch Analysis (Comprehensive)
**Best for**: Detailed analysis, research, backtesting

**What it does**:
- Performs comprehensive batch analysis
- Generates detailed reports
- Analyzes large datasets
- Creates extensive visualizations

**Usage**:
```
Enter your choice (1-8): 5
```

**Data source options**:
1. **All sources**: Reddit + News + Market data
2. **Reddit only**: Social media sentiment focus
3. **News only**: News sentiment analysis
4. **Analyze existing data**: Process previously collected data

**Example**:
```
Select data source:
1. All sources (Reddit + News + Market)
2. Reddit only
3. News only
4. Analyze existing data
Enter choice (1-4): 1
```

---

### Option 6: 🎯 GoQuant Performance Test (Benchmarking)
**Best for**: System optimization, performance validation

**What it does**:
- Benchmarks system performance
- Tests against GoQuant requirements
- Measures processing speed and accuracy
- Generates performance reports

**Usage**:
```
Enter your choice (1-8): 6
```

**Test duration options**:
1. **Quick test (2 minutes)**: Basic performance check
2. **Standard test (5 minutes)**: Comprehensive benchmarking
3. **Extended test (10 minutes)**: Thorough performance analysis

**Example**:
```
Select test duration:
1. Quick test (2 minutes)
2. Standard test (5 minutes)
3. Extended test (10 minutes)
Enter choice (1-3): 2
```

---

### Option 7: 🔧 Complete Setup and Start Dashboard
**Best for**: Full system initialization, production setup

**What it does**:
- **Step 1/3**: Collects initial data from all sources
- **Step 2/3**: Runs system validation tests
- **Step 3/3**: Starts web dashboard for monitoring

**Usage**:
```
Enter your choice (1-8): 7
```

**Process**:
1. Data collection runs automatically
2. System tests validate functionality
3. Dashboard starts and remains running
4. Press `Ctrl+C` to stop

---

### Option 8: 🚀 GoQuant Full Pipeline (Professional Trading)
**Best for**: Production trading environments, complete automation

**What it does**:
- **Step 1/4**: Initial batch data collection
- **Step 2/4**: Starts web dashboard
- **Step 3/4**: Runs system validation
- **Step 4/4**: Starts real-time engine

**Usage**:
```
Enter your choice (1-8): 8
```

**Services running**:
- Web dashboard at `http://localhost:5000`
- Real-time sentiment engine
- Continuous data processing
- Live trading signal generation

**To stop**: Press `Ctrl+C` to stop both services

---

## 🎛️ Advanced Usage

### Running with Environment Variables
Set API keys as environment variables for enhanced functionality:

```bash
# Twitter API
export TWITTER_BEARER_TOKEN="your_token_here"
export TWITTER_API_KEY="your_key_here"
export TWITTER_API_SECRET="your_secret_here"

# Reddit API
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USER_AGENT="fear_greed_engine v0.1.0"

# News API
export NEWS_API_KEY="your_news_api_key"

# Run the script
./quick_start.sh
```

### Running Specific Components
You can also run individual components directly:

```bash
# Data collection only
python main.py --mode collect

# Sentiment analysis only
python main.py --mode analyze

# Signal generation only
python main.py --mode signal

# Web dashboard only
python web_app.py

# GoQuant engine directly
python goquant_main.py --mode=real-time
```

## 📊 Understanding the Output

### Data Directories Created
- `data/collection_*`: Raw data from APIs
- `data/sentiment_*`: Sentiment analysis results
- `data/signals/`: Trading signals
- `data/visualizations/`: Generated charts and graphs

### Key Files
- `fear_greed_index.json`: Current Fear & Greed Index
- `general_sentiment.json`: Overall sentiment metrics
- `entity_sentiment.json`: Asset-specific sentiment
- `market_data_*.csv`: Financial market data
- `news_*.json`: News articles and sentiment
- `reddit_*.json`: Reddit posts and analysis

### Fear & Greed Index Scale
- **0-25**: 😰 **Extreme Fear** - Potential buying opportunity
- **26-45**: 😟 **Fear** - Market uncertainty
- **46-55**: 😐 **Neutral** - Balanced sentiment
- **56-75**: 😊 **Greed** - Optimistic market
- **76-100**: 🤑 **Extreme Greed** - Potential selling opportunity

## 🔧 Troubleshooting

### Common Issues

#### "Permission denied" when running script
```bash
chmod +x quick_start.sh
./quick_start.sh
```

#### "Python not found"
Make sure Python 3.8+ is installed:
```bash
python3 --version
```

#### "Port 5000 already in use"
Stop other services using port 5000:
```bash
lsof -ti:5000 | xargs kill -9
```

#### "No sentiment data available"
Run data collection first:
```bash
python main.py --mode collect
```

#### Configuration errors
Check if config files exist:
```bash
ls -la config/
```

Create config from example:
```bash
cp config/config.json.example config/config.json
```

## 📈 Performance Expectations

### Typical Performance Metrics
- **Data Processing**: 200+ posts in ~4 seconds
- **API Response Time**: <100ms average
- **Memory Usage**: ~50MB peak
- **Dashboard Load Time**: <2 seconds
- **Fear & Greed Calculation**: <1ms

### Data Sources
- **Reddit**: r/Bitcoin, r/CryptoCurrency, r/wallstreetbets
- **News**: Financial news from major outlets
- **Market**: Real-time price and volume data
- **Update Frequency**: Every 30 minutes

## 🎯 Recommended Workflows

### For New Users
1. Start with **Option 1** (Basic Mode)
2. Explore the web dashboard
3. Try **Option 3** (System Tests)
4. Move to **Option 5** (Batch Analysis)

### For Traders
1. Use **Option 4** (Real-time Engine)
2. Monitor with **Option 2** (Web Dashboard)
3. Run **Option 6** (Performance Tests) regularly
4. Use **Option 8** (Full Pipeline) for production

### For Developers
1. Run **Option 3** (System Tests) first
2. Use **Option 5** (Batch Analysis) for development
3. Test with **Option 6** (Performance Tests)
4. Deploy with **Option 8** (Full Pipeline)

### For Researchers
1. Use **Option 5** (Batch Analysis) with different data sources
2. Analyze results in generated directories
3. Use **Option 7** (Complete Setup) for comprehensive data
4. Export data for further analysis

## 🆘 Support

If you encounter issues:

1. **Check the logs**: Look in the `logs/` directory
2. **Run tests**: Use Option 3 to validate your setup
3. **Check data**: Ensure data directories are created
4. **Review configuration**: Verify `config/config.json` is valid
5. **GitHub Issues**: Report bugs and request features

## 🎉 Next Steps

After successfully running the quick start:

1. **📊 Explore the Dashboard**: Visit `http://localhost:5000`
2. **📖 Read Documentation**: Check the `docs/` directory
3. **🔧 Customize Configuration**: Edit `config/config.json`
4. **🧪 Run Tests**: Validate your setup with Option 3
5. **📈 Analyze Results**: Review generated data and reports

Happy analyzing! 🚀📊
