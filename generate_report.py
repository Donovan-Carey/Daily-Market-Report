import os
import openai
from datetime import datetime, timedelta
import pytz
import requests
import yfinance as yf
import json

def get_finnhub_data():
    """
    Fetch real-time market data from Finnhub API
    """
    api_key = os.environ.get('FINNHUB_API_KEY')
    base_url = "https://finnhub.io/api/v1"
    
    data = {
        'news': [],
        'market_status': None,
        'forex': {},
        'crypto': {}
    }
    
    try:
        # Get market news
        news_response = requests.get(
            f"{base_url}/news",
            params={'category': 'general', 'token': api_key}
        )
        if news_response.status_code == 200:
            data['news'] = news_response.json()[:10]  # Top 10 news items
        
        # Get forex rates
        forex_pairs = ['EUR/USD', 'USD/JPY', 'GBP/USD']
        for pair in forex_pairs:
            symbol = pair.replace('/', '')
            forex_response = requests.get(
                f"{base_url}/forex/rates",
                params={'base': symbol[:3], 'token': api_key}
            )
            if forex_response.status_code == 200:
                forex_data = forex_response.json()
                data['forex'][pair] = forex_data
        
        # Get crypto prices
        crypto_symbols = ['BINANCE:BTCUSDT', 'BINANCE:ETHUSDT']
        for symbol in crypto_symbols:
            crypto_response = requests.get(
                f"{base_url}/quote",
                params={'symbol': symbol, 'token': api_key}
            )
            if crypto_response.status_code == 200:
                data['crypto'][symbol] = crypto_response.json()
        
        # Get market status
        status_response = requests.get(
            f"{base_url}/stock/market-status",
            params={'exchange': 'US', 'token': api_key}
        )
        if status_response.status_code == 200:
            data['market_status'] = status_response.json()
            
    except Exception as e:
        print(f"Error fetching Finnhub data: {str(e)}")
    
    return data

