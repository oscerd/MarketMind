"""
Pytest configuration and shared fixtures
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


@pytest.fixture
def sample_stock_data():
    """Generate sample stock price data for testing."""
    dates = pd.date_range(end=datetime.now(), periods=252, freq='D')
    np.random.seed(42)

    # Generate realistic price data
    prices = 100 + np.cumsum(np.random.randn(252) * 2)
    prices = np.maximum(prices, 50)  # Ensure prices don't go too low

    df = pd.DataFrame({
        'Open': prices + np.random.randn(252) * 0.5,
        'High': prices + np.abs(np.random.randn(252) * 1),
        'Low': prices - np.abs(np.random.randn(252) * 1),
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, 252)
    }, index=dates)

    return df


@pytest.fixture
def sample_earnings_data():
    """Generate sample earnings data for testing."""
    dates = pd.date_range(end=datetime.now(), periods=8, freq='QE')

    data = []
    for date in dates:
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'eps_estimate': round(np.random.uniform(1.0, 3.0), 2),
            'reported_eps': round(np.random.uniform(1.0, 3.0), 2),
            'surprise_pct': round(np.random.uniform(-5, 10), 2)
        })

    return data


@pytest.fixture
def sample_quote_info():
    """Generate sample quote information for testing."""
    return {
        'symbol': 'TEST',
        'name': 'Test Company Inc.',
        'current_price': 150.25,
        'previous_close': 148.50,
        'open': 149.00,
        'day_high': 151.50,
        'day_low': 148.75,
        'volume': 5000000,
        'market_cap': 500000000000,
        'fifty_two_week_high': 160.00,
        'fifty_two_week_low': 120.00,
        'change': 1.75,
        'change_percent': 1.18
    }


@pytest.fixture
def sample_search_info():
    """Generate sample search information for testing."""
    return {
        'symbol': 'TEST',
        'name': 'Test Company Inc.',
        'exchange': 'NASDAQ',
        'quote_type': 'EQUITY',
        'currency': 'USD',
        'market_cap': 500000000000,
        'sector': 'Technology',
        'industry': 'Software',
        'country': 'United States',
        'website': 'https://test.com',
        'description': 'Test Company is a leading technology company.'
    }


@pytest.fixture
def sample_financial_metrics():
    """Generate sample financial metrics for testing."""
    return {
        'symbol': 'TEST',
        'valuation_metrics': {
            'market_cap': 500000000000,
            'pe_ratio': 25.5,
            'price_to_book': 5.2,
            'price_to_sales': 3.5
        },
        'profitability_metrics': {
            'profit_margin': 0.25,
            'operating_margin': 0.30,
            'return_on_equity': 0.45,
            'return_on_assets': 0.15
        },
        'financial_health': {
            'current_ratio': 1.5,
            'quick_ratio': 1.2,
            'debt_to_equity': 0.5,
            'free_cash_flow': 10000000000
        }
    }


@pytest.fixture
def sample_calendar_dict():
    """Generate sample earnings calendar as dictionary."""
    next_date = datetime.now() + timedelta(days=30)
    return {
        'Earnings Date': next_date.date(),
        'Earnings Average': 1.60,
        'Earnings Low': 1.55,
        'Earnings High': 1.65,
        'Revenue Average': 89500000000,
        'Revenue Low': 88000000000,
        'Revenue High': 91000000000
    }


@pytest.fixture
def sample_calendar_series():
    """Generate sample earnings calendar as pandas Series."""
    import pandas as pd
    next_date = datetime.now() + timedelta(days=30)
    return pd.Series({
        'Earnings Date': next_date.date(),
        'Earnings Average': 1.60,
        'Earnings Low': 1.55,
        'Earnings High': 1.65,
        'Revenue Average': 89500000000,
        'Revenue Low': 88000000000,
        'Revenue High': 91000000000
    })
