"""
Tests for financial_data module
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from src.financial_data import FinancialData


class TestFinancialData:
    """Test FinancialData class"""

    def test_init(self):
        """Test FinancialData initialization"""
        fd = FinancialData('AAPL')
        assert fd.symbol == 'AAPL'
        assert fd.ticker is not None

    def test_symbol_uppercase(self):
        """Test that symbols are converted to uppercase"""
        fd = FinancialData('aapl')
        assert fd.symbol == 'AAPL'

    @patch('src.financial_data.yf.Ticker')
    def test_get_next_earnings_with_dict(self, mock_ticker, sample_calendar_dict):
        """Test get_next_earnings with dictionary calendar"""
        mock_ticker_instance = Mock()
        mock_ticker_instance.calendar = sample_calendar_dict
        mock_ticker.return_value = mock_ticker_instance

        fd = FinancialData('TEST')
        result = fd.get_next_earnings()

        assert result['symbol'] == 'TEST'
        assert result['next_earnings_date'] is not None
        assert result['earnings_estimate']['average'] == 1.60
        assert result['earnings_estimate']['low'] == 1.55
        assert result['earnings_estimate']['high'] == 1.65
        assert result['revenue_estimate']['average'] == 89500000000

    @patch('src.financial_data.yf.Ticker')
    def test_get_next_earnings_with_series(self, mock_ticker, sample_calendar_series):
        """Test get_next_earnings with pandas Series calendar"""
        mock_ticker_instance = Mock()
        mock_ticker_instance.calendar = sample_calendar_series
        mock_ticker.return_value = mock_ticker_instance

        fd = FinancialData('TEST')
        result = fd.get_next_earnings()

        assert result['symbol'] == 'TEST'
        assert result['next_earnings_date'] is not None
        assert result['earnings_estimate']['average'] == 1.60

    @patch('src.financial_data.yf.Ticker')
    def test_get_next_earnings_no_data(self, mock_ticker):
        """Test get_next_earnings with no calendar data"""
        mock_ticker_instance = Mock()
        mock_ticker_instance.calendar = None
        mock_ticker.return_value = mock_ticker_instance

        fd = FinancialData('TEST')
        result = fd.get_next_earnings()

        assert 'error' in result
        assert result['error'] == 'No earnings calendar data available'

    @patch('src.financial_data.yf.Ticker')
    def test_get_next_earnings_empty_dict(self, mock_ticker):
        """Test get_next_earnings with empty dictionary"""
        mock_ticker_instance = Mock()
        mock_ticker_instance.calendar = {}
        mock_ticker.return_value = mock_ticker_instance

        fd = FinancialData('TEST')
        result = fd.get_next_earnings()

        assert 'error' in result

    @patch('src.financial_data.yf.Ticker')
    def test_get_earnings_history_success(self, mock_ticker, sample_earnings_data):
        """Test get_earnings_history with valid data"""
        import pandas as pd

        # Create mock earnings dates DataFrame
        dates = pd.date_range(end=datetime.now(), periods=5, freq='QE')
        mock_df = pd.DataFrame({
            'EPS Estimate': [1.5, 1.6, 1.7, 1.8, 1.9],
            'Reported EPS': [1.55, 1.65, 1.68, None, None],
            'Surprise(%)': [3.3, 3.1, -1.2, None, None]
        }, index=dates)

        mock_ticker_instance = Mock()
        mock_ticker_instance.earnings_dates = mock_df
        mock_ticker.return_value = mock_ticker_instance

        fd = FinancialData('TEST')
        result = fd.get_earnings_history()

        assert result['symbol'] == 'TEST'
        assert len(result['earnings_history']) == 5
        assert result['earnings_history'][0]['eps_estimate'] == 1.5

    @patch('src.financial_data.yf.Ticker')
    def test_get_earnings_history_no_data(self, mock_ticker):
        """Test get_earnings_history with no data"""
        import pandas as pd

        mock_ticker_instance = Mock()
        mock_ticker_instance.earnings_dates = pd.DataFrame()
        mock_ticker.return_value = mock_ticker_instance

        fd = FinancialData('TEST')
        result = fd.get_earnings_history()

        assert 'error' in result

    @patch('src.financial_data.yf.Ticker')
    def test_get_key_metrics_success(self, mock_ticker, sample_financial_metrics):
        """Test get_key_metrics with valid data"""
        mock_ticker_instance = Mock()
        mock_ticker_instance.info = {
            'marketCap': 500000000000,
            'trailingPE': 25.5,
            'priceToBook': 5.2,
            'profitMargins': 0.25,
            'returnOnEquity': 0.45,
            'currentRatio': 1.5,
            'revenueGrowth': 0.15
        }
        mock_ticker.return_value = mock_ticker_instance

        fd = FinancialData('TEST')
        result = fd.get_key_metrics()

        assert result['symbol'] == 'TEST'
        assert 'valuation_metrics' in result
        assert 'profitability_metrics' in result
        assert 'financial_health' in result
        assert 'metrics_glossary' in result
        assert result['valuation_metrics']['market_cap'] == 500000000000

    @patch('src.financial_data.yf.Ticker')
    def test_get_financial_summary_success(self, mock_ticker):
        """Test get_financial_summary with valid data"""
        mock_ticker_instance = Mock()
        mock_ticker_instance.info = {
            'longName': 'Test Company Inc.',
            'totalRevenue': 100000000000,
            'revenuePerShare': 50.0,
            'revenueGrowth': 0.15,
            'netIncomeToCommon': 25000000000,
            'trailingEps': 5.0,
            'profitMargins': 0.25,
            'trailingPE': 20.0,
            'returnOnEquity': 0.30
        }
        mock_ticker.return_value = mock_ticker_instance

        fd = FinancialData('TEST')
        result = fd.get_financial_summary()

        assert result['symbol'] == 'TEST'
        assert result['company_name'] == 'Test Company Inc.'
        assert 'revenue' in result
        assert 'profitability' in result
        assert 'key_ratios' in result

    def test_format_percentage(self):
        """Test _format_percentage method"""
        fd = FinancialData('TEST')

        assert fd._format_percentage(0.25) == "25.00%"
        assert fd._format_percentage(0.1234) == "12.34%"
        assert fd._format_percentage(None) == "N/A"
        assert fd._format_percentage(float('nan')) == "N/A"

    def test_get_metrics_glossary(self):
        """Test _get_metrics_glossary method"""
        fd = FinancialData('TEST')
        glossary = fd._get_metrics_glossary()

        assert 'valuation_metrics' in glossary
        assert 'profitability_metrics' in glossary
        assert 'financial_health' in glossary
        assert 'growth_metrics' in glossary
        assert 'dividend_metrics' in glossary

        # Check that descriptions exist
        assert 'market_cap' in glossary['valuation_metrics']
        assert 'profit_margin' in glossary['profitability_metrics']
