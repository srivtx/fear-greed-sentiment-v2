# Adding the simulate_sentiment_data method to Backtester class

def simulate_sentiment_data(self, historical_data, volatility_factor=0.8, lag_days=1):
    """
    Simulate sentiment data for backtesting based on price movements

    Args:
        historical_data (dict): Dictionary of historical price DataFrames
        volatility_factor (float): How much volatility affects sentiment
        lag_days (int): Lag between price movement and sentiment response

    Returns:
        dict: Simulated sentiment data for each asset and date
    """
    logger.info("Simulating historical sentiment data for backtesting")

    sentiment_data = {}

    for symbol, df in historical_data.items():
        sentiment_data[symbol] = {}

        # Calculate returns
        df['Return'] = df['Close'].pct_change()

        # Calculate volatility (20-day rolling standard deviation)
        df['Volatility'] = df['Return'].rolling(window=20).std()

        # Fill NaN values
        df['Return'] = df['Return'].fillna(0)
        df['Volatility'] = df['Volatility'].fillna(df['Volatility'].mean())

        # Generate simulated sentiment with noise
        for i in range(lag_days, len(df)):
            # Base sentiment on lagged returns
            lagged_return = df['Return'].iloc[i - lag_days]

            # Adjust by volatility
            volatility = df['Volatility'].iloc[i]

            # Add random noise
            noise = np.random.normal(0, 0.2)

            # Calculate sentiment score (-1 to 1 range)
            sentiment_score = np.tanh(lagged_return * 10 * volatility_factor + noise)

            # Determine sentiment label
            if sentiment_score > 0.2:
                sentiment_label = "positive"
            elif sentiment_score < -0.2:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"

            # Add to sentiment data
            date = df['Date'].iloc[i].strftime("%Y-%m-%d")
            sentiment_data[symbol][date] = {
                "sentiment_score": sentiment_score,
                "sentiment_label": sentiment_label,
                "mention_count": np.random.randint(5, 50)
            }

    logger.info(f"Generated simulated sentiment data for {len(sentiment_data)} symbols")
    return sentiment_data


# Adding the generate_historical_signals method to Backtester class

