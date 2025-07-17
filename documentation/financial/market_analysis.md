# Financial Market Analysis Documentation

## What This Document Explains

This guide shows you how to **turn sentiment into profitable trading strategies**. While the technical docs explain *how* the system works, this document explains *how to make money with it*.

### The Core Financial Insight

**Markets are driven by two primary emotions: Fear and Greed**

- **Fear** = Selling pressure, oversold conditions, buying opportunities
- **Greed** = Buying pressure, overbought conditions, selling opportunities
- **Neutral** = Sideways markets, trend continuation, wait-and-see

### Real Trading Applications

1. **Contrarian Trading**: When fear is extreme, smart money buys
2. **Momentum Trading**: When greed builds gradually, ride the trend
3. **Risk Management**: High fear = reduce position sizes
4. **Market Timing**: Sentiment extremes often mark reversals

### What You'll Learn Here

- How to correlate sentiment with actual price movements
- How to build trading strategies using sentiment signals  
- How to manage risk based on market emotions
- How to optimize portfolios with sentiment data
- Real backtesting results and performance metrics

## Overview

This documentation provides comprehensive financial analysis capabilities of the Fear & Greed Sentiment Engine, covering market correlation studies, risk assessment models, trading strategy development, and portfolio optimization techniques based on sentiment data.

## Market Correlation Analysis

### Sentiment-Price Correlation Studies

#### 1. Correlation Methodology

The system analyzes correlations between sentiment scores and price movements across different timeframes and market conditions.

```python
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

class SentimentPriceCorrelation:
    def __init__(self):
        self.correlation_data = {}
        self.significance_threshold = 0.05
        
    def calculate_correlation_matrix(self, sentiment_data, price_data, timeframes=['1h', '4h', '1d', '1w']):
        """Calculate correlation between sentiment and price across timeframes"""
        
        correlations = {}
        
        for timeframe in timeframes:
            # Resample data to timeframe
            sentiment_resampled = self.resample_sentiment_data(sentiment_data, timeframe)
            price_resampled = self.resample_price_data(price_data, timeframe)
            
            # Align timestamps
            aligned_data = self.align_timestamps(sentiment_resampled, price_resampled)
            
            if len(aligned_data) > 30:  # Minimum data points for meaningful correlation
                correlation_results = self.compute_correlations(aligned_data, timeframe)
                correlations[timeframe] = correlation_results
        
        return correlations
    
    def compute_correlations(self, aligned_data, timeframe):
        """Compute various correlation metrics"""
        
        sentiment_scores = aligned_data['sentiment_score']
        price_changes = aligned_data['price_change_pct']
        
        # Pearson correlation
        pearson_corr, pearson_p = stats.pearsonr(sentiment_scores, price_changes)
        
        # Spearman correlation (rank-based)
        spearman_corr, spearman_p = stats.spearmanr(sentiment_scores, price_changes)
        
        # Kendall Tau correlation
        kendall_corr, kendall_p = stats.kendalltau(sentiment_scores, price_changes)
        
        # Lead-lag analysis
        lead_lag_results = self.analyze_lead_lag(sentiment_scores, price_changes)
        
        return {
            'timeframe': timeframe,
            'data_points': len(aligned_data),
            'pearson': {
                'correlation': pearson_corr,
                'p_value': pearson_p,
                'significant': pearson_p < self.significance_threshold
            },
            'spearman': {
                'correlation': spearman_corr,
                'p_value': spearman_p,
                'significant': spearman_p < self.significance_threshold
            },
            'kendall': {
                'correlation': kendall_corr,
                'p_value': kendall_p,
                'significant': kendall_p < self.significance_threshold
            },
            'lead_lag': lead_lag_results
        }
    
    def analyze_lead_lag(self, sentiment, prices, max_lag=24):
        """Analyze if sentiment leads or lags price movements"""
        
        correlations = []
        lags = range(-max_lag, max_lag + 1)
        
        for lag in lags:
            if lag < 0:
                # Sentiment leads price (negative lag)
                sent_data = sentiment[:lag] if lag != 0 else sentiment
                price_data = prices[-lag:]
            elif lag > 0:
                # Price leads sentiment (positive lag)
                sent_data = sentiment[lag:]
                price_data = prices[:-lag] if lag != 0 else prices
            else:
                # No lag
                sent_data = sentiment
                price_data = prices
            
            if len(sent_data) > 10 and len(price_data) > 10:
                min_len = min(len(sent_data), len(price_data))
                corr, p_val = stats.pearsonr(sent_data[:min_len], price_data[:min_len])
                correlations.append((lag, corr, p_val))
        
        # Find optimal lag
        correlations.sort(key=lambda x: abs(x[1]), reverse=True)
        best_lag, best_corr, best_p = correlations[0]
        
        return {
            'optimal_lag': best_lag,
            'max_correlation': best_corr,
            'p_value': best_p,
            'interpretation': self.interpret_lag(best_lag),
            'all_correlations': correlations[:10]  # Top 10
        }
    
    def interpret_lag(self, lag):
        """Interpret lag results"""
        if lag < 0:
            return f"Sentiment leads price by {abs(lag)} periods"
        elif lag > 0:
            return f"Price leads sentiment by {lag} periods"
        else:
            return "Sentiment and price move simultaneously"

# Example usage and results
correlation_analyzer = SentimentPriceCorrelation()

# Sample results for major assets
correlation_results = {
    'AAPL': {
        '1h': {'pearson': 0.23, 'p_value': 0.001, 'optimal_lag': -2},
        '4h': {'pearson': 0.34, 'p_value': 0.0001, 'optimal_lag': -1},
        '1d': {'pearson': 0.45, 'p_value': 0.00001, 'optimal_lag': 0},
        '1w': {'pearson': 0.52, 'p_value': 0.000001, 'optimal_lag': 0}
    },
    'BTC': {
        '1h': {'pearson': 0.18, 'p_value': 0.01, 'optimal_lag': -3},
        '4h': {'pearson': 0.31, 'p_value': 0.001, 'optimal_lag': -2},
        '1d': {'pearson': 0.41, 'p_value': 0.0001, 'optimal_lag': -1},
        '1w': {'pearson': 0.48, 'p_value': 0.00001, 'optimal_lag': 0}
    }
}
```

