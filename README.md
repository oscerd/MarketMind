# MarketMind - Stock Analysis CLI & API

A powerful tool for fetching real-time stock quotes, analyst ratings, and market data using Yahoo Finance. Available as both a command-line interface (CLI) and REST API.

## Features

- **Triple Interface**: CLI, REST API, and MCP Server for maximum flexibility
- **Quantitative Finance Analysis**: Professional-grade metrics including Sharpe ratio, Beta, Alpha, VaR, CVaR, drawdown analysis
- **Automated Investment Recommendations**: AI-driven BUY/SELL/HOLD recommendations based on quantitative analysis
- **AI-Powered Price Prediction**: Machine learning models predict future stock prices (ensemble, linear regression, moving average, advanced)
- **Real-time Quotes**: Get current stock prices, changes, and key metrics
- **Ticker Search**: Search for detailed company information by ticker symbol
- **Analyst Ratings**: View analyst recommendations, upgrades, and downgrades for individual stocks
- **Market-Wide Analyst Changes**: Scan major stocks to see all analyst rating changes across the market
- **Symbol Comparison**: Compare two stocks side-by-side with price or performance charts
- **Interactive Charts**: Display candlestick, line, and intraday charts (CLI only)
- **Live Monitoring**: Continuously monitor stock prices with auto-refresh (CLI only)
- **Multiple Time Periods**: View data from 1 day to max historical range
- **REST API**: Full-featured API with Swagger documentation and CORS support
- **MCP Server**: Model Context Protocol support for AI assistant integration
- **Colorful Display**: Easy-to-read colored output for better visualization (CLI)

## Installation

1. Navigate to the project directory:
```bash
cd MarketMind
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

This project provides three interfaces:
1. **Command-Line Interface (CLI)** - For terminal usage
2. **REST API** - For programmatic access via HTTP
3. **MCP Server** - For AI assistant integration via Model Context Protocol

All interfaces include **AI-powered price prediction** using machine learning models!

### REST API

#### Starting the Server

Start the API server:
```bash
# Basic start
python api.py

# With custom host and port
uvicorn api:app --host 0.0.0.0 --port 8080

# With auto-reload (for development)
uvicorn api:app --reload

# With logging
uvicorn api:app --log-level debug
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
| `/predict/{symbol}?days=7` | GET | Predict future stock prices |
| `/quant/{symbol}?benchmark=SPY&period=1y` | GET | Get quantitative finance analysis |
| `/financials/{symbol}/summary` | GET | Get comprehensive financial summary |
| `/financials/{symbol}/income?quarterly=false` | GET | Get income statement |
| `/financials/{symbol}/balance?quarterly=false` | GET | Get balance sheet |
| `/financials/{symbol}/cashflow?quarterly=false` | GET | Get cash flow statement |
| `/financials/{symbol}/metrics` | GET | Get key financial metrics and ratios |
| `/financials/{symbol}/earnings` | GET | Get historical earnings data |
| `/financials/{symbol}/next-earnings` | GET | Get next earnings date with estimates |
| `/health` | GET | Health check endpoint |

#### Detailed API Examples

**1. Get Stock Quote**

Request:
```bash
curl http://localhost:8000/quote/AAPL
```

