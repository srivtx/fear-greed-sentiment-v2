# Experimental Design and Validation Framework

## Overview

This document details the comprehensive experimental design, validation protocols, and testing methodologies used to evaluate the Fear & Greed Sentiment Engine's performance, accuracy, and reliability across various market conditions and asset classes.

## Experimental Design Framework

### 1. Research Design Principles

#### A/B Testing Framework
```python
class SentimentExperimentDesign:
    def __init__(self):
        self.design_principles = {
            'randomization': 'Ensure unbiased sample selection',
            'control_groups': 'Compare against benchmark strategies',
            'blinding': 'Prevent look-ahead bias in backtesting',
            'replication': 'Validate results across multiple periods',
            'statistical_power': 'Sufficient sample size for significance'
        }
    
    def create_experimental_groups(self, asset_universe, test_period):
        """Create experimental groups for A/B testing"""
        
        groups = {
            'treatment_group': {
                'description': 'Sentiment-enhanced trading strategy',
                'strategy': 'SentimentMomentumStrategy',
                'assets': self.stratified_sample(asset_universe, 0.5),
                'features': ['sentiment_score', 'sentiment_momentum', 'price_data'],
                'rebalance_frequency': 'daily'
            },
            'control_group_1': {
                'description': 'Traditional momentum strategy (no sentiment)',
                'strategy': 'MomentumOnlyStrategy', 
                'assets': self.stratified_sample(asset_universe, 0.25),
                'features': ['price_data', 'volume_data'],
                'rebalance_frequency': 'daily'
            },
            'control_group_2': {
                'description': 'Buy and hold benchmark',
                'strategy': 'BuyHoldStrategy',
                'assets': self.stratified_sample(asset_universe, 0.25),
                'features': ['price_data'],
                'rebalance_frequency': 'never'
            }
        }
        
        return groups
    
    def stratified_sample(self, universe, proportion):
        """Create stratified sample by market cap and sector"""
        
        strata = {
            'large_cap_tech': universe[
                (universe['market_cap'] > 10e9) & 
                (universe['sector'] == 'Technology')
            ].sample(frac=proportion),
            'large_cap_finance': universe[
                (universe['market_cap'] > 10e9) & 
                (universe['sector'] == 'Finance')
            ].sample(frac=proportion),
            'mid_cap': universe[
                (universe['market_cap'] > 2e9) & 
                (universe['market_cap'] <= 10e9)
            ].sample(frac=proportion),
            'small_cap': universe[
                universe['market_cap'] <= 2e9
            ].sample(frac=proportion)
        }
        
        return pd.concat(strata.values())
```

#### Factorial Design for Multi-Factor Analysis
```python
class FactorialExperimentDesign:
    def __init__(self):
        self.factors = {
            'sentiment_source': ['twitter', 'reddit', 'news', 'combined'],
            'prediction_horizon': ['1h', '4h', '1d', '1w'],
            'model_type': ['linear', 'random_forest', 'xgboost', 'ensemble'],
            'market_regime': ['bull', 'bear', 'sideways', 'volatile']
        }
    
    def generate_factor_combinations(self):
        """Generate all factor combinations for full factorial design"""
        
        import itertools
        
        factor_names = list(self.factors.keys())
        factor_levels = list(self.factors.values())
        
        combinations = list(itertools.product(*factor_levels))
        
        experiment_grid = []
        for combo in combinations:
            experiment = dict(zip(factor_names, combo))
            experiment['experiment_id'] = self.generate_experiment_id(experiment)
            experiment_grid.append(experiment)
        
        return experiment_grid
    
    def analyze_factorial_results(self, results_df):
        """Analyze main effects and interactions"""
        
        import statsmodels.api as sm
        from statsmodels.formula.api import ols
        
        # Main effects analysis
        main_effects = {}
        for factor in self.factors.keys():
            formula = f'performance ~ C({factor})'
            model = ols(formula, data=results_df).fit()
            main_effects[factor] = {
                'f_statistic': model.fvalue,
                'p_value': model.f_pvalue,
                'r_squared': model.rsquared,
                'significant': model.f_pvalue < 0.05
            }
        
        # Interaction effects
        interaction_effects = {}
        factor_pairs = itertools.combinations(self.factors.keys(), 2)
        
        for factor1, factor2 in factor_pairs:
            formula = f'performance ~ C({factor1}) * C({factor2})'
            model = ols(formula, data=results_df).fit()
            interaction_effects[f'{factor1}_x_{factor2}'] = {
                'f_statistic': model.fvalue,
                'p_value': model.f_pvalue,
                'interaction_significant': model.f_pvalue < 0.05
            }
        
        return {
            'main_effects': main_effects,
            'interaction_effects': interaction_effects,
            'anova_table': sm.stats.anova_lm(model, typ=2)
        }
```

