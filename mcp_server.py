#!/usr/bin/env python3
"""
MarketMind MCP Server
Exposes stock analysis functionality through the Model Context Protocol.
"""

import json
import logging
from typing import Any
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from stock_fetcher import StockFetcher
from stock_predictor import StockPredictor
from quant_analysis import QuantAnalysis
from financial_data import FinancialData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("marketmind-mcp")

# Initialize MCP server
app = Server("marketmind")

# Define available tools
TOOLS = [
    Tool(
        name="get_stock_quote",
        description="Get current stock quote with price, volume, and key metrics for a given symbol",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol (e.g., AAPL, GOOGL, TSLA)"
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="search_stock",
        description="Search for detailed company information by ticker symbol including sector, industry, and description",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol to search for"
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="get_analyst_ratings",
        description="Get analyst ratings, recommendations, and recent upgrades/downgrades for a stock",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of recent recommendations to return (default: 20, max: 100)",
                    "default": 20
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="get_historical_data",
        description="Get historical stock data for a given period and interval",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                },
                "period": {
                    "type": "string",
                    "description": "Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)",
                    "default": "1mo"
                },
                "interval": {
                    "type": "string",
                    "description": "Data interval (1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo)",
                    "default": "1d"
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="compare_stocks",
        description="Compare two stocks by returning their historical data side by side",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol1": {
                    "type": "string",
                    "description": "First stock ticker symbol"
                },
                "symbol2": {
                    "type": "string",
                    "description": "Second stock ticker symbol"
                },
                "period": {
                    "type": "string",
                    "description": "Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)",
                    "default": "1mo"
                }
            },
            "required": ["symbol1", "symbol2"]
        }
    ),
    Tool(
        name="predict_stock_price",
        description="Predict future stock prices using ensemble machine learning methods with conservative, moderate, and optimistic estimates",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to predict ahead (default: 7, max: 30)",
                    "default": 7
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="get_quantitative_analysis",
        description="Get comprehensive quantitative finance analysis including Sharpe ratio, Beta, Alpha, VaR, drawdown, and investment recommendations",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                },
                "benchmark": {
                    "type": "string",
                    "description": "Benchmark symbol for Beta/Alpha calculation (default: SPY)",
                    "default": "SPY"
                },
                "period": {
                    "type": "string",
                    "description": "Analysis period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)",
                    "default": "1y"
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="get_income_statement",
        description="Get income statement showing revenue, expenses, and profitability",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                },
                "quarterly": {
                    "type": "boolean",
                    "description": "Get quarterly data instead of annual (default: false)",
                    "default": False
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="get_balance_sheet",
        description="Get balance sheet showing assets, liabilities, and equity",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                },
                "quarterly": {
                    "type": "boolean",
                    "description": "Get quarterly data instead of annual (default: false)",
                    "default": False
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="get_cash_flow_statement",
        description="Get cash flow statement showing operating, investing, and financing activities",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                },
                "quarterly": {
                    "type": "boolean",
                    "description": "Get quarterly data instead of annual (default: false)",
                    "default": False
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="get_financial_metrics",
        description="Get key financial metrics including valuation ratios, profitability, financial health, growth, and dividend metrics",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="get_earnings_history",
        description="Get historical earnings data with estimates vs actual results",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="get_financial_summary",
        description="Get comprehensive financial summary including revenue, profitability, balance sheet, cash flow, and key ratios",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="get_next_earnings_date",
        description="Get next scheduled earnings date with analyst EPS and revenue estimates",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                }
            },
            "required": ["symbol"]
        }
    )
]


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "get_stock_quote":
            return await handle_get_quote(arguments)
        elif name == "search_stock":
            return await handle_search_stock(arguments)
        elif name == "get_analyst_ratings":
            return await handle_analyst_ratings(arguments)
        elif name == "get_historical_data":
            return await handle_historical_data(arguments)
        elif name == "compare_stocks":
            return await handle_compare_stocks(arguments)
        elif name == "predict_stock_price":
            return await handle_predict_price(arguments)
        elif name == "get_quantitative_analysis":
            return await handle_quant_analysis(arguments)
        elif name == "get_income_statement":
            return await handle_income_statement(arguments)
        elif name == "get_balance_sheet":
            return await handle_balance_sheet(arguments)
        elif name == "get_cash_flow_statement":
            return await handle_cash_flow(arguments)
        elif name == "get_financial_metrics":
            return await handle_financial_metrics(arguments)
        elif name == "get_earnings_history":
            return await handle_earnings_history(arguments)
        elif name == "get_financial_summary":
            return await handle_financial_summary(arguments)
        elif name == "get_next_earnings_date":
            return await handle_next_earnings(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"Error calling tool {name}: {str(e)}", exc_info=True)
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def handle_get_quote(arguments: dict) -> list[TextContent]:
    """Get stock quote."""
    symbol = arguments["symbol"].upper()
    logger.info(f"Getting quote for {symbol}")

    fetcher = StockFetcher(symbol)
    quote_data = fetcher.get_quote_info()

    if not quote_data:
        return [TextContent(
            type="text",
            text=f"No data found for symbol {symbol}"
        )]

    return [TextContent(
        type="text",
        text=json.dumps(quote_data, indent=2)
    )]