def generate_historical_signals(self, historical_data, sentiment_data):
    """
    Generate trading signals for historical data

    Args:
        historical_data (dict): Dictionary of historical price DataFrames
        sentiment_data (dict): Simulated sentiment data

    Returns:
        dict: Generated historical signals
    """
    logger.info("Generating historical trading signals")

    signals = {}
    dates = set()

    # Collect all unique dates
    for symbol, df in historical_data.items():
        for date in df['Date']:
            dates.add(date.strftime("%Y-%m-%d"))

    dates = sorted(list(dates))

    # Generate signals for each date
    for date in dates:
        date_signals = {
            "timestamp": date,
            "entity_signals": {
                "cryptos": {}
            }
        }

        # Generate entity-specific signals
        for symbol, data in sentiment_data.items():
            if date in data:
                sentiment = data[date]

                # Skip entities with weak sentiment or low mention count
                if (abs(sentiment["sentiment_score"]) < self.signal_generator.signal_config["sentiment_threshold"] or
                        sentiment["mention_count"] < self.signal_generator.signal_config["minimum_mentions"]):
                    continue

                # Determine signal direction
                signal_type = "BUY" if sentiment["sentiment_score"] > 0 else "SELL"

                # Calculate confidence and position size
                confidence = abs(sentiment["sentiment_score"])
                position_size = self.signal_generator.signal_config["position_size_factor"] * confidence

                # Generate signal
                date_signals["entity_signals"]["cryptos"][symbol] = {
                    "signal_type": signal_type,
                    "confidence": confidence,
                    "strength": abs(sentiment["sentiment_score"]),
                    "sentiment_score": sentiment["sentiment_score"],
                    "mention_count": sentiment["mention_count"],
                    "position_size": position_size,
                    "timestamp": date,
                    "expiry": (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
                }

        if date_signals["entity_signals"]["cryptos"]:
            signals[date] = date_signals

    logger.info(f"Generated signals for {len(signals)} trading days")
    return signals


# Adding the calculate_backtest_results method to Backtester class

def calculate_backtest_results(self, portfolio, params):
    """
    Calculate performance metrics from backtest

    Args:
        portfolio (dict): Portfolio data from backtest
        params (dict): Backtest parameters

    Returns:
        dict: Performance metrics
    """
    if not portfolio["history"]:
        return {"error": "No portfolio history found"}

    # Create a DataFrame from portfolio history
    history_df = pd.DataFrame(portfolio["history"])
    history_df["date"] = pd.to_datetime(history_df["date"])
    history_df = history_df.set_index("date")

    # Calculate daily returns
    history_df["daily_return"] = history_df["portfolio_value"].pct_change()

    # Calculate performance metrics
    initial_value = params["initial_capital"]
    final_value = history_df["portfolio_value"].iloc[-1]

    total_return = final_value / initial_value - 1
    total_return_pct = total_return * 100

    # Annualized return
    days = (history_df.index[-1] - history_df.index[0]).days
    years = days / 365
    annualized_return = (1 + total_return) ** (1 / max(years, 0.01)) - 1
    annualized_return_pct = annualized_return * 100

    # Risk metrics
    daily_std = history_df["daily_return"].std()
    annualized_std = daily_std * np.sqrt(252)  # Assuming 252 trading days per year

    # Sharpe ratio (assuming risk-free rate of 0)
    sharpe_ratio = annualized_return / annualized_std if annualized_std > 0 else 0

    # Maximum drawdown
    history_df["cum_return"] = (1 + history_df["daily_return"].fillna(0)).cumprod()
    history_df["cum_roll_max"] = history_df["cum_return"].cummax()
    history_df["drawdown"] = history_df["cum_roll_max"] - history_df["cum_return"]
    history_df["drawdown_pct"] = history_df["drawdown"] / history_df["cum_roll_max"]
    max_drawdown = history_df["drawdown_pct"].max()

    # Trade statistics
    trades_df = pd.DataFrame(portfolio["trades"])
    if not trades_df.empty:
        win_trades = trades_df[trades_df["pnl"] > 0] if "pnl" in trades_df.columns else pd.DataFrame()
        loss_trades = trades_df[trades_df["pnl"] <= 0] if "pnl" in trades_df.columns else pd.DataFrame()

        win_rate = len(win_trades) / len(trades_df) if len(trades_df) > 0 else 0

        avg_profit = win_trades["pnl"].mean() if not win_trades.empty else 0
        avg_loss = loss_trades["pnl"].mean() if not loss_trades.empty else 0

        profit_factor = abs(win_trades["pnl"].sum() / loss_trades["pnl"].sum()) if not loss_trades.empty and \
                                                                                   loss_trades[
                                                                                       "pnl"].sum() != 0 else float(
            'inf')

        avg_hold_days = trades_df["holding_days"].mean() if "holding_days" in trades_df.columns else 0
    else:
        win_rate = 0
        avg_profit = 0
        avg_loss = 0
        profit_factor = 0
        avg_hold_days = 0

    results = {
        "initial_portfolio_value": initial_value,
        "final_portfolio_value": final_value,
        "total_return": total_return,
        "total_return_pct": total_return_pct,
        "annualized_return": annualized_return,
        "annualized_return_pct": annualized_return_pct,
        "annualized_volatility": annualized_std,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "max_drawdown_pct": max_drawdown * 100,
        "num_trades": len(portfolio["trades"]),
        "win_rate": win_rate,
        "avg_profit": avg_profit,
        "avg_loss": avg_loss,
        "profit_factor": profit_factor,
        "avg_hold_days": avg_hold_days,
        "portfolio_history": history_df
    }

    return results