Response:
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
  "fifty_two_week_high": 199.62,
  "fifty_two_week_low": 164.08,
  "change": 2.30,
  "change_percent": 1.31
}
```

**2. Search for Ticker Information**

Request:
```bash
curl http://localhost:8000/search/TSLA
```

Response:
```json
{
  "symbol": "TSLA",
  "name": "Tesla, Inc.",
  "exchange": "NMS",
  "quote_type": "EQUITY",
  "currency": "USD",
  "market_cap": 800000000000,
  "sector": "Consumer Cyclical",
  "industry": "Auto Manufacturers",
  "country": "United States",
  "website": "https://www.tesla.com",
  "description": "Tesla, Inc. designs, develops, manufactures, leases, and sells electric vehicles..."
}
```

**3. Get Analyst Ratings**

Request:
```bash
curl http://localhost:8000/analyst/NVDA?limit=5
```

Response:
```json
{
  "summary": {
    "recommendation": "BUY",
    "target_mean": 650.50,
    "target_high": 850.00,
    "target_low": 500.00,
    "num_analysts": 52,
    "recommendation_mean": 1.85
  },
  "recent_changes": [
    {
      "date": "2024-03-15",
      "firm": "Morgan Stanley",
      "action": "Upgrade",
      "from_grade": "Overweight",
      "to_grade": "Buy"
    },
    {
      "date": "2024-03-10",
      "firm": "JP Morgan",
      "action": "Maintains",
      "from_grade": "N/A",
      "to_grade": "Overweight"
    }
  ]
}
```

**4. Get Market-Wide Analyst Changes**

Request:
```bash
curl http://localhost:8000/analyst/market?days=1
```

Response:
```json
[
  {
    "symbol": "NVDA",
    "date": "2024-03-15 14:30:00",
    "firm": "Morgan Stanley",
    "action": "Upgrade",
    "from_grade": "Overweight",
    "to_grade": "Buy"
  },
  {
    "symbol": "AAPL",
    "date": "2024-03-15 12:15:00",
    "firm": "JP Morgan",
    "action": "Maintains",
    "from_grade": "N/A",
    "to_grade": "Overweight"
  }
]
```

**5. Get Historical Data**

Request:
```bash
curl "http://localhost:8000/historical/AAPL?period=5d&interval=1d"
```

Response:
```json
[
  {
    "date": "2024-03-11 00:00:00",
    "open": 175.50,
    "high": 178.20,
    "low": 175.10,
    "close": 177.80,
    "volume": 52000000
  },
  {
    "date": "2024-03-12 00:00:00",
    "open": 177.90,
    "high": 179.50,
    "low": 176.80,
    "close": 178.45,
    "volume": 51500000
  }
]
```

**6. Compare Two Stocks**

Request:
```bash
curl "http://localhost:8000/compare/AAPL/MSFT?period=1mo&interval=1d"
```

Response:
```json
{
  "AAPL": [
    {
      "date": "2024-02-15 00:00:00",
      "open": 175.50,
      "high": 178.20,
      "low": 175.10,
      "close": 177.80,
      "volume": 52000000
    }
  ],
  "MSFT": [
    {
      "date": "2024-02-15 00:00:00",
      "open": 405.30,
      "high": 410.50,
      "low": 404.20,
      "close": 408.90,
      "volume": 28000000
    }
  ]
}
```

**7. Predict Future Stock Prices**

Request:
```bash
curl http://localhost:8000/predict/AAPL?days=7
```

Response includes predictions with conservative, moderate, and optimistic estimates using ensemble machine learning methods.

**8. Get Quantitative Analysis**

Request:
```bash
curl "http://localhost:8000/quant/AAPL?benchmark=SPY&period=1y"
```

Response includes:
- Comprehensive metrics: Sharpe ratio, Beta, Alpha, VaR, drawdown analysis
- Automated investment recommendations with confidence levels
- **metrics_glossary**: Detailed descriptions of every metric and interpretation guide
- **interpretation_guide**: Threshold values for rating each metric (good/poor/excellent)

**9. Get Financial Summary**

Request:
```bash
curl http://localhost:8000/financials/AAPL/summary
```

Response includes revenue, profitability, balance sheet, cash flow, and key financial ratios in a concise format.

**10. Get Financial Metrics**

Request:
```bash
curl http://localhost:8000/financials/TSLA/metrics
```

Response includes:
- **Valuation metrics**: P/E, PEG, Price/Book, EV/EBITDA, etc.
- **Profitability metrics**: Profit margin, ROE, ROA, Operating margin
- **Financial health**: Current ratio, Debt/Equity, Free cash flow
- **Growth metrics**: Revenue growth, Earnings growth
- **Dividend metrics**: Dividend yield, Payout ratio
- **metrics_glossary**: Descriptions of each metric

**11. Get Income Statement**

Request:
```bash
# Annual income statement
curl http://localhost:8000/financials/MSFT/income

