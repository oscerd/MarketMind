#!/usr/bin/env python3
"""
MarketMind CLI
A command-line tool for fetching real-time stock quotes and displaying charts.
"""

import argparse
import sys
from typing import List
from .stock_fetcher import StockFetcher
from .stock_visualizer import StockVisualizer
from .realtime_monitor import RealtimeMonitor
from .stock_predictor import StockPredictor
from .quant_analysis import QuantAnalysis
from .financial_data import FinancialData
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def print_quote(symbol: str):
    """Print current quote information."""
    fetcher = StockFetcher(symbol)
    quote_data = fetcher.get_quote_info()

    if not quote_data:
        print(f"{Fore.RED}Failed to fetch quote data for {symbol}{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== {symbol} Quote ==={Style.RESET_ALL}\n")
    print(f"{Fore.WHITE}{quote_data.get('name', 'N/A')}{Style.RESET_ALL}")

    current_price = quote_data.get('current_price', 'N/A')
    if current_price != 'N/A':
        print(f"Current Price: {Fore.YELLOW}${current_price:.2f}{Style.RESET_ALL}")
    else:
        print(f"Current Price: N/A")

    change = quote_data.get('change', 'N/A')
    change_percent = quote_data.get('change_percent', 'N/A')

    if change != 'N/A' and change_percent != 'N/A':
        color = Fore.GREEN if change >= 0 else Fore.RED
        sign = '+' if change >= 0 else ''
        print(f"Change: {color}{sign}${change:.2f} ({sign}{change_percent:.2f}%){Style.RESET_ALL}")
    else:
        print("Change: N/A")

    print(f"\nOpen: ${quote_data.get('open', 'N/A')}")
    print(f"High: ${quote_data.get('day_high', 'N/A')}")
    print(f"Low: ${quote_data.get('day_low', 'N/A')}")
    print(f"Previous Close: ${quote_data.get('previous_close', 'N/A')}")
    print(f"Volume: {quote_data.get('volume', 'N/A')}\n")


def show_chart(symbol: str, period: str = '1mo', chart_type: str = 'line', interval: str = None):
    """Display stock chart."""
    fetcher = StockFetcher(symbol)
    visualizer = StockVisualizer(symbol)

    # Auto-select interval based on period if not specified
    if interval is None:
        if period in ['1d']:
            interval = '5m'
        elif period in ['5d']:
            interval = '15m'
        elif period in ['1mo', '3mo']:
            interval = '1d'
        else:
            interval = '1d'

    print(f"{Fore.CYAN}Fetching {period} data for {symbol}...{Style.RESET_ALL}")
    data = fetcher.get_historical_data(period=period, interval=interval)

    if data.empty:
        print(f"{Fore.RED}No data available for the specified period{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}Data fetched successfully. Displaying chart...{Style.RESET_ALL}\n")

    if chart_type == 'candlestick':
        visualizer.plot_candlestick(data)
    elif chart_type == 'line':
        visualizer.plot_line(data)
    elif chart_type == 'intraday':
        visualizer.plot_intraday(data)
    elif chart_type == 'comparison':
        visualizer.plot_realtime_comparison(data)
    else:
        print(f"{Fore.RED}Unknown chart type: {chart_type}{Style.RESET_ALL}")


def start_realtime_monitor(symbol: str, refresh: int = 5):
    """Start real-time quote monitoring."""
    monitor = RealtimeMonitor(symbol, refresh_interval=refresh)
    monitor.start_monitoring()


# Default list of major stocks to monitor for market-wide changes
DEFAULT_MARKET_SYMBOLS = [
    # Tech giants
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'AMD', 'INTC', 'CRM',
    # Finance
    'JPM', 'BAC', 'GS', 'MS', 'WFC', 'C', 'V', 'MA',
    # Healthcare
    'JNJ', 'UNH', 'PFE', 'ABBV', 'MRK', 'LLY', 'TMO',
    # Consumer
    'WMT', 'HD', 'DIS', 'NKE', 'COST', 'MCD', 'SBUX', 'PG',
    # Energy
    'XOM', 'CVX', 'COP', 'SLB',
    # Industrial
    'BA', 'CAT', 'GE', 'UPS',
    # Communication
    'T', 'VZ', 'NFLX',
    # Semiconductors
    'TSM', 'AVGO', 'QCOM', 'MU',
]


