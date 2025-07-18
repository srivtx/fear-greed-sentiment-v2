# Chapter 15: Building New Features - Extending Your System 🚀

## Welcome to Advanced Development!

Your sentiment analysis system is powerful, but the beauty of coding is that you can always make it better! This chapter shows you how to add new features, integrate additional data sources, and create custom analysis tools.

## 🎯 Adding Custom Sentiment Indicators

### Building Your Own Technical Sentiment Indicators

```python
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from collections import deque

class CustomSentimentIndicators:
    """Build custom sentiment indicators for advanced analysis"""
    
    def __init__(self, window_size: int = 20):
        self.window_size = window_size
        self.sentiment_history = deque(maxlen=1000)  # Store last 1000 data points
        
    def sentiment_rsi(self, sentiment_scores: List[float], period: int = 14) -> float:
        """
        Calculate Relative Strength Index for sentiment
        
        Think of this like RSI for stock prices, but for sentiment:
        - Above 70: Sentiment is "overbought" (too positive)
        - Below 30: Sentiment is "oversold" (too negative)
        - 50: Neutral sentiment momentum
        """
        
        if len(sentiment_scores) < period + 1:
            return 50  # Neutral if not enough data
        
        # Calculate sentiment changes (like price changes)
        sentiment_changes = np.diff(sentiment_scores)
        
        # Separate gains and losses
        gains = np.where(sentiment_changes > 0, sentiment_changes, 0)
        losses = np.where(sentiment_changes < 0, -sentiment_changes, 0)
        
        # Calculate average gain and loss
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        # Calculate RS and RSI
        if avg_loss == 0:
            return 100  # All gains, maximum RSI
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def sentiment_macd(self, sentiment_scores: List[float], 
                      fast_period: int = 12, slow_period: int = 26, 
                      signal_period: int = 9) -> Dict[str, float]:
        """
        Moving Average Convergence Divergence for sentiment
        
        This shows:
        - MACD Line: Difference between fast and slow moving averages
        - Signal Line: Smoothed MACD
        - Histogram: MACD - Signal (momentum)
        """
        
        if len(sentiment_scores) < slow_period:
            return {'macd': 0, 'signal': 0, 'histogram': 0}
        
        scores = np.array(sentiment_scores)
        
        # Calculate exponential moving averages
        fast_ema = self._exponential_moving_average(scores, fast_period)
        slow_ema = self._exponential_moving_average(scores, slow_period)
        
        # MACD line
        macd = fast_ema - slow_ema
        
        # Signal line (EMA of MACD)
        if len(sentiment_scores) >= slow_period + signal_period - 1:
            # We need enough data for signal calculation
            macd_values = []
            for i in range(slow_period - 1, len(scores)):
                fast_val = self._exponential_moving_average(scores[:i+1], fast_period)
                slow_val = self._exponential_moving_average(scores[:i+1], slow_period)
                macd_values.append(fast_val - slow_val)
            
            signal = self._exponential_moving_average(np.array(macd_values), signal_period)
        else:
            signal = 0
        
        # Histogram (momentum)
        histogram = macd - signal
        
        return {
            'macd': macd,
            'signal': signal,
            'histogram': histogram,
            'interpretation': self._interpret_macd(macd, signal, histogram)
        }
    
    def sentiment_bollinger_bands(self, sentiment_scores: List[float], 
                                 period: int = 20, std_dev: float = 2) -> Dict[str, float]:
        """
        Bollinger Bands for sentiment analysis
        
        Shows:
        - Upper Band: High sentiment boundary
        - Lower Band: Low sentiment boundary  
        - Middle Band: Average sentiment
        - Position: Where current sentiment sits
        """
        
        if len(sentiment_scores) < period:
            current_sentiment = sentiment_scores[-1] if sentiment_scores else 0
            return {
                'upper_band': current_sentiment + 0.2,
                'middle_band': current_sentiment,
                'lower_band': current_sentiment - 0.2,
                'position': 50,  # Neutral position
                'squeeze': False
            }
        
        scores = np.array(sentiment_scores[-period:])
        
        # Calculate bands
        middle_band = np.mean(scores)
        std = np.std(scores)
        upper_band = middle_band + (std_dev * std)
        lower_band = middle_band - (std_dev * std)
        
        # Current position (0-100)
        current_sentiment = sentiment_scores[-1]
        if upper_band != lower_band:
            position = ((current_sentiment - lower_band) / (upper_band - lower_band)) * 100
        else:
            position = 50
        
        # Check for squeeze (low volatility)
        squeeze = std < 0.1  # Threshold for low volatility
        
        return {
            'upper_band': upper_band,
            'middle_band': middle_band,
            'lower_band': lower_band,
            'position': max(0, min(100, position)),
            'squeeze': squeeze,
            'interpretation': self._interpret_bollinger_bands(position, squeeze)
        }
    
    def sentiment_momentum_oscillator(self, sentiment_scores: List[float], 
                                    short_period: int = 10, long_period: int = 30) -> Dict[str, float]:
        """
        Custom momentum oscillator for sentiment
        
        Measures the speed and direction of sentiment changes
        """
        
        if len(sentiment_scores) < long_period:
            return {'momentum': 0, 'strength': 'neutral', 'trend': 'sideways'}
        
        scores = np.array(sentiment_scores)
        
        # Short-term momentum
        short_momentum = scores[-1] - scores[-short_period]
        
        # Long-term momentum
        long_momentum = scores[-1] - scores[-long_period]
        
        # Combined momentum (weighted)
        combined_momentum = (short_momentum * 0.7) + (long_momentum * 0.3)
        
        # Momentum strength
        momentum_strength = abs(combined_momentum)
        
        if momentum_strength > 0.3:
            strength = 'very_strong'
        elif momentum_strength > 0.2:
            strength = 'strong'
        elif momentum_strength > 0.1:
            strength = 'moderate'
        else:
            strength = 'weak'
        
        # Trend direction
        if combined_momentum > 0.05:
            trend = 'bullish'
        elif combined_momentum < -0.05:
            trend = 'bearish'
        else:
            trend = 'sideways'
        
        return {
            'momentum': combined_momentum,
            'short_momentum': short_momentum,
            'long_momentum': long_momentum,
            'strength': strength,
            'trend': trend
        }
    
    def sentiment_volatility_index(self, sentiment_scores: List[float], 
                                 period: int = 20) -> Dict[str, float]:
        """
        Calculate sentiment volatility (like VIX for stocks)
        """
        
        if len(sentiment_scores) < period:
            return {'volatility': 0, 'level': 'low', 'percentile': 50}
        
        scores = np.array(sentiment_scores[-period:])
        
        # Calculate rolling standard deviation
        volatility = np.std(scores)
        
        # Historical volatility percentile (if we have enough history)
        if len(self.sentiment_history) > period * 2:
            historical_vols = []
            history_array = np.array(list(self.sentiment_history))
            
            for i in range(period, len(history_array)):
                window_vol = np.std(history_array[i-period:i])
                historical_vols.append(window_vol)
            
            if historical_vols:
                percentile = (sum(1 for v in historical_vols if v <= volatility) / 
                            len(historical_vols)) * 100
            else:
                percentile = 50
        else:
            percentile = 50
        
        # Volatility level
        if volatility > 0.4:
            level = 'very_high'
        elif volatility > 0.3:
            level = 'high'
        elif volatility > 0.2:
            level = 'moderate'
        elif volatility > 0.1:
            level = 'low'
        else:
            level = 'very_low'
        
        return {
            'volatility': volatility,
            'level': level,
            'percentile': percentile
        }
    
    def _exponential_moving_average(self, data: np.array, period: int) -> float:
        """Calculate exponential moving average"""
        
        if len(data) < period:
            return np.mean(data)
        
        multiplier = 2 / (period + 1)
        ema = data[0]  # Start with first value
        
        for value in data[1:]:
            ema = (value * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    def _interpret_macd(self, macd: float, signal: float, histogram: float) -> str:
        """Interpret MACD signals"""
        
        if macd > signal and histogram > 0:
            return "bullish_momentum"
        elif macd < signal and histogram < 0:
            return "bearish_momentum"
        elif histogram > 0 and histogram > abs(histogram) * 0.1:  # Growing histogram
            return "building_bullish"
        elif histogram < 0 and abs(histogram) > abs(histogram) * 0.1:  # Growing negative
            return "building_bearish"
        else:
            return "neutral"
    
    def _interpret_bollinger_bands(self, position: float, squeeze: bool) -> str:
        """Interpret Bollinger Band signals"""
        
        if squeeze:
            return "low_volatility_breakout_expected"
        elif position > 80:
            return "overbought_potential_reversal"
        elif position < 20:
            return "oversold_potential_reversal"
        elif 40 <= position <= 60:
            return "neutral_range"
        else:
            return "trending"
```

