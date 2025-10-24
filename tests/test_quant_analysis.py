"""
Tests for quant_analysis module
"""

import pytest
import pandas as pd
import numpy as np
from src.quant_analysis import QuantAnalysis


class TestQuantAnalysis:
    """Test QuantAnalysis class"""

    def test_init_with_data(self, sample_stock_data):
        """Test QuantAnalysis initialization with valid data"""
        qa = QuantAnalysis('TEST', sample_stock_data)
        assert qa.symbol == 'TEST'
        assert not qa.data.empty
        assert 'Returns' in qa.data.columns

    def test_init_with_benchmark(self, sample_stock_data):
        """Test QuantAnalysis initialization with benchmark"""
        benchmark_data = sample_stock_data.copy()
        qa = QuantAnalysis('TEST', sample_stock_data, benchmark_data)

        assert qa.benchmark_data is not None
        assert 'Returns' in qa.benchmark_data.columns

    def test_calculate_returns_metrics(self, sample_stock_data):
        """Test calculate_returns_metrics"""
        qa = QuantAnalysis('TEST', sample_stock_data)
        metrics = qa.calculate_returns_metrics()

        assert 'total_return_pct' in metrics
        assert 'annualized_return_pct' in metrics
        assert 'annualized_volatility_pct' in metrics
        assert 'daily_return_mean_pct' in metrics
        assert 'max_return_pct' in metrics
        assert 'min_return_pct' in metrics

        # Check that values are reasonable
        assert isinstance(metrics['total_return_pct'], float)
        assert isinstance(metrics['annualized_volatility_pct'], float)

    def test_calculate_returns_metrics_insufficient_data(self):
        """Test calculate_returns_metrics with insufficient data"""
        # Create a DataFrame with only 1 row
        df = pd.DataFrame({
            'Close': [100]
        }, index=[pd.Timestamp.now()])

        qa = QuantAnalysis('TEST', df)
        metrics = qa.calculate_returns_metrics()

        assert 'error' in metrics

    def test_calculate_sharpe_ratio(self, sample_stock_data):
        """Test Sharpe ratio calculation"""
        qa = QuantAnalysis('TEST', sample_stock_data)
        sharpe = qa.calculate_sharpe_ratio(risk_free_rate=0.02)

        assert isinstance(sharpe, float)
        # Sharpe ratio should be a reasonable value
        assert -5 < sharpe < 10

    def test_calculate_sortino_ratio(self, sample_stock_data):
        """Test Sortino ratio calculation"""
        qa = QuantAnalysis('TEST', sample_stock_data)
        sortino = qa.calculate_sortino_ratio(risk_free_rate=0.02)

        assert isinstance(sortino, float)

    def test_calculate_beta_alpha_with_benchmark(self, sample_stock_data):
        """Test Beta and Alpha calculation with benchmark"""
        benchmark_data = sample_stock_data.copy()
        # Add some variation to benchmark
        benchmark_data['Close'] = benchmark_data['Close'] * 0.95

        qa = QuantAnalysis('TEST', sample_stock_data, benchmark_data)
        result = qa.calculate_beta_alpha()

        assert 'beta' in result
        assert 'alpha' in result
        assert 'interpretation' in result
        assert isinstance(result['beta'], float)
        assert isinstance(result['alpha'], float)

    def test_calculate_beta_alpha_no_benchmark(self, sample_stock_data):
        """Test Beta and Alpha calculation without benchmark"""
        qa = QuantAnalysis('TEST', sample_stock_data)
        result = qa.calculate_beta_alpha()

        assert 'error' in result

    def test_calculate_var(self, sample_stock_data):
        """Test Value at Risk calculation"""
        qa = QuantAnalysis('TEST', sample_stock_data)
        var_result = qa.calculate_var(confidence_level=0.95, time_horizon=1)

        assert 'confidence_level' in var_result
        assert 'time_horizon_days' in var_result
        assert 'historical_var_pct' in var_result
        assert 'parametric_var_pct' in var_result
        assert 'interpretation' in var_result

        assert var_result['confidence_level'] == 0.95
        assert var_result['time_horizon_days'] == 1

    def test_calculate_cvar(self, sample_stock_data):
        """Test Conditional VaR calculation"""
        qa = QuantAnalysis('TEST', sample_stock_data)
        cvar = qa.calculate_cvar(confidence_level=0.95)

        assert isinstance(cvar, float)
        # CVaR should be negative (representing loss)
        assert cvar < 0

    def test_calculate_max_drawdown(self, sample_stock_data):
        """Test maximum drawdown calculation"""
        qa = QuantAnalysis('TEST', sample_stock_data)
        drawdown = qa.calculate_max_drawdown()

        assert 'max_drawdown_pct' in drawdown
        assert 'peak_date' in drawdown
        assert 'trough_date' in drawdown
        assert 'current_drawdown_pct' in drawdown

        # Max drawdown should be negative
        assert drawdown['max_drawdown_pct'] < 0

    def test_calculate_information_ratio_with_benchmark(self, sample_stock_data):
        """Test Information Ratio calculation with benchmark"""
        benchmark_data = sample_stock_data.copy()
        qa = QuantAnalysis('TEST', sample_stock_data, benchmark_data)
        ir = qa.calculate_information_ratio()

        assert isinstance(ir, float)

    def test_calculate_information_ratio_no_benchmark(self, sample_stock_data):
        """Test Information Ratio calculation without benchmark"""
        qa = QuantAnalysis('TEST', sample_stock_data)
        ir = qa.calculate_information_ratio()

        assert ir == 0.0

    def test_generate_recommendation(self, sample_stock_data):
        """Test investment recommendation generation"""
        benchmark_data = sample_stock_data.copy()
        qa = QuantAnalysis('TEST', sample_stock_data, benchmark_data)
        recommendation = qa.generate_recommendation(risk_free_rate=0.02)

        assert 'recommendation' in recommendation
        assert 'confidence' in recommendation
        assert 'score' in recommendation
        assert 'action' in recommendation
        assert 'positive_signals' in recommendation
        assert 'risk_warnings' in recommendation
        assert 'summary' in recommendation
        assert 'disclaimer' in recommendation

        # Recommendation should be one of the valid values
        valid_recommendations = ['STRONG BUY', 'BUY', 'HOLD', 'SELL', 'STRONG SELL']
        assert recommendation['recommendation'] in valid_recommendations

        # Score should be an integer
        assert isinstance(recommendation['score'], int)

    def test_get_comprehensive_analysis(self, sample_stock_data):
        """Test comprehensive analysis"""
        benchmark_data = sample_stock_data.copy()
        qa = QuantAnalysis('TEST', sample_stock_data, benchmark_data)
        analysis = qa.get_comprehensive_analysis(risk_free_rate=0.02)

        assert 'symbol' in analysis
        assert 'analysis_period' in analysis
        assert 'returns' in analysis
        assert 'risk_metrics' in analysis
        assert 'market_metrics' in analysis
        assert 'recommendation' in analysis
        assert 'metrics_glossary' in analysis

        # Check analysis period
        assert 'start_date' in analysis['analysis_period']
        assert 'end_date' in analysis['analysis_period']
        assert 'trading_days' in analysis['analysis_period']

        # Check risk metrics
        assert 'sharpe_ratio' in analysis['risk_metrics']
        assert 'sortino_ratio' in analysis['risk_metrics']
        assert 'var_95' in analysis['risk_metrics']
        assert 'max_drawdown' in analysis['risk_metrics']

        # Check metrics glossary
        assert 'returns' in analysis['metrics_glossary']
        assert 'risk_metrics' in analysis['metrics_glossary']
        assert 'interpretation_guide' in analysis['metrics_glossary']

    def test_empty_data(self):
        """Test handling of empty data"""
        df = pd.DataFrame()
        qa = QuantAnalysis('TEST', df)

        metrics = qa.calculate_returns_metrics()
        assert 'error' in metrics

        sharpe = qa.calculate_sharpe_ratio()
        assert sharpe == 0.0

    def test_symbol_uppercase(self, sample_stock_data):
        """Test that symbol is converted to uppercase"""
        qa = QuantAnalysis('test', sample_stock_data)
        assert qa.symbol == 'TEST'
