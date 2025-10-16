# Stock Exchange Yahoo Finance - CLI & API

A powerful tool for fetching real-time stock quotes, analyst ratings, and market data using Yahoo Finance. Available as both a command-line interface (CLI) and REST API.

## Features

- **Dual Interface**: Both CLI and REST API for maximum flexibility
- **Real-time Quotes**: Get current stock prices, changes, and key metrics
- **Ticker Search**: Search for detailed company information by ticker symbol
- **Analyst Ratings**: View analyst recommendations, upgrades, and downgrades for individual stocks
- **Market-Wide Analyst Changes**: Scan major stocks to see all analyst rating changes across the market
- **Symbol Comparison**: Compare two stocks side-by-side with price or performance charts
- **Interactive Charts**: Display candlestick, line, and intraday charts (CLI only)
- **Live Monitoring**: Continuously monitor stock prices with auto-refresh (CLI only)
- **Multiple Time Periods**: View data from 1 day to max historical range
- **REST API**: Full-featured API with Swagger documentation and CORS support
- **Colorful Display**: Easy-to-read colored output for better visualization (CLI)

## Installation

1. Navigate to the project directory:
```bash
cd stock-exchange-yahoo
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

This project provides two interfaces:
1. **Command-Line Interface (CLI)** - For terminal usage
2. **REST API** - For programmatic access via HTTP

### REST API

Start the API server:
```bash
python api.py
```

Or using uvicorn directly:
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

**Interactive API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Available Endpoints:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/quote/{symbol}` | GET | Get current stock quote |
| `/search/{symbol}` | GET | Search for ticker information |
| `/analyst/{symbol}` | GET | Get analyst ratings and recommendations |
| `/analyst/market?days=1` | GET | Get market-wide analyst changes |
| `/historical/{symbol}?period=1mo&interval=1d` | GET | Get historical stock data |
| `/compare/{symbol1}/{symbol2}?period=1mo` | GET | Compare two stocks |
| `/health` | GET | Health check endpoint |

**Example API Calls:**

```bash
# Get quote for AAPL
curl http://localhost:8000/quote/AAPL

# Get analyst ratings for TSLA
curl http://localhost:8000/analyst/TSLA?limit=10

# Get market-wide analyst changes from last 3 days
curl http://localhost:8000/analyst/market?days=3

# Get historical data
curl "http://localhost:8000/historical/AAPL?period=1mo&interval=1d"

# Compare two stocks
curl http://localhost:8000/compare/AAPL/MSFT?period=6mo
```

**Response Example:**
```json
{
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "current_price": 178.45,
  "previous_close": 176.15,
  "open": 176.15,
  "day_high": 179.20,
  "day_low": 175.80,
  "volume": 52847600,
  "market_cap": 2890000000000,
  "change": 2.30,
  "change_percent": 1.31
}
```

**For more API examples and client code, see [API_EXAMPLES.md](API_EXAMPLES.md)**

### Command-Line Interface

The CLI has six main commands: `quote`, `chart`, `monitor`, `search`, `compare`, and `analyst`.

### Get Current Quote

Get the current stock price and key information:

```bash
python stock_cli.py quote AAPL
```

Example output:
```
=== AAPL Quote ===

Apple Inc.
Current Price: $178.45
Change: +$2.30 (+1.31%)

Open: $176.15
High: $179.20
Low: $175.80
Previous Close: $176.15
Volume: 52847600
```

### Search for Ticker Symbols

Search for detailed information about one or more ticker symbols:

**Search for a single ticker:**
```bash
python stock_cli.py search AAPL
```

Example output:
```
=== AAPL ===

Apple Inc.

Exchange: NMS
Type: EQUITY
Currency: USD
Market Cap: $2.89T
Sector: Technology
Industry: Consumer Electronics
Country: United States
```

**Search for multiple tickers:**
```bash
python stock_cli.py search AAPL GOOGL MSFT
```

**Search with detailed information (includes company description and website):**
```bash
python stock_cli.py search TSLA --detailed
```

This will display additional information including:
- Company website
- Business description/summary

### Get Analyst Ratings

View analyst recommendations, upgrades, and downgrades:

