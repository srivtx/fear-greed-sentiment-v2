import pandas as pd
import logging
import time
from datetime import datetime, timedelta
import yfinance as yf
import requests
import json
import os
from pathlib import Path
import random

from config.config import Config

logger = logging.getLogger(__name__)


class MarketDataCollector:
    """Collects market data for cryptocurrencies, stocks, and indices with improved reliability"""

    def __init__(self):
        self.config = Config()
        self.targets = self._get_targets()
        self.data_path = Path(self.config.get("data_storage.path", "data"))
        self.cache_dir = self.data_path / "market_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Define alternate symbol formats
        self.crypto_formats = {
            "BTC": ["BTC-USD", "BTCUSD=X", "BTC"],
            "ETH": ["ETH-USD", "ETHUSD=X", "ETH"],
            "XRP": ["XRP-USD", "XRPUSD=X", "XRP"],
            "ADA": ["ADA-USD", "ADAUSD=X", "ADA"],
            "SOL": ["SOL-USD", "SOLUSD=X", "SOL"],
            "DOGE": ["DOGE-USD", "DOGEUSD=X", "DOGE"],
            "BNB": ["BNB-USD", "BNBUSD=X", "BNB"]
        }

        # Define stock format by region
        self.stock_regions = ["", ".NE", ".L", ".DE"]

        # Use CoinGecko API as backup for crypto prices
        self.crypto_api_url = "https://api.coingecko.com/api/v3"

        # Add user-agent headers to avoid some blocking issues
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        ]

    def _get_targets(self):
        """Get financial targets to track"""
        # Check for cryptocurrencies in config
        cryptos = self.config.get("targets.cryptocurrencies")
        if not cryptos:
            # Try getting from 'coins' field
            coins = self.config.get("coins", ["bitcoin", "ethereum"])
            # Convert names to symbols if needed
            crypto_mapping = {
                "bitcoin": "BTC",
                "ethereum": "ETH",
                "ripple": "XRP",
                "cardano": "ADA",
                "solana": "SOL",
                "dogecoin": "DOGE",
                "binance": "BNB"
            }
            cryptos = [crypto_mapping.get(coin.lower(), coin.upper()) for coin in coins]

        # Get stocks and indices
        stocks = self.config.get("targets.stocks", ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"])
        indices = self.config.get("targets.indices", ["SPY", "QQQ", "DIA"])

        targets = {
            "cryptocurrencies": cryptos,
            "stocks": stocks,
            "indices": indices
        }

        return targets

    def collect_current_data(self):
        """
        Collect current market data for all targets with improved error handling

        Returns:
            dict: DataFrame of current market data by symbol
        """
        logger.info("Collecting current market data")

        market_data = {}

        # First try to collect crypto data via CoinGecko API
        crypto_data = self._collect_crypto_data_coingecko()
        if crypto_data:
            market_data.update(crypto_data)

        # Try Yahoo Finance for any missing cryptos
        for crypto in self.targets["cryptocurrencies"]:
            if crypto not in market_data and crypto + "-USD" not in market_data:
                self._collect_crypto_from_yahoo(crypto, market_data)

        # Collect stock data
        for stock in self.targets["stocks"]:
            self._collect_stock_from_yahoo(stock, market_data)

        # Collect index data
        for index in self.targets["indices"]:
            self._collect_index_from_yahoo(index, market_data)

        logger.info(f"Collected current market data for {len(market_data)} symbols")
        return market_data

    def _collect_crypto_data_coingecko(self):
        """
        Collect cryptocurrency data from CoinGecko API

        Returns:
            dict: Market data by symbol
        """
        crypto_data = {}

        try:
            # Convert crypto symbols to CoinGecko IDs
            symbol_to_id = {
                "BTC": "bitcoin",
                "ETH": "ethereum",
                "XRP": "ripple",
                "ADA": "cardano",
                "SOL": "solana",
                "DOGE": "dogecoin",
                "BNB": "binancecoin"
            }

            # Get IDs for our target cryptos
            coin_ids = [symbol_to_id.get(symbol, symbol.lower()) for symbol in self.targets["cryptocurrencies"]]
            coin_ids = [cid for cid in coin_ids if cid]  # Remove empty

            if not coin_ids:
                return {}

            # Build comma-separated list of IDs
            ids_param = ",".join(coin_ids)

            # Make API request with custom headers to reduce chance of blocking
            headers = {
                "User-Agent": random.choice(self.user_agents),
                "Accept": "application/json"
            }

            url = f"{self.crypto_api_url}/coins/markets"
            params = {
                "ids": ids_param,
                "vs_currency": "usd",
                "per_page": 100,
                "sparkline": "false"
            }

            response = requests.get(url, params=params, headers=headers)

            if response.status_code == 200:
                coin_data = response.json()

                for coin in coin_data:
                    # Convert to pandas DataFrame in format similar to Yahoo Finance
                    now = datetime.now()
                    data_dict = {
                        "Date": [now],
                        "Open": [coin["current_price"]],
                        "High": [coin["high_24h"] if "high_24h" in coin else coin["current_price"]],
                        "Low": [coin["low_24h"] if "low_24h" in coin else coin["current_price"]],
                        "Close": [coin["current_price"]],
                        "Volume": [coin["total_volume"] if "total_volume" in coin else 0],
                        "Symbol": [f"{coin['symbol'].upper()}-USD"],
                        "Type": ["crypto"],
                        "Datetime": [now],
                        "Price_Change_24h": [coin.get("price_change_24h", 0)],
                        "Price_Change_Percentage_24h": [coin.get("price_change_percentage_24h", 0)],
                        "Market_Cap": [coin.get("market_cap", 0)]
                    }

                    df = pd.DataFrame(data_dict)

                    # Get symbol back to uppercase
                    symbol = coin["symbol"].upper()

                    # Add to crypto data dictionary
                    crypto_data[f"{symbol}-USD"] = df

                    # Also cache the data
                    self._cache_market_data(f"{symbol}-USD", df)

                logger.info(f"Successfully collected data for {len(coin_data)} cryptocurrencies from CoinGecko")
            else:
                logger.warning(f"CoinGecko API returned status code {response.status_code}")

        except Exception as e:
            logger.error(f"Error collecting cryptocurrency data from CoinGecko: {e}")

        return crypto_data

    def _collect_crypto_from_yahoo(self, crypto, market_data):
        """Try to collect a specific crypto from Yahoo Finance with multiple format attempts"""

        # Try different formats for the symbol
        formats = self.crypto_formats.get(crypto, [f"{crypto}-USD"])

        for symbol_format in formats:
            try:
                # Configure yfinance with random user agent
                config = {'User-Agent': random.choice(self.user_agents)}
                yf.set_tz_cache_location(str(self.cache_dir))

                ticker = yf.Ticker(symbol_format, session=requests.Session())
                data = ticker.history(period="1d")

                if not data.empty:
                    # Format data
                    data = data.reset_index()
                    data["Symbol"] = symbol_format
                    data["Type"] = "crypto"
                    data["Datetime"] = data["Date"]  # Rename for consistency
                    market_data[symbol_format] = data
                    logger.info(f"Collected current data for {crypto} as {symbol_format}")

                    # Cache the data
                    self._cache_market_data(symbol_format, data)
                    return True

            except Exception as e:
                logger.debug(f"Failed to get {crypto} with format {symbol_format}: {e}")
                continue

        # If we got here, we couldn't get data in any format
        # Try to load from cache
        cached_data = self._load_from_cache(crypto + "-USD")
        if cached_data is not None:
            market_data[crypto + "-USD"] = cached_data
            logger.warning(f"Using cached data for {crypto}")
            return True

        logger.warning(f"No data found for {crypto} in any format")
        return False

    def _collect_stock_from_yahoo(self, stock, market_data):
        """Try to collect stock data with region suffixes if needed"""

        # Try with different region suffixes
        for region in self.stock_regions:
            symbol = f"{stock}{region}"

            try:
                # Configure yfinance with random user agent
                config = {'User-Agent': random.choice(self.user_agents)}
                yf.set_tz_cache_location(str(self.cache_dir))

                ticker = yf.Ticker(symbol, session=requests.Session())
                data = ticker.history(period="1d")

                if not data.empty:
                    # Format data
                    data = data.reset_index()
                    data["Symbol"] = stock  # Store the base symbol without region
                    data["Type"] = "stock"
                    data["Datetime"] = data["Date"]
                    market_data[stock] = data
                    logger.info(f"Collected current data for {stock} using {symbol}")

                    # Cache the data
                    self._cache_market_data(stock, data)
                    return True
            except Exception as e:
                logger.debug(f"Failed to get {symbol}: {e}")
                continue

        # If we got here, try to use cached data
        cached_data = self._load_from_cache(stock)
        if cached_data is not None:
            market_data[stock] = cached_data
            logger.warning(f"Using cached data for {stock}")
            return True

        # Generate mock data as last resort
        market_data[stock] = self._generate_mock_stock_data(stock)
        logger.warning(f"Using mock data for {stock}")
        return False

    def _collect_index_from_yahoo(self, index, market_data):
        """Collect index data with fallbacks"""

        # Try special format for indices (some need ^prefix)
        formats = [index, f"^{index}"]

        for symbol_format in formats:
            try:
                # Configure yfinance with random user agent
                config = {'User-Agent': random.choice(self.user_agents)}
                yf.set_tz_cache_location(str(self.cache_dir))

                ticker = yf.Ticker(symbol_format, session=requests.Session())
                data = ticker.history(period="1d")

                if not data.empty:
                    # Format data
                    data = data.reset_index()
                    data["Symbol"] = index  # Store original index symbol
                    data["Type"] = "index"
                    data["Datetime"] = data["Date"]
                    market_data[index] = data
                    logger.info(f"Collected current data for {index} using {symbol_format}")

                    # Cache the data
                    self._cache_market_data(index, data)
                    return True
            except Exception as e:
                logger.debug(f"Failed to get {symbol_format}: {e}")
                continue

        # Try to use cached data
        cached_data = self._load_from_cache(index)
        if cached_data is not None:
            market_data[index] = cached_data
            logger.warning(f"Using cached data for {index}")
            return True

        # Generate mock data as last resort
        market_data[index] = self._generate_mock_index_data(index)
        logger.warning(f"Using mock data for {index}")
        return False

    def _cache_market_data(self, symbol, data):
        """Cache market data to file"""
        try:
            cache_file = self.cache_dir / f"{symbol}_cache.csv"
            data.to_csv(cache_file, index=False)
        except Exception as e:
            logger.error(f"Error caching data for {symbol}: {e}")

    def _load_from_cache(self, symbol):
        """Load market data from cache"""
        cache_file = self.cache_dir / f"{symbol}_cache.csv"

        if cache_file.exists():
            try:
                data = pd.read_csv(cache_file)
                # Check if cache is reasonably recent (less than 24h old)
                cache_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache_file))

                if cache_age < timedelta(hours=24):
                    return data
                else:
                    logger.warning(f"Cache for {symbol} is too old ({cache_age.total_seconds() / 3600:.1f} hours)")
                    return None
            except Exception:
                return None
        return None

    def _generate_mock_stock_data(self, symbol):
        """Generate mock stock data when API fails"""
        now = datetime.now()
        mock_price = 100.0  # Default price

        # Use symbol first letter to generate different mock prices
        if symbol:
            # Generate a somewhat predictable price based on symbol
            ascii_sum = sum(ord(c) for c in symbol)
            mock_price = 50.0 + (ascii_sum % 950)

        data_dict = {
            "Date": [now],
            "Open": [mock_price * 0.99],
            "High": [mock_price * 1.02],
            "Low": [mock_price * 0.98],
            "Close": [mock_price],
            "Volume": [1000000],
            "Symbol": [symbol],
            "Type": ["stock"],
            "Datetime": [now],
            "IsMock": [True]  # Flag to indicate this is mock data
        }

        return pd.DataFrame(data_dict)

    def _generate_mock_index_data(self, symbol):
        """Generate mock index data when API fails"""
        now = datetime.now()

        # Indices typically have higher values
        mock_price = 1000.0

        # Use symbol to generate different mock prices
        if symbol:
            ascii_sum = sum(ord(c) for c in symbol)
            mock_price = 1000.0 + (ascii_sum % 3000)

        data_dict = {
            "Date": [now],
            "Open": [mock_price * 0.99],
            "High": [mock_price * 1.01],
            "Low": [mock_price * 0.98],
            "Close": [mock_price],
            "Volume": [10000000],
            "Symbol": [symbol],
            "Type": ["index"],
            "Datetime": [now],
            "IsMock": [True]  # Flag to indicate this is mock data
        }

        return pd.DataFrame(data_dict)

    def collect_historical_data(self, period="1y"):
        """
        Collect historical market data for all targets with improved error handling

        Args:
            period (str): Lookback period (e.g., '1d', '5d', '1mo', '3mo', '1y', '5y', 'max')

        Returns:
            dict: DataFrame of historical market data by symbol
        """
        logger.info(f"Collecting historical market data for period: {period}")

        historical_data = {}

        # Try to collect historical crypto data from CoinGecko first
        if period.endswith('d'):
            days = int(period[:-1])
        elif period.endswith('mo'):
            days = int(period[:-2]) * 30
        elif period.endswith('y'):
            days = int(period[:-1]) * 365
        else:
            days = 365  # Default to 1 year

        crypto_hist_data = self._collect_historical_crypto_coingecko(days)
        if crypto_hist_data:
            historical_data.update(crypto_hist_data)

        # Try Yahoo Finance for any missing cryptos
        for crypto in self.targets["cryptocurrencies"]:
            crypto_key = f"{crypto}-USD"
            if crypto not in historical_data and crypto_key not in historical_data:
                self._collect_historical_crypto_yahoo(crypto, period, historical_data)

        # Collect historical stock data with regional attempts
        for stock in self.targets["stocks"]:
            self._collect_historical_stock_yahoo(stock, period, historical_data)

        # Collect historical index data
        for index in self.targets["indices"]:
            self._collect_historical_index_yahoo(index, period, historical_data)

        logger.info(f"Collected historical market data for {len(historical_data)} symbols")
        return historical_data

    def _collect_historical_crypto_coingecko(self, days):
        """
        Collect historical cryptocurrency data from CoinGecko

        Args:
            days (int): Number of days to look back

        Returns:
            dict: Historical data by symbol
        """
        historical_data = {}

        try:
            # Convert crypto symbols to CoinGecko IDs
            symbol_to_id = {
                "BTC": "bitcoin",
                "ETH": "ethereum",
                "XRP": "ripple",
                "ADA": "cardano",
                "SOL": "solana",
                "DOGE": "dogecoin",
                "BNB": "binancecoin"
            }

            # Max days for one request in CoinGecko API
            max_days = 90

            # Limit days to reasonable range
            days = min(days, 365)  # Max 1 year

            # Process each cryptocurrency
            for crypto in self.targets["cryptocurrencies"]:
                coin_id = symbol_to_id.get(crypto, crypto.lower())

                # Make API request
                url = f"{self.crypto_api_url}/coins/{coin_id}/market_chart"
                params = {
                    "vs_currency": "usd",
                    "days": min(days, max_days),
                    "interval": "daily"
                }

                # Use custom headers
                headers = {
                    "User-Agent": random.choice(self.user_agents),
                    "Accept": "application/json"
                }

                try:
                    response = requests.get(url, params=params, headers=headers)

                    if response.status_code == 200:
                        coin_data = response.json()

                        # Process prices, volumes
                        prices = coin_data.get("prices", [])
                        volumes = coin_data.get("total_volumes", [])

                        # Create DataFrame
                        records = []

                        for i, (timestamp, price) in enumerate(prices):
                            dt = datetime.fromtimestamp(timestamp / 1000)
                            volume = volumes[i][1] if i < len(volumes) else 0

                            record = {
                                "Date": dt.date(),
                                "Datetime": dt,
                                "Close": price,
                                "Volume": volume,
                                # Estimate other values since we only get close price
                                "Open": price,
                                "High": price,
                                "Low": price
                            }
                            records.append(record)

                        if records:
                            df = pd.DataFrame(records)
                            df["Symbol"] = f"{crypto}-USD"
                            df["Type"] = "crypto"
                            historical_data[f"{crypto}-USD"] = df
                            logger.debug(f"Collected historical data for {crypto} from CoinGecko: {len(df)} rows")

                    else:
                        logger.warning(f"CoinGecko API returned status code {response.status_code} for {coin_id}")

                except Exception as e:
                    logger.error(f"Error collecting historical data for {crypto} from CoinGecko: {e}")

                # Sleep to avoid rate limiting
                time.sleep(1.5)  # CoinGecko free tier has strict rate limits

        except Exception as e:
            logger.error(f"Error in historical crypto data collection from CoinGecko: {e}")

        return historical_data

    def _collect_historical_crypto_yahoo(self, crypto, period, historical_data):
        """Try to collect historical data for a specific crypto from Yahoo Finance"""

        # Try different formats for the symbol
        formats = self.crypto_formats.get(crypto, [f"{crypto}-USD"])

        for symbol_format in formats:
            try:
                # Configure yfinance with random user agent
                config = {'User-Agent': random.choice(self.user_agents)}
                yf.set_tz_cache_location(str(self.cache_dir))

                ticker = yf.Ticker(symbol_format, session=requests.Session())
                data = ticker.history(period=period)

                if not data.empty:
                    # Format data
                    data = data.reset_index()
                    data["Symbol"] = symbol_format
                    data["Type"] = "crypto"
                    data["Date"] = data["Date"].dt.date  # Convert to date only
                    historical_data[symbol_format] = data
                    logger.debug(f"Collected historical data for {crypto} as {symbol_format}: {len(data)} rows")
                    return True

            except Exception as e:
                logger.debug(f"Failed to get historical data for {crypto} with format {symbol_format}: {e}")
                continue

        logger.warning(f"No historical data found for {crypto} in any format")
        return False

    def _collect_historical_stock_yahoo(self, stock, period, historical_data):
        """Collect historical stock data with region attempts"""

        # Try with different region suffixes
        for region in self.stock_regions:
            symbol = f"{stock}{region}"

            try:
                # Configure yfinance with random user agent
                config = {'User-Agent': random.choice(self.user_agents)}
                yf.set_tz_cache_location(str(self.cache_dir))

                ticker = yf.Ticker(symbol, session=requests.Session())
                data = ticker.history(period=period)

                if not data.empty:
                    # Format data
                    data = data.reset_index()
                    data["Symbol"] = stock  # Store the base symbol without region
                    data["Type"] = "stock"
                    data["Date"] = data["Date"].dt.date
                    historical_data[stock] = data
                    logger.info(f"Collected historical data for {stock} using {symbol}: {len(data)} rows")
                    return True
            except Exception as e:
                logger.debug(f"Failed to get historical data for {symbol}: {e}")
                continue

        logger.warning(f"No historical data found for {stock}")

        # Generate mock historical data
        historical_data[stock] = self._generate_mock_historical_stock_data(stock, period)
        logger.warning(f"Using mock historical data for {stock}")
        return False

    def _collect_historical_index_yahoo(self, index, period, historical_data):
        """Collect historical index data with fallbacks"""

        # Try special format for indices (some need ^prefix)
        formats = [index, f"^{index}"]

        for symbol_format in formats:
            try:
                # Configure yfinance with random user agent
                config = {'User-Agent': random.choice(self.user_agents)}
                yf.set_tz_cache_location(str(self.cache_dir))

                ticker = yf.Ticker(symbol_format, session=requests.Session())
                data = ticker.history(period=period)

                if not data.empty:
                    # Format data
                    data = data.reset_index()
                    data["Symbol"] = index  # Store original index symbol
                    data["Type"] = "index"
                    data["Date"] = data["Date"].dt.date
                    historical_data[index] = data
                    logger.info(f"Collected historical data for {index} using {symbol_format}: {len(data)} rows")
                    return True
            except Exception as e:
                logger.debug(f"Failed to get historical data for {symbol_format}: {e}")
                continue

        logger.warning(f"No historical data found for {index}")

        # Generate mock historical data
        historical_data[index] = self._generate_mock_historical_index_data(index, period)
        logger.warning(f"Using mock historical data for {index}")
        return False

    def _generate_mock_historical_stock_data(self, symbol, period):
        """Generate mock historical stock data"""
        # Create realistic looking mock data
        now = datetime.now().date()

        # Determine how many days of data to generate
        if period.endswith('d'):
            days = int(period[:-1])
        elif period.endswith('mo'):
            days = int(period[:-2]) * 30
        elif period.endswith('y'):
            days = int(period[:-1]) * 252  # Trading days in a year
        else:
            days = 252  # Default to 1 year

        # Use symbol to generate base price
        ascii_sum = sum(ord(c) for c in symbol)
        base_price = 50.0 + (ascii_sum % 950)

        # Generate data with realistic patterns
        records = []
        current_price = base_price

        for i in range(days):
            date = now - timedelta(days=i)

            # Skip weekends in mock data
            if date.weekday() >= 5:  # 5=Saturday, 6=Sunday
                continue

            # Add some randomness but with trend
            daily_change = (random.random() - 0.5) * 0.03 * current_price  # -1.5% to +1.5%

            # Add a slight long-term trend
            trend_factor = 1.0 + (random.random() - 0.45) * 0.001  # Slight upward bias

            open_price = current_price
            close_price = current_price + daily_change
            current_price = close_price * trend_factor

            # Ensure reasonable high/low values
            high_price = max(open_price, close_price) * (1 + random.random() * 0.01)  # Up to 1% higher
            low_price = min(open_price, close_price) * (1 - random.random() * 0.01)  # Up to 1% lower

            # Randomize volume
            volume = int(random.uniform(500000, 5000000))

            record = {
                "Date": date,
                "Open": open_price,
                "High": high_price,
                "Low": low_price,
                "Close": close_price,
                "Volume": volume,
                "Datetime": date,
                "Symbol": symbol,
                "Type": "stock",
                "IsMock": True
            }
            records.append(record)

        # Sort by date ascending
        df = pd.DataFrame(records).sort_values("Date")
        return df

    def _generate_mock_historical_index_data(self, symbol, period):
        """Generate mock historical index data"""
        # Similar to stock data but with higher base prices for indices
        now = datetime.now().date()

        # Determine how many days of data to generate
        if period.endswith('d'):
            days = int(period[:-1])
        elif period.endswith('mo'):
            days = int(period[:-2]) * 30
        elif period.endswith('y'):
            days = int(period[:-1]) * 252  # Trading days in a year
        else:
            days = 252  # Default to 1 year

        # Use symbol to generate base price
        ascii_sum = sum(ord(c) for c in symbol)
        base_price = 1000.0 + (ascii_sum % 3000)

        # Generate data with realistic patterns
        records = []
        current_price = base_price

        for i in range(days):
            date = now - timedelta(days=i)

            # Skip weekends in mock data
            if date.weekday() >= 5:  # 5=Saturday, 6=Sunday
                continue

            # Add some randomness but with trend
            daily_change = (random.random() - 0.5) * 0.02 * current_price  # -1% to +1%

            # Add a slight long-term trend
            trend_factor = 1.0 + (random.random() - 0.45) * 0.0008  # Slight upward bias

            open_price = current_price
            close_price = current_price + daily_change
            current_price = close_price * trend_factor

            # Ensure reasonable high/low values
            high_price = max(open_price, close_price) * (1 + random.random() * 0.01)
            low_price = min(open_price, close_price) * (1 - random.random() * 0.01)

            # Randomize volume
            volume = int(random.uniform(5000000, 50000000))

            record = {
                "Date": date,
                "Open": open_price,
                "High": high_price,
                "Low": low_price,
                "Close": close_price,
                "Volume": volume,
                "Datetime": date,
                "Symbol": symbol,
                "Type": "index",
                "IsMock": True
            }
            records.append(record)

        # Sort by date ascending
        df = pd.DataFrame(records).sort_values("Date")
        return df