### 2. Time Series Experimental Design

#### Walk-Forward Analysis
```python
class WalkForwardValidation:
    def __init__(self):
        self.training_window = 252  # 1 year of trading days
        self.validation_window = 63  # 1 quarter
        self.test_window = 21       # 1 month
        self.step_size = 21         # Monthly rebalancing
    
    def create_time_splits(self, data, start_date, end_date):
        """Create time-based splits for walk-forward analysis"""
        
        date_range = pd.date_range(start_date, end_date, freq='D')
        trading_days = [d for d in date_range if d.weekday() < 5]  # Exclude weekends
        
        splits = []
        
        for i in range(self.training_window, 
                      len(trading_days) - self.test_window, 
                      self.step_size):
            
            train_start = i - self.training_window
            train_end = i
            val_start = i
            val_end = i + self.validation_window
            test_start = i + self.validation_window
            test_end = min(i + self.validation_window + self.test_window, 
                          len(trading_days))
            
            split = {
                'split_id': len(splits) + 1,
                'train_period': (trading_days[train_start], trading_days[train_end-1]),
                'validation_period': (trading_days[val_start], trading_days[val_end-1]),
                'test_period': (trading_days[test_start], trading_days[test_end-1]),
                'market_conditions': self.analyze_market_conditions(
                    trading_days[train_start:test_end]
                )
            }
            
            splits.append(split)
        
        return splits
    
    def analyze_market_conditions(self, period_dates):
        """Analyze market conditions during the period"""
        
        # This would typically fetch actual market data
        # For demonstration, using simulated conditions
        
        return {
            'avg_volatility': np.random.uniform(0.15, 0.35),
            'trend_direction': np.random.choice(['bull', 'bear', 'sideways']),
            'regime_changes': np.random.randint(0, 3),
            'earnings_seasons': self.count_earnings_seasons(period_dates)
        }
    
    def execute_walk_forward_test(self, strategy, data_splits):
        """Execute walk-forward validation"""
        
        results = []
        
        for split in data_splits:
            # Train model on training data
            model = strategy.train(split['train_period'])
            
            # Validate and tune on validation data
            tuned_model = strategy.tune_hyperparameters(
                model, split['validation_period']
            )
            
            # Test on out-of-sample data
            test_results = strategy.backtest(
                tuned_model, split['test_period']
            )
            
            results.append({
                'split_id': split['split_id'],
                'test_period': split['test_period'],
                'returns': test_results['returns'],
                'sharpe_ratio': test_results['sharpe_ratio'],
                'max_drawdown': test_results['max_drawdown'],
                'hit_rate': test_results['hit_rate'],
                'market_conditions': split['market_conditions']
            })
        
        return self.aggregate_walk_forward_results(results)
```

