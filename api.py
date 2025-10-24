#!/usr/bin/env python3
"""
MarketMind REST API
A FastAPI server exposing stock data endpoints.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import pandas as pd

from stock_fetcher import StockFetcher
from stock_predictor import StockPredictor
from quant_analysis import QuantAnalysis
from financial_data import FinancialData
from stock_cli import DEFAULT_MARKET_SYMBOLS

# Initialize FastAPI app
app = FastAPI(
    title="MarketMind API",
    description="REST API for fetching real-time stock quotes, analyst ratings, and market data",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for responses
class QuoteResponse(BaseModel):
    symbol: str
    name: str
    current_price: Optional[float]
    previous_close: Any
    open: Any
    day_high: Any
    day_low: Any
    volume: Any
    market_cap: Any
    fifty_two_week_high: Any
    fifty_two_week_low: Any
    change: Any
    change_percent: Any


class SearchResponse(BaseModel):
    symbol: str
    name: str
    exchange: str
    quote_type: str
    currency: str
    market_cap: Any
    sector: str
    industry: str
    country: str
    website: str
    description: str


class AnalystRecommendation(BaseModel):
    date: str
    firm: str
    action: str
    from_grade: str
    to_grade: str


class AnalystSummary(BaseModel):
    recommendation: str
    target_mean: Any
    target_high: Any
    target_low: Any
    num_analysts: Any
    recommendation_mean: Any


class AnalystResponse(BaseModel):
    summary: AnalystSummary
    recent_changes: List[AnalystRecommendation]


class MarketAnalystChange(BaseModel):
    symbol: str
    date: str
    firm: str
    action: str
    from_grade: str
    to_grade: str


class HistoricalDataPoint(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class ComparisonData(BaseModel):
    symbol: str
    dates: List[str]
    close_prices: List[float]
    volumes: List[int]


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None


class PredictionPoint(BaseModel):
    date: str
    conservative: float
    moderate: float
    optimistic: float
    change_percent_moderate: float


class PredictionResponse(BaseModel):
    symbol: str
    current_price: float
    predictions: List[PredictionPoint]
    methods_used: List[str]
    disclaimer: str


# Helper functions
def dataframe_to_dict(df: pd.DataFrame) -> List[Dict]:
    """Convert DataFrame to list of dictionaries."""
    if df.empty:
        return []

    result = []
    for idx, row in df.iterrows():
        date_str = idx.strftime('%Y-%m-%d %H:%M:%S') if hasattr(idx, 'strftime') else str(idx)
        result.append({
            'date': date_str,
            'open': float(row.get('Open', 0)),
            'high': float(row.get('High', 0)),
            'low': float(row.get('Low', 0)),
            'close': float(row.get('Close', 0)),
            'volume': int(row.get('Volume', 0))
        })
    return result


# API Endpoints

@app.get("/", tags=["General"])
async def root():
    """API root endpoint with welcome message."""
    return {
        "message": "MarketMind API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "quote": "/quote/{symbol}",
            "search": "/search/{symbol}",
            "analyst": "/analyst/{symbol}",
            "market_analyst": "/analyst/market",
            "historical": "/historical/{symbol}",
            "compare": "/compare/{symbol1}/{symbol2}",
            "predict": "/predict/{symbol}",
            "quant": "/quant/{symbol}",
            "financials_income": "/financials/{symbol}/income",
            "financials_balance": "/financials/{symbol}/balance",
            "financials_cashflow": "/financials/{symbol}/cashflow",
            "financials_metrics": "/financials/{symbol}/metrics",
            "financials_earnings": "/financials/{symbol}/earnings",
            "financials_next_earnings": "/financials/{symbol}/next-earnings",
            "financials_summary": "/financials/{symbol}/summary",
            "health": "/health"
        }
    }


@app.get("/quote/{symbol}", response_model=QuoteResponse, tags=["Stock Data"])
async def get_quote(symbol: str):
    """
    Get current stock quote with price, volume, and key metrics.

    - **symbol**: Stock ticker symbol (e.g., AAPL, GOOGL)
    """
    try:
        fetcher = StockFetcher(symbol.upper())
        quote_data = fetcher.get_quote_info()

        if not quote_data:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")

        return quote_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/{symbol}", response_model=SearchResponse, tags=["Stock Data"])
async def search_ticker(symbol: str):
    """
    Search for detailed company information by ticker symbol.

    - **symbol**: Stock ticker symbol to search for
    """
    try:
        result = StockFetcher.search_ticker(symbol.upper())

        if not result:
            raise HTTPException(status_code=404, detail=f"No information found for symbol {symbol}")

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analyst/market", response_model=List[MarketAnalystChange], tags=["Analyst Ratings"])
async def get_market_analyst_changes(
    days: int = Query(1, description="Number of days to look back", ge=1, le=30)
):
    """
    Get market-wide analyst changes across major stocks.

    - **days**: Number of days to look back for changes (default: 1, max: 30)
    """
    try:
        changes = StockFetcher.get_market_analyst_changes(DEFAULT_MARKET_SYMBOLS, days)

        result = []
        for change in changes:
            result.append(MarketAnalystChange(
                symbol=change['symbol'],
                date=change['date'].strftime('%Y-%m-%d %H:%M:%S') if hasattr(change['date'], 'strftime') else str(change['date']),
                firm=change['firm'],
                action=change['action'],
                from_grade=change['from_grade'],
                to_grade=change['to_grade']
            ))

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analyst/{symbol}", response_model=AnalystResponse, tags=["Analyst Ratings"])
async def get_analyst_ratings(
    symbol: str,
    limit: int = Query(20, description="Number of recent recommendations to return", ge=1, le=100)
):
    """
    Get analyst ratings, recommendations, and recent upgrades/downgrades for a stock.

    - **symbol**: Stock ticker symbol
    - **limit**: Number of recent recommendations to return (default: 20, max: 100)
    """
    try:
        fetcher = StockFetcher(symbol.upper())

        # Get summary
        summary_data = fetcher.get_recommendations_summary()
        summary = AnalystSummary(
            recommendation=summary_data.get('strong_buy', 'N/A'),
            target_mean=summary_data.get('target_mean', 'N/A'),
            target_high=summary_data.get('target_high', 'N/A'),
            target_low=summary_data.get('target_low', 'N/A'),
            num_analysts=summary_data.get('num_analysts', 'N/A'),
            recommendation_mean=summary_data.get('recommendation_mean', 'N/A')
        )

        # Get recent changes
        recommendations_df = fetcher.get_analyst_recommendations()
        recent_changes = []

        if not recommendations_df.empty:
            for idx, row in recommendations_df.head(limit).iterrows():
                date_str = idx.strftime('%Y-%m-%d') if hasattr(idx, 'strftime') else str(idx)
                recent_changes.append(AnalystRecommendation(
                    date=date_str,
                    firm=row.get('Firm', 'Unknown'),
                    action=row.get('Action', 'N/A'),
                    from_grade=row.get('FromGrade', 'N/A'),
                    to_grade=row.get('ToGrade', 'N/A')
                ))

        return AnalystResponse(summary=summary, recent_changes=recent_changes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/historical/{symbol}", tags=["Stock Data"])
async def get_historical_data(
    symbol: str,
    period: str = Query("1mo", description="Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)"),
    interval: str = Query("1d", description="Data interval (1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo)")
):
    """
    Get historical stock data.

    - **symbol**: Stock ticker symbol
    - **period**: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)
    - **interval**: Data interval (1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo)
    """
    try:
        fetcher = StockFetcher(symbol.upper())
        data = fetcher.get_historical_data(period=period, interval=interval)

        if data.empty:
            raise HTTPException(status_code=404, detail=f"No historical data found for {symbol}")

        return dataframe_to_dict(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/compare/{symbol1}/{symbol2}", tags=["Comparison"])
async def compare_stocks(
    symbol1: str,
    symbol2: str,
    period: str = Query("1mo", description="Time period"),
    interval: str = Query("1d", description="Data interval")
):
    """
    Compare two stocks by returning their historical data.

    - **symbol1**: First stock ticker symbol
    - **symbol2**: Second stock ticker symbol
    - **period**: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)
    - **interval**: Data interval (1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo)
    """
    try:
        fetcher1 = StockFetcher(symbol1.upper())
        fetcher2 = StockFetcher(symbol2.upper())

        data1 = fetcher1.get_historical_data(period=period, interval=interval)
        data2 = fetcher2.get_historical_data(period=period, interval=interval)

        if data1.empty:
            raise HTTPException(status_code=404, detail=f"No data found for {symbol1}")
        if data2.empty:
            raise HTTPException(status_code=404, detail=f"No data found for {symbol2}")

        return {
            symbol1.upper(): dataframe_to_dict(data1),
            symbol2.upper(): dataframe_to_dict(data2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/predict/{symbol}", response_model=PredictionResponse, tags=["Prediction"])
async def predict_stock_price(
    symbol: str,
    days: int = Query(7, description="Number of days to predict ahead", ge=1, le=30)
):
    """
    Predict future stock prices using ensemble machine learning methods.

    - **symbol**: Stock ticker symbol
    - **days**: Number of days to predict ahead (default: 7, max: 30)

    Returns predictions with conservative, moderate, and optimistic estimates.
    """
    try:
        fetcher = StockFetcher(symbol.upper())

        # Get 3 months of historical data
        historical_data = fetcher.get_historical_data(period='3mo', interval='1d')

        if historical_data.empty:
            raise HTTPException(status_code=404, detail=f"No historical data available for {symbol}")

        # Create predictor and get ensemble prediction
        predictor = StockPredictor(symbol.upper(), historical_data)
        result = predictor.predict_ensemble(days)

        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/quant/{symbol}", tags=["Quantitative Analysis"])
async def get_quant_analysis(
    symbol: str,
    benchmark: str = Query("SPY", description="Benchmark symbol for comparison"),
    period: str = Query("1y", description="Analysis period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)")
):
    """
    Get comprehensive quantitative finance analysis.

    - **symbol**: Stock ticker symbol
    - **benchmark**: Benchmark symbol for Beta/Alpha calculation (default: SPY)
    - **period**: Analysis period (default: 1y)

    Returns metrics including Sharpe ratio, Beta, Alpha, VaR, drawdown, and more.
    """
    try:
        # Fetch stock data
        fetcher = StockFetcher(symbol.upper())
        stock_data = fetcher.get_historical_data(period=period, interval='1d')

        if stock_data.empty:
            raise HTTPException(status_code=404, detail=f"No historical data available for {symbol}")

        # Fetch benchmark data
        benchmark_data = None
        if benchmark:
            benchmark_fetcher = StockFetcher(benchmark.upper())
            benchmark_data = benchmark_fetcher.get_historical_data(period=period, interval='1d')

        # Perform quantitative analysis
        quant = QuantAnalysis(symbol.upper(), stock_data, benchmark_data)
        analysis = quant.get_comprehensive_analysis()

        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/financials/{symbol}/income", tags=["Financials"])
async def get_income_statement(
    symbol: str,
    quarterly: bool = Query(False, description="Get quarterly data instead of annual")
):
    """
    Get income statement for a stock.

    - **symbol**: Stock ticker symbol
    - **quarterly**: If true, returns quarterly data; otherwise annual data
    """
    try:
        financials = FinancialData(symbol.upper())
        result = financials.get_income_statement(quarterly=quarterly)

        if 'error' in result:
            raise HTTPException(status_code=404, detail=result['error'])

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/financials/{symbol}/balance", tags=["Financials"])
async def get_balance_sheet(
    symbol: str,
    quarterly: bool = Query(False, description="Get quarterly data instead of annual")
):
    """
    Get balance sheet for a stock.

    - **symbol**: Stock ticker symbol
    - **quarterly**: If true, returns quarterly data; otherwise annual data
    """
    try:
        financials = FinancialData(symbol.upper())
        result = financials.get_balance_sheet(quarterly=quarterly)

        if 'error' in result:
            raise HTTPException(status_code=404, detail=result['error'])

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/financials/{symbol}/cashflow", tags=["Financials"])
async def get_cash_flow(
    symbol: str,
    quarterly: bool = Query(False, description="Get quarterly data instead of annual")
):
    """
    Get cash flow statement for a stock.

    - **symbol**: Stock ticker symbol
    - **quarterly**: If true, returns quarterly data; otherwise annual data
    """
    try:
        financials = FinancialData(symbol.upper())
        result = financials.get_cash_flow(quarterly=quarterly)

        if 'error' in result:
            raise HTTPException(status_code=404, detail=result['error'])

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/financials/{symbol}/metrics", tags=["Financials"])
async def get_key_metrics(symbol: str):
    """
    Get key financial metrics and ratios for a stock.

    Returns valuation, profitability, financial health, growth, and dividend metrics.

    - **symbol**: Stock ticker symbol
    """
    try:
        financials = FinancialData(symbol.upper())
        result = financials.get_key_metrics()

        if 'error' in result:
            raise HTTPException(status_code=404, detail=result['error'])

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/financials/{symbol}/earnings", tags=["Financials"])
async def get_earnings_history(symbol: str):
    """
    Get historical earnings data with estimates vs actual.

    - **symbol**: Stock ticker symbol
    """
    try:
        financials = FinancialData(symbol.upper())
        result = financials.get_earnings_history()

        if 'error' in result:
            raise HTTPException(status_code=404, detail=result['error'])

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/financials/{symbol}/summary", tags=["Financials"])
async def get_financial_summary(symbol: str):
    """
    Get comprehensive financial summary.

    Returns revenue, profitability, balance sheet, cash flow, and key ratios.

    - **symbol**: Stock ticker symbol
    """
    try:
        financials = FinancialData(symbol.upper())
        result = financials.get_financial_summary()

        if 'error' in result:
            raise HTTPException(status_code=404, detail=result['error'])

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/financials/{symbol}/next-earnings", tags=["Financials"])
async def get_next_earnings_date(symbol: str):
    """
    Get next earnings date and analyst estimates.

    Returns the next scheduled earnings date with EPS and revenue estimates.

    - **symbol**: Stock ticker symbol
    """
    try:
        financials = FinancialData(symbol.upper())
        result = financials.get_next_earnings()

        if 'error' in result:
            raise HTTPException(status_code=404, detail=result['error'])

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", tags=["General"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