# Quarterly income statement
curl "http://localhost:8000/financials/MSFT/income?quarterly=true"
```

Response includes revenue, expenses, and net income across multiple periods.

**12. Get Earnings History**

Request:
```bash
curl http://localhost:8000/financials/NVDA/earnings
```

Response shows historical earnings with analyst estimates vs actual reported EPS.

**13. Get Next Earnings Date**

Request:
```bash
curl http://localhost:8000/financials/AAPL/next-earnings
```

Response:
```json
{
  "symbol": "AAPL",
  "next_earnings_date": "2024-11-01",
  "earnings_estimate": {
    "average": 1.60,
    "low": 1.55,
    "high": 1.65
  },
  "revenue_estimate": {
    "average": 89500000000,
    "low": 88000000000,
    "high": 91000000000
  },
  "description": "Next scheduled earnings date with analyst estimates"
}
```

This shows the next scheduled earnings report date along with analyst consensus estimates for both EPS and revenue.

**14. Health Check**

Request:
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-03-15T14:30:00.123456"
}
```

#### Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Get quote
response = requests.get(f"{BASE_URL}/quote/AAPL")
quote = response.json()
print(f"{quote['symbol']}: ${quote['current_price']}")

# Get analyst ratings
response = requests.get(f"{BASE_URL}/analyst/TSLA", params={"limit": 10})
analyst_data = response.json()
print(f"Recommendation: {analyst_data['summary']['recommendation']}")
print(f"Price Target: ${analyst_data['summary']['target_mean']}")

# Get market changes
response = requests.get(f"{BASE_URL}/analyst/market", params={"days": 3})
changes = response.json()
for change in changes:
    print(f"{change['symbol']}: {change['action']} by {change['firm']}")

# Compare stocks
response = requests.get(f"{BASE_URL}/compare/AAPL/MSFT", params={"period": "1mo"})
comparison = response.json()
print(f"AAPL has {len(comparison['AAPL'])} data points")
print(f"MSFT has {len(comparison['MSFT'])} data points")

# Get quantitative analysis with recommendation
response = requests.get(f"{BASE_URL}/quant/AAPL", params={"benchmark": "SPY", "period": "1y"})
quant = response.json()
rec = quant['recommendation']
print(f"Recommendation: {rec['recommendation']}")
print(f"Action: {rec['action']}")
print(f"Score: {rec['score']}/10")
print(f"Positive Signals: {len(rec['positive_signals'])}")
print(f"Risk Warnings: {len(rec['risk_warnings'])}")
```

#### JavaScript Client Example

```javascript
const BASE_URL = 'http://localhost:8000';

// Get quote
async function getQuote(symbol) {
  const response = await fetch(`${BASE_URL}/quote/${symbol}`);
  const quote = await response.json();
  console.log(`${quote.symbol}: $${quote.current_price}`);
  return quote;
}

// Get analyst ratings
async function getAnalystRatings(symbol, limit = 10) {
  const response = await fetch(`${BASE_URL}/analyst/${symbol}?limit=${limit}`);
  const data = await response.json();
  console.log(`Recommendation: ${data.summary.recommendation}`);
  console.log(`Price Target: $${data.summary.target_mean}`);
  return data;
}

// Get market changes
async function getMarketChanges(days = 1) {
  const response = await fetch(`${BASE_URL}/analyst/market?days=${days}`);
  const changes = await response.json();
  changes.forEach(change => {
    console.log(`${change.symbol}: ${change.action} by ${change.firm}`);
  });
  return changes;
}

// Usage
getQuote('AAPL');
getAnalystRatings('TSLA', 5);
getMarketChanges(3);
```

#### Error Handling

The API returns standard HTTP status codes:

- **200 OK**: Successful request
- **404 Not Found**: Symbol or data not found
- **500 Internal Server Error**: Server error

**Error Response Format:**
```json
{
  "detail": "No data found for symbol XYZ"
}
```

#### Rate Limiting

Yahoo Finance may rate limit requests. If you experience issues:
- Add delays between requests
- Cache responses when possible
- Consider the time of day (market hours vs. off-hours)

#### CORS Configuration

CORS is enabled for all origins by default. In production, configure specific origins in `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Production Deployment

