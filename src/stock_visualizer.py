import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from datetime import datetime
import numpy as np


class StockVisualizer:
    """Visualizes stock data using matplotlib and mplfinance."""

    def __init__(self, symbol: str):
        """Initialize the visualizer with a symbol.

        Args:
            symbol: Stock ticker symbol
        """
        self.symbol = symbol.upper()

    def plot_candlestick(self, data: pd.DataFrame, title: str = None):
        """Plot candlestick chart.

        Args:
            data: DataFrame with OHLC data
            title: Optional chart title
        """
        if data.empty:
            print("No data available to plot")
            return

        if title is None:
            title = f"{self.symbol} Stock Price"

        # mplfinance expects datetime index
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data.index)

        # Create custom style
        mc = mpf.make_marketcolors(up='g', down='r', edge='inherit',
                                     wick='inherit', volume='in')
        s = mpf.make_mpf_style(marketcolors=mc, gridstyle='--', y_on_right=False)

        # Plot
        try:
            mpf.plot(data, type='candle', style=s, title=title,
                     ylabel='Price ($)', volume=True, figsize=(12, 8))
            plt.show()
        except KeyboardInterrupt:
            print("\nChart closed by user.")
            plt.close('all')
        except Exception as e:
            print(f"Error plotting candlestick chart: {e}")

    def plot_line(self, data: pd.DataFrame, column: str = 'Close', title: str = None):
        """Plot simple line chart.

        Args:
            data: DataFrame with stock data
            column: Column to plot (default: 'Close')
            title: Optional chart title
        """
        if data.empty:
            print("No data available to plot")
            return

        if column not in data.columns:
            print(f"Column '{column}' not found in data")
            return

        if title is None:
            title = f"{self.symbol} {column} Price"

        try:
            plt.figure(figsize=(12, 6))
            plt.plot(data.index, data[column], linewidth=2, color='blue')
            plt.title(title, fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel(f'{column} Price ($)', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
        except KeyboardInterrupt:
            print("\nChart closed by user.")
            plt.close('all')
        except Exception as e:
            print(f"Error plotting line chart: {e}")

    def plot_realtime_comparison(self, data: pd.DataFrame):
        """Plot multiple metrics in subplots for real-time monitoring.

        Args:
            data: DataFrame with stock data
        """
        if data.empty:
            print("No data available to plot")
            return

        try:
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            fig.suptitle(f"{self.symbol} Real-Time Data", fontsize=16, fontweight='bold')

            # Price chart
            axes[0].plot(data.index, data['Close'], linewidth=2, color='blue', label='Close')
            axes[0].fill_between(data.index, data['Low'], data['High'], alpha=0.2, color='gray', label='High-Low Range')
            axes[0].set_ylabel('Price ($)', fontsize=12)
            axes[0].grid(True, alpha=0.3)
            axes[0].legend()

            # Volume chart
            axes[1].bar(data.index, data['Volume'], color='green', alpha=0.5)
            axes[1].set_ylabel('Volume', fontsize=12)
            axes[1].set_xlabel('Time', fontsize=12)
            axes[1].grid(True, alpha=0.3)

            plt.tight_layout()
            plt.show()
        except KeyboardInterrupt:
            print("\nChart closed by user.")
            plt.close('all')
        except Exception as e:
            print(f"Error plotting realtime comparison chart: {e}")

    def plot_intraday(self, data: pd.DataFrame):
        """Plot intraday price movements.

        Args:
            data: DataFrame with intraday data
        """
        if data.empty:
            print("No data available to plot")
            return

        try:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8),
                                            gridspec_kw={'height_ratios': [3, 1]})

            fig.suptitle(f"{self.symbol} Intraday Trading", fontsize=16, fontweight='bold')

            # Price and moving average
            ax1.plot(data.index, data['Close'], linewidth=1.5, color='blue', label='Price')

            # Add simple moving average if enough data points
            if len(data) >= 20:
                data['SMA20'] = data['Close'].rolling(window=20).mean()
                ax1.plot(data.index, data['SMA20'], linewidth=1, color='orange',
                         label='20-period SMA', linestyle='--')

            ax1.set_ylabel('Price ($)', fontsize=12)
            ax1.grid(True, alpha=0.3)
            ax1.legend()

            # Volume
            colors = ['g' if data['Close'].iloc[i] >= data['Open'].iloc[i] else 'r'
                      for i in range(len(data))]
            ax2.bar(data.index, data['Volume'], color=colors, alpha=0.5)
            ax2.set_ylabel('Volume', fontsize=12)
            ax2.set_xlabel('Time', fontsize=12)
            ax2.grid(True, alpha=0.3)

            plt.tight_layout()
            plt.show()
        except KeyboardInterrupt:
            print("\nChart closed by user.")
            plt.close('all')
        except Exception as e:
            print(f"Error plotting intraday chart: {e}")

    @staticmethod
    def plot_comparison_symbols(symbol1: str, data1: pd.DataFrame,
                                symbol2: str, data2: pd.DataFrame,
                                comparison_type: str = 'price'):
        """Plot comparison between two stock symbols.

        Args:
            symbol1: First stock symbol
            data1: DataFrame with first stock data
            symbol2: Second stock symbol
            data2: DataFrame with second stock data
            comparison_type: Type of comparison ('price' or 'performance')
        """
        if data1.empty or data2.empty:
            print("No data available to plot for one or both symbols")
            return

        try:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10),
                                           gridspec_kw={'height_ratios': [3, 1]})

            if comparison_type == 'performance':
                # Normalize to percentage change from first value
                norm_data1 = (data1['Close'] / data1['Close'].iloc[0] - 1) * 100
                norm_data2 = (data2['Close'] / data2['Close'].iloc[0] - 1) * 100

                ax1.plot(norm_data1.index, norm_data1, linewidth=2,
                        color='blue', label=symbol1, alpha=0.8)
                ax1.plot(norm_data2.index, norm_data2, linewidth=2,
                        color='red', label=symbol2, alpha=0.8)
                ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
                ax1.set_ylabel('Performance (%)', fontsize=12)
                ax1.set_title(f'{symbol1} vs {symbol2} - Performance Comparison',
                             fontsize=16, fontweight='bold')

            else:  # price comparison with dual axes
                # Plot first symbol on left axis
                color1 = 'blue'
                ax1.plot(data1.index, data1['Close'], linewidth=2,
                        color=color1, label=symbol1, alpha=0.8)
                ax1.set_ylabel(f'{symbol1} Price ($)', fontsize=12, color=color1)
                ax1.tick_params(axis='y', labelcolor=color1)
                ax1.set_title(f'{symbol1} vs {symbol2} - Price Comparison',
                             fontsize=16, fontweight='bold')

                # Create second y-axis for second symbol
                ax1_twin = ax1.twinx()
                color2 = 'red'
                ax1_twin.plot(data2.index, data2['Close'], linewidth=2,
                             color=color2, label=symbol2, alpha=0.8)
                ax1_twin.set_ylabel(f'{symbol2} Price ($)', fontsize=12, color=color2)
                ax1_twin.tick_params(axis='y', labelcolor=color2)

                # Combine legends
                lines1, labels1 = ax1.get_legend_handles_labels()
                lines2, labels2 = ax1_twin.get_legend_handles_labels()
                ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

            if comparison_type == 'performance':
                ax1.legend(loc='upper left')

            ax1.grid(True, alpha=0.3)

            # Volume comparison on bottom subplot
            width1 = 0.4
            x1 = np.arange(len(data1))
            x2 = x1 + width1

            # Normalize volume bars to fit nicely
            ax2.bar(data1.index, data1['Volume'], width=width1,
                   color='blue', alpha=0.5, label=f'{symbol1} Volume')

            # Create second y-axis for second symbol's volume
            ax2_twin = ax2.twinx()
            ax2_twin.bar(data2.index, data2['Volume'], width=width1,
                        color='red', alpha=0.5, label=f'{symbol2} Volume')

            ax2.set_ylabel(f'{symbol1} Volume', fontsize=10, color='blue')
            ax2_twin.set_ylabel(f'{symbol2} Volume', fontsize=10, color='red')
            ax2.set_xlabel('Date', fontsize=12)
            ax2.tick_params(axis='y', labelcolor='blue')
            ax2_twin.tick_params(axis='y', labelcolor='red')
            ax2.grid(True, alpha=0.3)

            # Combine volume legends
            lines1, labels1 = ax2.get_legend_handles_labels()
            lines2, labels2 = ax2_twin.get_legend_handles_labels()
            ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)

            plt.tight_layout()
            plt.show()

        except KeyboardInterrupt:
            print("\nChart closed by user.")
            plt.close('all')
        except Exception as e:
            print(f"Error plotting comparison chart: {e}")
