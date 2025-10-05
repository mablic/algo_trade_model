import yfinance as yf
import pandas as pd

def load_ticker_data(ticker, start_date, end_date):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        if stock_data.empty:
            raise ValueError(f"No data found for ticker: {ticker}")
        if isinstance(stock_data.columns, pd.MultiIndex):
            stock_data.columns = stock_data.columns.get_level_values(0)
        if stock_data.empty:
            raise ValueError(f"No data found for ticker: {ticker}")
        return stock_data
    except Exception as e:
        raise ValueError(f"Download data error: {str(e)}")
    
def load_rf_data():
    try:
        treasury = yf.Ticker("^IRX")
        treasury_data = treasury.history(period="1d")
        if not treasury_data.empty:
            return treasury_data['Close'].iloc[-1] / 100
        return 0.05 
    except:
        return 0.05

def load_strike_data(ticker_symbol, expiration_date=None):
    from datetime import datetime

    ticker = yf.Ticker(ticker_symbol)

    expirations = ticker.options
    if not expirations:
        raise ValueError(f"No option data available for {ticker_symbol}")

    print(f"Available expirations: {expirations}")

    if expiration_date:
        # Convert to string format
        if hasattr(expiration_date, 'strftime'):
            expiration_str = expiration_date.strftime('%Y-%m-%d')
            requested_dt = expiration_date
        else:
            expiration_str = str(expiration_date)
            requested_dt = datetime.strptime(expiration_str, '%Y-%m-%d')

        print(f"Requested expiration: {expiration_str}")

        # Check if it's in available expirations
        if expiration_str in expirations:
            expiration = expiration_str
            print(f"Using requested expiration: {expiration}")
        else:
            # Find the closest expiration date
            expiration_dates = [datetime.strptime(exp, '%Y-%m-%d') for exp in expirations]
            closest_exp = min(expiration_dates, key=lambda x: abs((x - requested_dt).days))
            expiration = closest_exp.strftime('%Y-%m-%d')
            print(f"Warning: Expiration {expiration_str} not available. Using closest available: {expiration}")
    else:
        # Use first available expiration
        expiration = expirations[0]
        print(f"No expiration requested. Using first available: {expiration}")

    option_chain = ticker.option_chain(expiration)
    return {
        'calls': option_chain.calls,
        'puts': option_chain.puts,
        'expiration': expiration,
        'expiration_dates': expiration
    }

if __name__ == '__main__':
    risk_free = load_rf_data()
    print("Risk Free is:", risk_free)

    strike = load_strike_data('AAPL')
    for key, val in strike.items():
        print(f"{key} is: {val}")