For production use:

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Or with uvicorn
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

**Docker Deployment**

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t stock-api .
docker run -p 8000:8000 stock-api
```

### MCP Server

MarketMind can be exposed as an MCP (Model Context Protocol) server, allowing AI assistants like Claude to directly access stock market data and analysis.

#### What is MCP?

The Model Context Protocol (MCP) is an open protocol that standardizes how AI assistants connect to external data sources and tools. By running MarketMind as an MCP server, you can enable Claude or other AI assistants to fetch stock quotes, perform quantitative analysis, get predictions, and more.

#### Running the MCP Server

Start the MCP server using Python:

```bash
python mcp_server.py
```

Or use it with the MCP Python SDK:

```bash
mcp run mcp_server.py
```

#### Available Tools

The MCP server exposes the following tools:

| Tool | Description |
|------|-------------|
| `get_stock_quote` | Get current stock quote with price, volume, and key metrics |
| `search_stock` | Search for detailed company information by ticker symbol |
| `get_analyst_ratings` | Get analyst ratings and recent upgrades/downgrades |
| `get_historical_data` | Get historical stock data for a given period |
| `compare_stocks` | Compare two stocks side by side |
| `predict_stock_price` | Predict future prices using ML ensemble methods |
| `get_quantitative_analysis` | Get comprehensive quant analysis with investment recommendations |
| `get_financial_summary` | Get comprehensive financial summary (revenue, profitability, ratios) |
| `get_financial_metrics` | Get detailed financial metrics (valuation, profitability, growth, dividends) |
| `get_income_statement` | Get income statement (revenue, expenses, net income) |
| `get_balance_sheet` | Get balance sheet (assets, liabilities, equity) |
| `get_cash_flow_statement` | Get cash flow statement (operating, investing, financing) |
| `get_earnings_history` | Get historical earnings with estimates vs actuals |
| `get_next_earnings_date` | Get next scheduled earnings date with analyst EPS and revenue estimates |

#### Configuring Claude Desktop

To use MarketMind with Claude Desktop, add this configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "marketmind": {
      "command": "python",
      "args": ["/absolute/path/to/MarketMind/mcp_server.py"]
    }
  }
}
```

Replace `/absolute/path/to/MarketMind/` with the actual path to your MarketMind installation.

A template configuration file is provided in `mcp_config_example.json` for your reference.

#### Using with Claude

Once configured, you can ask Claude things like:

**Stock Data:**
- "What's the current price of AAPL?"
- "Get me analyst ratings for TSLA"
- "Compare AAPL and MSFT performance over the last month"

**Analysis:**
- "Predict the price of NVDA for the next 7 days"
- "Give me a quantitative analysis of GOOGL"

**Financials:**
- "Show me Apple's financial summary"
- "What are Tesla's key financial metrics and ratios?"
- "Get Microsoft's latest earnings results"
- "When is Apple's next earnings date?"
- "Show me the income statement for NVDA"
- "What's Amazon's profit margin and ROE?"

Claude will automatically use the MarketMind MCP tools to fetch and analyze the data.

#### Example Interactions

**Getting a stock quote:**
```
User: What's the current price and key metrics for Apple stock?
Claude: [Uses get_stock_quote tool with symbol "AAPL"]
```

**Quantitative analysis:**
```
User: Can you analyze Tesla's performance with risk metrics?
Claude: [Uses get_quantitative_analysis tool to get Sharpe ratio, Beta, VaR, etc.]
```

**Price prediction:**
```
User: Predict NVIDIA's stock price for the next week
Claude: [Uses predict_stock_price tool to get ML-based predictions]
```

### Command-Line Interface

The CLI has eight main commands: `quote`, `chart`, `monitor`, `search`, `compare`, `analyst`, `predict`, and `quant`.

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

### Predict Future Stock Prices

Use machine learning to predict future stock prices based on historical data:

**Ensemble prediction (combines multiple ML methods - recommended):**
```bash
python stock_cli.py predict AAPL
```

Example output:
```
=== AAPL Price Prediction ===

Current Price: $178.45

Ensemble Predictions (Next 7 days):

Date         Conservative    Moderate        Optimistic      Change %
---------------------------------------------------------------------------
2024-03-16   $176.20        $179.30        $182.40        ↑   0.48%
2024-03-17   $177.50        $180.15        $182.80        ↑   0.95%
2024-03-18   $178.10        $181.00        $183.90        ↑   1.43%
2024-03-19   $178.80        $181.85        $184.90        ↑   1.91%
2024-03-20   $179.40        $182.70        $186.00        ↑   2.38%
2024-03-21   $180.00        $183.55        $187.10        ↑   2.86%
2024-03-22   $180.60        $184.40        $188.20        ↑   3.34%

Methods Used: Linear Regression, Moving Average, Advanced Multi-Feature
```

**Predict with specific method:**
```bash
# Linear regression
python stock_cli.py predict TSLA --method linear --days 14

# Moving average
python stock_cli.py predict GOOGL --method ma --days 5

# Advanced multi-feature
python stock_cli.py predict NVDA --method advanced --days 10
```

**Available Methods:**
- `ensemble` (default) - Combines multiple methods for best accuracy
- `linear` - Linear regression on recent trend
- `ma` - Moving average based prediction
- `advanced` - Uses technical indicators (SMA, MACD, ROC, volatility)

**Prediction Outputs:**
- **Conservative**: Lower bound estimate (minimum expected price)
- **Moderate**: Most likely price (weighted average of methods)
- **Optimistic**: Upper bound estimate (maximum expected price)
- **Change %**: Percentage change from current price (for moderate estimate)

⚠️ **Important**: Predictions are for informational purposes only and should NOT be used as financial advice.

### Quantitative Finance Analysis

Perform professional-grade quantitative analysis with risk metrics, performance ratios, and market comparisons:

**Basic quantitative analysis:**
```bash
python stock_cli.py quant AAPL
```

Example output:
```
=== AAPL Quantitative Analysis ===

Analysis Period:
From: 2023-03-16
To:   2024-03-15
Trading Days: 252

Return Metrics:
Total Return:            25.34%
Annualized Return:       25.34%
Annualized Volatility:   28.45%
Daily Avg Return:        0.1005%
Daily Volatility:        1.7893%

Risk-Adjusted Performance:
Sharpe Ratio:              1.85
Sortino Ratio:             2.43
Information Ratio:         0.67

Value at Risk (VaR):
95% VaR (1-day):          -2.85%
95% CVaR:                 -3.92%
99% VaR (1-day):          -4.21%

Drawdown Analysis:
Max Drawdown:            -18.45%
Peak Date:                2023-07-31
Trough Date:              2023-10-27
Recovery Period:          45 days
Current Drawdown:         -2.13%

Market Metrics (vs SPY):
Beta:                      1.15
  → More volatile than market
Alpha (annualized):        3.42%
  → Outperforming market

Investment Recommendation:
===========================================================================

Recommendation: BUY
Confidence: Moderate
Score: 4/10

Action: Consider initiating or adding to position. Positive indicators outweigh concerns.

Positive Signals:
  ✓ Good risk-adjusted returns (Sharpe > 1)
  ✓ Modest outperformance vs benchmark (Alpha: 3.42%)
  ✓ Positive returns (25.3%)

Risk Warnings:
  ⚠ Currently in moderate drawdown (-2.1%)
  ⚠ High daily risk (VaR: 2.9%)

Summary:
Based on quantitative analysis, the recommendation is BUY. Score: 4/10. 3 positive signals, 2 warnings.

⚠️  DISCLAIMER:
This recommendation is based solely on historical quantitative metrics and should not be
considered as financial advice. Always conduct thorough research and consider your personal
financial situation before making investment decisions.

===========================================================================

Quick Interpretation Guide:
  Sharpe Ratio:  >1 = Good, >2 = Very Good, >3 = Excellent
  Sortino Ratio: Similar to Sharpe, but focuses on downside risk
  Beta:          <1 = Less volatile, =1 = Market volatility, >1 = More volatile
  Alpha:         >0 = Outperforming, <0 = Underperforming
  VaR:           Maximum expected loss at given confidence level

For detailed explanations of all metrics, see the comprehensive glossary below.
```

