"""
Quantitative Finance Analysis Module
Provides financial metrics and quantitative analysis for stocks.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class QuantAnalysis:
    """Performs quantitative financial analysis on stock data."""

    def __init__(self, symbol: str, stock_data: pd.DataFrame, benchmark_data: Optional[pd.DataFrame] = None):
        """Initialize quantitative analysis.

        Args:
            symbol: Stock ticker symbol
            stock_data: DataFrame with historical stock data (OHLCV)
            benchmark_data: Optional DataFrame with benchmark data (e.g., S&P 500)
        """
        self.symbol = symbol.upper()
        self.data = stock_data.copy()
        self.benchmark_data = benchmark_data.copy() if benchmark_data is not None else None

        # Calculate returns
        if not self.data.empty:
            self.data['Returns'] = self.data['Close'].pct_change()
            self.data['Log_Returns'] = np.log(self.data['Close'] / self.data['Close'].shift(1))

        if self.benchmark_data is not None and not self.benchmark_data.empty:
            self.benchmark_data['Returns'] = self.benchmark_data['Close'].pct_change()
            self.benchmark_data['Log_Returns'] = np.log(
                self.benchmark_data['Close'] / self.benchmark_data['Close'].shift(1)
            )

    def calculate_returns_metrics(self) -> Dict[str, Any]:
        """Calculate return-based metrics.

        Returns:
            Dictionary with return metrics
        """
        if self.data.empty or len(self.data) < 2:
            return {'error': 'Insufficient data'}

        returns = self.data['Returns'].dropna()

        # Calculate various return metrics
        total_return = (self.data['Close'].iloc[-1] / self.data['Close'].iloc[0] - 1) * 100
        avg_daily_return = returns.mean() * 100
        std_daily_return = returns.std() * 100

        # Annualized metrics (assuming 252 trading days)
        annualized_return = avg_daily_return * 252
        annualized_volatility = std_daily_return * np.sqrt(252)

        # Cumulative returns
        cumulative_returns = (1 + returns).cumprod() - 1

        return {
            'total_return_pct': float(total_return),
            'daily_return_mean_pct': float(avg_daily_return),
            'daily_return_std_pct': float(std_daily_return),
            'annualized_return_pct': float(annualized_return),
            'annualized_volatility_pct': float(annualized_volatility),
            'max_return_pct': float(returns.max() * 100),
            'min_return_pct': float(returns.min() * 100),
            'cumulative_return_pct': float(cumulative_returns.iloc[-1] * 100)
        }

    def calculate_sharpe_ratio(self, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio.

        Args:
            risk_free_rate: Annual risk-free rate (default: 2%)

        Returns:
            Sharpe ratio
        """
        if self.data.empty or len(self.data) < 2:
            return 0.0

        returns = self.data['Returns'].dropna()

        # Annualized returns and volatility
        avg_return = returns.mean() * 252
        volatility = returns.std() * np.sqrt(252)

        if volatility == 0:
            return 0.0

        sharpe = (avg_return - risk_free_rate) / volatility
        return float(sharpe)

    def calculate_sortino_ratio(self, risk_free_rate: float = 0.02, target_return: float = 0) -> float:
        """Calculate Sortino ratio (focuses on downside risk).

        Args:
            risk_free_rate: Annual risk-free rate (default: 2%)
            target_return: Target return threshold

        Returns:
            Sortino ratio
        """
        if self.data.empty or len(self.data) < 2:
            return 0.0

        returns = self.data['Returns'].dropna()

        # Annualized return
        avg_return = returns.mean() * 252

        # Downside deviation (only negative returns)
        downside_returns = returns[returns < target_return]
        downside_std = downside_returns.std() * np.sqrt(252)

        if downside_std == 0:
            return 0.0

        sortino = (avg_return - risk_free_rate) / downside_std
        return float(sortino)

    def calculate_beta_alpha(self) -> Dict[str, float]:
        """Calculate Beta and Alpha relative to benchmark.

        Returns:
            Dictionary with beta and alpha
        """
        if self.benchmark_data is None or self.data.empty or self.benchmark_data.empty:
            return {'beta': 0.0, 'alpha': 0.0, 'error': 'No benchmark data available'}

        # Align data by date
        stock_returns = self.data['Returns'].dropna()
        benchmark_returns = self.benchmark_data['Returns'].dropna()

        # Find common dates
        common_dates = stock_returns.index.intersection(benchmark_returns.index)
        if len(common_dates) < 2:
            return {'beta': 0.0, 'alpha': 0.0, 'error': 'Insufficient overlapping data'}

        stock_returns = stock_returns.loc[common_dates]
        benchmark_returns = benchmark_returns.loc[common_dates]

        # Calculate beta (covariance / variance)
        covariance = np.cov(stock_returns, benchmark_returns)[0][1]
        benchmark_variance = np.var(benchmark_returns)

        if benchmark_variance == 0:
            return {'beta': 0.0, 'alpha': 0.0}

        beta = covariance / benchmark_variance

        # Calculate alpha (annualized)
        stock_avg_return = stock_returns.mean() * 252
        benchmark_avg_return = benchmark_returns.mean() * 252
        alpha = stock_avg_return - (beta * benchmark_avg_return)

        return {
            'beta': float(beta),
            'alpha': float(alpha),
            'interpretation': {
                'beta': 'Less volatile than market' if beta < 1 else 'More volatile than market' if beta > 1 else 'Same volatility as market',
                'alpha': 'Outperforming market' if alpha > 0 else 'Underperforming market' if alpha < 0 else 'Matching market'
            }
        }

    def calculate_var(self, confidence_level: float = 0.95, time_horizon: int = 1) -> Dict[str, float]:
        """Calculate Value at Risk (VaR).

        Args:
            confidence_level: Confidence level (default: 95%)
            time_horizon: Time horizon in days (default: 1)

        Returns:
            Dictionary with VaR metrics
        """
        if self.data.empty or len(self.data) < 2:
            return {'error': 'Insufficient data'}

        returns = self.data['Returns'].dropna()

        # Historical VaR
        var_percentile = (1 - confidence_level) * 100
        historical_var = np.percentile(returns, var_percentile) * 100

        # Parametric VaR (assumes normal distribution)
        mean_return = returns.mean()
        std_return = returns.std()
        z_score = np.abs(np.percentile(np.random.standard_normal(10000), var_percentile))
        parametric_var = (mean_return - z_score * std_return) * 100

        # Scale for time horizon
        scaled_historical_var = historical_var * np.sqrt(time_horizon)
        scaled_parametric_var = parametric_var * np.sqrt(time_horizon)

        return {
            'confidence_level': confidence_level,
            'time_horizon_days': time_horizon,
            'historical_var_pct': float(scaled_historical_var),
            'parametric_var_pct': float(scaled_parametric_var),
            'interpretation': f"With {confidence_level*100}% confidence, maximum loss in {time_horizon} day(s) won't exceed {abs(scaled_historical_var):.2f}%"
        }

    def calculate_cvar(self, confidence_level: float = 0.95) -> float:
        """Calculate Conditional Value at Risk (CVaR/Expected Shortfall).

        Args:
            confidence_level: Confidence level (default: 95%)

        Returns:
            CVaR value
        """
        if self.data.empty or len(self.data) < 2:
            return 0.0

        returns = self.data['Returns'].dropna()

        # CVaR is the average of returns below VaR threshold
        var_percentile = (1 - confidence_level) * 100
        var_threshold = np.percentile(returns, var_percentile)

        cvar = returns[returns <= var_threshold].mean() * 100
        return float(cvar)

    def calculate_max_drawdown(self) -> Dict[str, Any]:
        """Calculate maximum drawdown.

        Returns:
            Dictionary with drawdown metrics
        """
        if self.data.empty or len(self.data) < 2:
            return {'error': 'Insufficient data'}

        prices = self.data['Close']

        # Calculate running maximum
        running_max = prices.cummax()

        # Calculate drawdown
        drawdown = (prices - running_max) / running_max * 100

        max_drawdown = drawdown.min()
        max_drawdown_idx = drawdown.idxmin()

        # Find the peak before max drawdown
        peak_idx = prices[:max_drawdown_idx].idxmax()

        # Calculate recovery
        if max_drawdown_idx < prices.index[-1]:
            recovery_period = len(prices[max_drawdown_idx:]) - 1
        else:
            recovery_period = None

        return {
            'max_drawdown_pct': float(max_drawdown),
            'peak_date': peak_idx.strftime('%Y-%m-%d') if hasattr(peak_idx, 'strftime') else str(peak_idx),
            'trough_date': max_drawdown_idx.strftime('%Y-%m-%d') if hasattr(max_drawdown_idx, 'strftime') else str(max_drawdown_idx),
            'recovery_period_days': recovery_period,
            'current_drawdown_pct': float(drawdown.iloc[-1])
        }

    def calculate_information_ratio(self) -> float:
        """Calculate Information Ratio (IR) relative to benchmark.

        Returns:
            Information ratio
        """
        if self.benchmark_data is None or self.data.empty or self.benchmark_data.empty:
            return 0.0

        # Align data
        stock_returns = self.data['Returns'].dropna()
        benchmark_returns = self.benchmark_data['Returns'].dropna()

        common_dates = stock_returns.index.intersection(benchmark_returns.index)
        if len(common_dates) < 2:
            return 0.0

        stock_returns = stock_returns.loc[common_dates]
        benchmark_returns = benchmark_returns.loc[common_dates]

        # Active returns
        active_returns = stock_returns - benchmark_returns

        # Information ratio
        if active_returns.std() == 0:
            return 0.0

        ir = (active_returns.mean() / active_returns.std()) * np.sqrt(252)
        return float(ir)

    def generate_recommendation(self, risk_free_rate: float = 0.02) -> Dict[str, Any]:
        """Generate investment recommendation based on quantitative metrics.

        Args:
            risk_free_rate: Annual risk-free rate

        Returns:
            Dictionary with recommendation and reasoning
        """
        # Get all metrics
        returns = self.calculate_returns_metrics()
        sharpe = self.calculate_sharpe_ratio(risk_free_rate)
        sortino = self.calculate_sortino_ratio(risk_free_rate)
        beta_alpha = self.calculate_beta_alpha() if self.benchmark_data is not None else None
        drawdown = self.calculate_max_drawdown()
        var_95 = self.calculate_var(0.95)

        # Scoring system
        score = 0
        signals = []
        warnings = []

        # 1. Sharpe Ratio Analysis
        if sharpe > 2:
            score += 2
            signals.append("Excellent risk-adjusted returns (Sharpe > 2)")
        elif sharpe > 1:
            score += 1
            signals.append("Good risk-adjusted returns (Sharpe > 1)")
        elif sharpe < 0:
            score -= 2
            warnings.append("Negative risk-adjusted returns")
        else:
            warnings.append("Below-average risk-adjusted returns")

        # 2. Alpha Analysis (if available)
        if beta_alpha and 'error' not in beta_alpha:
            alpha = beta_alpha['alpha']
            if alpha > 0.05:  # 5% positive alpha
                score += 2
                signals.append(f"Strong outperformance vs benchmark (Alpha: {alpha*100:.2f}%)")
            elif alpha > 0:
                score += 1
                signals.append(f"Modest outperformance vs benchmark (Alpha: {alpha*100:.2f}%)")
            elif alpha < -0.05:
                score -= 2
                warnings.append(f"Underperforming benchmark (Alpha: {alpha*100:.2f}%)")
            else:
                warnings.append("Slight underperformance vs benchmark")

        # 3. Returns Analysis
        if 'error' not in returns:
            total_return = returns['total_return_pct']
            volatility = returns['annualized_volatility_pct']

            if total_return > 20 and volatility < 30:
                score += 2
                signals.append(f"Strong returns ({total_return:.1f}%) with reasonable volatility")
            elif total_return > 10:
                score += 1
                signals.append(f"Positive returns ({total_return:.1f}%)")
            elif total_return < -10:
                score -= 2
                warnings.append(f"Negative returns ({total_return:.1f}%)")

            if volatility > 50:
                score -= 1
                warnings.append(f"High volatility ({volatility:.1f}%)")

        # 4. Drawdown Analysis
        if 'error' not in drawdown:
            max_dd = drawdown['max_drawdown_pct']
            current_dd = drawdown['current_drawdown_pct']

            if current_dd < -15:
                score -= 1
                warnings.append(f"Currently in significant drawdown ({current_dd:.1f}%)")
            elif current_dd < -5:
                warnings.append(f"Currently in moderate drawdown ({current_dd:.1f}%)")

            if max_dd < -30:
                score -= 1
                warnings.append(f"Experienced severe drawdown ({max_dd:.1f}%)")

        # 5. VaR Analysis
        if 'error' not in var_95:
            var_value = abs(var_95['historical_var_pct'])
            if var_value > 5:
                warnings.append(f"High daily risk (VaR: {var_value:.1f}%)")

        # 6. Beta Analysis
        if beta_alpha and 'error' not in beta_alpha:
            beta = beta_alpha['beta']
            if beta > 1.5:
                warnings.append(f"Much more volatile than market (Beta: {beta:.2f})")
            elif beta < 0.5:
                signals.append(f"Low correlation with market (Beta: {beta:.2f})")

        # Determine recommendation
        if score >= 4:
            recommendation = "STRONG BUY"
            confidence = "High"
            action = "Consider accumulating position. Strong fundamentals and performance metrics."
        elif score >= 2:
            recommendation = "BUY"
            confidence = "Moderate"
            action = "Consider initiating or adding to position. Positive indicators outweigh concerns."
        elif score >= 0:
            recommendation = "HOLD"
            confidence = "Moderate"
            action = "Maintain current position. Mixed signals suggest waiting for clearer trend."
        elif score >= -2:
            recommendation = "SELL"
            confidence = "Moderate"
            action = "Consider reducing position. Negative indicators suggest caution."
        else:
            recommendation = "STRONG SELL"
            confidence = "High"
            action = "Consider exiting position. Multiple negative indicators present."

        return {
            'recommendation': recommendation,
            'confidence': confidence,
            'score': score,
            'action': action,
            'positive_signals': signals,
            'risk_warnings': warnings,
            'summary': f"Based on quantitative analysis, the recommendation is {recommendation}. " +
                      f"Score: {score}/10. {len(signals)} positive signals, {len(warnings)} warnings.",
            'disclaimer': "This recommendation is based solely on historical quantitative metrics and should not be considered as financial advice. " +
                         "Always conduct thorough research and consider your personal financial situation before making investment decisions."
        }

    def get_comprehensive_analysis(self, risk_free_rate: float = 0.02) -> Dict[str, Any]:
        """Get comprehensive quantitative analysis.

        Args:
            risk_free_rate: Annual risk-free rate (default: 2%)

        Returns:
            Dictionary with all quantitative metrics
        """
        analysis = {
            'symbol': self.symbol,
            'analysis_period': {
                'start_date': self.data.index[0].strftime('%Y-%m-%d') if not self.data.empty else None,
                'end_date': self.data.index[-1].strftime('%Y-%m-%d') if not self.data.empty else None,
                'trading_days': len(self.data)
            },
            'returns': self.calculate_returns_metrics(),
            'risk_metrics': {
                'sharpe_ratio': self.calculate_sharpe_ratio(risk_free_rate),
                'sortino_ratio': self.calculate_sortino_ratio(risk_free_rate),
                'information_ratio': self.calculate_information_ratio() if self.benchmark_data is not None else None,
                'var_95': self.calculate_var(0.95),
                'var_99': self.calculate_var(0.99),
                'cvar_95': self.calculate_cvar(0.95),
                'max_drawdown': self.calculate_max_drawdown()
            },
            'market_metrics': self.calculate_beta_alpha() if self.benchmark_data is not None else None,
            'recommendation': self.generate_recommendation(risk_free_rate)
        }

        return analysis