#### 2. Sector Correlation Analysis

```python
class SectorCorrelationAnalysis:
    def __init__(self):
        self.sectors = {
            'Technology': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META'],
            'Finance': ['JPM', 'BAC', 'WFC', 'GS', 'MS'],
            'Healthcare': ['JNJ', 'PFE', 'UNH', 'ABBV', 'MRK'],
            'Energy': ['XOM', 'CVX', 'COP', 'EOG', 'SLB'],
            'Consumer': ['TSLA', 'NKE', 'SBUX', 'MCD', 'DIS']
        }
    
    def analyze_sector_sentiment_correlation(self, sentiment_data, price_data):
        """Analyze how sentiment correlates within and across sectors"""
        
        sector_results = {}
        
        for sector_name, symbols in self.sectors.items():
            sector_sentiment = self.aggregate_sector_sentiment(sentiment_data, symbols)
            sector_prices = self.aggregate_sector_prices(price_data, symbols)
            
            # Within-sector correlation
            within_sector_corr = self.calculate_within_sector_correlation(
                sentiment_data, price_data, symbols
            )
            
            # Cross-sector correlation
            cross_sector_corr = self.calculate_cross_sector_correlation(
                sector_sentiment, sentiment_data, symbols
            )
            
            sector_results[sector_name] = {
                'within_sector_correlation': within_sector_corr,
                'cross_sector_correlation': cross_sector_corr,
                'sector_sentiment_trend': self.analyze_sector_trend(sector_sentiment),
                'leading_indicators': self.identify_leading_stocks(sentiment_data, symbols)
            }
        
        return sector_results
    
    def identify_leading_stocks(self, sentiment_data, symbols):
        """Identify stocks that lead sector sentiment"""
        
        correlations = []
        
        for symbol in symbols:
            symbol_sentiment = sentiment_data[sentiment_data['symbol'] == symbol]
            
            # Calculate correlation with other stocks in sector
            for other_symbol in symbols:
                if symbol != other_symbol:
                    other_sentiment = sentiment_data[sentiment_data['symbol'] == other_symbol]
                    
                    # Lead-lag analysis
                    lead_lag = self.calculate_lead_lag_correlation(
                        symbol_sentiment, other_sentiment
                    )
                    
                    correlations.append({
                        'leader': symbol,
                        'follower': other_symbol,
                        'correlation': lead_lag['correlation'],
                        'lag': lead_lag['optimal_lag']
                    })
        
        # Identify stocks that consistently lead others
        leading_scores = {}
        for corr in correlations:
            if corr['lag'] < 0:  # Negative lag means leader
                leader = corr['leader']
                if leader not in leading_scores:
                    leading_scores[leader] = []
                leading_scores[leader].append(abs(corr['correlation']))
        
        # Calculate average leading score
        leader_rankings = {
            symbol: np.mean(scores) 
            for symbol, scores in leading_scores.items()
        }
        
        return sorted(leader_rankings.items(), key=lambda x: x[1], reverse=True)
```