**Analysis with custom benchmark:**
```bash
python stock_cli.py quant TSLA --benchmark QQQ --period 2y
```

**Custom analysis period:**
```bash
python stock_cli.py quant NVDA --period 6mo
```

**Quantitative Metrics Glossary:**

#### Return Metrics

- **Total Return**: The overall percentage gain or loss over the analysis period
- **Annualized Return**: Expected yearly return based on average daily performance (assumes 252 trading days)
- **Annualized Volatility**: Standard deviation of returns scaled to annual basis. Measures how much prices fluctuate
- **Daily Return Mean**: Average daily percentage change
- **Daily Volatility**: Standard deviation of daily returns

#### Risk-Adjusted Performance

- **Sharpe Ratio**: Measures excess return per unit of total risk
  - Formula: (Return - Risk-Free Rate) / Volatility
  - Interpretation: >1 = Good, >2 = Very Good, >3 = Excellent
  - Higher values indicate better risk-adjusted performance

- **Sortino Ratio**: Similar to Sharpe but only penalizes downside volatility
  - Better for assets with asymmetric return distributions
  - Only considers negative returns when calculating risk
  - Interpretation: Same as Sharpe (>1 is good)

- **Information Ratio**: Measures consistency of excess returns versus benchmark
  - Shows how reliably a stock outperforms its benchmark
  - Interpretation: >0.5 = Good, >1.0 = Excellent

#### Market-Relative Metrics

- **Beta**: Measures volatility relative to the market (typically S&P 500)
  - Beta < 1: Less volatile than market (defensive)
  - Beta = 1: Moves with market
  - Beta > 1: More volatile than market (aggressive)
  - Example: Beta of 1.3 means stock moves 30% more than market

- **Alpha**: Excess return beyond what Beta predicts (annualized)
  - Positive Alpha: Outperforming the market
  - Negative Alpha: Underperforming the market
  - Example: Alpha of 3% means stock returns 3% more per year than expected

#### Risk Metrics

- **Value at Risk (VaR)**: Maximum expected loss at a given confidence level
  - VaR 95% of -2.5%: 95% confidence you won't lose more than 2.5% in one day
  - VaR 99% provides higher confidence but larger loss estimate
  - Used for risk management and position sizing

- **Conditional VaR (CVaR)**: Average loss when VaR threshold is breached
  - Also called Expected Shortfall
  - Measures "tail risk" - how bad losses are when they occur
  - Always worse than VaR (measures extreme scenarios)

- **Maximum Drawdown**: Largest peak-to-trough decline during the period
  - Shows worst historical loss from a high point
  - Important for understanding downside risk
  - Interpretation: <-10% = Low Risk, -10% to -20% = Moderate, -20% to -30% = High, >-30% = Very High

- **Current Drawdown**: Current decline from recent peak
  - Negative value indicates stock is below its recent high
  - Shows if currently in a losing position

#### Understanding the Metrics Together

**Risk-Adjusted Returns (Sharpe/Sortino)**: Higher ratios mean you're getting better returns for the risk you're taking. A Sharpe of 2.0 is twice as good as 1.0.

**Market Comparison (Beta/Alpha)**: Beta tells you how volatile the stock is. Alpha tells you if the extra risk is worth it. Ideal: High Alpha (outperforming) with manageable Beta.

**Downside Protection (VaR/CVaR/Drawdown)**: These show potential losses. VaR gives typical bad days, CVaR shows extreme scenarios, and Max Drawdown shows historical worst case.

**Trading Days**: All annualized metrics assume 252 trading days per year (typical for US markets)

#### JSON Output Format

