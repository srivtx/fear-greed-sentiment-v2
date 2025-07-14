import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class SentimentVisualizer:
    """Generates visualizations from sentiment analysis"""

    def __init__(self):
        # Create visualizations directory if it doesn't exist
        self.viz_dir = Path("data") / "visualizations"
        self.viz_dir.mkdir(parents=True, exist_ok=True)

        # Set up plot style
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (12, 8)

    def plot_fear_greed_gauge(self, fear_greed_index, sentiment_label=None):
        """
        Create a gauge chart for the Fear & Greed Index

        Args:
            fear_greed_index (float): Fear & Greed Index value (0-100)
            sentiment_label (str, optional): Market sentiment label

        Returns:
            str: Path to saved image
        """
        fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': 'polar'})

        # Normalize fear greed index to 0-1
        norm_index = fear_greed_index / 100

        # Create color gradient
        cmap = plt.cm.RdYlGn  # Red -> Yellow -> Green
        colors = [cmap(i) for i in np.linspace(0, 1, 100)]

        # Plot the gauge
        N = 100
        angles = np.linspace(np.pi, 0, N)
        bars = ax.bar(angles, np.ones(N), width=np.pi / N, color=colors)

        # Set the ticks and labels
        ax.set_xticks([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi])
        ax.set_xticklabels(['Extreme\nGreed', 'Greed', 'Neutral', 'Fear', 'Extreme\nFear'], fontsize=12)

        # Remove radial ticks and labels
        ax.set_yticks([])

        # Needle position
        needle_angle = np.pi * (1 - norm_index)
        ax.plot([0, needle_angle], [0, 0.8], 'k-', linewidth=3)
        ax.plot([0], [0], 'ko', markersize=10)

        # Title and subtitle
        title = f"Fear & Greed Index: {fear_greed_index:.2f}"
        if sentiment_label:
            title += f"\nMarket Sentiment: {sentiment_label}"

        ax.set_title(title, fontsize=16, pad=20)

        # Set y limit for gauge
        ax.set_ylim(0, 1.2)

        # Add timestamp
        plt.figtext(0.5, 0.01, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    ha="center", fontsize=10)

        # Save the image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = self.viz_dir / f"fear_greed_gauge_{timestamp}.png"
        plt.savefig(file_path, dpi=150, bbox_inches='tight')
        plt.close(fig)

        logger.info(f"Fear & Greed gauge saved to {file_path}")
        return str(file_path)

    def plot_sentiment_trends(self, days=7):
        """
        Plot sentiment trends over time

        Args:
            days (int): Number of days to include in the trend

        Returns:
            str: Path to saved image
        """
        # Get sentiment data from previous days
        data_path = Path("data")
        sentiment_dirs = sorted(list(data_path.glob("sentiment_*")))

        # Check if we have enough data
        if len(sentiment_dirs) < 2:
            logger.warning("Not enough historical data for sentiment trend chart")
            return None

        # Collect sentiment data
        dates = []
        fear_greed_values = []

        for sentiment_dir in sentiment_dirs:
            fear_greed_path = sentiment_dir / "fear_greed_index.json"

            if fear_greed_path.exists():
                try:
                    with open(fear_greed_path, "r") as f:
                        data = json.load(f)

                    timestamp = data.get("timestamp")
                    if timestamp:
                        date = datetime.fromisoformat(timestamp.split('T')[0])
                        fear_greed = data.get("fear_greed_index", 50)

                        dates.append(date)
                        fear_greed_values.append(fear_greed)

                except Exception as e:
                    logger.error(f"Error reading sentiment data from {fear_greed_path}: {e}")
                    continue

        # Check if we have data to plot
        if not dates:
            logger.warning("No sentiment data found for trend chart")
            return None

        # Create plot
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot sentiment line
        ax.plot(dates, fear_greed_values, 'o-', linewidth=2)

        # Add color bands
        ax.axhspan(0, 20, alpha=0.2, color='red', label='Extreme Fear')
        ax.axhspan(20, 40, alpha=0.2, color='orange', label='Fear')
        ax.axhspan(40, 60, alpha=0.2, color='yellow', label='Neutral')
        ax.axhspan(60, 80, alpha=0.2, color='lightgreen', label='Greed')
        ax.axhspan(80, 100, alpha=0.2, color='green', label='Extreme Greed')

        # Set y-axis limits and ticks
        ax.set_ylim(0, 100)
        ax.set_yticks([10, 30, 50, 70, 90])
        ax.set_yticklabels(['Extreme\nFear', 'Fear', 'Neutral', 'Greed', 'Extreme\nGreed'])

        # Format x-axis
        plt.xticks(rotation=45)

        # Set title and labels
        plt.title("Fear & Greed Index Trend", fontsize=16)
        plt.xlabel("Date", fontsize=12)
        plt.grid(True, alpha=0.3)

        # Add legend
        plt.legend(loc='upper left')

        # Adjust layout
        plt.tight_layout()

        # Save the image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = self.viz_dir / f"sentiment_trend_{timestamp}.png"
        plt.savefig(file_path, dpi=150, bbox_inches='tight')
        plt.close(fig)

        logger.info(f"Sentiment trend chart saved to {file_path}")
        return str(file_path)

    def plot_entity_sentiment(self, sentiment_dir, entity_type="cryptos"):
        """
        Plot sentiment for specific entities

        Args:
            sentiment_dir (str): Path to sentiment directory
            entity_type (str): Type of entities to plot (cryptos, stocks, indices)

        Returns:
            str: Path to saved image
        """
        # Load entity sentiment data
        entity_sentiment_path = Path(sentiment_dir) / "entity_sentiment.json"

        if not entity_sentiment_path.exists():
            logger.warning(f"Entity sentiment file not found: {entity_sentiment_path}")
            return None

        try:
            with open(entity_sentiment_path, "r") as f:
                entity_sentiment = json.load(f)

            if entity_type not in entity_sentiment:
                logger.warning(f"No {entity_type} found in entity sentiment data")
                return None

            entities = entity_sentiment[entity_type]

            # Extract entity data
            symbols = []
            sentiment_scores = []
            mentions = []

            for symbol, data in entities.items():
                # Skip entities with no mentions
                if data.get("mentions", 0) == 0:
                    continue

                symbols.append(symbol)

                # Handle different ways sentiment might be stored
                if "compound" in data:
                    sentiment_scores.append(data["compound"])
                elif "sentiment_score" in data:
                    sentiment_scores.append(data["sentiment_score"])
                elif "positive" in data and "negative" in data:
                    sentiment_scores.append(data["positive"] - data["negative"])
                else:
                    sentiment_scores.append(0)

                mentions.append(data.get("mentions", 1))

            # Check if we have data to plot
            if not symbols:
                logger.warning(f"No {entity_type} with mentions found")
                return None

            # Create plot
            fig, ax = plt.subplots(figsize=(12, 8))

            # Define colors based on sentiment
            colors = ['red' if score < -0.05 else 'green' if score > 0.05 else 'gray' for score in sentiment_scores]

            # Create horizontal bar chart
            y_pos = np.arange(len(symbols))
            ax.barh(y_pos, sentiment_scores, color=colors, alpha=0.7)

            # Set labels
            ax.set_yticks(y_pos)
            ax.set_yticklabels(symbols)
            ax.invert_yaxis()  # Labels read top-to-bottom

            # Add mention count as text
            for i, v in enumerate(sentiment_scores):
                ax.text(v + 0.01, i, f"  Mentions: {mentions[i]}", color='black', va='center')

            # Set title and labels
            title = f"{entity_type.capitalize()} Sentiment Analysis"
            ax.set_title(title, fontsize=16)
            ax.set_xlabel("Sentiment Score (-1: Negative, +1: Positive)", fontsize=12)

            # Add zero line
            ax.axvline(x=0, color='black', linestyle='-', alpha=0.3)

            # Set x-axis limits
            ax.set_xlim(-1, 1)

            # Adjust layout
            plt.tight_layout()

            # Save the image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = self.viz_dir / f"{entity_type}_sentiment_{timestamp}.png"
            plt.savefig(file_path, dpi=150, bbox_inches='tight')
            plt.close(fig)

            logger.info(f"{entity_type.capitalize()} sentiment chart saved to {file_path}")
            return str(file_path)

        except Exception as e:
            logger.error(f"Error generating {entity_type} sentiment chart: {e}")
            return None

    def plot_signal_distribution(self, signals_file):
        """
        Plot distribution of trading signals

        Args:
            signals_file (str): Path to signals JSON file

        Returns:
            str: Path to saved image
        """
        try:
            with open(signals_file, "r") as f:
                signals_data = json.load(f)

            signals = signals_data.get("signals", [])

            if not signals:
                logger.warning("No signals found to visualize")
                return None

            # Count signal types by entity type
            entity_types = set(signal.get("entity_type", "unknown") for signal in signals)
            buy_signals = {entity: 0 for entity in entity_types}
            sell_signals = {entity: 0 for entity in entity_types}

            for signal in signals:
                entity_type = signal.get("entity_type", "unknown")
                signal_type = signal.get("type", "UNKNOWN")

                if signal_type == "BUY":
                    buy_signals[entity_type] += 1
                elif signal_type == "SELL":
                    sell_signals[entity_type] += 1

            # Create plot
            fig, ax = plt.subplots(figsize=(10, 6))

            # Set width of bars
            bar_width = 0.35
            x = np.arange(len(entity_types))

            # Create bars
            buy_bars = ax.bar(x - bar_width / 2, [buy_signals[entity] for entity in entity_types],
                              bar_width, label='BUY', color='green', alpha=0.7)
            sell_bars = ax.bar(x + bar_width / 2, [sell_signals[entity] for entity in entity_types],
                               bar_width, label='SELL', color='red', alpha=0.7)

            # Add labels and title
            ax.set_xlabel('Asset Type')
            ax.set_ylabel('Number of Signals')
            ax.set_title('Trading Signals by Asset Type')
            ax.set_xticks(x)
            ax.set_xticklabels(entity_types)
            ax.legend()

            # Add values on bars
            for bar in buy_bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2., height,
                            str(int(height)), ha='center', va='bottom')

            for bar in sell_bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2., height,
                            str(int(height)), ha='center', va='bottom')

            # Save the image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = self.viz_dir / f"signals_distribution_{timestamp}.png"
            plt.savefig(file_path, dpi=150, bbox_inches='tight')
            plt.close(fig)

            logger.info(f"Signal distribution chart saved to {file_path}")
            return str(file_path)

        except Exception as e:
            logger.error(f"Error generating signal distribution chart: {e}")
            return None

    def plot_market_correlation(self, sentiment_dir, collection_dir=None):
        """
        Plot correlation between sentiment and market data

        Args:
            sentiment_dir (str): Path to sentiment directory
            collection_dir (str, optional): Path to collection directory

        Returns:
            str: Path to saved image
        """
        try:
            # Find market data files
            if not collection_dir:
                # Find most recent collection directory
                data_path = Path("data")
                collection_dirs = sorted(list(data_path.glob("collection_*")))
                if not collection_dirs:
                    logger.error("No collection directories found")
                    return None
                collection_dir = collection_dirs[-1]
            else:
                collection_dir = Path(collection_dir)

            market_files = list(Path(collection_dir).glob("market_data_*.csv"))
            if not market_files:
                logger.error(f"No market data found in {collection_dir}")
                return None

            # Load market data
            market_df = pd.read_csv(market_files[0])

            # Load entity sentiment data
            entity_sentiment_path = Path(sentiment_dir) / "entity_sentiment.json"
            if not entity_sentiment_path.exists():
                logger.error(f"Entity sentiment file not found in {sentiment_dir}")
                return None

            with open(entity_sentiment_path, "r") as f:
                entity_sentiment = json.load(f)

            # Create plot
            fig, ax = plt.subplots(figsize=(14, 8))

            # Track plot data
            x_data = []
            y_data = []
            colors = []
            sizes = []
            labels = []

            # For each entity type
            for entity_type in ["cryptos", "stocks", "indices"]:
                if entity_type not in entity_sentiment:
                    continue

                for symbol, data in entity_sentiment[entity_type].items():
                    # Get sentiment score
                    if "compound" in data:
                        sentiment_score = data["compound"]
                    elif "sentiment_score" in data:
                        sentiment_score = data["sentiment_score"]
                    else:
                        continue

                    # Filter market data for this symbol
                    symbol_data = market_df[market_df["Symbol"] == symbol]

                    if symbol_data.empty:
                        # Try different format for crypto symbols
                        if entity_type == "cryptos":
                            symbol_data = market_df[market_df["Symbol"] == f"{symbol}-USD"]

                    if symbol_data.empty:
                        continue

                    # Get price change
                    price_change = symbol_data["Change"].values[0]

                    # Add to plot data
                    x_data.append(sentiment_score)
                    y_data.append(price_change)

                    # Set color based on entity type
                    if entity_type == "cryptos":
                        colors.append('blue')
                    elif entity_type == "stocks":
                        colors.append('green')
                    else:
                        colors.append('purple')

                    # Set size based on mentions
                    mentions = data.get("mentions", 1)
                    sizes.append(min(500, mentions * 20))

                    # Set label
                    labels.append(symbol)

            # Create scatter plot
            scatter = ax.scatter(x_data, y_data, c=colors, s=sizes, alpha=0.6)

            # Add labels for points
            for i, label in enumerate(labels):
                ax.annotate(label, (x_data[i], y_data[i]), fontsize=8)

            # Add regression line
            if x_data and y_data:
                z = np.polyfit(x_data, y_data, 1)
                p = np.poly1d(z)
                ax.plot(sorted(x_data), p(sorted(x_data)), "r--", alpha=0.8)

                # Calculate correlation coefficient
                correlation = np.corrcoef(x_data, y_data)[0, 1]

                # Add correlation text
                ax.text(0.05, 0.95, f"Correlation: {correlation:.2f}", transform=ax.transAxes,
                        fontsize=12, va='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

            # Add vertical and horizontal lines at 0
            ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)

            # Add colored regions to indicate quadrants
            ax.fill_between([-1, 0], 0, 5, color='red', alpha=0.1)
            ax.fill_between([0, 1], 0, 5, color='green', alpha=0.1)
            ax.fill_between([-1, 0], -5, 0, color='yellow', alpha=0.1)
            ax.fill_between([0, 1], -5, 0, color='orange', alpha=0.1)

            # Set labels and title
            ax.set_xlabel('Sentiment Score (-1: Negative, +1: Positive)')
            ax.set_ylabel('Price Change (%)')
            ax.set_title('Correlation between Sentiment and Price Movement')

            # Add legend for entity types
            legend_elements = [
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Cryptos'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Stocks'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='purple', markersize=10, label='Indices')
            ]
            ax.legend(handles=legend_elements, loc='best')

            # Save the image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = self.viz_dir / f"market_correlation_{timestamp}.png"
            plt.savefig(file_path, dpi=150, bbox_inches='tight')
            plt.close(fig)

            logger.info(f"Market correlation chart saved to {file_path}")
            return str(file_path)

        except Exception as e:
            logger.error(f"Error generating market correlation chart: {e}")
            return None