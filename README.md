# Stock Analysis Tool

A Python-based stock analysis tool that fetches historical stock data and generates comprehensive visualizations and statistical analysis.

## Features

- Download historical stock price data using Yahoo Finance API
- Calculate log returns and volatility metrics
- Generate multiple visualization charts:
  - Price charts
  - Returns distribution histograms
  - Volatility analysis with rolling windows
  - Cumulative returns
  - Summary dashboard combining all metrics

## Requirements

- Python 3.x
- yfinance
- pandas
- numpy
- matplotlib

## Installation

```bash
pip install yfinance pandas numpy matplotlib
```

## Usage

Run the main script to analyze a stock (default: AAPL for 2024):

```bash
python main.py
```

To analyze different stocks or date ranges, modify the parameters in `main.py`:

```python
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
model_param = DataLoader.load_data('AAPL', start_date, end_date)
```

## Project Structure

- `main.py` - Entry point for running stock analysis
- `price_model.py` - Data loading and statistical calculations
  - `ModelParam`: Dataclass for stock data and metrics
  - `DataLoader`: Fetches data from Yahoo Finance
  - `ConfigData`: Validates and provides access to stock data
- `graph_model.py` - Visualization and charting functionality
  - `GraphModel`: Creates various charts and dashboards

## Example Output

The tool displays statistical metrics including:
- Current price
- Price mean and standard deviation
- Return mean and standard deviation
- Annualized volatility
- Number of data points

And generates multiple charts showing price movements, return distributions, volatility patterns, and cumulative performance.
