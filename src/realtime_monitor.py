import time
import os
from datetime import datetime
from colorama import Fore, Style, init
from .stock_fetcher import StockFetcher

# Initialize colorama
init(autoreset=True)


class RealtimeMonitor:
    """Monitors and displays real-time stock quotes."""

    def __init__(self, symbol: str, refresh_interval: int = 5):
        """Initialize the real-time monitor.

        Args:
            symbol: Stock ticker symbol
            refresh_interval: Seconds between updates (default: 5)
        """
        self.symbol = symbol.upper()
        self.fetcher = StockFetcher(self.symbol)
        self.refresh_interval = refresh_interval

    def format_number(self, value, prefix: str = '', suffix: str = '') -> str:
        """Format a number for display.

        Args:
            value: Value to format
            prefix: String to add before value
            suffix: String to add after value

        Returns:
            Formatted string
        """
        if value == 'N/A' or value is None:
            return 'N/A'

        if isinstance(value, (int, float)):
            if value >= 1_000_000_000:
                return f"{prefix}{value / 1_000_000_000:.2f}B{suffix}"
            elif value >= 1_000_000:
                return f"{prefix}{value / 1_000_000:.2f}M{suffix}"
            elif value >= 1_000:
                return f"{prefix}{value / 1_000:.2f}K{suffix}"
            else:
                return f"{prefix}{value:.2f}{suffix}"
        return str(value)

    def display_quote(self, quote_data: dict):
        """Display formatted quote information.

        Args:
            quote_data: Dictionary containing quote details
        """
        # Clear screen (works on Unix/Linux/Mac and Windows)
        os.system('clear' if os.name == 'posix' else 'cls')

        print("\n" + "=" * 80)
        print(f"{Fore.CYAN}{Style.BRIGHT}STOCK QUOTE MONITOR - {self.symbol}{Style.RESET_ALL}")
        print("=" * 80 + "\n")

        # Company name
        print(f"{Fore.WHITE}{Style.BRIGHT}{quote_data.get('name', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Symbol: {self.symbol}{Style.RESET_ALL}\n")

        # Current price
        current_price = quote_data.get('current_price', 'N/A')
        if current_price != 'N/A':
            price_str = f"${current_price:.2f}"
        else:
            price_str = 'N/A'

        print(f"{Fore.WHITE}{Style.BRIGHT}Current Price: {Fore.YELLOW}{price_str}{Style.RESET_ALL}")

        # Change
        change = quote_data.get('change', 'N/A')
        change_percent = quote_data.get('change_percent', 'N/A')

        if change != 'N/A' and change_percent != 'N/A':
            if change >= 0:
                color = Fore.GREEN
                symbol = "▲"
            else:
                color = Fore.RED
                symbol = "▼"

            change_str = f"{symbol} ${abs(change):.2f} ({abs(change_percent):.2f}%)"
            print(f"{color}{Style.BRIGHT}{change_str}{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.WHITE}Change: N/A{Style.RESET_ALL}\n")

        # Trading day info
        print(f"{Fore.CYAN}--- Today's Trading ---{Style.RESET_ALL}")
        print(f"Open:       ${quote_data.get('open', 'N/A')}")
        print(f"High:       {Fore.GREEN}${quote_data.get('day_high', 'N/A')}{Style.RESET_ALL}")
        print(f"Low:        {Fore.RED}${quote_data.get('day_low', 'N/A')}{Style.RESET_ALL}")
        print(f"Prev Close: ${quote_data.get('previous_close', 'N/A')}\n")

        # Volume and market cap
        print(f"{Fore.CYAN}--- Market Data ---{Style.RESET_ALL}")
        volume = self.format_number(quote_data.get('volume', 'N/A'))
        market_cap = self.format_number(quote_data.get('market_cap', 'N/A'), prefix='$')
        print(f"Volume:     {volume}")
        print(f"Market Cap: {market_cap}\n")

        # 52-week range
        print(f"{Fore.CYAN}--- 52 Week Range ---{Style.RESET_ALL}")
        print(f"High: {Fore.GREEN}${quote_data.get('fifty_two_week_high', 'N/A')}{Style.RESET_ALL}")
        print(f"Low:  {Fore.RED}${quote_data.get('fifty_two_week_low', 'N/A')}{Style.RESET_ALL}\n")

        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("=" * 80)
        print(f"{Fore.WHITE}Last Updated: {timestamp}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Refreshing every {self.refresh_interval} seconds... (Press Ctrl+C to stop){Style.RESET_ALL}")
        print("=" * 80)

    def start_monitoring(self):
        """Start real-time monitoring loop."""
        print(f"\n{Fore.CYAN}Starting real-time monitoring for {self.symbol}...{Style.RESET_ALL}\n")

        try:
            while True:
                quote_data = self.fetcher.get_quote_info()
                if quote_data:
                    self.display_quote(quote_data)
                else:
                    print(f"{Fore.RED}Failed to fetch quote data{Style.RESET_ALL}")

                time.sleep(self.refresh_interval)

        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Monitoring stopped.{Style.RESET_ALL}\n")
