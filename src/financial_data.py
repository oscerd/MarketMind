"""
Financial Data Module
Fetches and processes company financial statements and metrics.
"""

import yfinance as yf
import pandas as pd
from typing import Dict, Any, Optional, List


class FinancialData:
    """Fetches financial statements and key metrics for stocks."""

    def __init__(self, symbol: str):
        """Initialize financial data fetcher.

        Args:
            symbol: Stock ticker symbol
        """
        self.symbol = symbol.upper()
        self.ticker = yf.Ticker(self.symbol)

    def get_income_statement(self, quarterly: bool = False) -> Dict[str, Any]:
        """Get income statement.

        Args:
            quarterly: If True, get quarterly data; otherwise annual

        Returns:
            Dictionary with income statement data
        """
        try:
            if quarterly:
                data = self.ticker.quarterly_income_stmt
            else:
                data = self.ticker.income_stmt

            if data.empty:
                return {'error': 'No income statement data available'}

            # Convert DataFrame to dict format
            result = self._dataframe_to_dict(data)
            return {
                'symbol': self.symbol,
                'period': 'quarterly' if quarterly else 'annual',
                'data': result,
                'description': 'Income statement showing revenue, expenses, and profitability'
            }
        except Exception as e:
            return {'error': str(e)}

    def get_balance_sheet(self, quarterly: bool = False) -> Dict[str, Any]:
        """Get balance sheet.

        Args:
            quarterly: If True, get quarterly data; otherwise annual

        Returns:
            Dictionary with balance sheet data
        """
        try:
            if quarterly:
                data = self.ticker.quarterly_balance_sheet
            else:
                data = self.ticker.balance_sheet

            if data.empty:
                return {'error': 'No balance sheet data available'}

            result = self._dataframe_to_dict(data)
            return {
                'symbol': self.symbol,
                'period': 'quarterly' if quarterly else 'annual',
                'data': result,
                'description': 'Balance sheet showing assets, liabilities, and equity'
            }
        except Exception as e:
            return {'error': str(e)}

    def get_cash_flow(self, quarterly: bool = False) -> Dict[str, Any]:
        """Get cash flow statement.

        Args:
            quarterly: If True, get quarterly data; otherwise annual

        Returns:
            Dictionary with cash flow data
        """
        try:
            if quarterly:
                data = self.ticker.quarterly_cashflow
            else:
                data = self.ticker.cashflow

            if data.empty:
                return {'error': 'No cash flow data available'}

            result = self._dataframe_to_dict(data)
            return {
                'symbol': self.symbol,
                'period': 'quarterly' if quarterly else 'annual',
                'data': result,
                'description': 'Cash flow statement showing operating, investing, and financing activities'
            }
        except Exception as e:
            return {'error': str(e)}

    def get_key_metrics(self) -> Dict[str, Any]:
        """Get key financial metrics and ratios.

        Returns:
            Dictionary with key financial metrics
        """
        try:
            info = self.ticker.info

            metrics = {
                'symbol': self.symbol,
                'valuation_metrics': {
                    'market_cap': info.get('marketCap', 'N/A'),
                    'enterprise_value': info.get('enterpriseValue', 'N/A'),
                    'pe_ratio': info.get('trailingPE', 'N/A'),
                    'forward_pe': info.get('forwardPE', 'N/A'),
                    'peg_ratio': info.get('pegRatio', 'N/A'),
                    'price_to_book': info.get('priceToBook', 'N/A'),
                    'price_to_sales': info.get('priceToSalesTrailing12Months', 'N/A'),
                    'ev_to_revenue': info.get('enterpriseToRevenue', 'N/A'),
                    'ev_to_ebitda': info.get('enterpriseToEbitda', 'N/A')
                },
                'profitability_metrics': {
                    'profit_margin': info.get('profitMargins', 'N/A'),
                    'operating_margin': info.get('operatingMargins', 'N/A'),
                    'return_on_assets': info.get('returnOnAssets', 'N/A'),
                    'return_on_equity': info.get('returnOnEquity', 'N/A'),
                    'gross_margin': info.get('grossMargins', 'N/A'),
                    'ebitda_margin': info.get('ebitdaMargins', 'N/A')
                },
                'financial_health': {
                    'current_ratio': info.get('currentRatio', 'N/A'),
                    'quick_ratio': info.get('quickRatio', 'N/A'),
                    'debt_to_equity': info.get('debtToEquity', 'N/A'),
                    'total_debt': info.get('totalDebt', 'N/A'),
                    'total_cash': info.get('totalCash', 'N/A'),
                    'free_cash_flow': info.get('freeCashflow', 'N/A'),
                    'operating_cash_flow': info.get('operatingCashflow', 'N/A')
                },
                'growth_metrics': {
                    'revenue_growth': info.get('revenueGrowth', 'N/A'),
                    'earnings_growth': info.get('earningsGrowth', 'N/A'),
                    'revenue_per_share': info.get('revenuePerShare', 'N/A'),
                    'earnings_per_share': info.get('trailingEps', 'N/A'),
                    'forward_eps': info.get('forwardEps', 'N/A')
                },
                'dividend_metrics': {
                    'dividend_rate': info.get('dividendRate', 'N/A'),
                    'dividend_yield': info.get('dividendYield', 'N/A'),
                    'payout_ratio': info.get('payoutRatio', 'N/A'),
                    'ex_dividend_date': info.get('exDividendDate', 'N/A')
                },
                'metrics_glossary': self._get_metrics_glossary()
            }

            return metrics
        except Exception as e:
            return {'error': str(e)}

    def get_earnings_history(self) -> Dict[str, Any]:
        """Get historical earnings data.

        Returns:
            Dictionary with earnings history
        """
        try:
            earnings = self.ticker.earnings_dates

            if earnings is None or earnings.empty:
                return {'error': 'No earnings history available'}

            result = []
            for idx, row in earnings.head(20).iterrows():
                result.append({
                    'date': idx.strftime('%Y-%m-%d') if hasattr(idx, 'strftime') else str(idx),
                    'eps_estimate': float(row.get('EPS Estimate', 0)) if pd.notna(row.get('EPS Estimate')) else None,
                    'reported_eps': float(row.get('Reported EPS', 0)) if pd.notna(row.get('Reported EPS')) else None,
                    'surprise_pct': float(row.get('Surprise(%)', 0)) if pd.notna(row.get('Surprise(%)')) else None
                })

            return {
                'symbol': self.symbol,
                'earnings_history': result,
                'description': 'Historical earnings reports with estimates vs actual'
            }
        except Exception as e:
            return {'error': str(e)}

    def get_next_earnings(self) -> Dict[str, Any]:
        """Get next earnings date and analyst estimates.

        Returns:
            Dictionary with next earnings information
        """
        try:
            calendar = self.ticker.calendar

            # Check if calendar data exists (can be dict, Series, or DataFrame)
            if calendar is None:
                return {'error': 'No earnings calendar data available'}

            # Handle both Series and dict formats
            if isinstance(calendar, dict):
                if not calendar:
                    return {'error': 'No earnings calendar data available'}
            elif hasattr(calendar, 'empty'):
                if calendar.empty:
                    return {'error': 'No earnings calendar data available'}

            result = {
                'symbol': self.symbol,
                'next_earnings_date': None,
                'earnings_estimate': {
                    'average': None,
                    'low': None,
                    'high': None
                },
                'revenue_estimate': {
                    'average': None,
                    'low': None,
                    'high': None
                },
                'description': 'Next scheduled earnings date with analyst estimates'
            }

            # Extract earnings date - handle both dict and Series
            calendar_keys = calendar.keys() if isinstance(calendar, dict) else calendar.index

            if 'Earnings Date' in calendar_keys:
                earnings_date = calendar['Earnings Date'] if isinstance(calendar, dict) else calendar.loc['Earnings Date']

                # Handle both single value and series
                if hasattr(earnings_date, 'iloc'):
                    earnings_date = earnings_date.iloc[0]

                # Handle if it's a list (sometimes yfinance returns [date1, date2])
                if isinstance(earnings_date, (list, tuple)) and len(earnings_date) > 0:
                    earnings_date = earnings_date[0]

                # Convert to string format
                if hasattr(earnings_date, 'strftime'):
                    # It's a datetime/date object
                    result['next_earnings_date'] = earnings_date.strftime('%Y-%m-%d')
                elif hasattr(earnings_date, 'date'):
                    # It's a Timestamp with a date() method
                    result['next_earnings_date'] = earnings_date.date().strftime('%Y-%m-%d')
                else:
                    # Fallback to string conversion and clean it up
                    date_str = str(earnings_date)
                    # Remove any list brackets or datetime.date() wrapper
                    import re
                    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date_str)
                    if date_match:
                        result['next_earnings_date'] = date_match.group(1)
                    else:
                        result['next_earnings_date'] = date_str

            # Extract earnings estimates
            if 'Earnings Average' in calendar_keys:
                val = calendar['Earnings Average'] if isinstance(calendar, dict) else calendar.loc['Earnings Average']
                result['earnings_estimate']['average'] = float(val.iloc[0] if hasattr(val, 'iloc') else val)
            if 'Earnings Low' in calendar_keys:
                val = calendar['Earnings Low'] if isinstance(calendar, dict) else calendar.loc['Earnings Low']
                result['earnings_estimate']['low'] = float(val.iloc[0] if hasattr(val, 'iloc') else val)
            if 'Earnings High' in calendar_keys:
                val = calendar['Earnings High'] if isinstance(calendar, dict) else calendar.loc['Earnings High']
                result['earnings_estimate']['high'] = float(val.iloc[0] if hasattr(val, 'iloc') else val)

            # Extract revenue estimates
            if 'Revenue Average' in calendar_keys:
                val = calendar['Revenue Average'] if isinstance(calendar, dict) else calendar.loc['Revenue Average']
                result['revenue_estimate']['average'] = float(val.iloc[0] if hasattr(val, 'iloc') else val)
            if 'Revenue Low' in calendar_keys:
                val = calendar['Revenue Low'] if isinstance(calendar, dict) else calendar.loc['Revenue Low']
                result['revenue_estimate']['low'] = float(val.iloc[0] if hasattr(val, 'iloc') else val)
            if 'Revenue High' in calendar_keys:
                val = calendar['Revenue High'] if isinstance(calendar, dict) else calendar.loc['Revenue High']
                result['revenue_estimate']['high'] = float(val.iloc[0] if hasattr(val, 'iloc') else val)

            return result

        except Exception as e:
            return {'error': str(e)}

    def get_financial_summary(self) -> Dict[str, Any]:
        """Get a comprehensive financial summary.

        Returns:
            Dictionary with financial summary
        """
        try:
            info = self.ticker.info

            summary = {
                'symbol': self.symbol,
                'company_name': info.get('longName', 'N/A'),
                'revenue': {
                    'total_revenue': info.get('totalRevenue', 'N/A'),
                    'revenue_per_share': info.get('revenuePerShare', 'N/A'),
                    'revenue_growth': self._format_percentage(info.get('revenueGrowth'))
                },
                'profitability': {
                    'net_income': info.get('netIncomeToCommon', 'N/A'),
                    'earnings_per_share': info.get('trailingEps', 'N/A'),
                    'profit_margin': self._format_percentage(info.get('profitMargins')),
                    'operating_margin': self._format_percentage(info.get('operatingMargins'))
                },
                'balance_sheet': {
                    'total_assets': info.get('totalAssets', 'N/A'),
                    'total_debt': info.get('totalDebt', 'N/A'),
                    'total_cash': info.get('totalCash', 'N/A'),
                    'book_value_per_share': info.get('bookValue', 'N/A')
                },
                'cash_flow': {
                    'operating_cash_flow': info.get('operatingCashflow', 'N/A'),
                    'free_cash_flow': info.get('freeCashflow', 'N/A')
                },
                'key_ratios': {
                    'pe_ratio': info.get('trailingPE', 'N/A'),
                    'price_to_book': info.get('priceToBook', 'N/A'),
                    'return_on_equity': self._format_percentage(info.get('returnOnEquity')),
                    'return_on_assets': self._format_percentage(info.get('returnOnAssets')),
                    'current_ratio': info.get('currentRatio', 'N/A'),
                    'debt_to_equity': info.get('debtToEquity', 'N/A')
                }
            }

            return summary
        except Exception as e:
            return {'error': str(e)}

    def _dataframe_to_dict(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Convert financial DataFrame to dictionary format.

        Args:
            df: Pandas DataFrame

        Returns:
            Dictionary representation
        """
        result = {}

        for col in df.columns:
            date_key = col.strftime('%Y-%m-%d') if hasattr(col, 'strftime') else str(col)
            result[date_key] = {}

            for idx in df.index:
                value = df.loc[idx, col]
                if pd.notna(value):
                    result[date_key][str(idx)] = float(value) if isinstance(value, (int, float)) else str(value)

        return result

    def _format_percentage(self, value: Optional[float]) -> str:
        """Format a decimal value as percentage.

        Args:
            value: Decimal value

        Returns:
            Formatted percentage string
        """
        if value is None or pd.isna(value):
            return 'N/A'
        return f"{float(value) * 100:.2f}%"

    def _get_metrics_glossary(self) -> Dict[str, str]:
        """Get descriptions for financial metrics.

        Returns:
            Dictionary with metric descriptions
        """
        return {
            'valuation_metrics': {
                'market_cap': 'Total market value of company\'s outstanding shares',
                'enterprise_value': 'Total value of company including debt, minus cash',
                'pe_ratio': 'Price-to-Earnings ratio. Price per share divided by earnings per share',
                'forward_pe': 'P/E ratio using forecasted earnings',
                'peg_ratio': 'P/E ratio adjusted for earnings growth rate',
                'price_to_book': 'Share price divided by book value per share',
                'price_to_sales': 'Market cap divided by total revenue',
                'ev_to_revenue': 'Enterprise Value divided by revenue',
                'ev_to_ebitda': 'Enterprise Value divided by EBITDA'
            },
            'profitability_metrics': {
                'profit_margin': 'Net income as percentage of revenue',
                'operating_margin': 'Operating income as percentage of revenue',
                'return_on_assets': 'Net income divided by total assets',
                'return_on_equity': 'Net income divided by shareholder equity',
                'gross_margin': 'Gross profit as percentage of revenue',
                'ebitda_margin': 'EBITDA as percentage of revenue'
            },
            'financial_health': {
                'current_ratio': 'Current assets divided by current liabilities',
                'quick_ratio': 'Liquid assets divided by current liabilities',
                'debt_to_equity': 'Total debt divided by shareholder equity',
                'total_debt': 'Sum of short-term and long-term debt',
                'total_cash': 'Cash and cash equivalents',
                'free_cash_flow': 'Operating cash flow minus capital expenditures',
                'operating_cash_flow': 'Cash generated from operations'
            },
            'growth_metrics': {
                'revenue_growth': 'Year-over-year revenue growth rate',
                'earnings_growth': 'Year-over-year earnings growth rate',
                'revenue_per_share': 'Total revenue divided by shares outstanding',
                'earnings_per_share': 'Net income divided by shares outstanding',
                'forward_eps': 'Forecasted earnings per share'
            },
            'dividend_metrics': {
                'dividend_rate': 'Annual dividend payment per share',
                'dividend_yield': 'Annual dividend as percentage of share price',
                'payout_ratio': 'Dividends divided by earnings',
                'ex_dividend_date': 'Date after which stock trades without dividend'
            }
        }