### Market Regime Analysis

```python
class MarketRegimeAnalysis:
    def __init__(self):
        self.regimes = ['bull_market', 'bear_market', 'sideways', 'high_volatility']
        
    def identify_market_regime(self, price_data, volatility_data, sentiment_data):
        """Identify current market regime using multiple indicators"""
        
        # Price trend analysis
        price_trend = self.calculate_price_trend(price_data)
        
        # Volatility analysis
        volatility_regime = self.analyze_volatility_regime(volatility_data)
        
        # Sentiment regime
        sentiment_regime = self.analyze_sentiment_regime(sentiment_data)
        
        # Combine indicators
        regime_scores = self.combine_regime_indicators(
            price_trend, volatility_regime, sentiment_regime
        )
        
        return {
            'current_regime': max(regime_scores.items(), key=lambda x: x[1]),
            'regime_probabilities': regime_scores,
            'regime_characteristics': self.get_regime_characteristics(regime_scores),
            'trading_implications': self.get_trading_implications(regime_scores)
        }
    
    def analyze_sentiment_in_regime(self, sentiment_data, price_data, regime_periods):
        """Analyze how sentiment behaves in different market regimes"""
        
        regime_analysis = {}
        
        for regime, periods in regime_periods.items():
            regime_sentiment = []
            regime_returns = []
            
            for start_date, end_date in periods:
                period_sentiment = sentiment_data[
                    (sentiment_data['timestamp'] >= start_date) & 
                    (sentiment_data['timestamp'] <= end_date)
                ]
                period_returns = price_data[
                    (price_data['timestamp'] >= start_date) & 
                    (price_data['timestamp'] <= end_date)
                ]
                
                if len(period_sentiment) > 0 and len(period_returns) > 0:
                    regime_sentiment.extend(period_sentiment['sentiment_score'].tolist())
                    regime_returns.extend(period_returns['returns'].tolist())
            
            if len(regime_sentiment) > 30:  # Minimum samples
                regime_analysis[regime] = {
                    'avg_sentiment': np.mean(regime_sentiment),
                    'sentiment_volatility': np.std(regime_sentiment),
                    'sentiment_skewness': stats.skew(regime_sentiment),
                    'sentiment_kurtosis': stats.kurtosis(regime_sentiment),
                    'sentiment_return_correlation': np.corrcoef(
                        regime_sentiment, regime_returns[:len(regime_sentiment)]
                    )[0,1],
                    'extreme_sentiment_frequency': self.calculate_extreme_frequency(regime_sentiment)
                }
        
        return regime_analysis
```

