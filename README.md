# Algorithmic Trading Backend

A comprehensive Python-based financial analysis tool that provides data models for stocks and options, including pricing, statistical analysis, and visualization capabilities.

## Features

### Data Models
- **Base Data**: Historical price data for any ticker
- **Stock Data**: Extended analysis including log returns and volatility calculations
- **Option Data**: Options pricing with Black-Scholes model and Greeks calculation
  - Support for both Call and Put options
  - Automatic expiration date matching (finds closest available date)
  - Real-time risk-free rate fetching from treasury data

### Analysis Capabilities
- Historical stock price data via Yahoo Finance API
- Log returns and annualized volatility calculations
- Option pricing using Black-Scholes model
- Greeks calculation (Delta, Gamma, Vega, Theta, Rho)
- Statistical metrics and price analysis

### Visualizations
- Price charts with customizable timeframes
- Returns distribution histograms
- Volatility analysis with 30-day rolling windows
- Cumulative returns tracking
- Comprehensive summary dashboard combining all metrics

## Requirements

- Python 3.x
- yfinance
- pandas
- numpy
- matplotlib
- scipy

## Installation

```bash
pip install yfinance pandas numpy matplotlib scipy
```

## Usage

Run the main script to execute all three test cases (Base Data, Stock Data, and Option Data):

```bash
python main.py
```

The script will automatically:
1. Load base price data for AAPL and display a price chart
2. Load stock data with volatility analysis and display a comprehensive dashboard
3. Load option data with Greeks calculation and pricing

### Customizing Parameters

Modify the test configuration in `main.py`:

```python
ticker = "AAPL"
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 10, 31)
```

### Loading Different Data Types

```python
from data.data_factory import DataLoader
from datetime import datetime

# Load base data
base_data = DataLoader.load_data(
    ticker="AAPL",
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31),
    data_type="base"
)

# Load stock data with volatility
stock_data = DataLoader.load_data(
    ticker="AAPL",
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31),
    data_type="stock"
)

# Load option data (automatically finds closest expiration)
option_data = DataLoader.load_data(
    ticker="AAPL",
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31),
    data_type="option",
    option_type="call",  # or "put"
    expiration_date="2025-01-17"  # or None for first available
)
```

## Project Structure

```
algo_backend/
├── main.py                 # Entry point - runs 3 test cases with visualizations
├── data/                   # Data models and loaders
│   ├── base_data.py       # BaseData class - basic price data model
│   ├── stock_data.py      # StockData class - extends BaseData with returns/volatility
│   ├── option_data.py     # OptionData class - option pricing and Greeks
│   ├── data_factory.py    # DataLoader factory for creating data objects
│   └── download_data.py   # Yahoo Finance API integration
├── graph/                  # Visualization modules
│   └── graph_model.py     # GraphModel class - all charting functionality
└── README.md              # This file
```

## Data Models

### BaseData
- Basic price data container
- Properties: `get_prices`, `get_current_price`, `get_ticker`, `get_type`

### StockData (extends BaseData)
- Adds log returns and volatility calculations
- Properties: `get_log_returns`, `get_volatility`, `get_prices_stats()`
- Automatically calculates annualized volatility (252 trading days)

### OptionData (extends StockData)
- Black-Scholes option pricing model
- Greeks calculation: Delta, Gamma, Vega, Theta, Rho
- Properties: `strike_price`, `expiration_date`, `risk_free_rate`, `time_to_maturity`
- Methods: `get_option_price()`, `get_greeks_dict()`, `get_option_info()`

## Example Output

### Statistical Metrics
- Current price
- Price mean and standard deviation
- Return mean and standard deviation
- Annualized volatility
- Number of data points

### Option Metrics
- Strike price
- Expiration date and time to maturity
- Risk-free rate (fetched from ^IRX - 13 Week Treasury Bill)
- Option price (Black-Scholes)
- All Greeks (Delta, Gamma, Vega, Theta, Rho)

### Visualizations
- Multi-panel dashboard with price, returns, cumulative returns, and volatility
- Individual charts for detailed analysis
- Customizable figure sizes and time periods

## Code Style

- Indentation: 4 spaces (no tabs)
- Python version: 3.x
- Type hints: Using dataclasses for data models