When using the API or MCP server, the quantitative analysis includes a `metrics_glossary` section with descriptions for every metric:

```json
{
  "symbol": "AAPL",
  "returns": { ... },
  "risk_metrics": { ... },
  "market_metrics": { ... },
  "recommendation": { ... },
  "metrics_glossary": {
    "returns": {
      "total_return_pct": "Total percentage return over the analysis period",
      "annualized_return_pct": "Expected annual return..."
    },
    "risk_metrics": {
      "sharpe_ratio": "Risk-adjusted return metric. Measures excess return per unit of risk...",
      "var_95": "Value at Risk at 95% confidence..."
    },
    "interpretation_guide": {
      "sharpe_ratio": {
        "poor": "< 0",
        "acceptable": "0 - 1",
        "good": "1 - 2",
        "very_good": "2 - 3",
        "excellent": "> 3"
      }
    }
  }
}
```

This makes the API self-documenting - every response includes explanations of what each metric means and how to interpret it.

**Investment Recommendation System:**

The analysis includes an automated recommendation (STRONG BUY, BUY, HOLD, SELL, STRONG SELL) based on:
- Risk-adjusted performance (Sharpe ratio)
- Market outperformance (Alpha)
- Return vs volatility analysis
- Current drawdown status
- Risk metrics (VaR, Beta)

Each recommendation includes:
- **Confidence Level**: High or Moderate
- **Score**: -10 to +10 based on quantitative factors
- **Positive Signals**: Strengths identified
- **Risk Warnings**: Concerns to consider
- **Action Guidance**: Suggested course of action

**Important**: Recommendations are based purely on historical quantitative data and should not be the sole basis for investment decisions.

### Financial Statements and Metrics

Get comprehensive financial data including income statements, balance sheets, cash flow, and key financial metrics.

**Get financial summary:**
```bash
python stock_cli.py financials AAPL
```

Example output:
```
=== AAPL Financial Data ===

Apple Inc.

Revenue:
Total Revenue:      $394,328,000,000
Revenue/Share:      $24.54
Revenue Growth:     -2.80%

Profitability:
Net Income:         $96,995,000,000
EPS:                $6.13
Profit Margin:      24.57%
Operating Margin:   30.74%

Balance Sheet:
Total Assets:       $352,755,000,000
Total Debt:         $111,088,000,000
Total Cash:         $61,555,000,000
Book Value/Share:   $4.837

Cash Flow:
Operating CF:       $110,543,000,000
Free Cash Flow:     $99,584,000,000

Key Ratios:
P/E Ratio:          29.43
Price/Book:         46.67
ROE:                147.25%
ROA:                27.51%
Current Ratio:      0.98
Debt/Equity:        181.18
```

**Get detailed financial metrics:**
```bash
python stock_cli.py financials AAPL --type metrics
```

This displays comprehensive metrics across five categories:
- **Valuation Metrics**: Market cap, P/E, PEG, Price/Book, Price/Sales, EV/EBITDA
- **Profitability Metrics**: Profit margin, Operating margin, ROE, ROA, Gross margin
- **Financial Health**: Current ratio, Quick ratio, Debt/Equity, Free cash flow
- **Growth Metrics**: Revenue growth, Earnings growth, EPS
- **Dividend Metrics**: Dividend rate, Yield, Payout ratio

**Get earnings history:**
```bash
python stock_cli.py financials TSLA --type earnings
```

Shows historical earnings reports with:
- Analyst estimates vs actual reported EPS
- Earnings surprise percentage (color-coded: green for beat, red for miss)
- Date of each earnings report

**Get income statement:**
```bash
python stock_cli.py financials MSFT --type income
```

Get quarterly data instead of annual:
```bash
python stock_cli.py financials GOOGL --type income --quarterly
```

**Get balance sheet:**
```bash
python stock_cli.py financials NVDA --type balance
```

**Get cash flow statement:**
```bash
python stock_cli.py financials META --type cashflow --quarterly
```

**Get next earnings date:**
```bash
python stock_cli.py financials AAPL --type next-earnings
```

