import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List


class StockFetcher:
    """Fetches stock data from Yahoo Finance."""

    def __init__(self, symbol: str):
        """Initialize the stock fetcher with a symbol.

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        """
        self.symbol = symbol.upper()
        self.ticker = yf.Ticker(self.symbol)

    def get_current_price(self) -> Optional[float]:
        """Get the current/latest stock price.

        Returns:
            Current price as float, or None if unavailable
        """
        try:
            data = self.ticker.history(period='1d', interval='1m')
            if not data.empty:
                return data['Close'].iloc[-1]
            return None
        except Exception as e:
            print(f"Error fetching current price: {e}")
            return None

    def get_quote_info(self) -> Dict[str, Any]:
        """Get detailed quote information.

        Returns:
            Dictionary containing quote details
        """
        try:
            info = self.ticker.info
            current_price = self.get_current_price()

            quote_data = {
                'symbol': self.symbol,
                'name': info.get('longName', 'N/A'),
                'current_price': current_price,
                'previous_close': info.get('previousClose', 'N/A'),
                'open': info.get('open', 'N/A'),
                'day_high': info.get('dayHigh', 'N/A'),
                'day_low': info.get('dayLow', 'N/A'),
                'volume': info.get('volume', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
            }

            # Calculate change
            if current_price and quote_data['previous_close'] != 'N/A':
                change = current_price - quote_data['previous_close']
                change_percent = (change / quote_data['previous_close']) * 100
                quote_data['change'] = change
                quote_data['change_percent'] = change_percent
            else:
                quote_data['change'] = 'N/A'
                quote_data['change_percent'] = 'N/A'

            return quote_data
        except Exception as e:
            print(f"Error fetching quote info: {e}")
            return {}

    def get_historical_data(self, period: str = '1mo', interval: str = '1d') -> pd.DataFrame:
        """Get historical stock data.

        Args:
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
            interval: Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1d', '5d', '1wk', '1mo', '3mo')

        Returns:
            DataFrame with historical data
        """
        try:
            data = self.ticker.history(period=period, interval=interval)
            return data
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return pd.DataFrame()

    @staticmethod
    def search_ticker(query: str) -> Dict[str, Any]:
        """Search for a ticker symbol and return its information.

        Args:
            query: Ticker symbol to search for

        Returns:
            Dictionary containing ticker information if found, empty dict otherwise
        """
        try:
            ticker = yf.Ticker(query.upper())
            info = ticker.info

            # Check if ticker is valid by looking for key fields
            if not info or 'symbol' not in info:
                return {}

            # Extract relevant information
            result = {
                'symbol': info.get('symbol', query.upper()),
                'name': info.get('longName', info.get('shortName', 'N/A')),
                'exchange': info.get('exchange', 'N/A'),
                'quote_type': info.get('quoteType', 'N/A'),
                'currency': info.get('currency', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'country': info.get('country', 'N/A'),
                'website': info.get('website', 'N/A'),
                'description': info.get('longBusinessSummary', 'N/A'),
            }

            return result
        except Exception as e:
            return {}

    @staticmethod
    def search_multiple(queries: List[str]) -> List[Dict[str, Any]]:
        """Search for multiple ticker symbols.

        Args:
            queries: List of ticker symbols to search for

        Returns:
            List of dictionaries containing ticker information
        """
        results = []
        for query in queries:
            result = StockFetcher.search_ticker(query)
            if result:
                results.append(result)
        return results

    def get_analyst_recommendations(self) -> pd.DataFrame:
        """Get analyst recommendations and upgrades/downgrades.

        Returns:
            DataFrame with recommendation history
        """
        try:
            # Get upgrades/downgrades
            upgrades_downgrades = self.ticker.upgrades_downgrades
            if upgrades_downgrades is not None and not upgrades_downgrades.empty:
                return upgrades_downgrades
            return pd.DataFrame()
        except Exception as e:
            print(f"Error fetching analyst recommendations: {e}")
            return pd.DataFrame()

    def get_recommendations_summary(self) -> Dict[str, Any]:
        """Get summary of current analyst recommendations.

        Returns:
            Dictionary with recommendation counts
        """
        try:
            info = self.ticker.info
            recommendations = {
                'strong_buy': info.get('recommendationKey', 'N/A'),
                'target_mean': info.get('targetMeanPrice', 'N/A'),
                'target_high': info.get('targetHighPrice', 'N/A'),
                'target_low': info.get('targetLowPrice', 'N/A'),
                'num_analysts': info.get('numberOfAnalystOpinions', 'N/A'),
                'recommendation_mean': info.get('recommendationMean', 'N/A'),
            }
            return recommendations
        except Exception as e:
            return {}

    @staticmethod
    def get_market_analyst_changes(symbols: List[str], days_back: int = 1) -> List[Dict[str, Any]]:
        """Get analyst changes across multiple stocks.

        Args:
            symbols: List of stock symbols to check
            days_back: Number of days to look back (default: 1 for today)

        Returns:
            List of dictionaries containing analyst changes
        """
        from datetime import datetime, timedelta

        changes = []
        cutoff_date = datetime.now() - timedelta(days=days_back)

        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                recommendations = ticker.upgrades_downgrades

                if recommendations is not None and not recommendations.empty:
                    # Filter for recent changes
                    for idx, row in recommendations.iterrows():
                        if hasattr(idx, 'to_pydatetime'):
                            rec_date = idx.to_pydatetime()
                        else:
                            continue

                        if rec_date >= cutoff_date:
                            changes.append({
                                'symbol': symbol,
                                'date': rec_date,
                                'firm': row.get('Firm', 'Unknown'),
                                'action': row.get('Action', 'N/A'),
                                'from_grade': row.get('FromGrade', 'N/A'),
                                'to_grade': row.get('ToGrade', 'N/A')
                            })
            except Exception:
                # Skip symbols that fail
                continue

        # Sort by date (most recent first)
        changes.sort(key=lambda x: x['date'], reverse=True)
        return changes