def show_quant_analysis(symbol: str, benchmark: str = 'SPY', period: str = '1y'):
    """Display quantitative finance analysis."""
    fetcher = StockFetcher(symbol)

    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== {symbol} Quantitative Analysis ==={Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}Fetching {period} of historical data...{Style.RESET_ALL}\n")

    # Get stock data
    stock_data = fetcher.get_historical_data(period=period, interval='1d')

    if stock_data.empty:
        print(f"{Fore.RED}No data available for {symbol}{Style.RESET_ALL}\n")
        return

    # Get benchmark data if specified
    benchmark_data = None
    if benchmark:
        print(f"{Fore.YELLOW}Fetching benchmark data ({benchmark})...{Style.RESET_ALL}\n")
        benchmark_fetcher = StockFetcher(benchmark)
        benchmark_data = benchmark_fetcher.get_historical_data(period=period, interval='1d')

    # Perform analysis
    quant = QuantAnalysis(symbol, stock_data, benchmark_data)
    analysis = quant.get_comprehensive_analysis()

    # Display analysis period
    print(f"{Fore.WHITE}{Style.BRIGHT}Analysis Period:{Style.RESET_ALL}")
    print(f"From: {analysis['analysis_period']['start_date']}")
    print(f"To:   {analysis['analysis_period']['end_date']}")
    print(f"Trading Days: {analysis['analysis_period']['trading_days']}\n")

    # Display returns
    returns = analysis['returns']
    if 'error' not in returns:
        print(f"{Fore.WHITE}{Style.BRIGHT}Return Metrics:{Style.RESET_ALL}")
        print(f"Total Return:          {Fore.GREEN if returns['total_return_pct'] > 0 else Fore.RED}{returns['total_return_pct']:>8.2f}%{Style.RESET_ALL}")
        print(f"Annualized Return:     {returns['annualized_return_pct']:>8.2f}%")
        print(f"Annualized Volatility: {returns['annualized_volatility_pct']:>8.2f}%")
        print(f"Daily Avg Return:      {returns['daily_return_mean_pct']:>8.4f}%")
        print(f"Daily Volatility:      {returns['daily_return_std_pct']:>8.4f}%\n")

    # Display risk metrics
    risk = analysis['risk_metrics']
    print(f"{Fore.WHITE}{Style.BRIGHT}Risk-Adjusted Performance:{Style.RESET_ALL}")

    sharpe = risk['sharpe_ratio']
    sharpe_color = Fore.GREEN if sharpe > 1 else Fore.YELLOW if sharpe > 0 else Fore.RED
    print(f"Sharpe Ratio:          {sharpe_color}{sharpe:>8.2f}{Style.RESET_ALL}")

    sortino = risk['sortino_ratio']
    sortino_color = Fore.GREEN if sortino > 1 else Fore.YELLOW if sortino > 0 else Fore.RED
    print(f"Sortino Ratio:         {sortino_color}{sortino:>8.2f}{Style.RESET_ALL}")

    if risk['information_ratio'] is not None:
        ir = risk['information_ratio']
        ir_color = Fore.GREEN if ir > 0.5 else Fore.YELLOW if ir > 0 else Fore.RED
        print(f"Information Ratio:     {ir_color}{ir:>8.2f}{Style.RESET_ALL}")

    print()

    # Display VaR
    print(f"{Fore.WHITE}{Style.BRIGHT}Value at Risk (VaR):{Style.RESET_ALL}")
    var_95 = risk['var_95']
    if 'error' not in var_95:
        print(f"95% VaR (1-day):       {Fore.RED}{var_95['historical_var_pct']:>8.2f}%{Style.RESET_ALL}")
        print(f"95% CVaR:              {Fore.RED}{risk['cvar_95']:>8.2f}%{Style.RESET_ALL}")

    var_99 = risk['var_99']
    if 'error' not in var_99:
        print(f"99% VaR (1-day):       {Fore.RED}{var_99['historical_var_pct']:>8.2f}%{Style.RESET_ALL}")

    print()

    # Display drawdown
    dd = risk['max_drawdown']
    if 'error' not in dd:
        print(f"{Fore.WHITE}{Style.BRIGHT}Drawdown Analysis:{Style.RESET_ALL}")
        print(f"Max Drawdown:          {Fore.RED}{dd['max_drawdown_pct']:>8.2f}%{Style.RESET_ALL}")
        print(f"Peak Date:             {dd['peak_date']}")
        print(f"Trough Date:           {dd['trough_date']}")
        if dd['recovery_period_days']:
            print(f"Recovery Period:       {dd['recovery_period_days']} days")
        print(f"Current Drawdown:      {Fore.YELLOW if dd['current_drawdown_pct'] < -5 else Fore.GREEN}{dd['current_drawdown_pct']:>8.2f}%{Style.RESET_ALL}\n")

    # Display market metrics
    if analysis['market_metrics'] and 'error' not in analysis['market_metrics']:
        market = analysis['market_metrics']
        print(f"{Fore.WHITE}{Style.BRIGHT}Market Metrics (vs {benchmark}):{Style.RESET_ALL}")

        beta = market['beta']
        beta_color = Fore.GREEN if 0.8 <= beta <= 1.2 else Fore.YELLOW
        print(f"Beta:                  {beta_color}{beta:>8.2f}{Style.RESET_ALL}")
        print(f"  → {market['interpretation']['beta']}")

        alpha = market['alpha']
        alpha_color = Fore.GREEN if alpha > 0 else Fore.RED
        print(f"Alpha (annualized):    {alpha_color}{alpha*100:>8.2f}%{Style.RESET_ALL}")
        print(f"  → {market['interpretation']['alpha']}\n")

    # Display recommendation
    if 'recommendation' in analysis:
        rec = analysis['recommendation']
        print(f"{Fore.WHITE}{Style.BRIGHT}Investment Recommendation:{Style.RESET_ALL}")
        print("=" * 75)

        # Color code recommendation
        rec_text = rec['recommendation']
        if rec_text == 'STRONG BUY':
            rec_color = Fore.GREEN + Style.BRIGHT
        elif rec_text == 'BUY':
            rec_color = Fore.GREEN
        elif rec_text == 'HOLD':
            rec_color = Fore.YELLOW
        elif rec_text == 'SELL':
            rec_color = Fore.RED
        else:  # STRONG SELL
            rec_color = Fore.RED + Style.BRIGHT

        print(f"\n{rec_color}Recommendation: {rec_text}{Style.RESET_ALL}")
        print(f"Confidence: {rec['confidence']}")
        print(f"Score: {rec['score']}/10\n")

        print(f"{Fore.WHITE}Action:{Style.RESET_ALL} {rec['action']}\n")

        if rec['positive_signals']:
            print(f"{Fore.GREEN}Positive Signals:{Style.RESET_ALL}")
            for signal in rec['positive_signals']:
                print(f"  ✓ {signal}")
            print()

        if rec['risk_warnings']:
            print(f"{Fore.YELLOW}Risk Warnings:{Style.RESET_ALL}")
            for warning in rec['risk_warnings']:
                print(f"  ⚠ {warning}")
            print()

        print(f"{Fore.WHITE}Summary:{Style.RESET_ALL}")
        print(f"{rec['summary']}\n")

        print(f"{Fore.RED}⚠️  DISCLAIMER:{Style.RESET_ALL}")
        print(f"{rec['disclaimer']}\n")

        print("=" * 75)
        print()

    # Interpretation guide
    print(f"{Fore.CYAN}Interpretation Guide:{Style.RESET_ALL}")
    print(f"  Sharpe Ratio:  >1 = Good, >2 = Very Good, >3 = Excellent")
    print(f"  Sortino Ratio: Similar to Sharpe, but focuses on downside risk")
    print(f"  Beta:          <1 = Less volatile, =1 = Market volatility, >1 = More volatile")
    print(f"  Alpha:         >0 = Outperforming, <0 = Underperforming")
    print(f"  VaR:           Maximum expected loss at given confidence level")
    print()