async def handle_search_stock(arguments: dict) -> list[TextContent]:
    """Search for stock information."""
    symbol = arguments["symbol"].upper()
    logger.info(f"Searching for {symbol}")

    result = StockFetcher.search_ticker(symbol)

    if not result:
        return [TextContent(
            type="text",
            text=f"No information found for symbol {symbol}"
        )]

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def handle_analyst_ratings(arguments: dict) -> list[TextContent]:
    """Get analyst ratings."""
    symbol = arguments["symbol"].upper()
    limit = arguments.get("limit", 20)
    logger.info(f"Getting analyst ratings for {symbol}")

    fetcher = StockFetcher(symbol)

    # Get summary
    summary_data = fetcher.get_recommendations_summary()

    # Get recent changes
    recommendations_df = fetcher.get_analyst_recommendations()
    recent_changes = []

    if not recommendations_df.empty:
        for idx, row in recommendations_df.head(limit).iterrows():
            date_str = idx.strftime('%Y-%m-%d') if hasattr(idx, 'strftime') else str(idx)
            recent_changes.append({
                "date": date_str,
                "firm": row.get('Firm', 'Unknown'),
                "action": row.get('Action', 'N/A'),
                "from_grade": row.get('FromGrade', 'N/A'),
                "to_grade": row.get('ToGrade', 'N/A')
            })

    result = {
        "summary": summary_data,
        "recent_changes": recent_changes
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def handle_historical_data(arguments: dict) -> list[TextContent]:
    """Get historical stock data."""
    symbol = arguments["symbol"].upper()
    period = arguments.get("period", "1mo")
    interval = arguments.get("interval", "1d")
    logger.info(f"Getting historical data for {symbol} ({period}, {interval})")

    fetcher = StockFetcher(symbol)
    data = fetcher.get_historical_data(period=period, interval=interval)

    if data.empty:
        return [TextContent(
            type="text",
            text=f"No historical data found for {symbol}"
        )]

    # Convert DataFrame to list of dicts
    result = []
    for idx, row in data.iterrows():
        date_str = idx.strftime('%Y-%m-%d %H:%M:%S') if hasattr(idx, 'strftime') else str(idx)
        result.append({
            'date': date_str,
            'open': float(row.get('Open', 0)),
            'high': float(row.get('High', 0)),
            'low': float(row.get('Low', 0)),
            'close': float(row.get('Close', 0)),
            'volume': int(row.get('Volume', 0))
        })

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def handle_compare_stocks(arguments: dict) -> list[TextContent]:
    """Compare two stocks."""
    symbol1 = arguments["symbol1"].upper()
    symbol2 = arguments["symbol2"].upper()
    period = arguments.get("period", "1mo")
    logger.info(f"Comparing {symbol1} and {symbol2}")

    fetcher1 = StockFetcher(symbol1)
    fetcher2 = StockFetcher(symbol2)

    data1 = fetcher1.get_historical_data(period=period, interval="1d")
    data2 = fetcher2.get_historical_data(period=period, interval="1d")

    if data1.empty:
        return [TextContent(
            type="text",
            text=f"No data found for {symbol1}"
        )]

    if data2.empty:
        return [TextContent(
            type="text",
            text=f"No data found for {symbol2}"
        )]

    # Convert to comparable format
    result = {
        symbol1: [],
        symbol2: []
    }

    for idx, row in data1.iterrows():
        date_str = idx.strftime('%Y-%m-%d') if hasattr(idx, 'strftime') else str(idx)
        result[symbol1].append({
            'date': date_str,
            'close': float(row.get('Close', 0)),
            'volume': int(row.get('Volume', 0))
        })

    for idx, row in data2.iterrows():
        date_str = idx.strftime('%Y-%m-%d') if hasattr(idx, 'strftime') else str(idx)
        result[symbol2].append({
            'date': date_str,
            'close': float(row.get('Close', 0)),
            'volume': int(row.get('Volume', 0))
        })

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def handle_predict_price(arguments: dict) -> list[TextContent]:
    """Predict future stock prices."""
    symbol = arguments["symbol"].upper()
    days = arguments.get("days", 7)
    logger.info(f"Predicting prices for {symbol} ({days} days)")

    fetcher = StockFetcher(symbol)
    historical_data = fetcher.get_historical_data(period='3mo', interval='1d')

    if historical_data.empty:
        return [TextContent(
            type="text",
            text=f"No historical data available for {symbol}"
        )]

    predictor = StockPredictor(symbol, historical_data)
    result = predictor.predict_ensemble(days)

    if 'error' in result:
        return [TextContent(
            type="text",
            text=f"Error: {result['error']}"
        )]

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def handle_quant_analysis(arguments: dict) -> list[TextContent]:
    """Get quantitative analysis."""
    symbol = arguments["symbol"].upper()
    benchmark = arguments.get("benchmark", "SPY")
    period = arguments.get("period", "1y")
    logger.info(f"Performing quantitative analysis for {symbol}")

    # Fetch stock data
    fetcher = StockFetcher(symbol)
    stock_data = fetcher.get_historical_data(period=period, interval='1d')

    if stock_data.empty:
        return [TextContent(
            type="text",
            text=f"No historical data available for {symbol}"
        )]

    # Fetch benchmark data
    benchmark_data = None
    if benchmark:
        benchmark_fetcher = StockFetcher(benchmark)
        benchmark_data = benchmark_fetcher.get_historical_data(period=period, interval='1d')

    # Perform analysis
    quant = QuantAnalysis(symbol, stock_data, benchmark_data)
    analysis = quant.get_comprehensive_analysis()

    return [TextContent(
        type="text",
        text=json.dumps(analysis, indent=2, default=str)
    )]


async def handle_income_statement(arguments: dict) -> list[TextContent]:
    """Get income statement."""
    symbol = arguments["symbol"].upper()
    quarterly = arguments.get("quarterly", False)
    logger.info(f"Getting income statement for {symbol} ({'quarterly' if quarterly else 'annual'})")

    financials = FinancialData(symbol)
    result = financials.get_income_statement(quarterly=quarterly)

    if 'error' in result:
        return [TextContent(
            type="text",
            text=f"Error: {result['error']}"
        )]

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def handle_balance_sheet(arguments: dict) -> list[TextContent]:
    """Get balance sheet."""
    symbol = arguments["symbol"].upper()
    quarterly = arguments.get("quarterly", False)
    logger.info(f"Getting balance sheet for {symbol} ({'quarterly' if quarterly else 'annual'})")

    financials = FinancialData(symbol)
    result = financials.get_balance_sheet(quarterly=quarterly)

    if 'error' in result:
        return [TextContent(
            type="text",
            text=f"Error: {result['error']}"
        )]

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def handle_cash_flow(arguments: dict) -> list[TextContent]:
    """Get cash flow statement."""
    symbol = arguments["symbol"].upper()
    quarterly = arguments.get("quarterly", False)
    logger.info(f"Getting cash flow for {symbol} ({'quarterly' if quarterly else 'annual'})")

    financials = FinancialData(symbol)
    result = financials.get_cash_flow(quarterly=quarterly)

    if 'error' in result:
        return [TextContent(
            type="text",
            text=f"Error: {result['error']}"
        )]

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def handle_financial_metrics(arguments: dict) -> list[TextContent]:
    """Get financial metrics."""
    symbol = arguments["symbol"].upper()
    logger.info(f"Getting financial metrics for {symbol}")

    financials = FinancialData(symbol)
    result = financials.get_key_metrics()

    if 'error' in result:
        return [TextContent(
            type="text",
            text=f"Error: {result['error']}"
        )]

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def handle_earnings_history(arguments: dict) -> list[TextContent]:
    """Get earnings history."""
    symbol = arguments["symbol"].upper()
    logger.info(f"Getting earnings history for {symbol}")

    financials = FinancialData(symbol)
    result = financials.get_earnings_history()

    if 'error' in result:
        return [TextContent(
            type="text",
            text=f"Error: {result['error']}"
        )]

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def handle_financial_summary(arguments: dict) -> list[TextContent]:
    """Get financial summary."""
    symbol = arguments["symbol"].upper()
    logger.info(f"Getting financial summary for {symbol}")

    financials = FinancialData(symbol)
    result = financials.get_financial_summary()

    if 'error' in result:
        return [TextContent(
            type="text",
            text=f"Error: {result['error']}"
        )]

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def handle_next_earnings(arguments: dict) -> list[TextContent]:
    """Get next earnings date."""
    symbol = arguments["symbol"].upper()
    logger.info(f"Getting next earnings date for {symbol}")

    financials = FinancialData(symbol)
    result = financials.get_next_earnings()

    if 'error' in result:
        return [TextContent(
            type="text",
            text=f"Error: {result['error']}"
        )]

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def main():
    """Run the MCP server."""
    logger.info("Starting MarketMind MCP Server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
