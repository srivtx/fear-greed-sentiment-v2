#!/usr/bin/env python3
"""
Advanced Signal Generation Engine for GoQuant Requirements
Implements sophisticated trading signals with risk management and correlation analysis
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass
from collections import defaultdict, deque
import logging
import json
import time
from statistics import correlation

# Financial analysis libraries
import yfinance as yf
from scipy import stats
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

@dataclass
class TradingSignal:
    """Enhanced trading signal with risk metrics"""
    symbol: str
    signal_type: str  # 'BUY', 'SELL', 'HOLD'
    confidence: float  # 0-1
    strength: float    # Signal strength 0-1
    sentiment_score: float
    price_target: Optional[float]
    stop_loss: Optional[float]
    position_size: float  # Recommended position size as % of portfolio
    risk_score: float     # Risk assessment 0-1
    time_horizon: str     # 'SHORT', 'MEDIUM', 'LONG'
    reasoning: str
    correlation_factors: Dict[str, float]
    generated_at: datetime
    expires_at: datetime
    metadata: Dict

@dataclass
class MarketRegime:
    """Market regime classification"""
    regime_type: str  # 'BULL', 'BEAR', 'SIDEWAYS', 'VOLATILE'
    confidence: float
    duration_days: int
    volatility_level: str  # 'LOW', 'MEDIUM', 'HIGH', 'EXTREME'
    fear_greed_zone: str   # 'EXTREME_FEAR', 'FEAR', 'NEUTRAL', 'GREED', 'EXTREME_GREED'

class AdvancedSignalGenerator:
    """
    Advanced signal generation engine for GoQuant requirements
    Features: Risk management, correlation analysis, multi-timeframe analysis
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Signal generation parameters
        self.sentiment_thresholds = {
            'strong_buy': 0.6,
            'buy': 0.3,
            'neutral': 0.1,
            'sell': -0.3,
            'strong_sell': -0.6
        }
        
        # Risk management parameters
        self.max_position_size = 0.1  # Maximum 10% position size
        self.base_position_size = 0.02  # Base 2% position size
        self.risk_free_rate = 0.02  # 2% annual risk-free rate
        
        # Correlation thresholds
        self.correlation_threshold = 0.3
        
        # Market regime detection
        self.regime_lookback_days = 30
        
        # Performance tracking
        self.signal_history = deque(maxlen=1000)
        self.performance_metrics = {
            'total_signals': 0,
            'generation_times': [],
            'accuracy_estimates': []
        }
        
        # Market data cache
        self.price_cache = {}
        self.cache_expiry = {}
        
        self.logger.info("AdvancedSignalGenerator initialized")
    
    def generate_signals(self, sentiment_data: Dict, market_data: Dict = None, 
                        historical_data: Dict = None) -> List[TradingSignal]:
        """
        Generate advanced trading signals with risk management
        
        Args:
            sentiment_data: Sentiment analysis results
            market_data: Current market data
            historical_data: Historical price data for correlation analysis
            
        Returns:
            List of enhanced trading signals
        """
        start_time = time.time()
        signals = []
        
        try:
            # Detect current market regime
            market_regime = self._detect_market_regime(market_data, historical_data)
            
            # Generate signals for each entity
            entity_sentiments = sentiment_data.get('entity_sentiment', {})
            
            for entity, sentiment_info in entity_sentiments.items():
                if isinstance(sentiment_info, dict):
                    signal = self._generate_entity_signal(
                        entity, sentiment_info, market_regime, 
                        market_data, historical_data
                    )
                    if signal:
                        signals.append(signal)
            
            # Generate portfolio-level signals
            portfolio_signals = self._generate_portfolio_signals(
                sentiment_data, market_regime, signals
            )
            signals.extend(portfolio_signals)
            
            # Filter and rank signals
            signals = self._filter_and_rank_signals(signals)
            
            # Track performance
            generation_time = (time.time() - start_time) * 1000
            self.performance_metrics['generation_times'].append(generation_time)
            self.performance_metrics['total_signals'] += len(signals)
            
            # Store in history
            for signal in signals:
                self.signal_history.append(signal)
            
            self.logger.info(f"Generated {len(signals)} trading signals in {generation_time:.2f}ms")
            
        except Exception as e:
            self.logger.error(f"Error generating signals: {e}")
        
        return signals
    
    def _detect_market_regime(self, market_data: Dict = None, 
                             historical_data: Dict = None) -> MarketRegime:
        """Detect current market regime using multiple indicators"""
        
        # Default regime if no data
        if not historical_data:
            return MarketRegime(
                regime_type='SIDEWAYS',
                confidence=0.5,
                duration_days=0,
                volatility_level='MEDIUM',
                fear_greed_zone='NEUTRAL'
            )
        
        try:
            # Analyze major market indices for regime detection
            market_indices = ['SPY', 'QQQ', 'DIA']
            regime_indicators = []
            
            for index in market_indices:
                if index in historical_data:
                    df = historical_data[index]
                    if len(df) >= self.regime_lookback_days:
                        indicators = self._calculate_regime_indicators(df)
                        regime_indicators.append(indicators)
            
            if not regime_indicators:
                # Fallback: use any available historical data
                for symbol, df in historical_data.items():
                    if len(df) >= self.regime_lookback_days:
                        indicators = self._calculate_regime_indicators(df)
                        regime_indicators.append(indicators)
                        break
            
            if regime_indicators:
                return self._aggregate_regime_indicators(regime_indicators)
            
        except Exception as e:
            self.logger.error(f"Error detecting market regime: {e}")
        
        # Default regime
        return MarketRegime(
            regime_type='SIDEWAYS',
            confidence=0.5,
            duration_days=0,
            volatility_level='MEDIUM',
            fear_greed_zone='NEUTRAL'
        )
    
    def _calculate_regime_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate regime indicators for a single asset"""
        
        indicators = {}
        
        # Ensure we have required columns
        if 'Close' not in df.columns:
            return indicators
        
        prices = df['Close'].values
        
        # Trend indicators
        if len(prices) >= 20:
            sma_20 = np.mean(prices[-20:])
            sma_50 = np.mean(prices[-50:]) if len(prices) >= 50 else sma_20
            current_price = prices[-1]
            
            indicators['trend_strength'] = (current_price - sma_50) / sma_50 if sma_50 > 0 else 0
            indicators['short_term_trend'] = (current_price - sma_20) / sma_20 if sma_20 > 0 else 0
        
        # Volatility indicators
        if len(prices) >= 20:
            returns = np.diff(prices) / prices[:-1]
            volatility = np.std(returns) * np.sqrt(252)  # Annualized volatility
            indicators['volatility'] = volatility
            
            # Rolling volatility for regime change detection
            recent_vol = np.std(returns[-10:]) * np.sqrt(252) if len(returns) >= 10 else volatility
            indicators['recent_volatility'] = recent_vol
            indicators['volatility_ratio'] = recent_vol / volatility if volatility > 0 else 1
        
        # Momentum indicators
        if len(prices) >= 14:
            # RSI-like momentum
            price_changes = np.diff(prices)
            gains = np.where(price_changes > 0, price_changes, 0)
            losses = np.where(price_changes < 0, -price_changes, 0)
            
            avg_gain = np.mean(gains[-14:])
            avg_loss = np.mean(losses[-14:])
            
            if avg_loss > 0:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
                indicators['momentum'] = (rsi - 50) / 50  # Normalize to -1 to 1
            else:
                indicators['momentum'] = 1.0
        
        # Market structure (higher highs, lower lows)
        if len(prices) >= 10:
            recent_high = np.max(prices[-10:])
            recent_low = np.min(prices[-10:])
            previous_high = np.max(prices[-20:-10]) if len(prices) >= 20 else recent_high
            previous_low = np.min(prices[-20:-10]) if len(prices) >= 20 else recent_low
            
            indicators['structure_bullish'] = (recent_high > previous_high) and (recent_low > previous_low)
            indicators['structure_bearish'] = (recent_high < previous_high) and (recent_low < previous_low)
        
        return indicators
    
    def _aggregate_regime_indicators(self, regime_indicators: List[Dict]) -> MarketRegime:
        """Aggregate regime indicators from multiple assets"""
        
        # Average indicators across assets
        avg_indicators = {}
        for key in ['trend_strength', 'volatility', 'momentum', 'volatility_ratio']:
            values = [ind.get(key, 0) for ind in regime_indicators if key in ind]
            if values:
                avg_indicators[key] = np.mean(values)
            else:
                avg_indicators[key] = 0
        
        # Count structural indicators
        bullish_count = sum(1 for ind in regime_indicators if ind.get('structure_bullish', False))
        bearish_count = sum(1 for ind in regime_indicators if ind.get('structure_bearish', False))
        total_count = len(regime_indicators)
        
        # Determine regime type
        trend_strength = avg_indicators.get('trend_strength', 0)
        momentum = avg_indicators.get('momentum', 0)
        
        if trend_strength > 0.1 and momentum > 0.2 and bullish_count > bearish_count:
            regime_type = 'BULL'
            confidence = min(0.9, abs(trend_strength) + abs(momentum))
        elif trend_strength < -0.1 and momentum < -0.2 and bearish_count > bullish_count:
            regime_type = 'BEAR'
            confidence = min(0.9, abs(trend_strength) + abs(momentum))
        elif avg_indicators.get('volatility_ratio', 1) > 1.5:
            regime_type = 'VOLATILE'
            confidence = min(0.8, avg_indicators.get('volatility_ratio', 1) - 1)
        else:
            regime_type = 'SIDEWAYS'
            confidence = 0.6
        
        # Determine volatility level
        volatility = avg_indicators.get('volatility', 0.2)
        if volatility > 0.4:
            volatility_level = 'EXTREME'
        elif volatility > 0.3:
            volatility_level = 'HIGH'
        elif volatility > 0.15:
            volatility_level = 'MEDIUM'
        else:
            volatility_level = 'LOW'
        
        # Determine fear/greed zone (simplified)
        if momentum > 0.4:
            fear_greed_zone = 'EXTREME_GREED'
        elif momentum > 0.2:
            fear_greed_zone = 'GREED'
        elif momentum < -0.4:
            fear_greed_zone = 'EXTREME_FEAR'
        elif momentum < -0.2:
            fear_greed_zone = 'FEAR'
        else:
            fear_greed_zone = 'NEUTRAL'
        
        return MarketRegime(
            regime_type=regime_type,
            confidence=confidence,
            duration_days=self.regime_lookback_days,
            volatility_level=volatility_level,
            fear_greed_zone=fear_greed_zone
        )
    
    def _generate_entity_signal(self, entity: str, sentiment_info: Dict, 
                               market_regime: MarketRegime, market_data: Dict = None,
                               historical_data: Dict = None) -> Optional[TradingSignal]:
        """Generate trading signal for a specific entity"""
        
        try:
            sentiment = sentiment_info.get('sentiment', 0)
            confidence = sentiment_info.get('confidence', 0)
            mention_count = sentiment_info.get('mention_count', 0)
            
            # Skip if insufficient data
            if confidence < 0.3 or mention_count < 2:
                return None
            
            # Base signal determination
            signal_type = self._determine_base_signal(sentiment)
            
            if signal_type == 'HOLD':
                return None
            
            # Calculate signal strength
            strength = self._calculate_signal_strength(
                sentiment, confidence, mention_count, market_regime
            )
            
            # Risk assessment
            risk_score = self._calculate_risk_score(
                entity, sentiment, market_regime, historical_data
            )
            
            # Position sizing
            position_size = self._calculate_position_size(
                strength, risk_score, market_regime
            )
            
            # Price targets and stop losses
            price_target, stop_loss = self._calculate_price_levels(
                entity, signal_type, strength, market_data, historical_data
            )
            
            # Time horizon
            time_horizon = self._determine_time_horizon(
                strength, market_regime, sentiment_info
            )
            
            # Correlation factors
            correlation_factors = self._calculate_correlation_factors(
                entity, historical_data
            )
            
            # Reasoning
            reasoning = self._generate_reasoning(
                entity, signal_type, sentiment, strength, market_regime
            )
            
            # Signal expiration
            expires_at = self._calculate_expiration(time_horizon)
            
            signal = TradingSignal(
                symbol=entity,
                signal_type=signal_type,
                confidence=confidence,
                strength=strength,
                sentiment_score=sentiment,
                price_target=price_target,
                stop_loss=stop_loss,
                position_size=position_size,
                risk_score=risk_score,
                time_horizon=time_horizon,
                reasoning=reasoning,
                correlation_factors=correlation_factors,
                generated_at=datetime.now(),
                expires_at=expires_at,
                metadata={
                    'market_regime': market_regime.regime_type,
                    'volatility_level': market_regime.volatility_level,
                    'mention_count': mention_count,
                    'sentiment_trend': sentiment_info.get('trend', 0)
                }
            )
            
            return signal
            
        except Exception as e:
            self.logger.error(f"Error generating signal for {entity}: {e}")
            return None
    
    def _determine_base_signal(self, sentiment: float) -> str:
        """Determine base signal type from sentiment"""
        if sentiment >= self.sentiment_thresholds['strong_buy']:
            return 'STRONG_BUY'
        elif sentiment >= self.sentiment_thresholds['buy']:
            return 'BUY'
        elif sentiment <= self.sentiment_thresholds['strong_sell']:
            return 'STRONG_SELL'
        elif sentiment <= self.sentiment_thresholds['sell']:
            return 'SELL'
        else:
            return 'HOLD'
    
    def _calculate_signal_strength(self, sentiment: float, confidence: float, 
                                  mention_count: int, market_regime: MarketRegime) -> float:
        """Calculate signal strength considering multiple factors"""
        
        # Base strength from sentiment and confidence
        base_strength = abs(sentiment) * confidence
        
        # Mention count factor (more mentions = higher strength, but with diminishing returns)
        mention_factor = min(1.0, np.log(mention_count + 1) / 3)
        
        # Market regime adjustment
        regime_factor = 1.0
        if market_regime.regime_type == 'BULL' and sentiment > 0:
            regime_factor = 1.2  # Boost buy signals in bull market
        elif market_regime.regime_type == 'BEAR' and sentiment < 0:
            regime_factor = 1.2  # Boost sell signals in bear market
        elif market_regime.regime_type == 'VOLATILE':
            regime_factor = 0.8  # Reduce strength in volatile markets
        
        # Combine factors
        strength = base_strength * mention_factor * regime_factor
        
        return min(1.0, strength)
    
    def _calculate_risk_score(self, entity: str, sentiment: float, 
                             market_regime: MarketRegime, historical_data: Dict = None) -> float:
        """Calculate risk score for the signal"""
        
        base_risk = 0.5  # Base risk level
        
        # Market regime risk adjustment
        regime_risk = {
            'BULL': 0.3,
            'BEAR': 0.4,
            'SIDEWAYS': 0.5,
            'VOLATILE': 0.8
        }.get(market_regime.regime_type, 0.5)
        
        # Volatility risk
        volatility_risk = {
            'LOW': 0.2,
            'MEDIUM': 0.4,
            'HIGH': 0.6,
            'EXTREME': 0.9
        }.get(market_regime.volatility_level, 0.4)
        
        # Sentiment extremity risk (extreme sentiment can be risky)
        sentiment_risk = abs(sentiment) * 0.3
        
        # Historical volatility risk
        historical_risk = 0.5
        if historical_data and entity in historical_data:
            try:
                df = historical_data[entity]
                if 'Close' in df.columns and len(df) >= 20:
                    returns = df['Close'].pct_change().dropna()
                    if len(returns) > 0:
                        volatility = returns.std() * np.sqrt(252)  # Annualized
                        historical_risk = min(1.0, volatility)
            except:
                pass
        
        # Combine risk factors
        risk_score = (regime_risk * 0.3 + volatility_risk * 0.3 + 
                     sentiment_risk * 0.2 + historical_risk * 0.2)
        
        return min(1.0, max(0.1, risk_score))
    
    def _calculate_position_size(self, strength: float, risk_score: float, 
                                market_regime: MarketRegime) -> float:
        """Calculate recommended position size"""
        
        # Base position size adjusted by strength
        base_size = self.base_position_size * strength
        
        # Risk adjustment (higher risk = smaller position)
        risk_adjusted_size = base_size * (1 - risk_score * 0.5)
        
        # Market regime adjustment
        regime_factor = {
            'BULL': 1.2,
            'BEAR': 1.0,
            'SIDEWAYS': 0.8,
            'VOLATILE': 0.6
        }.get(market_regime.regime_type, 1.0)
        
        final_size = risk_adjusted_size * regime_factor
        
        # Ensure within limits
        return min(self.max_position_size, max(0.005, final_size))  # Min 0.5%, max 10%
    
    def _calculate_price_levels(self, entity: str, signal_type: str, strength: float,
                               market_data: Dict = None, historical_data: Dict = None) -> Tuple[Optional[float], Optional[float]]:
        """Calculate price target and stop loss levels"""
        
        price_target = None
        stop_loss = None
        
        try:
            # Get current price
            current_price = None
            if market_data and entity in market_data:
                df = market_data[entity]
                if not df.empty and 'Close' in df.columns:
                    current_price = df['Close'].iloc[-1]
            
            if current_price is None:
                return None, None
            
            # Calculate volatility for price level calculation
            volatility = 0.2  # Default 20% annual volatility
            if historical_data and entity in historical_data:
                df = historical_data[entity]
                if 'Close' in df.columns and len(df) >= 20:
                    returns = df['Close'].pct_change().dropna()
                    if len(returns) > 0:
                        volatility = returns.std() * np.sqrt(252)
            
            # Calculate price levels based on signal type and strength
            if signal_type in ['BUY', 'STRONG_BUY']:
                # Target: current price + (strength * volatility * time factor)
                target_return = strength * volatility * 0.5  # 50% of annual volatility
                price_target = current_price * (1 + target_return)
                
                # Stop loss: current price - (risk-adjusted volatility)
                stop_loss_return = (1 - strength * 0.5) * volatility * 0.25
                stop_loss = current_price * (1 - stop_loss_return)
                
            elif signal_type in ['SELL', 'STRONG_SELL']:
                # Target: current price - (strength * volatility * time factor)
                target_return = strength * volatility * 0.5
                price_target = current_price * (1 - target_return)
                
                # Stop loss: current price + (risk-adjusted volatility)
                stop_loss_return = (1 - strength * 0.5) * volatility * 0.25
                stop_loss = current_price * (1 + stop_loss_return)
        
        except Exception as e:
            self.logger.error(f"Error calculating price levels for {entity}: {e}")
        
        return price_target, stop_loss
    
    def _determine_time_horizon(self, strength: float, market_regime: MarketRegime, 
                               sentiment_info: Dict) -> str:
        """Determine appropriate time horizon for the signal"""
        
        # Base time horizon from strength
        if strength > 0.8:
            base_horizon = 'LONG'  # High conviction = longer hold
        elif strength > 0.5:
            base_horizon = 'MEDIUM'
        else:
            base_horizon = 'SHORT'
        
        # Market regime adjustment
        if market_regime.regime_type == 'VOLATILE':
            # Volatile markets favor shorter time horizons
            if base_horizon == 'LONG':
                return 'MEDIUM'
            elif base_horizon == 'MEDIUM':
                return 'SHORT'
        
        return base_horizon
    
    def _calculate_correlation_factors(self, entity: str, historical_data: Dict = None) -> Dict[str, float]:
        """Calculate correlation factors with other assets"""
        
        correlations = {}
        
        if not historical_data or entity not in historical_data:
            return correlations
        
        try:
            entity_data = historical_data[entity]
            if 'Close' not in entity_data.columns:
                return correlations
            
            entity_returns = entity_data['Close'].pct_change().dropna()
            
            # Calculate correlations with other major assets
            major_assets = ['SPY', 'QQQ', 'BTC-USD', 'ETH-USD']
            
            for asset in major_assets:
                if asset != entity and asset in historical_data:
                    asset_data = historical_data[asset]
                    if 'Close' in asset_data.columns:
                        asset_returns = asset_data['Close'].pct_change().dropna()
                        
                        # Align data (common dates)
                        common_index = entity_returns.index.intersection(asset_returns.index)
                        if len(common_index) >= 20:  # Minimum data points
                            entity_aligned = entity_returns.loc[common_index]
                            asset_aligned = asset_returns.loc[common_index]
                            
                            corr, p_value = pearsonr(entity_aligned, asset_aligned)
                            if not np.isnan(corr) and p_value < 0.05:  # Significant correlation
                                correlations[asset] = corr
        
        except Exception as e:
            self.logger.error(f"Error calculating correlations for {entity}: {e}")
        
        return correlations
    
    def _generate_reasoning(self, entity: str, signal_type: str, sentiment: float, 
                           strength: float, market_regime: MarketRegime) -> str:
        """Generate human-readable reasoning for the signal"""
        
        reasoning_parts = []
        
        # Sentiment reasoning
        if abs(sentiment) > 0.6:
            sentiment_desc = "very positive" if sentiment > 0 else "very negative"
        elif abs(sentiment) > 0.3:
            sentiment_desc = "positive" if sentiment > 0 else "negative"
        else:
            sentiment_desc = "neutral"
        
        reasoning_parts.append(f"{sentiment_desc} sentiment ({sentiment:.2f})")
        
        # Strength reasoning
        if strength > 0.7:
            reasoning_parts.append("high conviction signal")
        elif strength > 0.4:
            reasoning_parts.append("moderate conviction signal")
        else:
            reasoning_parts.append("low conviction signal")
        
        # Market regime reasoning
        regime_desc = {
            'BULL': "supportive bull market conditions",
            'BEAR': "challenging bear market conditions", 
            'SIDEWAYS': "neutral sideways market conditions",
            'VOLATILE': "volatile market conditions requiring caution"
        }.get(market_regime.regime_type, "uncertain market conditions")
        
        reasoning_parts.append(regime_desc)
        
        # Combine reasoning
        reasoning = f"{signal_type} signal for {entity} based on {', '.join(reasoning_parts)}"
        
        return reasoning
    
    def _calculate_expiration(self, time_horizon: str) -> datetime:
        """Calculate when the signal expires"""
        now = datetime.now()
        
        if time_horizon == 'SHORT':
            return now + timedelta(days=1)
        elif time_horizon == 'MEDIUM':
            return now + timedelta(days=7)
        else:  # LONG
            return now + timedelta(days=30)
    
    def _generate_portfolio_signals(self, sentiment_data: Dict, market_regime: MarketRegime, 
                                   entity_signals: List[TradingSignal]) -> List[TradingSignal]:
        """Generate portfolio-level signals"""
        
        portfolio_signals = []
        
        try:
            # Market-wide sentiment signal
            overall_sentiment = sentiment_data.get('overall_sentiment', 0)
            confidence = sentiment_data.get('confidence', 0)
            
            if confidence > 0.5 and abs(overall_sentiment) > 0.3:
                signal_type = 'BUY' if overall_sentiment > 0 else 'SELL'
                
                market_signal = TradingSignal(
                    symbol='MARKET',
                    signal_type=signal_type,
                    confidence=confidence,
                    strength=abs(overall_sentiment),
                    sentiment_score=overall_sentiment,
                    price_target=None,
                    stop_loss=None,
                    position_size=0.05,  # 5% portfolio allocation
                    risk_score=0.4,
                    time_horizon='MEDIUM',
                    reasoning=f"Market-wide {signal_type.lower()} signal based on overall sentiment {overall_sentiment:.2f}",
                    correlation_factors={},
                    generated_at=datetime.now(),
                    expires_at=datetime.now() + timedelta(days=7),
                    metadata={
                        'signal_type': 'PORTFOLIO',
                        'market_regime': market_regime.regime_type
                    }
                )
                
                portfolio_signals.append(market_signal)
        
        except Exception as e:
            self.logger.error(f"Error generating portfolio signals: {e}")
        
        return portfolio_signals
    
    def _filter_and_rank_signals(self, signals: List[TradingSignal]) -> List[TradingSignal]:
        """Filter and rank signals by quality"""
        
        # Filter out low-quality signals
        filtered_signals = [
            signal for signal in signals
            if signal.confidence > 0.4 and signal.strength > 0.3
        ]
        
        # Rank by composite score
        def signal_score(signal):
            return signal.confidence * signal.strength * (1 - signal.risk_score)
        
        filtered_signals.sort(key=signal_score, reverse=True)
        
        # Limit to top signals to avoid over-trading
        return filtered_signals[:20]
    
    def get_performance_metrics(self) -> Dict:
        """Get signal generator performance metrics"""
        
        metrics = {
            'total_signals_generated': self.performance_metrics['total_signals'],
            'signals_in_history': len(self.signal_history),
        }
        
        if self.performance_metrics['generation_times']:
            times = self.performance_metrics['generation_times']
            metrics.update({
                'avg_generation_time_ms': np.mean(times),
                'p95_generation_time_ms': np.percentile(times, 95),
                'max_generation_time_ms': max(times),
                'min_generation_time_ms': min(times)
            })
        
        return metrics

# Example usage
if __name__ == "__main__":
    # Test the signal generator
    generator = AdvancedSignalGenerator()
    
    # Mock sentiment data
    sentiment_data = {
        'overall_sentiment': 0.4,
        'confidence': 0.7,
        'entity_sentiment': {
            'BTC': {'sentiment': 0.6, 'confidence': 0.8, 'mention_count': 15, 'trend': 0.1},
            'AAPL': {'sentiment': 0.3, 'confidence': 0.6, 'mention_count': 8, 'trend': -0.05},
            'ETH': {'sentiment': -0.4, 'confidence': 0.7, 'mention_count': 12, 'trend': -0.2}
        }
    }
    
    print("Testing Advanced Signal Generator")
    print("=" * 50)
    
    signals = generator.generate_signals(sentiment_data)
    
    print(f"Generated {len(signals)} signals:")
    for signal in signals:
        print(f"\n{signal.symbol}: {signal.signal_type}")
        print(f"  Confidence: {signal.confidence:.2f}, Strength: {signal.strength:.2f}")
        print(f"  Position Size: {signal.position_size:.1%}, Risk: {signal.risk_score:.2f}")
        print(f"  Time Horizon: {signal.time_horizon}")
        print(f"  Reasoning: {signal.reasoning}")
    
    print(f"\nPerformance metrics:")
    metrics = generator.get_performance_metrics()
    for key, value in metrics.items():
        print(f"  {key}: {value}")