#### Cross-Validation for Time Series
```python
class TimeSeriesCrossValidation:
    def __init__(self):
        self.cv_methods = [
            'purged_group_time_series_split',
            'blocked_time_series_split', 
            'expanding_window_split'
        ]
    
    def purged_group_time_series_split(self, data, n_splits=5, purge_length=5):
        """Purged group time series split to prevent data leakage"""
        
        n_samples = len(data)
        test_size = n_samples // n_splits
        
        splits = []
        
        for i in range(n_splits):
            test_start = i * test_size
            test_end = (i + 1) * test_size
            
            # Training data: everything before test set minus purge period
            train_end = test_start - purge_length
            train_indices = list(range(0, max(0, train_end)))
            
            # Test data
            test_indices = list(range(test_start, test_end))
            
            if len(train_indices) > 0 and len(test_indices) > 0:
                splits.append({
                    'train': train_indices,
                    'test': test_indices,
                    'purge_period': (max(0, train_end), test_start)
                })
        
        return splits
    
    def blocked_time_series_split(self, data, n_splits=5, block_size=50):
        """Blocked time series split with non-overlapping blocks"""
        
        n_samples = len(data)
        total_blocks = n_samples // block_size
        test_blocks_per_split = total_blocks // n_splits
        
        splits = []
        
        for i in range(n_splits):
            test_block_start = i * test_blocks_per_split
            test_block_end = (i + 1) * test_blocks_per_split
            
            # Test indices
            test_indices = []
            for block_idx in range(test_block_start, test_block_end):
                start_idx = block_idx * block_size
                end_idx = min((block_idx + 1) * block_size, n_samples)
                test_indices.extend(range(start_idx, end_idx))
            
            # Train indices (all other blocks)
            train_indices = []
            for block_idx in range(total_blocks):
                if block_idx < test_block_start or block_idx >= test_block_end:
                    start_idx = block_idx * block_size
                    end_idx = min((block_idx + 1) * block_size, n_samples)
                    train_indices.extend(range(start_idx, end_idx))
            
            splits.append({
                'train': train_indices,
                'test': test_indices,
                'test_blocks': (test_block_start, test_block_end)
            })
        
        return splits
```

## Validation Protocols

### 1. Model Validation Framework

#### Performance Metrics Validation
```python
class PerformanceValidation:
    def __init__(self):
        self.metrics = [
            'sharpe_ratio', 'sortino_ratio', 'calmar_ratio',
            'information_ratio', 'alpha', 'beta', 'tracking_error',
            'max_drawdown', 'var_95', 'expected_shortfall'
        ]
    
    def validate_performance_metrics(self, strategy_returns, benchmark_returns):
        """Comprehensive performance validation"""
        
        validation_results = {}
        
        # Risk-adjusted returns
        validation_results['sharpe_ratio'] = self.validate_sharpe_ratio(strategy_returns)
        validation_results['sortino_ratio'] = self.validate_sortino_ratio(strategy_returns)
        
        # Relative performance
        validation_results['alpha_beta'] = self.validate_alpha_beta(
            strategy_returns, benchmark_returns
        )
        
        # Risk metrics
        validation_results['drawdown_analysis'] = self.validate_drawdown_metrics(strategy_returns)
        validation_results['var_analysis'] = self.validate_var_metrics(strategy_returns)
        
        # Stability tests
        validation_results['stability_tests'] = self.test_performance_stability(strategy_returns)
        
        return validation_results
    
    def validate_sharpe_ratio(self, returns, risk_free_rate=0.02):
        """Validate Sharpe ratio with confidence intervals"""
        
        excess_returns = returns - risk_free_rate/252  # Daily risk-free rate
        sharpe = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
        
        # Bootstrap confidence interval
        n_bootstrap = 1000
        bootstrap_sharpes = []
        
        for _ in range(n_bootstrap):
            sample_returns = np.random.choice(excess_returns, size=len(excess_returns), replace=True)
            bootstrap_sharpe = np.mean(sample_returns) / np.std(sample_returns) * np.sqrt(252)
            bootstrap_sharpes.append(bootstrap_sharpe)
        
        confidence_interval = np.percentile(bootstrap_sharpes, [2.5, 97.5])
        
        return {
            'sharpe_ratio': sharpe,
            'confidence_interval': confidence_interval,
            'bootstrap_distribution': bootstrap_sharpes,
            'statistical_significance': sharpe > 0 and confidence_interval[0] > 0
        }
    
    def test_performance_stability(self, returns, window_size=252):
        """Test stability of performance metrics over time"""
        
        rolling_sharpes = []
        rolling_max_dds = []
        
        for i in range(window_size, len(returns)):
            window_returns = returns[i-window_size:i]
            
            # Rolling Sharpe ratio
            sharpe = np.mean(window_returns) / np.std(window_returns) * np.sqrt(252)
            rolling_sharpes.append(sharpe)
            
            # Rolling max drawdown
            cumulative = (1 + window_returns).cumprod()
            rolling_max = cumulative.expanding().max()
            drawdown = (cumulative - rolling_max) / rolling_max
            max_dd = drawdown.min()
            rolling_max_dds.append(max_dd)
        
        stability_metrics = {
            'sharpe_ratio_stability': {
                'mean': np.mean(rolling_sharpes),
                'std': np.std(rolling_sharpes),
                'coefficient_of_variation': np.std(rolling_sharpes) / np.mean(rolling_sharpes),
                'min': np.min(rolling_sharpes),
                'max': np.max(rolling_sharpes)
            },
            'drawdown_stability': {
                'mean_max_drawdown': np.mean(rolling_max_dds),
                'worst_drawdown': np.min(rolling_max_dds),
                'drawdown_frequency': len([dd for dd in rolling_max_dds if dd < -0.05])
            }
        }
        
        return stability_metrics
```