def predict_price(symbol: str, days: int = 7, method: str = 'ensemble'):
    """Predict future stock prices."""
    fetcher = StockFetcher(symbol)

    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== {symbol} Price Prediction ==={Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}Fetching historical data for analysis...{Style.RESET_ALL}\n")

    # Get sufficient historical data (3 months)
    historical_data = fetcher.get_historical_data(period='3mo', interval='1d')

    if historical_data.empty:
        print(f"{Fore.RED}No historical data available for {symbol}{Style.RESET_ALL}\n")
        return

    predictor = StockPredictor(symbol, historical_data)

    # Get prediction based on method
    if method == 'ensemble':
        result = predictor.predict_ensemble(days)
    elif method == 'linear':
        result = predictor.predict_linear_regression(days)
    elif method == 'ma':
        result = predictor.predict_moving_average(days)
    elif method == 'advanced':
        result = predictor.predict_advanced(days)
    else:
        print(f"{Fore.RED}Unknown prediction method: {method}{Style.RESET_ALL}\n")
        return

    if 'error' in result:
        print(f"{Fore.RED}Error: {result['error']}{Style.RESET_ALL}\n")
        return

    # Display current price
    print(f"{Fore.WHITE}{Style.BRIGHT}Current Price: {Fore.YELLOW}${result['current_price']:.2f}{Style.RESET_ALL}\n")

    # Display predictions
    if method == 'ensemble':
        print(f"{Fore.WHITE}{Style.BRIGHT}Ensemble Predictions (Next {days} days):{Style.RESET_ALL}\n")
        print(f"{'Date':<12} {'Conservative':<15} {'Moderate':<15} {'Optimistic':<15} {'Change %'}")
        print("-" * 75)

        for pred in result['predictions']:
            date = pred['date']
            conservative = pred['conservative']
            moderate = pred['moderate']
            optimistic = pred['optimistic']
            change_pct = pred['change_percent_moderate']

            # Color code the change
            if change_pct > 0:
                change_color = Fore.GREEN
                arrow = "↑"
            else:
                change_color = Fore.RED
                arrow = "↓"

            print(f"{date:<12} "
                  f"{Fore.RED}${conservative:>7.2f}{Style.RESET_ALL}       "
                  f"{Fore.YELLOW}${moderate:>7.2f}{Style.RESET_ALL}       "
                  f"{Fore.GREEN}${optimistic:>7.2f}{Style.RESET_ALL}       "
                  f"{change_color}{arrow} {abs(change_pct):>6.2f}%{Style.RESET_ALL}")

        print("\n" + f"{Fore.CYAN}Methods Used: {', '.join(result['methods_used'])}{Style.RESET_ALL}")

    else:
        print(f"{Fore.WHITE}{Style.BRIGHT}{result['method']} Predictions (Next {days} days):{Style.RESET_ALL}\n")
        print(f"{'Date':<12} {'Predicted Price':<20} {'Confidence'}")
        print("-" * 50)

        for pred in result['predictions']:
            date = pred['date']
            price = pred['predicted_price']
            confidence = pred.get('confidence', 0.5)

            # Color code confidence
            if confidence >= 0.7:
                conf_color = Fore.GREEN
            elif confidence >= 0.5:
                conf_color = Fore.YELLOW
            else:
                conf_color = Fore.RED

            print(f"{date:<12} ${price:>10.2f}          {conf_color}{confidence*100:.1f}%{Style.RESET_ALL}")

        if 'r_squared' in result:
            print(f"\n{Fore.CYAN}Model R²: {result['r_squared']:.4f}{Style.RESET_ALL}")
        if 'trend' in result:
            trend_color = Fore.GREEN if result['trend'] == 'upward' else Fore.RED
            print(f"{Fore.CYAN}Trend: {trend_color}{result['trend'].upper()}{Style.RESET_ALL}")

    # Disclaimer
    print(f"\n{Fore.YELLOW}⚠️  Disclaimer: These predictions are based on historical data and statistical models.")
    print(f"   They should NOT be used as financial advice. Always do your own research.{Style.RESET_ALL}\n")