def get_yahoo_finance_data():
    """
    Fetch market data from Yahoo Finance
    """
    data = {
        'indices': {},
        'futures': {},
        'commodities': {},
        'premarket_movers': [],
        'sector_performance': {}
    }
    
    try:
        # Major indices
        indices = {
            '^GSPC': 'S&P 500',
            '^DJI': 'Dow Jones',
            '^IXIC': 'NASDAQ',
            '^VIX': 'VIX',
            '^FTSE': 'FTSE 100',
            '^GDAXI': 'DAX',
            '^FCHI': 'CAC 40',
            '^N225': 'Nikkei 225',
            '^HSI': 'Hang Seng',
            '000001.SS': 'Shanghai Composite',
            '^AXJO': 'ASX 200'
        }
        
        for symbol, name in indices.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='2d')
                if len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2]
                    change = ((current - previous) / previous) * 100
                    data['indices'][name] = {
                        'symbol': symbol,
                        'price': round(current, 2),
                        'change': round(change, 2)
                    }
            except Exception as e:
                print(f"Error fetching {name}: {str(e)}")
        
        # Futures
        futures = {
            'ES=F': 'S&P 500 Futures',
            'NQ=F': 'NASDAQ Futures',
            'YM=F': 'Dow Futures',
            'RTY=F': 'Russell 2000 Futures'
        }
        
        for symbol, name in futures.items():
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                data['futures'][name] = {
                    'symbol': symbol,
                    'price': info.get('regularMarketPrice', 'N/A'),
                    'change': info.get('regularMarketChangePercent', 'N/A')
                }
            except Exception as e:
                print(f"Error fetching {name}: {str(e)}")
        
        # Commodities
        commodities = {
            'CL=F': 'Crude Oil (WTI)',
            'BZ=F': 'Brent Crude',
            'GC=F': 'Gold',
            'SI=F': 'Silver',
            'HG=F': 'Copper',
            'DX-Y.NYB': 'US Dollar Index'
        }
        
        for symbol, name in commodities.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='2d')
                if len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2]
                    change = ((current - previous) / previous) * 100
                    data['commodities'][name] = {
                        'symbol': symbol,
                        'price': round(current, 2),
                        'change': round(change, 2)
                    }
            except Exception as e:
                print(f"Error fetching {name}: {str(e)}")
        
        # Treasury yield (using TLT ETF as proxy)
        try:
            tlt = yf.Ticker('TLT')
            hist = tlt.history(period='2d')
            if len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                previous = hist['Close'].iloc[-2]
                change = ((current - previous) / previous) * 100
                data['treasury'] = {
                    'tlt_price': round(current, 2),
                    'change': round(change, 2)
                }
        except Exception as e:
            print(f"Error fetching treasury data: {str(e)}")
        
        # Sector ETFs for performance
        sectors = {
            'XLK': 'Technology',
            'XLF': 'Financials',
            'XLE': 'Energy',
            'XLV': 'Healthcare',
            'XLI': 'Industrials',
            'XLP': 'Consumer Staples',
            'XLY': 'Consumer Discretionary',
            'XLB': 'Materials',
            'XLRE': 'Real Estate',
            'XLU': 'Utilities',
            'XLC': 'Communication Services'
        }
        
        for symbol, name in sectors.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='2d')
                if len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2]
                    change = ((current - previous) / previous) * 100
                    data['sector_performance'][name] = {
                        'symbol': symbol,
                        'change': round(change, 2)
                    }
            except Exception as e:
                print(f"Error fetching {name}: {str(e)}")
        
        # Top movers (using popular stocks as sample)
        popular_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'AMD', 'NFLX', 'DIS']
        movers = []
        
        for symbol in popular_stocks:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='2d', prepost=True)
                if len(hist) >= 1:
                    info = ticker.info
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2] if len(hist) >= 2 else current
                    change = ((current - previous) / previous) * 100 if previous != 0 else 0
                    
                    movers.append({
                        'symbol': symbol,
                        'name': info.get('shortName', symbol),
                        'price': round(current, 2),
                        'change': round(change, 2),
                        'volume': info.get('volume', 'N/A')
                    })
            except Exception as e:
                print(f"Error fetching {symbol}: {str(e)}")
        
        # Sort by absolute change
        movers.sort(key=lambda x: abs(x['change']), reverse=True)
        data['premarket_movers'] = movers[:10]
        
    except Exception as e:
        print(f"Error fetching Yahoo Finance data: {str(e)}")
    
    return data

def format_market_data(finnhub_data, yahoo_data):
    """
    Format the market data into a structured summary for the AI
    """
    summary = []
    
    # Indices summary
    summary.append("CURRENT MARKET DATA:")
    summary.append("\nMAJOR INDICES:")
    for name, info in yahoo_data['indices'].items():
        summary.append(f"- {name}: {info['price']} ({info['change']:+.2f}%)")
    
    # Futures
    summary.append("\nFUTURES:")
    for name, info in yahoo_data['futures'].items():
        summary.append(f"- {name}: {info['price']} ({info['change']:+.2f}%)")
    
    # Commodities
    summary.append("\nCOMMODITIES:")
    for name, info in yahoo_data['commodities'].items():
        summary.append(f"- {name}: ${info['price']} ({info['change']:+.2f}%)")
    
    # Sectors
    summary.append("\nSECTOR PERFORMANCE (Top 5):")
    sorted_sectors = sorted(yahoo_data['sector_performance'].items(), 
                          key=lambda x: x[1]['change'], reverse=True)
    for name, info in sorted_sectors[:5]:
        summary.append(f"- {name}: {info['change']:+.2f}%")
    
    # Top movers
    summary.append("\nTOP PREMARKET MOVERS:")
    for mover in yahoo_data['premarket_movers'][:5]:
        summary.append(f"- {mover['symbol']} ({mover['name']}): ${mover['price']} ({mover['change']:+.2f}%)")
    
    # Recent news headlines
    summary.append("\nRECENT MARKET NEWS:")
    for article in finnhub_data['news'][:5]:
        summary.append(f"- {article.get('headline', 'N/A')} (Source: {article.get('source', 'Unknown')})")
    
    return '\n'.join(summary)

