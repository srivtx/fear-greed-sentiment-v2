# Chapter 12: Configuration and Customization - Making the System Yours 🔧

## Welcome to System Mastery!

You've learned how our system works from data collection to beautiful visualizations. Now let's learn how to customize everything to fit your exact needs! Think of this chapter as getting the keys to modify, tune, and extend the system however you want.

## 🎛️ Why Configuration Matters

**Configuration = Making the system adaptable without changing code**

### The Power of Flexibility

Instead of hardcoding values like this:
```python
# Bad: Hardcoded values
TWITTER_BATCH_SIZE = 100
SENTIMENT_THRESHOLD = 0.05
UPDATE_INTERVAL = 15  # minutes
```

We use configuration files like this:
```python
# Good: Configurable values
batch_size = config.get('twitter_batch_size', 100)
threshold = config.get('sentiment_threshold', 0.05)
interval = config.get('update_interval_minutes', 15)
```

This means you can change behavior without touching code!

## 📁 Configuration File Structure

### Main Configuration File (`config/config.json`)

```json
{
  "system": {
    "name": "Fear & Greed Sentiment Engine",
    "version": "2.0",
    "environment": "production",
    "debug_mode": false,
    "log_level": "INFO"
  },
  
  "data_collection": {
    "update_interval_minutes": 15,
    "batch_processing": true,
    "real_time_processing": false,
    
    "twitter": {
      "enabled": true,
      "batch_size": 100,
      "search_terms": ["Bitcoin", "BTC", "$BTC", "Tesla", "TSLA", "$TSLA"],
      "rate_limit_delay": 1.5,
      "max_retries": 3,
      "timeout_seconds": 30
    },
    
    "reddit": {
      "enabled": true,
      "subreddits": ["cryptocurrency", "Bitcoin", "investing", "stocks"],
      "posts_per_subreddit": 50,
      "include_comments": true,
      "max_comment_depth": 2
    },
    
    "news": {
      "enabled": true,
      "sources": ["coindesk", "reuters", "bloomberg"],
      "categories": ["technology", "business"],
      "language": "en",
      "max_articles": 100
    },
    
    "market_data": {
      "enabled": true,
      "update_interval_minutes": 5,
      "symbols": ["BTC-USD", "ETH-USD", "TSLA", "AAPL"],
      "price_history_days": 7
    }
  },
  
  "sentiment_analysis": {
    "engine": "vader_enhanced",
    "confidence_threshold": 0.1,
    "min_text_length": 10,
    "max_text_length": 1000,
    
    "thresholds": {
      "very_positive": 0.5,
      "positive": 0.1,
      "neutral": 0.05,
      "negative": -0.1,
      "very_negative": -0.5
    },
    
    "financial_enhancement": {
      "enabled": true,
      "custom_lexicon_file": "config/financial_lexicon.json",
      "intensity_multiplier": 1.2,
      "negation_handling": true
    }
  },
  
  "entity_recognition": {
    "enabled": true,
    "fuzzy_matching": {
      "enabled": true,
      "similarity_threshold": 0.8
    },
    "context_validation": {
      "enabled": true,
      "financial_context_required": true,
      "ambiguous_terms": ["apple", "meta", "coin"]
    },
    "entities_file": "config/financial_entities.json"
  },
  
  "signal_generation": {
    "min_posts_for_signal": 5,
    "confidence_threshold": 0.4,
    
    "component_weights": {
      "sentiment": 0.35,
      "volume": 0.20,
      "momentum": 0.25,
      "market_correlation": 0.15,
      "news_sentiment": 0.05
    },
    
    "thresholds": {
      "strong_signal": 0.5,
      "moderate_signal": 0.2,
      "weak_signal": 0.1
    },
    
    "momentum": {
      "timeframes": ["15m", "1h", "4h", "24h"],
      "acceleration_threshold": 0.1,
      "sustainability_factor": 0.7
    }
  },
  
  "fear_greed_index": {
    "calculation_method": "weighted_average",
    "market_cap_weighting": true,
    "smoothing_factor": 0.1,
    
    "zones": {
      "extreme_fear": [0, 20],
      "fear": [20, 40],
      "neutral": [40, 60],
      "greed": [60, 80],
      "extreme_greed": [80, 100]
    }
  },
  
  "storage": {
    "data_directory": "data",
    "cache_directory": "data/cache",
    "log_directory": "logs",
    "backup_enabled": true,
    "cleanup_days": 30,
    
    "cache": {
      "memory_cache_size": 1000,
      "file_cache_hours": 24,
      "compression_enabled": true
    }
  },
  
  "visualization": {
    "default_theme": "dark",
    "auto_refresh_seconds": 30,
    "chart_height": 500,
    "gauge_size": [10, 8],
    
    "colors": {
      "positive": "#00ff88",
      "negative": "#ff4444",
      "neutral": "#ffbb33",
      "background": "#1a1a1a"
    }
  },
  
  "alerts": {
    "enabled": true,
    "channels": ["email", "webhook"],
    "thresholds": {
      "extreme_sentiment": 0.8,
      "high_volume": 1000,
      "rapid_change": 0.3
    }
  }
}
```