## 🌐 Integrating New Social Media Platforms

### Adding TikTok Data Collection

```python
import requests
import time
from typing import Dict, List

class TikTokCollector:
    """Collect sentiment data from TikTok (educational example)"""
    
    def __init__(self, config: Dict):
        self.config = config
        # Note: TikTok doesn't have a public API for content
        # This is a conceptual example of how you might structure it
        
    def collect_tiktok_sentiment(self, keywords: List[str], 
                               max_videos: int = 100) -> List[Dict]:
        """
        Conceptual TikTok sentiment collection
        
        In reality, you'd need:
        1. TikTok Research API access (limited availability)
        2. Web scraping tools (with legal considerations)
        3. Third-party data providers
        """
        
        # This is a placeholder showing the structure
        mock_tiktok_data = []
        
        for keyword in keywords:
            # In real implementation, you'd make API calls or scrape
            videos = self._simulate_tiktok_search(keyword, max_videos // len(keywords))
            
            for video in videos:
                sentiment_data = {
                    'platform': 'tiktok',
                    'keyword': keyword,
                    'video_id': video['id'],
                    'text': video['description'],
                    'hashtags': video['hashtags'],
                    'likes': video['likes'],
                    'comments': video['comments'],
                    'shares': video['shares'],
                    'views': video['views'],
                    'timestamp': video['timestamp'],
                    'author': video['author'],
                    'verified': video.get('verified', False)
                }
                
                mock_tiktok_data.append(sentiment_data)
        
        return mock_tiktok_data
    
    def _simulate_tiktok_search(self, keyword: str, count: int) -> List[Dict]:
        """Simulate TikTok search results for example"""
        
        import random
        from datetime import datetime, timedelta
        
        videos = []
        
        for i in range(count):
            video = {
                'id': f"tiktok_{keyword}_{i}",
                'description': f"Great video about {keyword}! #investing #finance",
                'hashtags': ['investing', 'finance', keyword.lower()],
                'likes': random.randint(10, 10000),
                'comments': random.randint(5, 1000),
                'shares': random.randint(1, 500),
                'views': random.randint(100, 100000),
                'timestamp': datetime.now() - timedelta(hours=random.randint(1, 168)),
                'author': f"user_{random.randint(1000, 9999)}",
                'verified': random.choice([True, False])
            }
            videos.append(video)
        
        return videos
```

