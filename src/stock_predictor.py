"""
Stock Price Prediction Module
Uses statistical analysis and machine learning to predict future stock prices.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
from typing import Dict, Any, List


class StockPredictor:
    """Predicts future stock prices using historical data."""

    def __init__(self, symbol: str, historical_data: pd.DataFrame):
        """Initialize predictor with historical data.

        Args:
            symbol: Stock ticker symbol
            historical_data: DataFrame with historical OHLCV data
        """
        self.symbol = symbol.upper()
        self.data = historical_data.copy()

        if not self.data.empty:
            # Ensure we have a datetime index
            if not isinstance(self.data.index, pd.DatetimeIndex):
                self.data.index = pd.to_datetime(self.data.index)

    def calculate_technical_indicators(self) -> pd.DataFrame:
        """Calculate technical indicators for prediction."""
        if self.data.empty:
            return self.data

        df = self.data.copy()

        # Moving averages
        df['SMA_5'] = df['Close'].rolling(window=5).mean()
        df['SMA_10'] = df['Close'].rolling(window=10).mean()
        df['SMA_20'] = df['Close'].rolling(window=20).mean()

        # Exponential moving average
        df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()

        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']

        # Rate of change
        df['ROC'] = df['Close'].pct_change(periods=10) * 100

        # Volatility (standard deviation)
        df['Volatility'] = df['Close'].rolling(window=10).std()

        # Price momentum
        df['Momentum'] = df['Close'] - df['Close'].shift(10)

        return df

    def predict_linear_regression(self, days_ahead: int = 7) -> Dict[str, Any]:
        """Predict using linear regression on recent trend.

        Args:
            days_ahead: Number of days to predict ahead

        Returns:
            Dictionary with predictions
        """
        if len(self.data) < 30:
            return {'error': 'Insufficient data for prediction (need at least 30 days)'}

        # Use last 60 days for training
        train_data = self.data.tail(60).copy()

        # Prepare features (days as numerical sequence)
        X = np.arange(len(train_data)).reshape(-1, 1)
        y = train_data['Close'].values

        # Train model
        model = LinearRegression()
        model.fit(X, y)

        # Predict future days
        future_X = np.arange(len(train_data), len(train_data) + days_ahead).reshape(-1, 1)
        predictions = model.predict(future_X)

        # Calculate confidence based on R-squared
        r_squared = model.score(X, y)

        # Get last date and generate future dates
        last_date = train_data.index[-1]
        future_dates = [last_date + timedelta(days=i+1) for i in range(days_ahead)]

        return {
            'method': 'Linear Regression',
            'predictions': [
                {
                    'date': date.strftime('%Y-%m-%d'),
                    'predicted_price': float(price),
                    'confidence': float(r_squared)
                }
                for date, price in zip(future_dates, predictions)
            ],
            'current_price': float(train_data['Close'].iloc[-1]),
            'trend': 'upward' if predictions[-1] > y[-1] else 'downward',
            'r_squared': float(r_squared)
        }

    def predict_moving_average(self, days_ahead: int = 7) -> Dict[str, Any]:
        """Predict using moving average extrapolation.

        Args:
            days_ahead: Number of days to predict ahead

        Returns:
            Dictionary with predictions
        """
        if len(self.data) < 20:
            return {'error': 'Insufficient data for prediction (need at least 20 days)'}

        # Calculate different moving averages
        recent = self.data.tail(30)
        sma_5 = recent['Close'].rolling(window=5).mean().iloc[-1]
        sma_10 = recent['Close'].rolling(window=10).mean().iloc[-1]
        sma_20 = recent['Close'].rolling(window=20).mean().iloc[-1]

        current_price = recent['Close'].iloc[-1]

        # Weight recent averages more heavily
        weighted_prediction = (sma_5 * 0.5 + sma_10 * 0.3 + sma_20 * 0.2)

        # Calculate momentum
        momentum = current_price - recent['Close'].iloc[-10]
        daily_momentum = momentum / 10

        # Generate predictions
        last_date = recent.index[-1]
        predictions = []

        for i in range(days_ahead):
            predicted_price = weighted_prediction + (daily_momentum * (i + 1) * 0.5)
            future_date = last_date + timedelta(days=i+1)

            predictions.append({
                'date': future_date.strftime('%Y-%m-%d'),
                'predicted_price': float(predicted_price),
                'confidence': 0.65  # MA-based predictions are moderately confident
            })

        return {
            'method': 'Moving Average',
            'predictions': predictions,
            'current_price': float(current_price),
            'sma_5': float(sma_5),
            'sma_10': float(sma_10),
            'sma_20': float(sma_20)
        }

    def predict_advanced(self, days_ahead: int = 7) -> Dict[str, Any]:
        """Advanced prediction using multiple features.

        Args:
            days_ahead: Number of days to predict ahead

        Returns:
            Dictionary with predictions
        """
        if len(self.data) < 60:
            return {'error': 'Insufficient data for advanced prediction (need at least 60 days)'}

        # Calculate technical indicators
        df = self.calculate_technical_indicators()
        df = df.dropna()

        if len(df) < 30:
            return {'error': 'Insufficient data after calculating indicators'}

        # Prepare features
        feature_cols = ['SMA_5', 'SMA_10', 'SMA_20', 'MACD', 'ROC', 'Volatility', 'Momentum']
        X = df[feature_cols].tail(50).values
        y = df['Close'].tail(50).values

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Train model
        model = LinearRegression()
        model.fit(X_scaled, y)

        # For prediction, use last known values and extrapolate
        last_features = X_scaled[-1].reshape(1, -1)

        predictions = []
        last_date = df.index[-1]
        current_price = y[-1]

        for i in range(days_ahead):
            predicted_price = model.predict(last_features)[0]
            future_date = last_date + timedelta(days=i+1)

            predictions.append({
                'date': future_date.strftime('%Y-%m-%d'),
                'predicted_price': float(predicted_price),
                'confidence': 0.70
            })

            # Update features for next prediction (simplified)
            # In practice, you'd recalculate indicators, but this gives a trend
            last_features = last_features * 1.001 if predicted_price > current_price else last_features * 0.999

        return {
            'method': 'Advanced Multi-Feature',
            'predictions': predictions,
            'current_price': float(current_price),
            'features_used': feature_cols
        }

    def predict_ensemble(self, days_ahead: int = 7) -> Dict[str, Any]:
        """Ensemble prediction combining multiple methods.

        Args:
            days_ahead: Number of days to predict ahead

        Returns:
            Dictionary with ensemble predictions
        """
        # Get predictions from different methods
        lr_pred = self.predict_linear_regression(days_ahead)
        ma_pred = self.predict_moving_average(days_ahead)
        adv_pred = self.predict_advanced(days_ahead)

        # Check for errors
        if 'error' in lr_pred or 'error' in ma_pred:
            return {'error': 'Insufficient data for ensemble prediction'}

        current_price = self.data['Close'].iloc[-1]
        last_date = self.data.index[-1]

        # Combine predictions
        ensemble_predictions = []

        for i in range(days_ahead):
            lr_price = lr_pred['predictions'][i]['predicted_price']
            ma_price = ma_pred['predictions'][i]['predicted_price']

            # Weighted average (can adjust weights based on historical performance)
            conservative = min(lr_price, ma_price)
            optimistic = max(lr_price, ma_price)
            moderate = (lr_price * 0.4 + ma_price * 0.6)  # Weight MA more

            # Include advanced if available
            if 'error' not in adv_pred and i < len(adv_pred['predictions']):
                adv_price = adv_pred['predictions'][i]['predicted_price']
                moderate = (lr_price * 0.3 + ma_price * 0.4 + adv_price * 0.3)
                conservative = min(conservative, adv_price)
                optimistic = max(optimistic, adv_price)

            future_date = last_date + timedelta(days=i+1)

            ensemble_predictions.append({
                'date': future_date.strftime('%Y-%m-%d'),
                'conservative': float(conservative),
                'moderate': float(moderate),
                'optimistic': float(optimistic),
                'change_percent_moderate': float(((moderate - current_price) / current_price) * 100)
            })

        return {
            'symbol': self.symbol,
            'current_price': float(current_price),
            'predictions': ensemble_predictions,
            'methods_used': ['Linear Regression', 'Moving Average', 'Advanced Multi-Feature'],
            'disclaimer': 'Predictions are based on historical data and should not be used as financial advice.'
        }