## 🔧 Configuration Management System

### Configuration Loader

```python
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

class ConfigurationManager:
    """Manages system configuration with validation and hot-reloading"""
    
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = Path(config_path)
        self.config_data = {}
        self.default_config = {}
        self.validators = {}
        self.change_callbacks = []
        
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.load_configuration()
        
        # Set up file watching for hot-reload
        self._setup_file_watcher()
    
    def load_configuration(self):
        """Load configuration from file with validation"""
        
        try:
            # Load main config
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    self.config_data = json.load(f)
                self.logger.info(f"Configuration loaded from {self.config_path}")
            else:
                self.logger.warning(f"Config file not found: {self.config_path}")
                self.config_data = {}
            
            # Load default values
            self._load_default_config()
            
            # Validate configuration
            self._validate_configuration()
            
            # Apply environment variable overrides
            self._apply_environment_overrides()
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            raise
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'twitter.batch_size')"""
        
        keys = key_path.split('.')
        value = self.config_data
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            # Try default config
            default_value = self._get_default_value(key_path)
            if default_value is not None:
                return default_value
            return default
    
    def set(self, key_path: str, value: Any, persist: bool = False):
        """Set configuration value using dot notation"""
        
        keys = key_path.split('.')
        config = self.config_data
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the value
        config[keys[-1]] = value
        
        # Validate the change
        if not self._validate_value(key_path, value):
            raise ValueError(f"Invalid value for {key_path}: {value}")
        
        # Persist to file if requested
        if persist:
            self.save_configuration()
        
        # Notify callbacks
        self._notify_change_callbacks(key_path, value)
        
        self.logger.info(f"Configuration updated: {key_path} = {value}")
    
    def save_configuration(self):
        """Save current configuration to file"""
        
        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write config with nice formatting
            with open(self.config_path, 'w') as f:
                json.dump(self.config_data, f, indent=2, sort_keys=True)
            
            self.logger.info(f"Configuration saved to {self.config_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            raise
    
    def _load_default_config(self):
        """Load default configuration values"""
        
        self.default_config = {
            "system": {
                "log_level": "INFO",
                "debug_mode": False
            },
            "data_collection": {
                "update_interval_minutes": 15,
                "twitter": {
                    "batch_size": 100,
                    "rate_limit_delay": 1.5,
                    "max_retries": 3
                },
                "reddit": {
                    "posts_per_subreddit": 50,
                    "include_comments": True
                }
            },
            "sentiment_analysis": {
                "confidence_threshold": 0.1,
                "min_text_length": 10
            },
            "signal_generation": {
                "min_posts_for_signal": 5,
                "confidence_threshold": 0.4
            }
        }
    
    def _validate_configuration(self):
        """Validate configuration values"""
        
        validators = {
            'data_collection.update_interval_minutes': lambda x: isinstance(x, int) and x > 0,
            'data_collection.twitter.batch_size': lambda x: isinstance(x, int) and 1 <= x <= 1000,
            'sentiment_analysis.confidence_threshold': lambda x: isinstance(x, (int, float)) and 0 <= x <= 1,
            'signal_generation.min_posts_for_signal': lambda x: isinstance(x, int) and x >= 1
        }
        
        for key_path, validator in validators.items():
            value = self.get(key_path)
            if value is not None and not validator(value):
                raise ValueError(f"Invalid configuration value for {key_path}: {value}")
        
        self.logger.info("Configuration validation passed")
    
    def _apply_environment_overrides(self):
        """Apply environment variable overrides"""
        
        # Map environment variables to config keys
        env_mappings = {
            'FG_LOG_LEVEL': 'system.log_level',
            'FG_DEBUG_MODE': 'system.debug_mode',
            'FG_TWITTER_BATCH_SIZE': 'data_collection.twitter.batch_size',
            'FG_UPDATE_INTERVAL': 'data_collection.update_interval_minutes'
        }
        
        for env_var, config_key in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                # Convert string to appropriate type
                converted_value = self._convert_env_value(env_value, config_key)
                self.set(config_key, converted_value)
                self.logger.info(f"Applied environment override: {config_key} = {converted_value}")
    
    def _convert_env_value(self, env_value: str, config_key: str) -> Any:
        """Convert environment variable string to appropriate type"""
        
        # Boolean conversion
        if config_key.endswith('debug_mode') or config_key.endswith('enabled'):
            return env_value.lower() in ['true', '1', 'yes', 'on']
        
        # Integer conversion
        if 'interval' in config_key or 'size' in config_key or 'retries' in config_key:
            return int(env_value)
        
        # Float conversion
        if 'threshold' in config_key or 'delay' in config_key:
            return float(env_value)
        
        # Default to string
        return env_value
    
    def add_change_callback(self, callback):
        """Add callback to be notified when configuration changes"""
        self.change_callbacks.append(callback)
    
    def _notify_change_callbacks(self, key_path: str, value: Any):
        """Notify all callbacks of configuration changes"""
        for callback in self.change_callbacks:
            try:
                callback(key_path, value)
            except Exception as e:
                self.logger.warning(f"Configuration callback failed: {e}")
```