### Adding YouTube Comments Analysis

```python
import googleapiclient.discovery
import googleapiclient.errors

class YouTubeCollector:
    """Collect sentiment from YouTube comments"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=api_key
        )
        
    def collect_video_comments(self, video_id: str, max_comments: int = 100) -> List[Dict]:
        """Collect comments from a specific YouTube video"""
        
        comments = []
        next_page_token = None
        
        while len(comments) < max_comments:
            try:
                # Request comment threads
                request = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=min(100, max_comments - len(comments)),
                    pageToken=next_page_token,
                    order="relevance"  # Get most relevant comments first
                )
                
                response = request.execute()
                
                for item in response['items']:
                    comment_data = item['snippet']['topLevelComment']['snippet']
                    
                    comment = {
                        'platform': 'youtube',
                        'video_id': video_id,
                        'comment_id': item['id'],
                        'text': comment_data['textDisplay'],
                        'author': comment_data['authorDisplayName'],
                        'likes': comment_data.get('likeCount', 0),
                        'timestamp': comment_data['publishedAt'],
                        'updated': comment_data.get('updatedAt', comment_data['publishedAt']),
                        'reply_count': item['snippet'].get('totalReplyCount', 0)
                    }
                    
                    comments.append(comment)
                
                # Check if there are more pages
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                    
            except googleapiclient.errors.HttpError as e:
                print(f"An error occurred: {e}")
                break
        
        return comments
    
    def search_finance_videos(self, query: str, max_results: int = 50) -> List[Dict]:
        """Search for finance-related videos"""
        
        try:
            request = self.youtube.search().list(
                part="snippet",
                q=query,
                type="video",
                maxResults=max_results,
                order="relevance",
                publishedAfter=(datetime.now() - timedelta(days=7)).isoformat() + "Z",
                regionCode="US"
            )
            
            response = request.execute()
            
            videos = []
            for item in response['items']:
                video = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'channel': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt'],
                    'thumbnail': item['snippet']['thumbnails']['default']['url']
                }
                videos.append(video)
            
            return videos
            
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
            return []
```