#### Model Robustness Testing
```python
class RobustnessValidation:
    def __init__(self):
        self.stress_tests = [
            'parameter_sensitivity',
            'data_quality_degradation',
            'market_regime_shifts',
            'outlier_resistance'
        ]
    
    def parameter_sensitivity_analysis(self, model, base_params, param_ranges):
        """Test model sensitivity to parameter changes"""
        
        sensitivity_results = {}
        base_performance = model.evaluate(base_params)
        
        for param_name, param_range in param_ranges.items():
            param_sensitivity = []
            
            for param_value in param_range:
                test_params = base_params.copy()
                test_params[param_name] = param_value
                
                test_performance = model.evaluate(test_params)
                performance_change = (test_performance - base_performance) / base_performance
                
                param_sensitivity.append({
                    'param_value': param_value,
                    'performance_change': performance_change,
                    'absolute_performance': test_performance
                })
            
            sensitivity_results[param_name] = {
                'sensitivity_curve': param_sensitivity,
                'max_sensitivity': max([abs(s['performance_change']) for s in param_sensitivity]),
                'optimal_value': max(param_sensitivity, key=lambda x: x['absolute_performance'])['param_value']
            }
        
        return sensitivity_results
    
    def data_quality_stress_test(self, model, clean_data, degradation_levels):
        """Test model performance under data quality degradation"""
        
        stress_test_results = {}
        
        for degradation_type, levels in degradation_levels.items():
            degradation_results = []
            
            for level in levels:
                if degradation_type == 'missing_data':
                    corrupted_data = self.introduce_missing_data(clean_data, level)
                elif degradation_type == 'noise':
                    corrupted_data = self.add_noise(clean_data, level)
                elif degradation_type == 'outliers':
                    corrupted_data = self.inject_outliers(clean_data, level)
                
                performance = model.evaluate_on_data(corrupted_data)
                
                degradation_results.append({
                    'degradation_level': level,
                    'performance': performance,
                    'performance_degradation': (performance - model.baseline_performance) / model.baseline_performance
                })
            
            stress_test_results[degradation_type] = degradation_results
        
        return stress_test_results
    
    def market_regime_robustness(self, model, historical_data, regime_definitions):
        """Test model performance across different market regimes"""
        
        regime_performance = {}
        
        for regime_name, regime_criteria in regime_definitions.items():
            # Filter data for this regime
            regime_data = self.filter_by_regime(historical_data, regime_criteria)
            
            if len(regime_data) > 100:  # Minimum data points
                performance = model.evaluate_on_data(regime_data)
                
                regime_performance[regime_name] = {
                    'performance': performance,
                    'data_points': len(regime_data),
                    'regime_characteristics': self.analyze_regime_characteristics(regime_data),
                    'relative_performance': performance / model.baseline_performance
                }
        
        # Test regime transition periods
        transition_performance = self.test_regime_transitions(model, historical_data, regime_definitions)
        
        return {
            'regime_performance': regime_performance,
            'transition_performance': transition_performance,
            'regime_stability_score': self.calculate_regime_stability(regime_performance)
        }
```