## Risk Assessment Models

### Sentiment-Based Risk Metrics

```python
class SentimentRiskModel:
    def __init__(self):
        self.risk_factors = [
            'sentiment_volatility',
            'sentiment_momentum',
            'sentiment_divergence',
            'sentiment_extremes',
            'sentiment_correlation'
        ]
    
    def calculate_sentiment_var(self, sentiment_data, price_data, confidence_level=0.05):
        """Calculate Value at Risk incorporating sentiment factors"""
        
        # Historical simulation with sentiment adjustment
        returns = price_data['returns'].values
        sentiment_scores = sentiment_data['sentiment_score'].values
        
        # Align data
        min_len = min(len(returns), len(sentiment_scores))
        returns = returns[:min_len]
        sentiment_scores = sentiment_scores[:min_len]
        
        # Calculate sentiment-adjusted returns
        sentiment_factor = self.calculate_sentiment_factor(sentiment_scores)
        adjusted_returns = returns * sentiment_factor
        
        # Calculate VaR
        var_historical = np.percentile(adjusted_returns, confidence_level * 100)
        
        # Monte Carlo simulation with sentiment
        mc_returns = self.monte_carlo_simulation_with_sentiment(
            returns, sentiment_scores, num_simulations=10000
        )
        var_monte_carlo = np.percentile(mc_returns, confidence_level * 100)
        
        # Parametric VaR with sentiment adjustment
        mean_return = np.mean(adjusted_returns)
        std_return = np.std(adjusted_returns)
        var_parametric = mean_return + stats.norm.ppf(confidence_level) * std_return
        
        return {
            'historical_var': var_historical,
            'monte_carlo_var': var_monte_carlo,
            'parametric_var': var_parametric,
            'sentiment_adjustment_factor': np.mean(sentiment_factor),
            'confidence_level': confidence_level
        }
    
    def calculate_sentiment_factor(self, sentiment_scores):
        """Calculate sentiment adjustment factor for returns"""
        
        # Normalize sentiment scores
        normalized_sentiment = (sentiment_scores - np.mean(sentiment_scores)) / np.std(sentiment_scores)
        
        # Apply non-linear transformation
        # Extreme sentiment leads to higher volatility
        sentiment_factor = 1 + 0.1 * np.abs(normalized_sentiment) + 0.05 * normalized_sentiment**2
        
        return sentiment_factor
    
    def calculate_drawdown_risk(self, sentiment_data, price_data):
        """Calculate maximum drawdown risk incorporating sentiment"""
        
        prices = price_data['price'].values
        sentiment = sentiment_data['sentiment_score'].values
        
        # Calculate rolling maximum
        rolling_max = pd.Series(prices).expanding().max()
        drawdowns = (prices - rolling_max) / rolling_max
        
        # Sentiment-based drawdown prediction
        sentiment_risk_periods = self.identify_sentiment_risk_periods(sentiment)
        
        drawdown_analysis = {
            'max_drawdown': np.min(drawdowns),
            'current_drawdown': drawdowns[-1],
            'avg_drawdown': np.mean(drawdowns[drawdowns < 0]),
            'drawdown_duration': self.calculate_drawdown_duration(drawdowns),
            'sentiment_risk_score': self.calculate_sentiment_drawdown_risk(
                sentiment, drawdowns
            ),
            'predicted_drawdown_periods': sentiment_risk_periods
        }
        
        return drawdown_analysis
    
    def stress_test_sentiment_scenarios(self, portfolio_data, sentiment_scenarios):
        """Stress test portfolio under different sentiment scenarios"""
        
        stress_results = {}
        
        for scenario_name, scenario_params in sentiment_scenarios.items():
            # Generate scenario sentiment data
            scenario_sentiment = self.generate_scenario_sentiment(scenario_params)
            
            # Calculate portfolio impact
            portfolio_impact = self.calculate_portfolio_impact(
                portfolio_data, scenario_sentiment
            )
            
            stress_results[scenario_name] = {
                'portfolio_return': portfolio_impact['total_return'],
                'portfolio_volatility': portfolio_impact['volatility'],
                'max_loss': portfolio_impact['max_loss'],
                'recovery_time': portfolio_impact['recovery_time'],
                'sector_impacts': portfolio_impact['sector_breakdown']
            }
        
        return stress_results

# Predefined stress test scenarios
sentiment_stress_scenarios = {
    'extreme_pessimism': {
        'sentiment_level': -0.8,
        'duration_days': 30,
        'volatility': 0.3,
        'persistence': 0.7
    },
    'extreme_optimism': {
        'sentiment_level': 0.8,
        'duration_days': 60,
        'volatility': 0.2,
        'persistence': 0.6
    },
    'sentiment_whipsaw': {
        'sentiment_level': 0.0,
        'duration_days': 90,
        'volatility': 0.5,
        'persistence': 0.1
    },
    'gradual_deterioration': {
        'sentiment_level': -0.6,
        'duration_days': 180,
        'volatility': 0.15,
        'persistence': 0.9
    }
}
```

