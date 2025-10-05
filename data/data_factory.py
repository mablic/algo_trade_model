from data import download_data as ddData
from data.base_data import BaseData
from data.stock_data import StockData
from data.option_data import OptionData
from datetime import datetime

class DataLoader:
    @staticmethod
    def load_data(ticker, start_date, end_date, data_type = "stock", option_type= "call", expiration_date=datetime.now()):
        try:
            stock_data = ddData.load_ticker_data(ticker, start_date, end_date)
            if data_type.lower() == "base":
                return BaseData(
                    ticker=ticker,
                    start_date=start_date,
                    end_date=end_date,
                    prices=stock_data
                )
            elif data_type.lower() == "stock":
                return StockData(
                    ticker=ticker,
                    start_date=start_date,
                    end_date=end_date,
                    prices=stock_data
                )
            elif data_type.lower() == 'option':
                risk_free_rate = ddData.load_rf_data()
                strike_data = ddData.load_strike_data(ticker, expiration_date)
                # Get the actual expiration date used
                actual_expiration = datetime.strptime(strike_data['expiration'], '%Y-%m-%d')
                if option_type == "call":
                    # Get ATM strike from calls
                    calls_df = strike_data['calls']
                    strike_price = calls_df.iloc[len(calls_df)//2]['strike'] if not calls_df.empty else 100.0
                    return OptionData(
                        ticker=ticker,
                        start_date=start_date,
                        end_date=end_date,
                        prices=stock_data,
                        strike_price=strike_price,
                        expiration_date=actual_expiration,
                        risk_free_rate=risk_free_rate
                    )
                else:
                    # Get ATM strike from puts
                    puts_df = strike_data['puts']
                    strike_price = puts_df.iloc[len(puts_df)//2]['strike'] if not puts_df.empty else 100.0
                    return OptionData(
                        ticker=ticker,
                        start_date=start_date,
                        end_date=end_date,
                        prices=stock_data,
                        strike_price=strike_price,
                        expiration_date=actual_expiration,
                        risk_free_rate=risk_free_rate
                    )
            else:
                raise ValueError(f"Unknown data type: {data_type}")

        except Exception as e:
            raise Exception(f"Failed to load data for {ticker}: {str(e)}")