### 2. Statistical Validation

#### Hypothesis Testing Framework
```python
class StatisticalValidation:
    def __init__(self):
        self.significance_level = 0.05
        self.test_types = [
            'normality_tests',
            'stationarity_tests', 
            'independence_tests',
            'homoscedasticity_tests'
        ]
    
    def comprehensive_statistical_validation(self, returns_data, predictions):
        """Comprehensive statistical validation of model outputs"""
        
        validation_results = {}
        
        # Test return distribution assumptions
        validation_results['normality'] = self.test_normality(returns_data)
        validation_results['stationarity'] = self.test_stationarity(returns_data)
        validation_results['independence'] = self.test_independence(returns_data)
        
        # Test prediction quality
        validation_results['prediction_tests'] = self.test_prediction_quality(returns_data, predictions)
        
        # Test model residuals
        residuals = returns_data - predictions
        validation_results['residual_analysis'] = self.analyze_residuals(residuals)
        
        return validation_results
    
    def test_normality(self, data):
        """Test normality of returns distribution"""
        
        from scipy import stats
        
        # Shapiro-Wilk test (small samples)
        shapiro_stat, shapiro_p = stats.shapiro(data[:5000])  # Limit sample size
        
        # Jarque-Bera test
        jb_stat, jb_p = stats.jarque_bera(data)
        
        # Anderson-Darling test
        ad_stat, ad_critical, ad_p = stats.anderson(data, dist='norm')
        
        # Kolmogorov-Smirnov test
        ks_stat, ks_p = stats.kstest(data, 'norm', args=(np.mean(data), np.std(data)))
        
        return {
            'shapiro_wilk': {'statistic': shapiro_stat, 'p_value': shapiro_p, 'normal': shapiro_p > self.significance_level},
            'jarque_bera': {'statistic': jb_stat, 'p_value': jb_p, 'normal': jb_p > self.significance_level},
            'anderson_darling': {'statistic': ad_stat, 'critical_values': ad_critical, 'normal': ad_stat < ad_critical[2]},
            'kolmogorov_smirnov': {'statistic': ks_stat, 'p_value': ks_p, 'normal': ks_p > self.significance_level},
            'summary': {
                'tests_passed': sum([
                    shapiro_p > self.significance_level,
                    jb_p > self.significance_level, 
                    ad_stat < ad_critical[2],
                    ks_p > self.significance_level
                ]),
                'total_tests': 4,
                'likely_normal': sum([
                    shapiro_p > self.significance_level,
                    jb_p > self.significance_level,
                    ad_stat < ad_critical[2],
                    ks_p > self.significance_level
                ]) >= 2
            }
        }
    
    def test_stationarity(self, data):
        """Test stationarity of time series"""
        
        from statsmodels.tsa.stattools import adfuller, kpss
        
        # Augmented Dickey-Fuller test
        adf_result = adfuller(data, autolag='AIC')
        
        # KPSS test
        kpss_result = kpss(data, regression='c')
        
        # Phillips-Perron test (approximated by ADF with different lag selection)
        pp_result = adfuller(data, regression='c', autolag=None, maxlag=int(12*(len(data)/100)**(1/4)))
        
        return {
            'adf_test': {
                'statistic': adf_result[0],
                'p_value': adf_result[1],
                'critical_values': adf_result[4],
                'stationary': adf_result[1] < self.significance_level
            },
            'kpss_test': {
                'statistic': kpss_result[0],
                'p_value': kpss_result[1],
                'critical_values': kpss_result[3],
                'stationary': kpss_result[1] > self.significance_level
            },
            'phillips_perron': {
                'statistic': pp_result[0],
                'p_value': pp_result[1],
                'stationary': pp_result[1] < self.significance_level
            },
            'summary': {
                'likely_stationary': (adf_result[1] < self.significance_level) and (kpss_result[1] > self.significance_level)
            }
        }
    
    def test_prediction_quality(self, actual, predicted):
        """Test quality of predictions"""
        
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        
        # Basic metrics
        mse = mean_squared_error(actual, predicted)
        mae = mean_absolute_error(actual, predicted)
        r2 = r2_score(actual, predicted)
        
        # Directional accuracy
        actual_direction = np.sign(actual)
        predicted_direction = np.sign(predicted)
        directional_accuracy = np.mean(actual_direction == predicted_direction)
        
        # Theil's U statistic
        naive_forecast = np.roll(actual, 1)[1:]  # Naive forecast (previous value)
        actual_test = actual[1:]
        predicted_test = predicted[1:]
        
        mse_model = mean_squared_error(actual_test, predicted_test)
        mse_naive = mean_squared_error(actual_test, naive_forecast)
        theil_u = np.sqrt(mse_model) / np.sqrt(mse_naive)
        
        # Diebold-Mariano test for forecast accuracy
        dm_stat, dm_p = self.diebold_mariano_test(actual, predicted, naive_forecast[:-1])
        
        return {
            'mse': mse,
            'mae': mae,
            'r2_score': r2,
            'directional_accuracy': directional_accuracy,
            'theil_u': theil_u,
            'forecast_improvement': theil_u < 1.0,
            'diebold_mariano': {
                'statistic': dm_stat,
                'p_value': dm_p,
                'significantly_better': dm_p < self.significance_level and dm_stat < 0
            }
        }
    
    def diebold_mariano_test(self, actual, forecast1, forecast2):
        """Diebold-Mariano test for comparing forecast accuracy"""
        
        # Calculate forecast errors
        e1 = actual - forecast1
        e2 = actual - forecast2
        
        # Calculate loss differential
        d = e1**2 - e2**2
        
        # Calculate test statistic
        d_mean = np.mean(d)
        d_var = np.var(d, ddof=1)
        dm_stat = d_mean / np.sqrt(d_var / len(d))
        
        # P-value (two-tailed test)
        from scipy import stats
        p_value = 2 * (1 - stats.norm.cdf(abs(dm_stat)))
        
        return dm_stat, p_value
```