def show_market_analyst_changes(days_back: int = 1, symbols: List = None):
    """Display market-wide analyst changes."""
    if symbols is None:
        symbols = DEFAULT_MARKET_SYMBOLS

    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Market-Wide Analyst Changes (Last {days_back} day{'s' if days_back > 1 else ''}) ==={Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}Scanning {len(symbols)} stocks...{Style.RESET_ALL}\n")

    changes = StockFetcher.get_market_analyst_changes(symbols, days_back)

    if not changes:
        print(f"{Fore.YELLOW}No analyst changes found in the last {days_back} day(s){Style.RESET_ALL}\n")
        return

    print(f"{Fore.GREEN}Found {len(changes)} analyst action(s){Style.RESET_ALL}\n")
    print("=" * 100)

    for change in changes:
        date_str = change['date'].strftime('%Y-%m-%d %H:%M') if hasattr(change['date'], 'strftime') else str(change['date'])
        symbol = change['symbol']
        firm = change['firm']
        action = change['action']
        from_grade = change['from_grade']
        to_grade = change['to_grade']

        # Color code the action
        if 'up' in action.lower():
            action_color = Fore.GREEN
            arrow = "↑"
        elif 'down' in action.lower():
            action_color = Fore.RED
            arrow = "↓"
        elif 'init' in action.lower() or 'main' in action.lower():
            action_color = Fore.CYAN
            arrow = "→"
        else:
            action_color = Fore.YELLOW
            arrow = "•"

        print(f"{Fore.WHITE}{date_str}{Style.RESET_ALL} | {Fore.CYAN}{Style.BRIGHT}{symbol:6s}{Style.RESET_ALL} | {arrow} {action_color}{Style.BRIGHT}{action:12s}{Style.RESET_ALL} | {firm}")

        if from_grade != 'N/A' and to_grade != 'N/A':
            print(f"{' ' * 29}{from_grade} → {to_grade}")
        elif to_grade != 'N/A':
            print(f"{' ' * 29}{to_grade}")

        print("-" * 100)

    print(f"\n{Fore.WHITE}Total changes: {len(changes)}{Style.RESET_ALL}\n")


def show_analyst_ratings(symbol: str, limit: int = 20):
    """Display analyst upgrades and downgrades."""
    fetcher = StockFetcher(symbol)

    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== {symbol} Analyst Ratings ==={Style.RESET_ALL}\n")

    # Get recommendations summary
    summary = fetcher.get_recommendations_summary()

    if summary:
        print(f"{Fore.WHITE}{Style.BRIGHT}Current Consensus:{Style.RESET_ALL}")

        if summary['strong_buy'] != 'N/A':
            rec_key = summary['strong_buy'].upper()
            if rec_key in ['STRONG_BUY', 'BUY']:
                color = Fore.GREEN
            elif rec_key in ['HOLD', 'NEUTRAL']:
                color = Fore.YELLOW
            else:
                color = Fore.RED
            print(f"Recommendation: {color}{Style.BRIGHT}{rec_key}{Style.RESET_ALL}")

        if summary['num_analysts'] != 'N/A':
            print(f"Number of Analysts: {summary['num_analysts']}")

        if summary['recommendation_mean'] != 'N/A':
            mean = summary['recommendation_mean']
            print(f"Recommendation Mean: {mean:.2f} (1=Strong Buy, 5=Sell)")

        print(f"\n{Fore.WHITE}{Style.BRIGHT}Price Targets:{Style.RESET_ALL}")
        if summary['target_mean'] != 'N/A':
            print(f"Mean Target:  ${summary['target_mean']:.2f}")
        if summary['target_high'] != 'N/A':
            print(f"High Target:  {Fore.GREEN}${summary['target_high']:.2f}{Style.RESET_ALL}")
        if summary['target_low'] != 'N/A':
            print(f"Low Target:   {Fore.RED}${summary['target_low']:.2f}{Style.RESET_ALL}")
        print()

    # Get upgrades/downgrades history
    recommendations = fetcher.get_analyst_recommendations()

    if recommendations.empty:
        print(f"{Fore.YELLOW}No recent upgrades/downgrades data available{Style.RESET_ALL}\n")
        return

    print(f"{Fore.WHITE}{Style.BRIGHT}Recent Upgrades/Downgrades:{Style.RESET_ALL}\n")

    # Display the most recent recommendations
    recent = recommendations.head(limit)

    for idx, row in recent.iterrows():
        date = idx.strftime('%Y-%m-%d') if hasattr(idx, 'strftime') else str(idx)

        # Determine colors based on action
        firm = row.get('Firm', 'Unknown')
        to_grade = row.get('ToGrade', 'N/A')
        from_grade = row.get('FromGrade', 'N/A')
        action = row.get('Action', 'N/A')

        # Color code the action
        if 'up' in action.lower():
            action_color = Fore.GREEN
            arrow = "↑"
        elif 'down' in action.lower():
            action_color = Fore.RED
            arrow = "↓"
        elif 'init' in action.lower() or 'main' in action.lower():
            action_color = Fore.CYAN
            arrow = "→"
        else:
            action_color = Fore.YELLOW
            arrow = "•"

        print(f"{Fore.WHITE}{date}{Style.RESET_ALL} | {arrow} {action_color}{Style.BRIGHT}{action:12s}{Style.RESET_ALL} | {Fore.CYAN}{firm}{Style.RESET_ALL}")

        if from_grade != 'N/A' and to_grade != 'N/A':
            print(f"           {from_grade} → {to_grade}")
        elif to_grade != 'N/A':
            print(f"           {to_grade}")
        print()

    if len(recommendations) > limit:
        print(f"{Fore.YELLOW}Showing {limit} most recent. Total: {len(recommendations)}{Style.RESET_ALL}\n")