### Entity Configuration

```python
class EntityManager:
    """Manages financial entities configuration"""
    
    def __init__(self, entities_file: str = "config/financial_entities.json"):
        self.entities_file = Path(entities_file)
        self.entities = {}
        self.load_entities()
    
    def load_entities(self):
        """Load entities from configuration file"""
        
        if self.entities_file.exists():
            with open(self.entities_file, 'r') as f:
                self.entities = json.load(f)
        else:
            # Create default entities file
            self.entities = self._get_default_entities()
            self.save_entities()
    
    def _get_default_entities(self) -> Dict:
        """Get default entity configuration"""
        
        return {
            "cryptocurrencies": {
                "bitcoin": {
                    "name": "Bitcoin",
                    "symbols": ["BTC", "BITCOIN", "₿"],
                    "hashtags": ["#bitcoin", "#btc"],
                    "aliases": ["digital gold", "crypto king", "satoshi coin"],
                    "patterns": [r"\$BTC\b", r"\bBTC\b", r"\bbitcoin\b"],
                    "market_cap_rank": 1,
                    "enabled": True
                },
                "ethereum": {
                    "name": "Ethereum",
                    "symbols": ["ETH", "ETHEREUM"],
                    "hashtags": ["#ethereum", "#eth"],
                    "aliases": ["ether", "vitalik coin", "smart contracts"],
                    "patterns": [r"\$ETH\b", r"\bETH\b", r"\bethereum\b"],
                    "market_cap_rank": 2,
                    "enabled": True
                }
            },
            "stocks": {
                "tesla": {
                    "name": "Tesla Inc",
                    "symbol": "TSLA",
                    "aliases": ["tesla", "tesla motors", "elon company", "ev company"],
                    "patterns": [r"\$TSLA\b", r"\bTSLA\b", r"\btesla\b"],
                    "sector": "Technology",
                    "enabled": True
                },
                "apple": {
                    "name": "Apple Inc",
                    "symbol": "AAPL",
                    "aliases": ["apple", "tim cook company", "iphone maker"],
                    "patterns": [r"\$AAPL\b", r"\bAAPL\b", r"\bapple\b(?!\s+pie)"],
                    "sector": "Technology",
                    "enabled": True
                }
            }
        }
    
    def add_entity(self, category: str, entity_id: str, entity_data: Dict):
        """Add a new entity"""
        
        if category not in self.entities:
            self.entities[category] = {}
        
        # Validate entity data
        required_fields = ['name', 'patterns', 'enabled']
        for field in required_fields:
            if field not in entity_data:
                raise ValueError(f"Missing required field: {field}")
        
        self.entities[category][entity_id] = entity_data
        self.save_entities()
    
    def remove_entity(self, category: str, entity_id: str):
        """Remove an entity"""
        
        if category in self.entities and entity_id in self.entities[category]:
            del self.entities[category][entity_id]
            self.save_entities()
    
    def update_entity(self, category: str, entity_id: str, updates: Dict):
        """Update an entity's configuration"""
        
        if category in self.entities and entity_id in self.entities[category]:
            self.entities[category][entity_id].update(updates)
            self.save_entities()
    
    def get_enabled_entities(self, category: str = None) -> Dict:
        """Get all enabled entities, optionally filtered by category"""
        
        enabled = {}
        
        categories = [category] if category else self.entities.keys()
        
        for cat in categories:
            if cat in self.entities:
                enabled[cat] = {
                    entity_id: entity_data
                    for entity_id, entity_data in self.entities[cat].items()
                    if entity_data.get('enabled', True)
                }
        
        return enabled
    
    def save_entities(self):
        """Save entities to file"""
        
        self.entities_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.entities_file, 'w') as f:
            json.dump(self.entities, f, indent=2, sort_keys=True)
```