## Testing Methodologies

### 1. Backtesting Framework

#### Advanced Backtesting Engine
```python
class AdvancedBacktestEngine:
    def __init__(self):
        self.execution_models = [
            'perfect_execution',
            'realistic_slippage',
            'market_impact',
            'latency_simulation'
        ]
    
    def comprehensive_backtest(self, strategy, data, config):
        """Comprehensive backtesting with multiple execution models"""
        
        backtest_results = {}
        
        for execution_model in self.execution_models:
            print(f"Running backtest with {execution_model} execution model...")
            
            # Configure execution model
            execution_config = self.configure_execution_model(execution_model, config)
            
            # Run backtest
            result = self.run_single_backtest(strategy, data, execution_config)
            
            backtest_results[execution_model] = result
        
        # Compare execution models
        execution_comparison = self.compare_execution_models(backtest_results)
        
        # Monte Carlo simulation
        mc_results = self.monte_carlo_backtest(strategy, data, config, n_simulations=1000)
        
        return {
            'execution_model_results': backtest_results,
            'execution_comparison': execution_comparison,
            'monte_carlo_results': mc_results,
            'summary_statistics': self.calculate_summary_statistics(backtest_results)
        }
    
    def configure_execution_model(self, model_type, base_config):
        """Configure specific execution model parameters"""
        
        configs = {
            'perfect_execution': {
                'slippage': 0.0,
                'commission': 0.0,
                'market_impact': 0.0,
                'latency': 0.0
            },
            'realistic_slippage': {
                'slippage': 0.0005,  # 5 basis points
                'commission': 0.001,  # 10 basis points
                'market_impact': 0.0,
                'latency': 0.0
            },
            'market_impact': {
                'slippage': 0.0005,
                'commission': 0.001,
                'market_impact': self.calculate_market_impact,
                'latency': 0.0
            },
            'latency_simulation': {
                'slippage': 0.0005,
                'commission': 0.001,
                'market_impact': self.calculate_market_impact,
                'latency': 0.1  # 100ms latency
            }
        }
        
        config = base_config.copy()
        config.update(configs[model_type])
        
        return config
    
    def calculate_market_impact(self, trade_size, avg_volume, volatility):
        """Calculate market impact based on trade characteristics"""
        
        # Simplified market impact model
        volume_participation = trade_size / avg_volume
        impact = 0.5 * volatility * np.sqrt(volume_participation)
        
        return min(impact, 0.01)  # Cap at 100 basis points
```