def compare_symbols(symbol1: str, symbol2: str, period: str = '1mo',
                   comparison_type: str = 'price', interval: str = None):
    """Compare two stock symbols."""
    fetcher1 = StockFetcher(symbol1)
    fetcher2 = StockFetcher(symbol2)

    # Auto-select interval based on period if not specified
    if interval is None:
        if period in ['1d']:
            interval = '5m'
        elif period in ['5d']:
            interval = '15m'
        elif period in ['1mo', '3mo']:
            interval = '1d'
        else:
            interval = '1d'

    print(f"{Fore.CYAN}Fetching {period} data for {symbol1} and {symbol2}...{Style.RESET_ALL}")

    data1 = fetcher1.get_historical_data(period=period, interval=interval)
    data2 = fetcher2.get_historical_data(period=period, interval=interval)

    if data1.empty:
        print(f"{Fore.RED}No data available for {symbol1}{Style.RESET_ALL}")
        return

    if data2.empty:
        print(f"{Fore.RED}No data available for {symbol2}{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}Data fetched successfully. Displaying comparison...{Style.RESET_ALL}\n")

    StockVisualizer.plot_comparison_symbols(symbol1, data1, symbol2, data2, comparison_type)


def search_ticker(symbols: list, detailed: bool = False):
    """Search for ticker symbols."""
    if not symbols:
        print(f"{Fore.RED}Please provide at least one ticker symbol to search{Style.RESET_ALL}")
        return

    results = StockFetcher.search_multiple(symbols)

    if not results:
        print(f"{Fore.RED}No results found for the provided symbols{Style.RESET_ALL}")
        return

    for i, result in enumerate(results):
        if i > 0:
            print("\n" + "-" * 80 + "\n")

        print(f"{Fore.CYAN}{Style.BRIGHT}=== {result['symbol']} ==={Style.RESET_ALL}\n")
        print(f"{Fore.WHITE}{Style.BRIGHT}{result['name']}{Style.RESET_ALL}")

        print(f"\nExchange: {result['exchange']}")
        print(f"Type: {result['quote_type']}")
        print(f"Currency: {result['currency']}")

        # Format market cap
        market_cap = result['market_cap']
        if market_cap != 'N/A' and isinstance(market_cap, (int, float)):
            if market_cap >= 1_000_000_000:
                market_cap_str = f"${market_cap / 1_000_000_000:.2f}B"
            elif market_cap >= 1_000_000:
                market_cap_str = f"${market_cap / 1_000_000:.2f}M"
            else:
                market_cap_str = f"${market_cap:,.0f}"
        else:
            market_cap_str = 'N/A'
        print(f"Market Cap: {market_cap_str}")

        if result['sector'] != 'N/A':
            print(f"Sector: {result['sector']}")
        if result['industry'] != 'N/A':
            print(f"Industry: {result['industry']}")
        if result['country'] != 'N/A':
            print(f"Country: {result['country']}")

        if detailed:
            if result['website'] != 'N/A':
                print(f"\nWebsite: {Fore.BLUE}{result['website']}{Style.RESET_ALL}")
            if result['description'] != 'N/A':
                # Truncate description if too long
                desc = result['description']
                if len(desc) > 500:
                    desc = desc[:497] + "..."
                print(f"\n{Fore.WHITE}Description:{Style.RESET_ALL}")
                print(desc)

    print()