## 🎨 Customization Examples

### Custom Sentiment Lexicon

```python
class CustomSentimentLexicon:
    """Manages custom sentiment lexicon for domain-specific terms"""
    
    def __init__(self, lexicon_file: str = "config/financial_lexicon.json"):
        self.lexicon_file = Path(lexicon_file)
        self.custom_words = {}
        self.load_lexicon()
    
    def load_lexicon(self):
        """Load custom lexicon from file"""
        
        if self.lexicon_file.exists():
            with open(self.lexicon_file, 'r') as f:
                self.custom_words = json.load(f)
        else:
            # Create default lexicon
            self.custom_words = self._get_default_lexicon()
            self.save_lexicon()
    
    def _get_default_lexicon(self) -> Dict:
        """Get default financial sentiment lexicon"""
        
        return {
            "positive_terms": {
                "moon": 2.0,
                "mooning": 2.5,
                "bullish": 2.0,
                "hodl": 1.5,
                "diamond_hands": 2.0,
                "pump": 1.8,
                "rally": 1.5,
                "surge": 2.0,
                "breakout": 2.0,
                "gains": 1.5,
                "profit": 1.5,
                "lambo": 2.0,
                "rocket": 2.0,
                "bull_run": 2.5
            },
            "negative_terms": {
                "dump": -2.0,
                "crash": -3.0,
                "rekt": -2.5,
                "bearish": -2.0,
                "fud": -1.5,
                "rugpull": -3.0,
                "scam": -2.5,
                "bubble": -1.5,
                "correction": -1.5,
                "dip": -1.0,
                "bear_market": -2.5,
                "panic_sell": -2.0
            },
            "context_modifiers": {
                "absolutely": 1.3,
                "extremely": 1.4,
                "really": 1.2,
                "very": 1.1,
                "quite": 1.05,
                "definitely": 1.2,
                "totally": 1.3
            }
        }
    
    def add_term(self, term: str, score: float, category: str = "positive_terms"):
        """Add a new term to the lexicon"""
        
        if category not in self.custom_words:
            self.custom_words[category] = {}
        
        self.custom_words[category][term] = score
        self.save_lexicon()
    
    def remove_term(self, term: str, category: str):
        """Remove a term from the lexicon"""
        
        if category in self.custom_words and term in self.custom_words[category]:
            del self.custom_words[category][term]
            self.save_lexicon()
    
    def update_term_score(self, term: str, new_score: float, category: str):
        """Update a term's sentiment score"""
        
        if category in self.custom_words and term in self.custom_words[category]:
            self.custom_words[category][term] = new_score
            self.save_lexicon()
    
    def save_lexicon(self):
        """Save lexicon to file"""
        
        self.lexicon_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.lexicon_file, 'w') as f:
            json.dump(self.custom_words, f, indent=2, sort_keys=True)
    
    def get_all_terms(self) -> Dict[str, float]:
        """Get all terms as a flat dictionary"""
        
        all_terms = {}
        
        for category, terms in self.custom_words.items():
            if isinstance(terms, dict):
                all_terms.update(terms)
        
        return all_terms
```

### Performance Tuning Configuration