**Get current analyst ratings and recent activity:**
```bash
python stock_cli.py analyst AAPL
```

Example output:
```
=== AAPL Analyst Ratings ===

Current Consensus:
Recommendation: BUY
Number of Analysts: 45
Recommendation Mean: 1.87 (1=Strong Buy, 5=Sell)

Price Targets:
Mean Target:  $195.50
High Target:  $220.00
Low Target:   $165.00

Recent Upgrades/Downgrades:

2024-03-15 | ↑ Upgrade       | Morgan Stanley
           Overweight → Buy

2024-03-10 | → Maintains     | JP Morgan
           Overweight

2024-03-05 | ↓ Downgrade     | Goldman Sachs
           Buy → Neutral
```

**View more history:**
```bash
python stock_cli.py analyst TSLA --limit 50
```

The analyst command shows:
- Current consensus recommendation (Buy, Hold, Sell, etc.)
- Number of analysts covering the stock
- Price targets (mean, high, low)
- Recent upgrades and downgrades with dates and firms
- Rating changes with before/after grades

**Get market-wide analyst changes:**
```bash
python stock_cli.py analyst market
```

This scans major stocks across different sectors and shows all analyst rating changes from today:

Example output:
```
=== Market-Wide Analyst Changes (Last 1 day) ===

Scanning 56 stocks...

Found 5 analyst action(s)

====================================================================================================
2024-03-15 14:30 | NVDA   | ↑ Upgrade       | Morgan Stanley
                           Overweight → Buy
----------------------------------------------------------------------------------------------------
2024-03-15 12:15 | AAPL   | → Maintains     | JP Morgan
                           Overweight
----------------------------------------------------------------------------------------------------
2024-03-15 10:45 | TSLA   | ↓ Downgrade     | Goldman Sachs
                           Buy → Neutral
----------------------------------------------------------------------------------------------------
```

**View changes from the last 3 days:**
```bash
python stock_cli.py analyst market --days 3
```

The market scan covers 56 major stocks across sectors including:
- Technology (AAPL, MSFT, NVDA, etc.)
- Finance (JPM, GS, BAC, etc.)
- Healthcare (JNJ, UNH, PFE, etc.)
- Consumer (WMT, HD, DIS, etc.)
- Energy (XOM, CVX, etc.)
- And more

### Compare Two Stock Symbols

Compare two stocks side-by-side to analyze their performance:

**Price comparison (dual y-axes for different price scales):**
```bash
python stock_cli.py compare AAPL MSFT --period 1mo
```

This shows both stocks' actual prices on the same chart with separate y-axes, along with volume comparison.

**Performance comparison (normalized percentage change):**
```bash
python stock_cli.py compare TSLA NVDA --period 6mo --type performance
```

This normalizes both stocks to show percentage change from the starting point, making it easy to compare relative performance regardless of price differences.

**Compare with custom period:**
```bash
python stock_cli.py compare GOOGL AMZN --period 1y --type price
```

#### Comparison Types

- **price** (default) - Shows actual stock prices with dual y-axes. Best for comparing absolute price movements when stocks have different price ranges.
- **performance** - Shows percentage change from the start of the period. Best for comparing relative performance and returns.

### Display Stock Chart

Show interactive charts with various options:

**Basic line chart (default - 1 month):**
```bash
python stock_cli.py chart AAPL
```

**Candlestick chart for 5 days:**
```bash
python stock_cli.py chart GOOGL --period 5d --type candlestick
```

**Intraday chart for today:**
```bash
python stock_cli.py chart TSLA --period 1d --type intraday
```

**Comparison chart (price + volume subplots):**
```bash
python stock_cli.py chart AAPL --period 5d --type comparison
```

**Custom period:**
```bash
python stock_cli.py chart MSFT --period 6mo --type line
```

#### Available Options

**Periods:**
- `1d` - One day
- `5d` - Five days
- `1mo` - One month (default)
- `3mo` - Three months
- `6mo` - Six months
- `1y` - One year
- `2y` - Two years
- `5y` - Five years
- `max` - Maximum available data

