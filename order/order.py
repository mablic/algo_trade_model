from enum import Enum
from datetime import datetime
import uuid

class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"

class OrderDirection(Enum):
    LONG = "LONG"
    SHORT = "SHORT"

class Order:

    def __init__(self, symbol, order_type, direction,
                 quantity, open_price=None, timestamp=None):
        self.symbol = symbol
        self.order_type = order_type
        self.direction = direction
        self.quantity = quantity
        self.open_price = open_price
        self.open_time = timestamp or datetime.now()
        self.filled = False
        self.fill_price = None
        self.fill_time = None
        self.pnl = None
        self.order_id = uuid.uuid4()

    def __str__(self):
        return f"Order({self.symbol}, {self.order_type.value}, {self.direction.value}, {self.quantity})"

    def execute_order(self, fill_price):
        try:
            pnl = 0
            cost = self.quantity * fill_price
            if self.direction == OrderDirection.LONG:
                pnl = self.open_price * self.quantity - cost
            else:
                pnl = cost - self.open_price * self.quantity
            self.filled = True
            self.fill_price = fill_price
            self.fill_time = datetime.now()
            self.pnl = pnl
            return True
        except Exception as e:
            raise Exception(f"Unexpected exception at execute_order: {e}")
        finally:
            pass

    def get_order(self):
        return {
            'order_id': self.order_id,
            'symbol': self.symbol,
            'order_type': self.order_type,
            'direction': self.direction,
            'quantity': self.quantity,
            'open_price': self.open_price,
            'open_time': self.open_time,
            'filled': self.filled,
            'fill_price': self.fill_price,
            'fill_time': self.fill_time,
            'pnl': self.pnl
        }

class LimitOrder(Order):

    def __init__(self, symbol, direction, quantity, limit_price, open_price=None, timestamp=None):
        super().__init__(symbol, OrderType.LIMIT, direction, quantity, open_price, timestamp)
        self.limit_price = limit_price
    
    def execute_order(self, curr_price):
        if self.order_type == OrderType.LIMIT:
            if self.direction == OrderDirection.LONG and curr_price <= self.limit_price:
                return super().execute_order(curr_price)
            elif self.direction == OrderDirection.SHORT and curr_price >= self.limit_price:
                return super().execute_order(curr_price)
        return False

class StopOrder(Order):

    def __init__(self, symbol, direction, quantity, stop_price, open_price=None, timestamp=None):
        super().__init__(symbol, OrderType.STOP, direction, quantity, open_price, timestamp)
        self.stop_price = stop_price
        self.stop_trigger = False
    
    def execute_order(self, curr_price):
        if self.order_type == OrderType.STOP:
            if self.direction == OrderDirection.LONG:
                if curr_price <= self.stop_price:
                    self.stop_trigger = True
                    return super().execute_order(curr_price)
            else:
                if curr_price >= self.stop_price:
                    self.stop_trigger = True
                    return super().execute_order(curr_price)
        return False