```python
class PerformanceConfig:
    """Manages performance-related configuration"""
    
    def __init__(self, config_manager: ConfigurationManager):
        self.config = config_manager
        self.performance_profiles = {
            'high_frequency': {
                'update_interval_minutes': 1,
                'batch_size': 50,
                'cache_duration_minutes': 5,
                'parallel_processing': True,
                'memory_cache_size': 2000
            },
            'balanced': {
                'update_interval_minutes': 15,
                'batch_size': 100,
                'cache_duration_minutes': 30,
                'parallel_processing': True,
                'memory_cache_size': 1000
            },
            'low_resource': {
                'update_interval_minutes': 60,
                'batch_size': 25,
                'cache_duration_minutes': 120,
                'parallel_processing': False,
                'memory_cache_size': 200
            }
        }
    
    def apply_performance_profile(self, profile_name: str):
        """Apply a performance profile"""
        
        if profile_name not in self.performance_profiles:
            raise ValueError(f"Unknown performance profile: {profile_name}")
        
        profile = self.performance_profiles[profile_name]
        
        # Apply settings
        self.config.set('data_collection.update_interval_minutes', 
                       profile['update_interval_minutes'], persist=True)
        self.config.set('data_collection.twitter.batch_size', 
                       profile['batch_size'], persist=True)
        self.config.set('storage.cache.memory_cache_size', 
                       profile['memory_cache_size'], persist=True)
        
        logging.info(f"Applied performance profile: {profile_name}")
    
    def auto_tune_performance(self, system_stats: Dict):
        """Automatically tune performance based on system stats"""
        
        cpu_usage = system_stats.get('cpu_usage', 50)
        memory_usage = system_stats.get('memory_usage', 50)
        api_latency = system_stats.get('api_latency', 1.0)
        
        # Determine optimal profile
        if cpu_usage < 30 and memory_usage < 40 and api_latency < 0.5:
            recommended_profile = 'high_frequency'
        elif cpu_usage > 80 or memory_usage > 80 or api_latency > 2.0:
            recommended_profile = 'low_resource'
        else:
            recommended_profile = 'balanced'
        
        self.apply_performance_profile(recommended_profile)
        
        return recommended_profile
```

## 🔍 Configuration Validation and Testing

### Configuration Validator

```python
class ConfigValidator:
    """Validates configuration files and settings"""
    
    def __init__(self):
        self.validation_rules = self._define_validation_rules()
    
    def _define_validation_rules(self) -> Dict:
        """Define validation rules for configuration values"""
        
        return {
            'data_collection.update_interval_minutes': {
                'type': int,
                'min': 1,
                'max': 1440,  # Max 24 hours
                'description': 'Update interval in minutes'
            },
            'data_collection.twitter.batch_size': {
                'type': int,
                'min': 1,
                'max': 1000,
                'description': 'Number of tweets to fetch per batch'
            },
            'sentiment_analysis.confidence_threshold': {
                'type': float,
                'min': 0.0,
                'max': 1.0,
                'description': 'Minimum confidence for sentiment analysis'
            },
            'signal_generation.component_weights.sentiment': {
                'type': float,
                'min': 0.0,
                'max': 1.0,
                'description': 'Weight for sentiment component in signal generation'
            }
        }
    
    def validate_config(self, config_data: Dict) -> Dict:
        """Validate entire configuration"""
        
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        for key_path, rules in self.validation_rules.items():
            try:
                value = self._get_nested_value(config_data, key_path)
                if value is not None:
                    result = self._validate_value(value, rules)
                    if not result['valid']:
                        validation_results['valid'] = False
                        validation_results['errors'].extend(result['errors'])
                    validation_results['warnings'].extend(result['warnings'])
            except KeyError:
                validation_results['warnings'].append(
                    f"Missing configuration key: {key_path}"
                )
        
        # Check for component weight sum
        self._validate_component_weights(config_data, validation_results)
        
        return validation_results
    
    def _validate_value(self, value: Any, rules: Dict) -> Dict:
        """Validate a single value against rules"""
        
        result = {'valid': True, 'errors': [], 'warnings': []}
        
        # Type validation
        expected_type = rules.get('type')
        if expected_type and not isinstance(value, expected_type):
            result['valid'] = False
            result['errors'].append(
                f"Expected {expected_type.__name__}, got {type(value).__name__}"
            )
            return result
        
        # Range validation
        if 'min' in rules and value < rules['min']:
            result['valid'] = False
            result['errors'].append(f"Value {value} below minimum {rules['min']}")
        
        if 'max' in rules and value > rules['max']:
            result['valid'] = False
            result['errors'].append(f"Value {value} above maximum {rules['max']}")
        
        # Warning thresholds
        if 'warning_min' in rules and value < rules['warning_min']:
            result['warnings'].append(
                f"Value {value} is below recommended minimum {rules['warning_min']}"
            )
        
        return result
    
    def _validate_component_weights(self, config_data: Dict, results: Dict):
        """Validate that component weights sum to 1.0"""
        
        try:
            weights = self._get_nested_value(config_data, 'signal_generation.component_weights')
            if weights:
                total = sum(weights.values())
                if abs(total - 1.0) > 0.01:  # Allow small floating point errors
                    results['warnings'].append(
                        f"Component weights sum to {total:.3f}, should sum to 1.0"
                    )
        except KeyError:
            pass
```