### Portfolio Risk Attribution

```python
class SentimentRiskAttribution:
    def __init__(self):
        self.risk_components = [
            'market_sentiment_risk',
            'idiosyncratic_sentiment_risk',
            'sector_sentiment_risk',
            'momentum_sentiment_risk'
        ]
    
    def decompose_portfolio_risk(self, portfolio_holdings, sentiment_data, price_data):
        """Decompose portfolio risk into sentiment-based components"""
        
        portfolio_risk = {}
        total_portfolio_var = self.calculate_portfolio_var(portfolio_holdings, price_data)
        
        # Market sentiment risk
        market_sentiment_var = self.calculate_market_sentiment_risk(
            portfolio_holdings, sentiment_data
        )
        
        # Idiosyncratic sentiment risk
        idiosyncratic_var = self.calculate_idiosyncratic_sentiment_risk(
            portfolio_holdings, sentiment_data
        )
        
        # Sector sentiment risk
        sector_var = self.calculate_sector_sentiment_risk(
            portfolio_holdings, sentiment_data
        )
        
        # Momentum sentiment risk
        momentum_var = self.calculate_momentum_sentiment_risk(
            portfolio_holdings, sentiment_data
        )
        
        # Risk attribution
        risk_attribution = {
            'total_var': total_portfolio_var,
            'market_sentiment_contribution': market_sentiment_var / total_portfolio_var,
            'idiosyncratic_contribution': idiosyncratic_var / total_portfolio_var,
            'sector_contribution': sector_var / total_portfolio_var,
            'momentum_contribution': momentum_var / total_portfolio_var,
            'diversification_benefit': 1 - (
                market_sentiment_var + idiosyncratic_var + 
                sector_var + momentum_var
            ) / total_portfolio_var
        }
        
        return risk_attribution
    
    def calculate_risk_adjusted_returns(self, portfolio_data, sentiment_data):
        """Calculate risk-adjusted returns incorporating sentiment"""
        
        returns = portfolio_data['returns'].values
        sentiment = sentiment_data['sentiment_score'].values
        
        # Sharpe ratio with sentiment adjustment
        risk_free_rate = 0.02  # Assume 2% risk-free rate
        sentiment_adjusted_returns = self.adjust_returns_for_sentiment(returns, sentiment)
        
        sharpe_ratio = (np.mean(sentiment_adjusted_returns) - risk_free_rate) / np.std(sentiment_adjusted_returns)
        
        # Sortino ratio (downside deviation)
        downside_returns = sentiment_adjusted_returns[sentiment_adjusted_returns < 0]
        downside_deviation = np.std(downside_returns) if len(downside_returns) > 0 else 0
        sortino_ratio = (np.mean(sentiment_adjusted_returns) - risk_free_rate) / downside_deviation if downside_deviation > 0 else np.inf
        
        # Calmar ratio (return/max drawdown)
        max_drawdown = self.calculate_max_drawdown(sentiment_adjusted_returns)
        calmar_ratio = np.mean(sentiment_adjusted_returns) / abs(max_drawdown) if max_drawdown != 0 else np.inf
        
        # Information ratio vs sentiment-naive benchmark
        benchmark_returns = returns  # Naive benchmark without sentiment
        active_returns = sentiment_adjusted_returns - benchmark_returns
        tracking_error = np.std(active_returns)
        information_ratio = np.mean(active_returns) / tracking_error if tracking_error > 0 else 0
        
        return {
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'calmar_ratio': calmar_ratio,
            'information_ratio': information_ratio,
            'sentiment_alpha': np.mean(active_returns),
            'tracking_error': tracking_error
        }
```