Example output:
```
=== AAPL Financial Data ===

Next Earnings Date:

📅  Earnings Date:     2024-11-01

EPS Estimates:
Average:            $1.60
Low:                $1.55
High:               $1.65

Revenue Estimates:
Average:            $89.50B
Low:                $88.00B
High:               $91.00B
```

#### Financial Data Types

- `summary` (default) - High-level overview of revenue, profitability, balance sheet, cash flow, and key ratios
- `metrics` - Comprehensive financial metrics across all categories
- `earnings` - Historical earnings with estimates vs actuals
- `next-earnings` - Next scheduled earnings date with analyst EPS and revenue estimates
- `income` - Income statement (revenue, expenses, net income)
- `balance` - Balance sheet (assets, liabilities, equity)
- `cashflow` - Cash flow statement (operating, investing, financing activities)

#### Understanding Financial Metrics

**Valuation Metrics** - How the market values the company:
- **P/E Ratio**: Price divided by earnings. Lower may indicate undervaluation
- **PEG Ratio**: P/E adjusted for growth. < 1 is considered attractive
- **Price/Book**: Price divided by book value. Useful for asset-heavy companies
- **EV/EBITDA**: Enterprise value to earnings. Good for comparing companies with different capital structures

**Profitability Metrics** - How efficiently the company generates profit:
- **Profit Margin**: Net income as % of revenue. Higher is better
- **ROE (Return on Equity)**: How well company uses shareholder equity. >15% is good
- **ROA (Return on Assets)**: How efficiently company uses assets. >5% is good

**Financial Health** - Company's ability to meet obligations:
- **Current Ratio**: Current assets / current liabilities. >1 means can cover short-term debts
- **Quick Ratio**: Like current ratio but excludes inventory. >1 is healthy
- **Debt/Equity**: Total debt / shareholder equity. Lower is generally better

**Growth Metrics** - How fast the company is expanding:
- **Revenue Growth**: Year-over-year revenue increase. Positive is good
- **Earnings Growth**: Year-over-year earnings increase

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

### Predict Future Prices
```bash
python stock_cli.py predict AAPL --days 14
```

### Quantitative Analysis
```bash
python stock_cli.py quant TSLA --benchmark QQQ --period 1y
```

### Get Financial Summary
```bash
python stock_cli.py financials AAPL
```

### View Financial Metrics
```bash
python stock_cli.py financials MSFT --type metrics
```

### Check Earnings History
```bash
python stock_cli.py financials NVDA --type earnings
```

### Get Next Earnings Date
```bash
python stock_cli.py financials TSLA --type next-earnings
```

### Get Quarterly Income Statement
```bash
python stock_cli.py financials GOOGL --type income --quarterly
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
MarketMind/
├── stock_cli.py             # Main CLI application
├── api.py                   # REST API server (FastAPI)
├── mcp_server.py            # MCP server for AI assistant integration
├── mcp_config_example.json  # Example MCP configuration
├── stock_fetcher.py         # Yahoo Finance data fetcher
├── stock_predictor.py       # AI price prediction models
├── quant_analysis.py        # Quantitative finance analysis
├── financial_data.py        # Financial statements and metrics
├── stock_visualizer.py      # Chart visualization module
├── realtime_monitor.py      # Real-time quote monitoring
├── requirements.txt         # Python dependencies
└── README.md                # Complete documentation
```

## Dependencies

### Core
- **yfinance** - Yahoo Finance data API
- **pandas** - Data manipulation
- **numpy** - Numerical computing

### Machine Learning
- **scikit-learn** - ML models for price prediction
- Technical indicators and statistical analysis

### CLI
- **matplotlib** - Plotting library
- **mplfinance** - Financial charts
- **colorama** - Colored terminal output

### API
- **fastapi** - Modern web framework for APIs
- **uvicorn** - ASGI server
- **pydantic** - Data validation

### MCP
- **mcp** - Model Context Protocol SDK for AI assistant integration

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

This is a pet project and it's used for demo purpose only. 
This tool is for informational purposes and it is not financial advice. Always do your own research before making investment decisions.