**Chart Types:**
- `line` - Simple line chart (default)
- `candlestick` - OHLC candlestick chart with volume
- `intraday` - Intraday chart with moving average and volume
- `comparison` - Dual subplot chart showing price range and volume

**Intervals:**
Data interval is auto-selected based on the period, but you can specify manually:
```bash
python stock_cli.py chart AAPL --period 1d --interval 5m
```

Valid intervals: `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1d`, `5d`, `1wk`, `1mo`, `3mo`

### Real-time Monitoring

Monitor stock prices in real-time with auto-refresh:

**Monitor with default 5-second refresh:**
```bash
python stock_cli.py monitor AAPL
```

**Monitor with custom refresh interval (10 seconds):**
```bash
python stock_cli.py monitor AMZN --refresh 10
```

Press `Ctrl+C` to stop monitoring.

## Examples

### Quick Price Check
```bash
python stock_cli.py quote MSFT
```

### View Weekly Performance
```bash
python stock_cli.py chart NVDA --period 5d --type candlestick
```

### Monitor Stock During Trading Hours
```bash
python stock_cli.py monitor TSLA --refresh 3
```

### View Long-term Trends
```bash
python stock_cli.py chart AAPL --period 5y --type line
```

### Intraday Trading Analysis
```bash
python stock_cli.py chart SPY --period 1d --type intraday
```

### View Price and Volume Comparison
```bash
python stock_cli.py chart AAPL --period 1mo --type comparison
```

### Search for Stock Information
```bash
python stock_cli.py search NVDA --detailed
```

### Compare Tech Giants Performance
```bash
python stock_cli.py compare AAPL MSFT --period 1y --type performance
```

### Compare Different Sectors
```bash
python stock_cli.py compare TSLA XOM --period 6mo --type price
```

### Check Analyst Ratings
```bash
python stock_cli.py analyst NVDA
```

### See Today's Market-Wide Analyst Changes
```bash
python stock_cli.py analyst market
```

## Common Stock Symbols

- **AAPL** - Apple Inc.
- **GOOGL** - Alphabet Inc. (Google)
- **MSFT** - Microsoft Corporation
- **AMZN** - Amazon.com Inc.
- **TSLA** - Tesla, Inc.
- **META** - Meta Platforms Inc. (Facebook)
- **NVDA** - NVIDIA Corporation
- **SPY** - S&P 500 ETF
- **QQQ** - NASDAQ-100 ETF

## Project Structure

```
stock-exchange-yahoo/
├── stock_cli.py          # Main CLI application
├── api.py                # REST API server (FastAPI)
├── stock_fetcher.py      # Yahoo Finance data fetcher
├── stock_visualizer.py   # Chart visualization module
├── realtime_monitor.py   # Real-time quote monitoring
├── requirements.txt      # Python dependencies
├── README.md             # Documentation
└── API_EXAMPLES.md       # API usage examples
```

## Dependencies

### Core
- **yfinance** - Yahoo Finance data API
- **pandas** - Data manipulation

### CLI
- **matplotlib** - Plotting library
- **mplfinance** - Financial charts
- **colorama** - Colored terminal output

### API
- **fastapi** - Modern web framework for APIs
- **uvicorn** - ASGI server
- **pydantic** - Data validation

## Tips

1. **Market Hours**: Real-time data is most accurate during market hours (9:30 AM - 4:00 PM ET)
2. **Refresh Rate**: For monitoring, a 5-10 second refresh rate is recommended to avoid rate limiting
3. **Data Intervals**: Shorter intervals (1m, 5m) are only available for recent periods (last 7 days)
4. **Chart Display**: Charts will open in a new window - close the window to return to the terminal

## Troubleshooting

**No data available:**
- Check that the stock symbol is correct
- Some symbols may not have data for all time periods
- Try a different period or interval

**Charts not displaying:**
- Ensure you have a display available (not in headless mode)
- On Linux, you may need to install tkinter: `sudo apt-get install python3-tk`

**Rate limiting:**
- If you see errors, reduce the frequency of requests
- For monitoring, increase the refresh interval

## Disclaimer

This tool is for informational purposes only. It is not financial advice. Always do your own research before making investment decisions.