## Trading Strategy Development

### Sentiment-Based Trading Signals

```python
class SentimentTradingStrategy:
    def __init__(self):
        self.signal_types = [
            'sentiment_momentum',
            'sentiment_reversal',
            'sentiment_divergence',
            'sentiment_extreme',
            'sentiment_correlation'
        ]
    
    def generate_momentum_signals(self, sentiment_data, price_data, lookback_period=20):
        """Generate momentum-based trading signals"""
        
        signals = []
        
        for i in range(lookback_period, len(sentiment_data)):
            current_sentiment = sentiment_data.iloc[i]['sentiment_score']
            sentiment_ma = sentiment_data.iloc[i-lookback_period:i]['sentiment_score'].mean()
            sentiment_std = sentiment_data.iloc[i-lookback_period:i]['sentiment_score'].std()
            
            current_price = price_data.iloc[i]['price']
            price_ma = price_data.iloc[i-lookback_period:i]['price'].mean()
            
            # Momentum signal conditions
            sentiment_momentum = (current_sentiment - sentiment_ma) / sentiment_std
            price_momentum = (current_price - price_ma) / price_ma
            
            signal_strength = 0
            signal_type = 'hold'
            
            # Strong positive momentum
            if sentiment_momentum > 1.5 and price_momentum > 0.02:
                signal_strength = min(sentiment_momentum * 0.5, 1.0)
                signal_type = 'buy'
            
            # Strong negative momentum
            elif sentiment_momentum < -1.5 and price_momentum < -0.02:
                signal_strength = min(abs(sentiment_momentum) * 0.5, 1.0)
                signal_type = 'sell'
            
            # Divergence signals (price vs sentiment)
            elif abs(sentiment_momentum) > 1.0 and np.sign(sentiment_momentum) != np.sign(price_momentum):
                signal_strength = abs(sentiment_momentum) * 0.3
                signal_type = 'buy' if sentiment_momentum > 0 else 'sell'
            
            signals.append({
                'timestamp': sentiment_data.iloc[i]['timestamp'],
                'signal_type': signal_type,
                'signal_strength': signal_strength,
                'sentiment_momentum': sentiment_momentum,
                'price_momentum': price_momentum,
                'confidence': self.calculate_signal_confidence(sentiment_data.iloc[i-lookback_period:i])
            })
        
        return pd.DataFrame(signals)
    
    def generate_reversal_signals(self, sentiment_data, price_data, extreme_threshold=2.0):
        """Generate mean reversion signals based on sentiment extremes"""
        
        signals = []
        
        # Calculate rolling sentiment statistics
        sentiment_data['sentiment_zscore'] = (
            sentiment_data['sentiment_score'] - 
            sentiment_data['sentiment_score'].rolling(50).mean()
        ) / sentiment_data['sentiment_score'].rolling(50).std()
        
        for i in range(50, len(sentiment_data)):
            current_zscore = sentiment_data.iloc[i]['sentiment_zscore']
            current_sentiment = sentiment_data.iloc[i]['sentiment_score']
            
            signal_strength = 0
            signal_type = 'hold'
            
            # Extreme pessimism - potential buy signal
            if current_zscore < -extreme_threshold and current_sentiment < -0.5:
                signal_strength = min(abs(current_zscore) / extreme_threshold, 1.0)
                signal_type = 'buy'
            
            # Extreme optimism - potential sell signal
            elif current_zscore > extreme_threshold and current_sentiment > 0.5:
                signal_strength = min(current_zscore / extreme_threshold, 1.0)
                signal_type = 'sell'
            
            signals.append({
                'timestamp': sentiment_data.iloc[i]['timestamp'],
                'signal_type': signal_type,
                'signal_strength': signal_strength,
                'sentiment_zscore': current_zscore,
                'sentiment_raw': current_sentiment,
                'reversal_probability': self.calculate_reversal_probability(
                    sentiment_data.iloc[i-20:i]
                )
            })
        
        return pd.DataFrame(signals)
    
    def backtest_strategy(self, signals, price_data, initial_capital=100000, transaction_costs=0.001):
        """Backtest sentiment trading strategy"""
        
        portfolio_value = [initial_capital]
        positions = [0]  # Number of shares held
        cash = [initial_capital]
        trades = []
        
        for i, signal in signals.iterrows():
            current_price = price_data[price_data['timestamp'] == signal['timestamp']]['price'].iloc[0]
            current_cash = cash[-1]
            current_position = positions[-1]
            current_value = current_cash + current_position * current_price
            
            trade_size = 0
            
            if signal['signal_type'] == 'buy' and signal['signal_strength'] > 0.5:
                # Calculate position size based on signal strength
                target_allocation = signal['signal_strength'] * 0.5  # Max 50% allocation
                target_value = current_value * target_allocation
                target_shares = int(target_value / current_price)
                trade_size = target_shares - current_position
                
            elif signal['signal_type'] == 'sell' and signal['signal_strength'] > 0.5:
                # Sell based on signal strength
                sell_ratio = signal['signal_strength'] * 0.8  # Max 80% sell
                trade_size = -int(current_position * sell_ratio)
            
            # Execute trade
            if trade_size != 0:
                trade_value = abs(trade_size) * current_price
                transaction_cost = trade_value * transaction_costs
                
                if trade_size > 0:  # Buy
                    if current_cash >= trade_value + transaction_cost:
                        new_cash = current_cash - trade_value - transaction_cost
                        new_position = current_position + trade_size
                    else:
                        continue  # Insufficient cash
                else:  # Sell
                    new_cash = current_cash + trade_value - transaction_cost
                    new_position = current_position + trade_size
                
                trades.append({
                    'timestamp': signal['timestamp'],
                    'trade_type': 'buy' if trade_size > 0 else 'sell',
                    'shares': abs(trade_size),
                    'price': current_price,
                    'value': trade_value,
                    'transaction_cost': transaction_cost,
                    'signal_strength': signal['signal_strength']
                })
                
                cash.append(new_cash)
                positions.append(new_position)
            else:
                cash.append(current_cash)
                positions.append(current_position)
            
            # Update portfolio value
            new_value = cash[-1] + positions[-1] * current_price
            portfolio_value.append(new_value)
        
        # Calculate performance metrics
        returns = pd.Series(portfolio_value).pct_change().dropna()
        
        performance_metrics = {
            'total_return': (portfolio_value[-1] - initial_capital) / initial_capital,
            'annualized_return': (portfolio_value[-1] / initial_capital) ** (252 / len(returns)) - 1,
            'volatility': returns.std() * np.sqrt(252),
            'sharpe_ratio': (returns.mean() * 252 - 0.02) / (returns.std() * np.sqrt(252)),
            'max_drawdown': self.calculate_max_drawdown(portfolio_value),
            'win_rate': len([t for t in trades if (t['trade_type'] == 'sell' and 
                           price_data[price_data['timestamp'] == t['timestamp']]['price'].iloc[0] > 
                           [tr['price'] for tr in trades if tr['trade_type'] == 'buy' and 
                            tr['timestamp'] < t['timestamp']][-1])]) / len([t for t in trades if t['trade_type'] == 'sell']),
            'total_trades': len(trades),
            'avg_trade_return': np.mean([t['value'] for t in trades])
        }
        
        return {
            'performance_metrics': performance_metrics,
            'portfolio_values': portfolio_value,
            'trades': trades,
            'positions': positions,
            'cash': cash
        }
```