### 2. Stress Testing

#### Market Stress Scenarios
```python
class StressTestFramework:
    def __init__(self):
        self.stress_scenarios = {
            'market_crash': {
                'description': '2008-style market crash',
                'duration_days': 180,
                'max_drawdown': -0.50,
                'volatility_multiplier': 3.0,
                'correlation_increase': 0.3
            },
            'flash_crash': {
                'description': 'Rapid intraday crash',
                'duration_days': 1,
                'max_drawdown': -0.20,
                'volatility_multiplier': 10.0,
                'recovery_days': 5
            },
            'prolonged_bear': {
                'description': 'Extended bear market',
                'duration_days': 720,
                'max_drawdown': -0.35,
                'volatility_multiplier': 1.8,
                'trend': -0.15
            },
            'sentiment_whipsaw': {
                'description': 'Extreme sentiment volatility',
                'duration_days': 90,
                'sentiment_volatility_multiplier': 5.0,
                'signal_noise_ratio': 0.3
            }
        }
    
    def run_stress_tests(self, strategy, base_data):
        """Run comprehensive stress tests"""
        
        stress_results = {}
        
        for scenario_name, scenario_params in self.stress_scenarios.items():
            print(f"Running stress test: {scenario_name}")
            
            # Generate stressed data
            stressed_data = self.generate_stress_scenario(base_data, scenario_params)
            
            # Run strategy on stressed data
            strategy_performance = strategy.backtest(stressed_data)
            
            # Analyze stress impact
            stress_impact = self.analyze_stress_impact(
                strategy.baseline_performance, 
                strategy_performance
            )
            
            stress_results[scenario_name] = {
                'scenario_parameters': scenario_params,
                'strategy_performance': strategy_performance,
                'stress_impact': stress_impact,
                'recovery_analysis': self.analyze_recovery(strategy_performance)
            }
        
        return {
            'individual_stress_tests': stress_results,
            'combined_stress_analysis': self.combined_stress_analysis(stress_results),
            'stress_resistance_score': self.calculate_stress_resistance_score(stress_results)
        }
    
    def generate_stress_scenario(self, base_data, scenario_params):
        """Generate stressed market data based on scenario parameters"""
        
        stressed_data = base_data.copy()
        
        if 'volatility_multiplier' in scenario_params:
            # Increase volatility
            returns = stressed_data['returns']
            vol_multiplier = scenario_params['volatility_multiplier']
            stressed_returns = returns * vol_multiplier
            stressed_data['returns'] = stressed_returns
            
            # Recalculate prices
            stressed_data['price'] = (1 + stressed_returns).cumprod() * base_data['price'].iloc[0]
        
        if 'max_drawdown' in scenario_params:
            # Impose maximum drawdown
            target_drawdown = scenario_params['max_drawdown']
            self.impose_drawdown(stressed_data, target_drawdown)
        
        if 'sentiment_volatility_multiplier' in scenario_params:
            # Increase sentiment volatility
            sentiment_vol_mult = scenario_params['sentiment_volatility_multiplier']
            sentiment_noise = np.random.normal(0, 0.1 * sentiment_vol_mult, len(stressed_data))
            stressed_data['sentiment_score'] += sentiment_noise
            stressed_data['sentiment_score'] = np.clip(stressed_data['sentiment_score'], -1, 1)
        
        return stressed_data
```

This comprehensive experimental design and validation framework ensures rigorous testing and validation of the Fear & Greed Sentiment Engine across multiple dimensions, providing confidence in its real-world performance and reliability.