## 🤖 Building Predictive Models

### Machine Learning Sentiment Predictor

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib

class SentimentPredictor:
    """Machine learning model to predict future sentiment"""
    
    def __init__(self, model_type: str = 'random_forest'):
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        
    def create_features(self, historical_data: pd.DataFrame) -> pd.DataFrame:
        """Create features for machine learning from historical sentiment data"""
        
        features = pd.DataFrame()
        
        # Time-based features
        features['hour'] = historical_data.index.hour
        features['day_of_week'] = historical_data.index.dayofweek
        features['is_weekend'] = (historical_data.index.dayofweek >= 5).astype(int)
        features['is_market_hours'] = ((historical_data.index.hour >= 9) & 
                                     (historical_data.index.hour <= 16)).astype(int)
        
        # Sentiment lag features (previous sentiment values)
        for lag in [1, 2, 3, 6, 12, 24]:  # 1 hour to 1 day lags
            features[f'sentiment_lag_{lag}'] = historical_data['sentiment_score'].shift(lag)
        
        # Moving averages
        for window in [3, 6, 12, 24]:
            features[f'sentiment_ma_{window}'] = (
                historical_data['sentiment_score'].rolling(window=window).mean()
            )
        
        # Volatility features
        for window in [6, 12, 24]:
            features[f'sentiment_vol_{window}'] = (
                historical_data['sentiment_score'].rolling(window=window).std()
            )
        
        # Momentum features
        features['momentum_3h'] = (historical_data['sentiment_score'] - 
                                 historical_data['sentiment_score'].shift(3))
        features['momentum_6h'] = (historical_data['sentiment_score'] - 
                                 historical_data['sentiment_score'].shift(6))
        features['momentum_24h'] = (historical_data['sentiment_score'] - 
                                  historical_data['sentiment_score'].shift(24))
        
        # Volume features (if available)
        if 'post_volume' in historical_data.columns:
            features['post_volume'] = historical_data['post_volume']
            features['volume_ma_6h'] = historical_data['post_volume'].rolling(window=6).mean()
            features['volume_spike'] = (
                historical_data['post_volume'] > 
                historical_data['post_volume'].rolling(window=24).mean() * 2
            ).astype(int)
        
        # Market correlation features (if market data available)
        if 'market_correlation' in historical_data.columns:
            features['market_correlation'] = historical_data['market_correlation']
            features['correlation_change'] = (
                historical_data['market_correlation'] - 
                historical_data['market_correlation'].shift(6)
            )
        
        # Technical indicators from our custom indicators
        sentiment_scores = historical_data['sentiment_score'].values
        
        # Add RSI
        if len(sentiment_scores) >= 14:
            rsi_values = []
            for i in range(len(sentiment_scores)):
                if i >= 13:  # Need 14 points for RSI
                    rsi = self._calculate_rsi(sentiment_scores[max(0, i-13):i+1])
                    rsi_values.append(rsi)
                else:
                    rsi_values.append(50)  # Neutral
            features['sentiment_rsi'] = rsi_values
        
        # Target variable (what we want to predict)
        # Predict sentiment 1 hour in the future
        features['target'] = historical_data['sentiment_score'].shift(-1)
        
        # Drop rows with NaN values
        features = features.dropna()
        
        self.feature_names = [col for col in features.columns if col != 'target']
        
        return features
    
    def train_model(self, historical_data: pd.DataFrame, test_size: float = 0.2):
        """Train the prediction model"""
        
        # Create features
        feature_df = self.create_features(historical_data)
        
        if len(feature_df) < 50:  # Need minimum data
            raise ValueError("Not enough historical data for training (need at least 50 points)")
        
        # Separate features and target
        X = feature_df[self.feature_names]
        y = feature_df['target']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, shuffle=False  # Don't shuffle time series
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Create and train model
        if self.model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            )
        elif self.model_type == 'gradient_boosting':
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=6,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        # Train the model
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        train_predictions = self.model.predict(X_train_scaled)
        test_predictions = self.model.predict(X_test_scaled)
        
        train_r2 = r2_score(y_train, train_predictions)
        test_r2 = r2_score(y_test, test_predictions)
        
        train_mse = mean_squared_error(y_train, train_predictions)
        test_mse = mean_squared_error(y_test, test_predictions)
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5, scoring='r2')
        
        self.is_trained = True
        
        return {
            'train_r2': train_r2,
            'test_r2': test_r2,
            'train_mse': train_mse,
            'test_mse': test_mse,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'feature_importance': dict(zip(self.feature_names, self.model.feature_importances_))
        }
    
    def predict_sentiment(self, current_data: pd.DataFrame, hours_ahead: int = 1) -> Dict:
        """Predict future sentiment"""
        
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        predictions = []
        confidence_intervals = []
        
        # Create features for current data
        feature_df = self.create_features(current_data)
        
        if len(feature_df) == 0:
            raise ValueError("Not enough current data to make predictions")
        
        # Get the latest features
        latest_features = feature_df[self.feature_names].iloc[-1:].values
        latest_features_scaled = self.scaler.transform(latest_features)
        
        # Make prediction
        for hour in range(1, hours_ahead + 1):
            prediction = self.model.predict(latest_features_scaled)[0]
            predictions.append(prediction)
            
            # For multi-step predictions, we'd need to update features
            # This is a simplified version
        
        # Calculate confidence (using ensemble predictions if Random Forest)
        if hasattr(self.model, 'estimators_'):
            # For Random Forest, get predictions from all trees
            tree_predictions = np.array([
                tree.predict(latest_features_scaled)[0] 
                for tree in self.model.estimators_
            ])
            
            confidence = 1 - (np.std(tree_predictions) / (np.abs(np.mean(tree_predictions)) + 1e-8))
            prediction_std = np.std(tree_predictions)
            
            # Confidence interval (approximate)
            confidence_intervals = [
                predictions[0] - 1.96 * prediction_std,
                predictions[0] + 1.96 * prediction_std
            ]
        else:
            confidence = 0.7  # Default confidence for other models
            confidence_intervals = [predictions[0] - 0.1, predictions[0] + 0.1]
        
        return {
            'predictions': predictions,
            'confidence': confidence,
            'confidence_interval': confidence_intervals,
            'model_type': self.model_type,
            'prediction_horizon': f"{hours_ahead} hours"
        }
    
    def save_model(self, filepath: str):
        """Save the trained model"""
        
        if not self.is_trained:
            raise ValueError("No trained model to save")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'model_type': self.model_type
        }
        
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath: str):
        """Load a saved model"""
        
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.model_type = model_data['model_type']
        self.is_trained = True
    
    def _calculate_rsi(self, prices: np.array, period: int = 14) -> float:
        """Calculate RSI for feature engineering"""
        
        if len(prices) < period + 1:
            return 50
        
        changes = np.diff(prices)
        gains = np.where(changes > 0, changes, 0)
        losses = np.where(changes < 0, -changes, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
```

## 📊 Creating Custom Visualizations

### Advanced Sentiment Dashboard

```python
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st

class AdvancedSentimentDashboard:
    """Create advanced visualizations for sentiment analysis"""
    
    def __init__(self):
        self.color_scheme = {
            'bullish': '#00C851',
            'bearish': '#FF4444', 
            'neutral': '#FFA726',
            'background': '#1E1E1E',
            'text': '#FFFFFF'
        }
    
    def create_sentiment_heatmap(self, entity_sentiments: Dict[str, Dict], 
                               timeframe: str = '24h') -> go.Figure:
        """Create a heatmap of sentiment across entities and time"""
        
        # This would normally use real time-series data
        # For demo, we'll create a sample heatmap
        
        entities = list(entity_sentiments.keys())
        hours = list(range(24))  # 24 hour heatmap
        
        # Create sentiment matrix (entities x hours)
        sentiment_matrix = []
        
        for entity in entities:
            hourly_sentiments = []
            base_sentiment = entity_sentiments[entity].get('overall_score', 0)
            
            for hour in hours:
                # Add some realistic variation
                variation = np.random.normal(0, 0.1)
                sentiment = np.clip(base_sentiment + variation, -1, 1)
                hourly_sentiments.append(sentiment)
            
            sentiment_matrix.append(hourly_sentiments)
        
        fig = go.Figure(data=go.Heatmap(
            z=sentiment_matrix,
            x=[f"{h:02d}:00" for h in hours],
            y=entities,
            colorscale='RdYlGn',
            zmid=0,
            colorbar=dict(
                title="Sentiment Score",
                titleside="right"
            ),
            hoverongaps=False
        ))
        
        fig.update_layout(
            title=f"Sentiment Heatmap - Last {timeframe}",
            xaxis_title="Time (Hours)",
            yaxis_title="Entities",
            plot_bgcolor=self.color_scheme['background'],
            paper_bgcolor=self.color_scheme['background'],
            font_color=self.color_scheme['text']
        )
        
        return fig
    
    def create_sentiment_flow_diagram(self, entity_relationships: Dict) -> go.Figure:
        """Create a flow diagram showing sentiment relationships between entities"""
        
        # This creates a network-style visualization
        fig = go.Figure()
        
        # Add nodes (entities)
        for entity, data in entity_relationships.items():
            sentiment = data.get('sentiment', 0)
            
            # Color based on sentiment
            if sentiment > 0.2:
                color = self.color_scheme['bullish']
            elif sentiment < -0.2:
                color = self.color_scheme['bearish']
            else:
                color = self.color_scheme['neutral']
            
            fig.add_trace(go.Scatter(
                x=[data['x']],
                y=[data['y']],
                mode='markers+text',
                marker=dict(
                    size=abs(sentiment) * 50 + 20,  # Size based on sentiment strength
                    color=color,
                    line=dict(width=2, color='white')
                ),
                text=entity,
                textposition="middle center",
                name=entity,
                showlegend=False
            ))
        
        # Add connections (correlations)
        for entity1, data1 in entity_relationships.items():
            for entity2, data2 in entity_relationships.items():
                if entity1 != entity2:
                    correlation = data1.get('correlations', {}).get(entity2, 0)
                    
                    if abs(correlation) > 0.3:  # Only show strong correlations
                        fig.add_trace(go.Scatter(
                            x=[data1['x'], data2['x']],
                            y=[data1['y'], data2['y']],
                            mode='lines',
                            line=dict(
                                width=abs(correlation) * 5,
                                color='rgba(255,255,255,0.3)'
                            ),
                            showlegend=False,
                            hoverinfo='skip'
                        ))
        
        fig.update_layout(
            title="Sentiment Relationship Network",
            showlegend=False,
            plot_bgcolor=self.color_scheme['background'],
            paper_bgcolor=self.color_scheme['background'],
            font_color=self.color_scheme['text'],
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
        
        return fig
    
    def create_sentiment_prediction_chart(self, historical_data: pd.DataFrame, 
                                        predictions: Dict) -> go.Figure:
        """Create a chart showing historical sentiment and predictions"""
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Sentiment Score', 'Prediction Confidence'),
            vertical_spacing=0.1
        )
        
        # Historical sentiment
        fig.add_trace(
            go.Scatter(
                x=historical_data.index,
                y=historical_data['sentiment_score'],
                mode='lines',
                name='Historical Sentiment',
                line=dict(color=self.color_scheme['neutral'])
            ),
            row=1, col=1
        )
        
        # Predictions
        if predictions and 'predictions' in predictions:
            prediction_times = pd.date_range(
                start=historical_data.index[-1] + pd.Timedelta(hours=1),
                periods=len(predictions['predictions']),
                freq='H'
            )
            
            fig.add_trace(
                go.Scatter(
                    x=prediction_times,
                    y=predictions['predictions'],
                    mode='lines+markers',
                    name='Predictions',
                    line=dict(color=self.color_scheme['bullish'], dash='dash')
                ),
                row=1, col=1
            )
            
            # Confidence intervals
            if 'confidence_interval' in predictions:
                upper_bound = [predictions['confidence_interval'][1]] * len(predictions['predictions'])
                lower_bound = [predictions['confidence_interval'][0]] * len(predictions['predictions'])
                
                fig.add_trace(
                    go.Scatter(
                        x=prediction_times,
                        y=upper_bound,
                        mode='lines',
                        line=dict(width=0),
                        showlegend=False
                    ),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=prediction_times,
                        y=lower_bound,
                        mode='lines',
                        line=dict(width=0),
                        fill='tonexty',
                        fillcolor='rgba(0,200,81,0.2)',
                        name='Confidence Interval',
                        showlegend=True
                    ),
                    row=1, col=1
                )
        
        # Confidence over time (if available)
        if 'confidence' in predictions:
            confidence_values = [predictions['confidence']] * len(historical_data)
            
            fig.add_trace(
                go.Scatter(
                    x=historical_data.index,
                    y=confidence_values,
                    mode='lines',
                    name='Model Confidence',
                    line=dict(color=self.color_scheme['bullish'])
                ),
                row=2, col=1
            )
        
        fig.update_layout(
            title="Sentiment Analysis with Predictions",
            plot_bgcolor=self.color_scheme['background'],
            paper_bgcolor=self.color_scheme['background'],
            font_color=self.color_scheme['text']
        )
        
        return fig
