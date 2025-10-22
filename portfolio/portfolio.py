import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from order.order import Order, OrderDirection, OrderType, LimitOrder, StopOrder

class Portfolio:

    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital
        self.current_cash = initial_capital
        self.position_df = pd.DataFrame(columns=['symbol','quantity','avg_price','market_value','unrealized_pnl']).set_index('symbol')
        self.open_orders_df = pd.DataFrame(columns=['order_id','symbol','order_type','direction','quantity','open_price','open_time','limit_price','stop_price','filled'])
        self.filled_orders_df = pd.DataFrame(columns=['order_id','symbol','order_type','direction','quantity','open_price','open_time','fill_price','fill_time','pnl'])
        self.portfolio_history_df = pd.DataFrame(columns=['timestamp','total_value','cash','positions_value','returns']).set_index('timestamp')

    def add_order(self, order, limit_price = None, stop_price = None):
        
        new_order = {
            'order_id': order.order_id,
            'symbol': order.symbol,
            'order_type': order.order_type,
            'direction': order.direction,
            'quantity': order.quantity,
            'open_price': order.open_price,
            'open_time': order.open_time,
            'limit_price': limit_price,
            'stop_price': stop_price,
            'filled': order.filled
        }

        self.open_orders_df = pd.concat([
            self.open_orders_df,
            pd.DataFrame([new_order])
        ], ignore_index=True)

    def execute_market_order(self, order, current_price):
        try:
            success = order.execute_order(current_price)
            if success:
                self._update_positions(order, current_price)
                filled_order = {
                    'order_id': order.order_id,
                    'symbol': order.symbol,
                    'order_type': order.order_type.value,
                    'direction': order.direction.value,
                    'quantity': order.quantity,
                    'open_price': order.open_price,
                    'open_time': order.open_time,
                    'fill_price': order.fill_price,
                    'fill_time': order.fill_time,
                    'pnl': order.pnl
                }
                self.filled_orders_df = pd.concat([
                    self.filled_orders_df,
                    pd.DataFrame([filled_order])
                ], ignore_index=True)
                return success
        except ValueError as e:
            # Re-raise ValueError (like insufficient cash) without wrapping
            raise
        except Exception as e:
            raise Exception(f"Execute order {order.order_id} with unexpect error {e}")
        finally:
            pass
    
    def check_pending_orders(self, market_data):

        executed_orders = []

        for idx, order_row in self.open_orders_df.iterrows():
            if order_row['filled']:
                continue
            symbol = order_row['symbol']
            if symbol not in market_data:
                continue
            current_price = market_data[symbol]
            order = self._create_order_from_row(order_row)
            order.execute_order(current_price)
            if order.filled:
                self.execute_market_order(order, current_price)
                self.open_orders_df.at[idx, 'filled'] = True
                executed_orders.append(order)
        
        return executed_orders

    def _create_order_from_row(self, order_row):
        order_type = order_row['order_type'] if isinstance(order_row['order_type'], OrderType) else OrderType(order_row['order_type'])
        direction = order_row['direction'] if isinstance(order_row['direction'], OrderDirection) else OrderDirection(order_row['direction'])
        
        if order_type == OrderType.LIMIT:
            return LimitOrder(
                symbol=order_row['symbol'],
                direction=direction,
                quantity=order_row['quantity'],
                limit_price=order_row['limit_price'],
                open_price=order_row['open_price'],
                timestamp=order_row['open_time']
            )
        elif order_type == OrderType.STOP:
            return StopOrder(
                symbol=order_row['symbol'],
                direction=direction,
                quantity=order_row['quantity'],
                stop_price=order_row['stop_price'],
                open_price=order_row['open_price'],
                timestamp=order_row['open_time']
            )
        else:
            return Order(
                symbol=order_row['symbol'],
                order_type=OrderType.MARKET,
                direction=direction,
                quantity=order_row['quantity'],
                open_price=order_row['open_price'],
                timestamp=order_row['open_time']
            )

    def _update_positions(self, order, current_price):
        symbol = order.symbol
        quantity = order.quantity
        direction = order.direction
        cost = quantity * current_price

        if direction == OrderDirection.LONG:
            if cost > self.current_cash:
                raise ValueError(f"Insufficient cash to buy {quantity} shares of {symbol} at {current_price}")
            self.current_cash -= cost
        else:
            self.current_cash += cost
        
        current_qty = 0
        if symbol not in self.position_df.index:
            if direction == OrderDirection.LONG:
                current_qty = quantity
            else:
                current_qty = -1 * quantity
            new_position = {
                'quantity': current_qty,
                'avg_price': current_price,
                'market_value': current_qty * current_price,
                'unrealized_pnl': 0.0
            }
            self.position_df.loc[symbol] = new_position                
        else:
            current_pos = self.position_df.loc[symbol]
            current_qty = current_pos['quantity']

            new_avg = 0.0
            new_qty = 0.0
            if direction == OrderDirection.LONG:
                new_qty = current_qty + quantity
                if current_qty * new_qty >= 0:
                    new_avg = (current_pos['avg_price'] * abs(current_qty) + current_price * quantity) / abs(new_qty)
                else:
                    new_avg = current_price if abs(new_qty) > abs(current_qty) else current_pos['avg_price']
            else:
                new_qty = current_qty - quantity
                if current_qty * new_qty >= 0:
                    new_avg = (current_pos['avg_price'] * abs(current_qty) + current_price * quantity) / abs(new_qty)
                else:
                    new_avg = current_price if abs(new_qty) > abs(current_qty) else current_pos['avg_price']
            
            self.position_df.at[symbol, 'quantity'] = new_qty
            self.position_df.at[symbol, 'avg_price'] = new_avg

    def update_portfolio_value(self, market_data, timestamp):
        positions_to_update = self.position_df.index.intersection(market_data.keys())
        
        if not positions_to_update.empty:
            current_prices = [market_data[symbol] for symbol in positions_to_update]
            quantities = self.position_df.loc[positions_to_update, 'quantity']
            avg_prices = self.position_df.loc[positions_to_update, 'avg_price']
            
            market_values = quantities * current_prices
            unrealized_pnls = (current_prices - avg_prices) * quantities
            
            self.position_df.loc[positions_to_update, 'market_value'] = market_values
            self.position_df.loc[positions_to_update, 'unrealized_pnl'] = unrealized_pnls
            
            total_positions_value = market_values.sum()
        else:
            total_positions_value = 0.0
        
        total_value = self.current_cash + total_positions_value
        
        new_record = {
            'total_value': total_value,
            'cash': self.current_cash,
            'positions_value': total_positions_value,
            'returns': (total_value / self.initial_capital - 1) * 100
        }
        
        self.portfolio_history_df.loc[timestamp] = new_record

    def get_portfolio_summary(self):
        if self.portfolio_history_df.empty:
            return {}
            
        total_value = self.portfolio_history_df['total_value'].iloc[-1]
        total_return = (total_value / self.initial_capital - 1) * 100
        
        open_orders_count = len(self.open_orders_df[self.open_orders_df['filled'] == False]) if not self.open_orders_df.empty else 0
        
        return {
            'initial_capital': self.initial_capital,
            'current_cash': self.current_cash,
            'total_value': total_value,
            'total_return_pct': total_return,
            'positions_count': len(self.position_df),
            'open_orders_count': open_orders_count,
            'filled_orders_count': len(self.filled_orders_df),
            'unrealized_pnl_total': self.position_df['unrealized_pnl'].sum() if not self.position_df.empty else 0.0
        }

    def get_position_analysis(self):
        if self.position_df.empty:
            return pd.DataFrame()
        
        analysis_df = self.position_df.copy()
        
        total_portfolio_value = self.current_cash + analysis_df['market_value'].sum()
        
        if total_portfolio_value > 0:
            analysis_df['weight_pct'] = (analysis_df['market_value'] / total_portfolio_value) * 100
        else:
            analysis_df['weight_pct'] = 0.0
        
        analysis_df['cost_basis'] = analysis_df['quantity'] * analysis_df['avg_price']
        analysis_df['pnl_pct'] = (analysis_df['unrealized_pnl'] / analysis_df['cost_basis'].abs()) * 100
        
        analysis_df['pnl_pct'] = analysis_df['pnl_pct'].replace([np.inf, -np.inf], 0).fillna(0)
        
        return analysis_df