def show_financials(symbol: str, statement_type: str = 'summary', quarterly: bool = False):
    """Display financial statements and metrics."""
    financials = FinancialData(symbol)

    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== {symbol} Financial Data ==={Style.RESET_ALL}\n")

    if statement_type == 'summary':
        result = financials.get_financial_summary()
        if 'error' in result:
            print(f"{Fore.RED}Error: {result['error']}{Style.RESET_ALL}\n")
            return

        print(f"{Fore.WHITE}{Style.BRIGHT}{result.get('company_name', symbol)}{Style.RESET_ALL}\n")

        # Revenue
        print(f"{Fore.WHITE}{Style.BRIGHT}Revenue:{Style.RESET_ALL}")
        rev = result.get('revenue', {})
        if rev.get('total_revenue') != 'N/A':
            print(f"Total Revenue:      ${rev.get('total_revenue', 'N/A'):,}")
        print(f"Revenue/Share:      ${rev.get('revenue_per_share', 'N/A')}")
        print(f"Revenue Growth:     {rev.get('revenue_growth', 'N/A')}\n")

        # Profitability
        print(f"{Fore.WHITE}{Style.BRIGHT}Profitability:{Style.RESET_ALL}")
        prof = result.get('profitability', {})
        if prof.get('net_income') != 'N/A':
            print(f"Net Income:         ${prof.get('net_income', 'N/A'):,}")
        print(f"EPS:                ${prof.get('earnings_per_share', 'N/A')}")
        print(f"Profit Margin:      {prof.get('profit_margin', 'N/A')}")
        print(f"Operating Margin:   {prof.get('operating_margin', 'N/A')}\n")

        # Balance Sheet
        print(f"{Fore.WHITE}{Style.BRIGHT}Balance Sheet:{Style.RESET_ALL}")
        bal = result.get('balance_sheet', {})
        if bal.get('total_assets') != 'N/A':
            print(f"Total Assets:       ${bal.get('total_assets', 'N/A'):,}")
        if bal.get('total_debt') != 'N/A':
            print(f"Total Debt:         ${bal.get('total_debt', 'N/A'):,}")
        if bal.get('total_cash') != 'N/A':
            print(f"Total Cash:         ${bal.get('total_cash', 'N/A'):,}")
        print(f"Book Value/Share:   ${bal.get('book_value_per_share', 'N/A')}\n")

        # Cash Flow
        print(f"{Fore.WHITE}{Style.BRIGHT}Cash Flow:{Style.RESET_ALL}")
        cf = result.get('cash_flow', {})
        if cf.get('operating_cash_flow') != 'N/A':
            print(f"Operating CF:       ${cf.get('operating_cash_flow', 'N/A'):,}")
        if cf.get('free_cash_flow') != 'N/A':
            print(f"Free Cash Flow:     ${cf.get('free_cash_flow', 'N/A'):,}\n")

        # Key Ratios
        print(f"{Fore.WHITE}{Style.BRIGHT}Key Ratios:{Style.RESET_ALL}")
        ratios = result.get('key_ratios', {})
        print(f"P/E Ratio:          {ratios.get('pe_ratio', 'N/A')}")
        print(f"Price/Book:         {ratios.get('price_to_book', 'N/A')}")
        print(f"ROE:                {ratios.get('return_on_equity', 'N/A')}")
        print(f"ROA:                {ratios.get('return_on_assets', 'N/A')}")
        print(f"Current Ratio:      {ratios.get('current_ratio', 'N/A')}")
        print(f"Debt/Equity:        {ratios.get('debt_to_equity', 'N/A')}\n")

    elif statement_type == 'metrics':
        result = financials.get_key_metrics()
        if 'error' in result:
            print(f"{Fore.RED}Error: {result['error']}{Style.RESET_ALL}\n")
            return

        # Valuation Metrics
        print(f"{Fore.WHITE}{Style.BRIGHT}Valuation Metrics:{Style.RESET_ALL}")
        val = result.get('valuation_metrics', {})
        for key, value in val.items():
            label = key.replace('_', ' ').title()
            print(f"{label:25s} {value}")

        # Profitability Metrics
        print(f"\n{Fore.WHITE}{Style.BRIGHT}Profitability Metrics:{Style.RESET_ALL}")
        prof = result.get('profitability_metrics', {})
        for key, value in prof.items():
            label = key.replace('_', ' ').title()
            if isinstance(value, float):
                value = f"{value * 100:.2f}%"
            print(f"{label:25s} {value}")

        # Financial Health
        print(f"\n{Fore.WHITE}{Style.BRIGHT}Financial Health:{Style.RESET_ALL}")
        health = result.get('financial_health', {})
        for key, value in health.items():
            label = key.replace('_', ' ').title()
            print(f"{label:25s} {value}")

        # Growth Metrics
        print(f"\n{Fore.WHITE}{Style.BRIGHT}Growth Metrics:{Style.RESET_ALL}")
        growth = result.get('growth_metrics', {})
        for key, value in growth.items():
            label = key.replace('_', ' ').title()
            if isinstance(value, float) and 'growth' in key:
                value = f"{value * 100:.2f}%"
            print(f"{label:25s} {value}")

        # Dividend Metrics
        print(f"\n{Fore.WHITE}{Style.BRIGHT}Dividend Metrics:{Style.RESET_ALL}")
        div = result.get('dividend_metrics', {})
        for key, value in div.items():
            label = key.replace('_', ' ').title()
            if isinstance(value, float) and 'yield' in key:
                value = f"{value * 100:.2f}%"
            elif isinstance(value, float) and 'ratio' in key:
                value = f"{value * 100:.2f}%"
            print(f"{label:25s} {value}")
        print()

    elif statement_type == 'earnings':
        result = financials.get_earnings_history()
        if 'error' in result:
            print(f"{Fore.RED}Error: {result['error']}{Style.RESET_ALL}\n")
            return

        print(f"{Fore.WHITE}{Style.BRIGHT}Earnings History:{Style.RESET_ALL}\n")
        print(f"{'Date':<12} {'Estimate':>12} {'Actual':>12} {'Surprise':>12}")
        print("-" * 50)

        for earning in result.get('earnings_history', []):
            date = earning['date']
            estimate = f"${earning['eps_estimate']:.2f}" if earning['eps_estimate'] is not None else 'N/A'
            actual = f"${earning['reported_eps']:.2f}" if earning['reported_eps'] is not None else 'N/A'
            surprise = f"{earning['surprise_pct']:.1f}%" if earning['surprise_pct'] is not None else 'N/A'

            # Color code the surprise
            if earning['surprise_pct'] is not None:
                if earning['surprise_pct'] > 0:
                    surprise = f"{Fore.GREEN}{surprise}{Style.RESET_ALL}"
                elif earning['surprise_pct'] < 0:
                    surprise = f"{Fore.RED}{surprise}{Style.RESET_ALL}"

            print(f"{date:<12} {estimate:>12} {actual:>12} {surprise:>12}")
        print()

    elif statement_type == 'next-earnings':
        result = financials.get_next_earnings()
        if 'error' in result:
            print(f"{Fore.RED}Error: {result['error']}{Style.RESET_ALL}\n")
            return

        print(f"{Fore.WHITE}{Style.BRIGHT}Next Earnings Date:{Style.RESET_ALL}\n")

        if result.get('next_earnings_date'):
            print(f"📅  Earnings Date:     {Fore.CYAN}{result['next_earnings_date']}{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.YELLOW}No upcoming earnings date available{Style.RESET_ALL}\n")
            return

        # Earnings estimates
        eps_est = result.get('earnings_estimate', {})
        if eps_est.get('average') is not None:
            print(f"{Fore.WHITE}{Style.BRIGHT}EPS Estimates:{Style.RESET_ALL}")
            print(f"Average:            ${eps_est['average']:.2f}")
            if eps_est.get('low') is not None:
                print(f"Low:                ${eps_est['low']:.2f}")
            if eps_est.get('high') is not None:
                print(f"High:               ${eps_est['high']:.2f}")
            print()

        # Revenue estimates
        rev_est = result.get('revenue_estimate', {})
        if rev_est.get('average') is not None:
            print(f"{Fore.WHITE}{Style.BRIGHT}Revenue Estimates:{Style.RESET_ALL}")
            if rev_est['average'] >= 1_000_000_000:
                print(f"Average:            ${rev_est['average'] / 1_000_000_000:.2f}B")
                if rev_est.get('low') is not None:
                    print(f"Low:                ${rev_est['low'] / 1_000_000_000:.2f}B")
                if rev_est.get('high') is not None:
                    print(f"High:               ${rev_est['high'] / 1_000_000_000:.2f}B")
            elif rev_est['average'] >= 1_000_000:
                print(f"Average:            ${rev_est['average'] / 1_000_000:.2f}M")
                if rev_est.get('low') is not None:
                    print(f"Low:                ${rev_est['low'] / 1_000_000:.2f}M")
                if rev_est.get('high') is not None:
                    print(f"High:               ${rev_est['high'] / 1_000_000:.2f}M")
            else:
                print(f"Average:            ${rev_est['average']:,.0f}")
                if rev_est.get('low') is not None:
                    print(f"Low:                ${rev_est['low']:,.0f}")
                if rev_est.get('high') is not None:
                    print(f"High:               ${rev_est['high']:,.0f}")
            print()

    else:
        # For income, balance, cashflow statements
        period_str = "Quarterly" if quarterly else "Annual"
        print(f"{Fore.YELLOW}Fetching {period_str} {statement_type.title()} Statement...{Style.RESET_ALL}\n")

        if statement_type == 'income':
            result = financials.get_income_statement(quarterly=quarterly)
        elif statement_type == 'balance':
            result = financials.get_balance_sheet(quarterly=quarterly)
        elif statement_type == 'cashflow':
            result = financials.get_cash_flow(quarterly=quarterly)
        else:
            print(f"{Fore.RED}Unknown statement type: {statement_type}{Style.RESET_ALL}\n")
            return

        if 'error' in result:
            print(f"{Fore.RED}Error: {result['error']}{Style.RESET_ALL}\n")
            return

        print(f"{Fore.GREEN}{result.get('description', '')}{Style.RESET_ALL}\n")

        data = result.get('data', {})
        if not data:
            print(f"{Fore.YELLOW}No data available{Style.RESET_ALL}\n")
            return

        # Display in simplified format
        print(f"{Fore.CYAN}Available periods: {', '.join(data.keys())}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Use the API for detailed financial statement data.{Style.RESET_ALL}\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='MarketMind CLI - Real-time quotes and charts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get current quote
  python stock_cli.py quote AAPL

  # Show line chart for last month
  python stock_cli.py chart AAPL --period 1mo

  # Show candlestick chart for last 5 days
  python stock_cli.py chart GOOGL --period 5d --type candlestick

  # Show intraday chart
  python stock_cli.py chart TSLA --period 1d --type intraday

  # Show comparison chart (price + volume subplots)
  python stock_cli.py chart AAPL --period 5d --type comparison

  # Real-time monitoring (refreshes every 5 seconds)
  python stock_cli.py monitor MSFT

  # Real-time monitoring with custom refresh rate
  python stock_cli.py monitor AMZN --refresh 10

  # Search for ticker information
  python stock_cli.py search AAPL

  # Search multiple tickers
  python stock_cli.py search AAPL GOOGL MSFT

  # Search with detailed information (includes description)
  python stock_cli.py search TSLA --detailed

  # Compare two symbols (price comparison with dual axes)
  python stock_cli.py compare AAPL MSFT --period 1mo

  # Compare performance (percentage change from start)
  python stock_cli.py compare TSLA NVDA --period 6mo --type performance

  # Get analyst ratings and upgrades/downgrades
  python stock_cli.py analyst AAPL

  # Get analyst ratings with more history
  python stock_cli.py analyst TSLA --limit 50

  # Get market-wide analyst changes for today
  python stock_cli.py analyst market

  # Get market-wide analyst changes for the last 3 days
  python stock_cli.py analyst market --days 3

  # Predict stock price for next 7 days (ensemble method)
  python stock_cli.py predict AAPL

  # Predict with specific method and timeframe
  python stock_cli.py predict TSLA --days 14 --method linear

  # Quantitative analysis
  python stock_cli.py quant AAPL

  # Quantitative analysis with custom benchmark and period
  python stock_cli.py quant TSLA --benchmark QQQ --period 2y

Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max
Valid chart types: line, candlestick, intraday, comparison
Valid comparison types: price, performance
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Quote command
    quote_parser = subparsers.add_parser('quote', help='Get current stock quote')
    quote_parser.add_argument('symbol', type=str, help='Stock ticker symbol (e.g., AAPL)')

    # Chart command
    chart_parser = subparsers.add_parser('chart', help='Display stock chart')
    chart_parser.add_argument('symbol', type=str, help='Stock ticker symbol (e.g., AAPL)')
    chart_parser.add_argument('--period', '-p', type=str, default='1mo',
                             help='Time period (default: 1mo)')
    chart_parser.add_argument('--type', '-t', type=str, default='line',
                             choices=['line', 'candlestick', 'intraday', 'comparison'],
                             help='Chart type (default: line)')
    chart_parser.add_argument('--interval', '-i', type=str,
                             help='Data interval (auto-selected if not specified)')

    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Real-time quote monitoring')
    monitor_parser.add_argument('symbol', type=str, help='Stock ticker symbol (e.g., AAPL)')
    monitor_parser.add_argument('--refresh', '-r', type=int, default=5,
                               help='Refresh interval in seconds (default: 5)')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search for ticker symbols')
    search_parser.add_argument('symbols', type=str, nargs='+',
                              help='One or more ticker symbols to search for')
    search_parser.add_argument('--detailed', '-d', action='store_true',
                              help='Show detailed information including description')

    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare two stock symbols')
    compare_parser.add_argument('symbol1', type=str, help='First stock ticker symbol')
    compare_parser.add_argument('symbol2', type=str, help='Second stock ticker symbol')
    compare_parser.add_argument('--period', '-p', type=str, default='1mo',
                               help='Time period (default: 1mo)')
    compare_parser.add_argument('--type', '-t', type=str, default='price',
                               choices=['price', 'performance'],
                               help='Comparison type: price (dual axes) or performance (normalized %)')
    compare_parser.add_argument('--interval', '-i', type=str,
                               help='Data interval (auto-selected if not specified)')

    # Analyst command
    analyst_parser = subparsers.add_parser('analyst',
                                           help='Get analyst ratings and upgrades/downgrades')
    analyst_parser.add_argument('symbol_or_market', type=str,
                               help='Stock ticker symbol (e.g., AAPL) or "market" for market-wide changes')
    analyst_parser.add_argument('--limit', '-l', type=int, default=20,
                               help='Number of recent recommendations to show for a symbol (default: 20)')
    analyst_parser.add_argument('--days', '-d', type=int, default=1,
                               help='Days back to search for market changes (default: 1)')

    # Predict command
    predict_parser = subparsers.add_parser('predict', help='Predict future stock prices')
    predict_parser.add_argument('symbol', type=str, help='Stock ticker symbol (e.g., AAPL)')
    predict_parser.add_argument('--days', '-d', type=int, default=7,
                               help='Number of days to predict ahead (default: 7)')
    predict_parser.add_argument('--method', '-m', type=str, default='ensemble',
                               choices=['ensemble', 'linear', 'ma', 'advanced'],
                               help='Prediction method: ensemble (default), linear, ma (moving average), advanced')

    # Quant command
    quant_parser = subparsers.add_parser('quant', help='Quantitative finance analysis')
    quant_parser.add_argument('symbol', type=str, help='Stock ticker symbol (e.g., AAPL)')
    quant_parser.add_argument('--benchmark', '-b', type=str, default='SPY',
                             help='Benchmark symbol for comparison (default: SPY)')
    quant_parser.add_argument('--period', '-p', type=str, default='1y',
                             help='Analysis period (default: 1y)')

    # Financials command
    financials_parser = subparsers.add_parser('financials', help='Get financial statements and metrics')
    financials_parser.add_argument('symbol', type=str, help='Stock ticker symbol (e.g., AAPL)')
    financials_parser.add_argument('--type', '-t', type=str, default='summary',
                                   choices=['summary', 'income', 'balance', 'cashflow', 'metrics', 'earnings', 'next-earnings'],
                                   help='Type of financial data (default: summary)')
    financials_parser.add_argument('--quarterly', '-q', action='store_true',
                                   help='Get quarterly data instead of annual (for income, balance, cashflow)')

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == 'quote':
            print_quote(args.symbol)
        elif args.command == 'chart':
            show_chart(args.symbol, args.period, args.type, args.interval)
        elif args.command == 'monitor':
            start_realtime_monitor(args.symbol, args.refresh)
        elif args.command == 'search':
            search_ticker(args.symbols, args.detailed)
        elif args.command == 'compare':
            compare_symbols(args.symbol1, args.symbol2, args.period, args.type, args.interval)
        elif args.command == 'analyst':
            if args.symbol_or_market.lower() == 'market':
                show_market_analyst_changes(args.days)
            else:
                show_analyst_ratings(args.symbol_or_market, args.limit)
        elif args.command == 'predict':
            predict_price(args.symbol, args.days, args.method)
        elif args.command == 'quant':
            show_quant_analysis(args.symbol, args.benchmark, args.period)
        elif args.command == 'financials':
            show_financials(args.symbol, args.type, args.quarterly)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == '__main__':
    main()