def generate_report():
    """
    Generate the pre-market analyst report using OpenAI API with real market data
    """
    # Set up OpenAI API key
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    
    # Get today's date in EST
    est = pytz.timezone('US/Eastern')
    today = datetime.now(est).strftime("%B %d, %Y")
    
    print("Fetching market data from Finnhub...")
    finnhub_data = get_finnhub_data()
    
    print("Fetching market data from Yahoo Finance...")
    yahoo_data = get_yahoo_finance_data()
    
    # Format the market data
    market_data_summary = format_market_data(finnhub_data, yahoo_data)
    
    # The comprehensive prompt with real data
    prompt = f"""Using the following REAL-TIME MARKET DATA, generate a comprehensive pre-market analyst report for {today} suitable for professional trading decisions.

{market_data_summary}

Structure the report as follows:

1. EXECUTIVE SUMMARY
* Brief overview of overnight market sentiment and key themes based on the data above
* Top 3 market-moving events or concerns

2. GLOBAL MARKETS OVERVIEW
* Asian markets performance (use the data provided for Nikkei, Hang Seng, Shanghai Composite, ASX)
* European markets performance (use the data provided for FTSE, DAX, CAC)
* Key indices movements with percentage changes
* Notable cross-market correlations or divergences

3. OVERNIGHT NEWS & CATALYSTS
* Analyze the news headlines provided
* Major economic data releases (domestic and international)
* Central bank announcements or commentary
* Geopolitical developments affecting markets
* Significant corporate earnings or guidance

4. PRE-MARKET MOVERS
* Analyze the top movers data provided above
* Specific catalysts for each (earnings, news, upgrades/downgrades)
* Volume analysis where relevant
* Notable options activity or unusual volume

5. SECTOR ANALYSIS
* Use the sector performance data provided
* Sector rotation patterns observed overnight
* Best and worst performing sectors with rationale
* Sector-specific news or catalysts

6. FUTURES & COMMODITIES
* Analyze the futures and commodities data provided (S&P 500, Nasdaq, Dow futures, Oil, Gold, Silver, Copper, DXY)
* Include the specific levels and percentage changes from the data
* Bitcoin and major cryptocurrencies (use crypto data if provided)

7. FIXED INCOME & CURRENCIES
* 10-year Treasury yield movements (infer from TLT data)
* Major currency pair movements (use forex data if available)
* Credit spread changes if notable

8. TECHNICAL LEVELS
* Key support/resistance levels for major indices based on current prices
* Notable technical breakouts or breakdowns
* VIX level and implied volatility assessment (use VIX data provided)

9. ECONOMIC CALENDAR
* Today's scheduled data releases with consensus expectations
* Fed speakers or central bank events
* Potential market-moving events

10. TRADING CONSIDERATIONS
* Risk-on vs risk-off sentiment assessment based on the data
* Potential intraday catalysts or volatility triggers
* Sectors/stocks to watch (use the data provided)
* Key price levels that could drive momentum

Use professional trading terminology, include the specific numbers and percentages from the data provided, and maintain an objective, analytical tone. Present information in a scannable format with clear headers and bullet points where appropriate."""

    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a professional market analyst with expertise in pre-market analysis, technical analysis, and global markets. Provide detailed, data-driven analysis using the real-time market data provided. Always cite specific numbers and percentages from the data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        report_content = response.choices[0].message.content
        
        return {
            'success': True,
            'content': report_content,
            'date': today,
            'raw_data': {
                'finnhub': finnhub_data,
                'yahoo': yahoo_data
            }
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'date': today
        }

if __name__ == "__main__":
    result = generate_report()
    if result['success']:
        print("Report generated successfully!")
        print("\n" + "="*80)
        print(result['content'])
        print("="*80)
    else:
        print(f"Error generating report: {result['error']}")