## 🎯 Configuration UI

### Web-Based Configuration Interface

```python
import streamlit as st

class ConfigurationUI:
    """Web-based configuration interface"""
    
    def __init__(self, config_manager: ConfigurationManager):
        self.config = config_manager
        self.entity_manager = EntityManager()
        self.lexicon_manager = CustomSentimentLexicon()
    
    def create_config_interface(self):
        """Create the configuration web interface"""
        
        st.title("🔧 System Configuration")
        
        # Sidebar with configuration sections
        section = st.sidebar.selectbox(
            "Configuration Section",
            [
                "System Settings",
                "Data Collection",
                "Sentiment Analysis",
                "Entity Management",
                "Signal Generation",
                "Performance Tuning",
                "Visualization"
            ]
        )
        
        # Display selected section
        if section == "System Settings":
            self._system_settings_ui()
        elif section == "Data Collection":
            self._data_collection_ui()
        elif section == "Sentiment Analysis":
            self._sentiment_analysis_ui()
        elif section == "Entity Management":
            self._entity_management_ui()
        elif section == "Signal Generation":
            self._signal_generation_ui()
        elif section == "Performance Tuning":
            self._performance_tuning_ui()
        elif section == "Visualization":
            self._visualization_ui()
    
    def _system_settings_ui(self):
        """System settings configuration UI"""
        
        st.header("System Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            debug_mode = st.checkbox(
                "Debug Mode",
                value=self.config.get('system.debug_mode', False),
                help="Enable debug logging and detailed error messages"
            )
            
            log_level = st.selectbox(
                "Log Level",
                ["DEBUG", "INFO", "WARNING", "ERROR"],
                index=["DEBUG", "INFO", "WARNING", "ERROR"].index(
                    self.config.get('system.log_level', 'INFO')
                )
            )
        
        with col2:
            environment = st.selectbox(
                "Environment",
                ["development", "staging", "production"],
                index=["development", "staging", "production"].index(
                    self.config.get('system.environment', 'development')
                )
            )
        
        if st.button("Save System Settings"):
            self.config.set('system.debug_mode', debug_mode, persist=True)
            self.config.set('system.log_level', log_level, persist=True)
            self.config.set('system.environment', environment, persist=True)
            st.success("System settings saved!")
    
    def _data_collection_ui(self):
        """Data collection configuration UI"""
        
        st.header("Data Collection Settings")
        
        # General settings
        st.subheader("General")
        update_interval = st.slider(
            "Update Interval (minutes)",
            min_value=1,
            max_value=120,
            value=self.config.get('data_collection.update_interval_minutes', 15),
            help="How often to collect new data"
        )
        
        # Twitter settings
        st.subheader("Twitter Configuration")
        twitter_enabled = st.checkbox(
            "Enable Twitter Collection",
            value=self.config.get('data_collection.twitter.enabled', True)
        )
        
        if twitter_enabled:
            col1, col2 = st.columns(2)
            
            with col1:
                twitter_batch_size = st.number_input(
                    "Batch Size",
                    min_value=1,
                    max_value=1000,
                    value=self.config.get('data_collection.twitter.batch_size', 100),
                    help="Number of tweets to fetch per request"
                )
            
            with col2:
                rate_limit_delay = st.number_input(
                    "Rate Limit Delay (seconds)",
                    min_value=0.1,
                    max_value=10.0,
                    value=self.config.get('data_collection.twitter.rate_limit_delay', 1.5),
                    step=0.1,
                    help="Delay between API requests"
                )
            
            search_terms = st.text_area(
                "Search Terms (one per line)",
                value="\n".join(self.config.get('data_collection.twitter.search_terms', [])),
                help="Terms to search for on Twitter"
            )
        
        # Save button
        if st.button("Save Data Collection Settings"):
            self.config.set('data_collection.update_interval_minutes', update_interval, persist=True)
            self.config.set('data_collection.twitter.enabled', twitter_enabled, persist=True)
            
            if twitter_enabled:
                self.config.set('data_collection.twitter.batch_size', twitter_batch_size, persist=True)
                self.config.set('data_collection.twitter.rate_limit_delay', rate_limit_delay, persist=True)
                
                terms_list = [term.strip() for term in search_terms.split('\n') if term.strip()]
                self.config.set('data_collection.twitter.search_terms', terms_list, persist=True)
            
            st.success("Data collection settings saved!")
    
    def _entity_management_ui(self):
        """Entity management UI"""
        
        st.header("Entity Management")
        
        # Display current entities
        entities = self.entity_manager.get_enabled_entities()
        
        for category, entity_dict in entities.items():
            st.subheader(f"{category.title()}")
            
            for entity_id, entity_data in entity_dict.items():
                with st.expander(f"{entity_data['name']} ({entity_id})"):
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        enabled = st.checkbox(
                            "Enabled",
                            value=entity_data.get('enabled', True),
                            key=f"enabled_{category}_{entity_id}"
                        )
                        
                        name = st.text_input(
                            "Name",
                            value=entity_data.get('name', ''),
                            key=f"name_{category}_{entity_id}"
                        )
                    
                    with col2:
                        symbols = st.text_area(
                            "Symbols/Aliases",
                            value="\n".join(entity_data.get('symbols', [])),
                            key=f"symbols_{category}_{entity_id}",
                            help="One symbol per line"
                        )
                    
                    if st.button(f"Update {entity_id}", key=f"update_{category}_{entity_id}"):
                        updates = {
                            'enabled': enabled,
                            'name': name,
                            'symbols': [s.strip() for s in symbols.split('\n') if s.strip()]
                        }
                        self.entity_manager.update_entity(category, entity_id, updates)
                        st.success(f"Updated {entity_id}")
                        st.experimental_rerun()
        
        # Add new entity section
        st.subheader("Add New Entity")
        
        with st.form("add_entity_form"):
            new_category = st.selectbox(
                "Category",
                ["cryptocurrencies", "stocks", "indices", "commodities"]
            )
            
            new_id = st.text_input("Entity ID (lowercase, no spaces)")
            new_name = st.text_input("Display Name")
            new_symbols = st.text_area("Symbols/Aliases (one per line)")
            
            if st.form_submit_button("Add Entity"):
                if new_id and new_name:
                    entity_data = {
                        'name': new_name,
                        'symbols': [s.strip() for s in new_symbols.split('\n') if s.strip()],
                        'patterns': [f"\\b{new_id}\\b"],  # Basic pattern
                        'enabled': True
                    }
                    
                    self.entity_manager.add_entity(new_category, new_id, entity_data)
                    st.success(f"Added new entity: {new_name}")
                    st.experimental_rerun()
                else:
                    st.error("Please provide both ID and name")
```