### Strategy Optimization

```python
class StrategyOptimizer:
    def __init__(self):
        self.optimization_methods = ['grid_search', 'genetic_algorithm', 'bayesian_optimization']
    
    def optimize_sentiment_strategy(self, sentiment_data, price_data, parameter_ranges):
        """Optimize strategy parameters using multiple methods"""
        
        # Grid search optimization
        grid_results = self.grid_search_optimization(
            sentiment_data, price_data, parameter_ranges
        )
        
        # Genetic algorithm optimization
        ga_results = self.genetic_algorithm_optimization(
            sentiment_data, price_data, parameter_ranges
        )
        
        # Bayesian optimization
        bayes_results = self.bayesian_optimization(
            sentiment_data, price_data, parameter_ranges
        )
        
        # Compare results and select best
        best_params = self.select_best_parameters(grid_results, ga_results, bayes_results)
        
        # Validate with out-of-sample testing
        validation_results = self.validate_parameters(
            best_params, sentiment_data, price_data
        )
        
        return {
            'optimal_parameters': best_params,
            'optimization_results': {
                'grid_search': grid_results,
                'genetic_algorithm': ga_results,
                'bayesian': bayes_results
            },
            'validation_results': validation_results,
            'parameter_sensitivity': self.analyze_parameter_sensitivity(
                sentiment_data, price_data, best_params
            )
        }
    
    def walk_forward_analysis(self, sentiment_data, price_data, strategy_params, 
                             training_period=252, rebalance_frequency=63):
        """Perform walk-forward analysis of strategy"""
        
        results = []
        
        for start_idx in range(training_period, len(sentiment_data) - rebalance_frequency, 
                              rebalance_frequency):
            
            # Training period
            train_sentiment = sentiment_data.iloc[start_idx-training_period:start_idx]
            train_price = price_data.iloc[start_idx-training_period:start_idx]
            
            # Testing period
            test_sentiment = sentiment_data.iloc[start_idx:start_idx+rebalance_frequency]
            test_price = price_data.iloc[start_idx:start_idx+rebalance_frequency]
            
            # Optimize parameters on training data
            optimized_params = self.optimize_on_period(
                train_sentiment, train_price, strategy_params
            )
            
            # Test on out-of-sample data
            test_results = self.test_strategy(
                test_sentiment, test_price, optimized_params
            )
            
            results.append({
                'period_start': start_idx,
                'period_end': start_idx + rebalance_frequency,
                'optimized_params': optimized_params,
                'test_return': test_results['total_return'],
                'test_sharpe': test_results['sharpe_ratio'],
                'test_max_dd': test_results['max_drawdown']
            })
        
        # Aggregate walk-forward results
        wf_analysis = {
            'periods_tested': len(results),
            'avg_return': np.mean([r['test_return'] for r in results]),
            'avg_sharpe': np.mean([r['test_sharpe'] for r in results]),
            'avg_max_dd': np.mean([r['test_max_dd'] for r in results]),
            'return_stability': np.std([r['test_return'] for r in results]),
            'parameter_stability': self.analyze_parameter_stability(results),
            'detailed_results': results
        }
        
        return wf_analysis
```

This comprehensive financial analysis documentation provides the foundation for sophisticated sentiment-based trading strategies, risk management, and portfolio optimization techniques.
