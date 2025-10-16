# API Usage Examples

This document provides detailed examples for using the Stock Exchange Yahoo Finance REST API.

## Starting the Server

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

## Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Examples

### 1. Get Stock Quote

**Request:**
```bash
curl http://localhost:8000/quote/AAPL
```

**Response:**
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

### 2. Search for Ticker Information

**Request:**
```bash
curl http://localhost:8000/search/TSLA
```

**Response:**
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

### 3. Get Analyst Ratings

**Request:**
```bash
curl http://localhost:8000/analyst/NVDA?limit=5
```

**Response:**
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

### 4. Get Market-Wide Analyst Changes

**Request:**
```bash
curl http://localhost:8000/analyst/market?days=1
```

**Response:**
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

### 5. Get Historical Data

**Request:**
```bash
curl "http://localhost:8000/historical/AAPL?period=5d&interval=1d"
```

**Response:**
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

### 6. Compare Two Stocks

**Request:**
```bash
curl "http://localhost:8000/compare/AAPL/MSFT?period=1mo&interval=1d"
```

**Response:**
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

### 7. Health Check

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-03-15T14:30:00.123456"
}
```

## Python Client Example

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
```

## JavaScript Client Example

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

## Error Handling

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

## Rate Limiting

Yahoo Finance may rate limit requests. If you experience issues:
- Add delays between requests
- Cache responses when possible
- Consider the time of day (market hours vs. off-hours)

## CORS

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

## Production Deployment

For production use:

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Or with uvicorn
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment

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