```

## 🎯 What You've Learned

Congratulations! You now know how to:

✅ **Build custom sentiment indicators** (RSI, MACD, Bollinger Bands)
✅ **Integrate new social media platforms** (TikTok, YouTube)
✅ **Create machine learning models** for sentiment prediction
✅ **Build advanced visualizations** and dashboards
✅ **Add new features** to existing systems
✅ **Extend functionality** with custom analysis tools
✅ **Process different types of data** from various sources
✅ **Create predictive models** for future sentiment

## 🚀 What's Next?

In **Chapter 16**, our final chapter, we'll wrap everything up with a **Summary and Next Steps** guide. You'll learn:

- How to put everything together
- Career opportunities in sentiment analysis
- Advanced topics to explore next
- Building a portfolio project
- Contributing to open-source projects

**Ready to complete your sentiment analysis journey?** Let's finish strong with **[Chapter 16: Summary and Next Steps](chapter_16_summary_next_steps.md)**!

---

## 💡 Feature Development Challenge

Try building these new features:

1. **Custom Indicator**: Create your own sentiment momentum indicator
2. **New Data Source**: Add Instagram or LinkedIn data collection
3. **Prediction Model**: Build a model to predict market movements from sentiment
4. **Advanced Visualization**: Create a real-time sentiment globe or network graph

Building new features is how you become an expert developer! 🚀
