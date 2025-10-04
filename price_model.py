import yfinance as yf
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ModelParam:
  ticker: str
  start_date: datetime
  end_date: datetime
  prices: pd.DataFrame = field(default_factory=pd.DataFrame)
  log_returns: pd.Series = field(default_factory=pd.Series)
  volatility: float = 0.0

  def __post_init__(self):
    if not self.prices.empty and self.log_returns.empty:
      self.calculate_log_returns()

  def calculate_log_returns(self):
    if self.prices.empty or 'Close' not in self.prices.columns:
      raise ValueError("Prices data is missing or invalid")
    close_prices = self.prices['Close']
    self.log_returns = np.log(close_prices/ close_prices.shift(1)).dropna()

    if not self.log_returns.empty:
      self.volatility = self.log_returns.std() * np.sqrt(252)

class DataLoader:
  @staticmethod
  def load_data(ticker, start_date, end_date):
    try:
      stock_data = yf.download(ticker, start=start_date, end=end_date)
      if stock_data.empty:
        raise ValueError(f"No data found for ticker: {ticker}")
      
      if isinstance(stock_data.columns, pd.MultiIndex):
          stock_data.columns = stock_data.columns.get_level_values(0)
      
      model_param = ModelParam(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        prices=stock_data
      )

      return model_param
    except Exception as e:
      raise Exception(f"Failed to load data for {ticker}: {str(e)}")

class ConfigData:

  def __init__(self, model_param):
    self.params = model_param
    self._validate_data()
  
  def _validate_data(self):
    if self.params.prices.empty:
      raise ValueError("Price data is empty")

    if 'Close' not in self.params.prices.columns:
      raise ValueError("Close prices are missing from the data")

  @property
  def get_ticker(self):
    return self.params.ticker
  
  @property
  def get_current_price(self):
    return self.params.prices["Close"].iloc[-1]
  
  @property
  def get_volatility(self):
    return self.params.volatility
  
  @property
  def get_log_returns(self):
    return self.params.log_returns

  @property
  def get_prices(self):
    return self.params.prices

  def get_prices_stats(self):
    close_prices = self.params.prices["Close"]
    returns = self.params.log_returns

    stats = {
      'current_price': self.get_current_price,
      'price_mean': close_prices.mean(),
      'price_std': close_prices.std(),
      'return_mean': returns.mean(),
      'return_std' : returns.std(),
      'volatility' : self.get_volatility,
      'data_points' : len(close_prices),
    }

    return stats

if __name__ == '__main__':
  start_date = datetime(2024, 1, 1)
  end_date = datetime(2024, 12, 31)

  try:
    model_param = DataLoader.load_data('AAPL', start_date, end_date)
    config_data = ConfigData(model_param)
    stats = config_data.get_prices_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")

  except Exception as e:
    print(f"Error {e}")

  finally:
    pass