## 🎯 What You've Learned

You now understand:

✅ **Configuration file structure** and organization
✅ **Configuration management** with validation and hot-reloading
✅ **Entity management** for adding/removing financial instruments
✅ **Custom sentiment lexicons** for domain-specific terms
✅ **Performance tuning** profiles and auto-optimization
✅ **Configuration validation** and error checking
✅ **Web-based configuration UI** for easy management
✅ **Environment variable overrides** for deployment flexibility

## 🚀 What's Next?

In **Chapter 13**, we'll explore **Optimization and Performance** - how to make your system run faster, handle more data, and scale efficiently. You'll learn:

- Performance monitoring and profiling
- Caching strategies and optimization
- Database optimization techniques
- Scaling for high-volume data

**Ready to supercharge your system's performance?** Let's continue to **[Chapter 13: Optimization and Performance](chapter_13_optimization_performance.md)**!

---

## 💡 Configuration Practice

Try these customization scenarios:

1. **Add a new cryptocurrency (Solana)**
   - What configuration changes would you need?
   - How would you test the new entity recognition?

2. **Create a "crypto-only" mode**
   - Which settings would you change?
   - How would you validate this configuration?

3. **Optimize for a low-resource server**
   - What performance settings would you adjust?
   - How would you monitor the impact?

Thinking through these scenarios helps you master system customization! 🔧
