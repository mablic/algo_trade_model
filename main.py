from datetime import datetime
import data.data_factory as df
from graph.graph_model import GraphModel

def print_separator(char='=', length=60):
    print(char * length)

def display_base_data(data):
    print_separator()
    print("BASE DATA RESULTS")
    print_separator()
    print(f"\nTicker: {data.get_ticker}")
    print(f"Type: {data.get_type}")
    print(f"Current Price: ${data.get_current_price:.2f}")
    print(f"Data Points: {len(data.get_prices)}")
    print(f"\nFirst 5 rows of price data:")
    print(data.get_prices.head())
    print(f"\nLast 5 rows of price data:")
    print(data.get_prices.tail())
    print_separator()

def display_stock_data(data):
    print_separator()
    print("STOCK DATA RESULTS")
    print_separator()
    print(f"\nTicker: {data.get_ticker}")
    print(f"Type: {data.get_type}")
    print(f"Current Price: ${data.get_current_price:.2f}")
    print(f"Volatility: {data.get_volatility:.4f} ({data.get_volatility*100:.2f}%)")
    print(f"Data Points: {len(data.get_prices)}")

    stats = data.get_prices_stats()
    print("\nPrice Statistics:")
    for key, value in stats.items():
        if key in ['price_mean', 'price_std', 'current_price']:
            print(f"  {key:15}: ${value:.2f}")
        elif key in ['volatility']:
            print(f"  {key:15}: {value:.4f} ({value*100:.2f}%)")
        elif key in ['return_mean', 'return_std']:
            print(f"  {key:15}: {value:.6f}")
        else:
            print(f"  {key:15}: {value}")

    print(f"\nFirst 5 log returns:")
    print(data.get_log_returns.head())
    print(f"\nLast 5 log returns:")
    print(data.get_log_returns.tail())
    print_separator()

def display_option_data(data, option_type):
    print_separator()
    print(f"OPTION DATA RESULTS ({option_type.upper()})")
    print_separator()
    print(f"\nTicker: {data.get_ticker}")
    print(f"Type: {data.get_type}")
    print(f"Option Type: {option_type.upper()}")
    print(f"Current Underlying Price: ${data.get_current_price:.2f}")
    print(f"Strike Price: ${data.strike_price:.2f}")
    print(f"Expiration Date: {data.expiration_date}")
    print(f"Time to Maturity: {data.time_to_maturity:.4f} years")
    print(f"Risk-free Rate: {data.risk_free_rate:.4f} ({data.risk_free_rate*100:.2f}%)")
    print(f"Volatility: {data.get_volatility:.4f} ({data.get_volatility*100:.2f}%)")
    print(f"Option Price: ${data.get_option_price():.2f}")

    greeks = data.get_greeks_dict()
    print("\nGreeks:")
    for key, value in greeks.items():
        print(f"  {key:8}: {value:.6f}")
    print_separator()

def main():
    # Test configuration
    ticker = "AAPL"
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 10, 31)

    print_separator()
    print("ALGO BACKEND DATA LOADER - RUNNING 3 TEST CASES")
    print_separator()
    print(f"\nTest Configuration:")
    print(f"  Ticker: {ticker}")
    print(f"  Start Date: {start_date.strftime('%Y-%m-%d')}")
    print(f"  End Date: {end_date.strftime('%Y-%m-%d')}")
    print()

    try:
        print("\n" + "="*60)
        print("TEST CASE 1: BASE DATA")
        print("="*60)
        base_data = df.DataLoader.load_data(
            ticker,
            start_date,
            end_date,
            data_type="base"
        )
        display_base_data(base_data)

        # Graph the base price data
        print("\nGenerating price chart...")
        graph = GraphModel(base_data)
        graph.plot_price_chart()
    except Exception as e:
        print(f"\n✗ Base Data test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

    try:
        print("\n" + "="*60)
        print("TEST CASE 2: STOCK DATA")
        print("="*60)
        stock_data = df.DataLoader.load_data(
            ticker,
            start_date,
            end_date,
            data_type="stock"
        )
        display_stock_data(stock_data)

        # Graph stock data with advanced visualizations
        print("\nGenerating stock analysis dashboard...")
        graph = GraphModel(stock_data)
        graph.plot_summary_dashboard()
    except Exception as e:
        print(f"\n✗ Stock Data test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

    try:
        print("\n" + "="*60)
        print("TEST CASE 3: OPTION DATA (CALL)")
        print("="*60)
        data = df.DataLoader.load_data(
            ticker,
            start_date,
            end_date,
            data_type="option",
            option_type="call",
            expiration_date="2026-01-01"
        )
        display_option_data(data, "call")
    except Exception as e:
        print(f"\n✗ Option Data (CALL) test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()