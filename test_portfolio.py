import unittest
from datetime import datetime
import pandas as pd
import sys
from pathlib import Path

# Add the current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from order.order import Order, OrderType, OrderDirection, LimitOrder, StopOrder
from portfolio.portfolio import Portfolio


class TestOrder(unittest.TestCase):
    """Test cases for Order class and its subclasses"""

    def test_order_creation(self):
        """Test basic order creation"""
        order = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=10,
            open_price=150.0
        )
        self.assertEqual(order.symbol, "AAPL")
        self.assertEqual(order.order_type, OrderType.MARKET)
        self.assertEqual(order.direction, OrderDirection.LONG)
        self.assertEqual(order.quantity, 10)
        self.assertEqual(order.open_price, 150.0)
        self.assertFalse(order.filled)
        self.assertIsNone(order.fill_price)

    def test_market_order_execution_long(self):
        """Test market order execution for LONG position"""
        order = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=10,
            open_price=150.0
        )
        result = order.execute_order(155.0)
        
        self.assertTrue(result)
        self.assertTrue(order.filled)
        self.assertEqual(order.fill_price, 155.0)
        self.assertIsNotNone(order.fill_time)
        # PnL = open_price * quantity - fill_price * quantity
        # PnL = 150 * 10 - 155 * 10 = -50
        self.assertEqual(order.pnl, -50.0)

    def test_market_order_execution_short(self):
        """Test market order execution for SHORT position"""
        order = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.SHORT,
            quantity=10,
            open_price=150.0
        )
        result = order.execute_order(145.0)
        
        self.assertTrue(result)
        self.assertTrue(order.filled)
        self.assertEqual(order.fill_price, 145.0)
        # PnL = fill_price * quantity - open_price * quantity
        # PnL = 145 * 10 - 150 * 10 = -50
        self.assertEqual(order.pnl, -50.0)

    def test_limit_order_long_execution(self):
        """Test limit order execution for LONG position"""
        order = LimitOrder(
            symbol="AAPL",
            direction=OrderDirection.LONG,
            quantity=10,
            limit_price=150.0,
            open_price=155.0
        )
        
        # Price is at limit, should execute
        result = order.execute_order(150.0)
        self.assertTrue(result)
        self.assertTrue(order.filled)
        
        # Create another order
        order2 = LimitOrder(
            symbol="AAPL",
            direction=OrderDirection.LONG,
            quantity=10,
            limit_price=150.0,
            open_price=155.0
        )
        
        # Price is below limit, should execute
        result2 = order2.execute_order(148.0)
        self.assertTrue(result2)
        self.assertTrue(order2.filled)
        
        # Create third order
        order3 = LimitOrder(
            symbol="AAPL",
            direction=OrderDirection.LONG,
            quantity=10,
            limit_price=150.0,
            open_price=155.0
        )
        
        # Price is above limit, should not execute
        result3 = order3.execute_order(152.0)
        self.assertFalse(result3)
        self.assertFalse(order3.filled)

    def test_limit_order_short_execution(self):
        """Test limit order execution for SHORT position"""
        order = LimitOrder(
            symbol="AAPL",
            direction=OrderDirection.SHORT,
            quantity=10,
            limit_price=150.0,
            open_price=145.0
        )
        
        # Price is at limit, should execute
        result = order.execute_order(150.0)
        self.assertTrue(result)
        self.assertTrue(order.filled)
        
        # Create another order
        order2 = LimitOrder(
            symbol="AAPL",
            direction=OrderDirection.SHORT,
            quantity=10,
            limit_price=150.0,
            open_price=145.0
        )
        
        # Price is above limit, should execute
        result2 = order2.execute_order(152.0)
        self.assertTrue(result2)
        self.assertTrue(order2.filled)
        
        # Create third order
        order3 = LimitOrder(
            symbol="AAPL",
            direction=OrderDirection.SHORT,
            quantity=10,
            limit_price=150.0,
            open_price=145.0
        )
        
        # Price is below limit, should not execute
        result3 = order3.execute_order(148.0)
        self.assertFalse(result3)
        self.assertFalse(order3.filled)

    def test_stop_order_long_execution(self):
        """Test stop order execution for LONG position"""
        order = StopOrder(
            symbol="AAPL",
            direction=OrderDirection.LONG,
            quantity=10,
            stop_price=145.0,
            open_price=150.0
        )
        
        # Price hits stop, should execute
        result = order.execute_order(145.0)
        self.assertTrue(result)
        self.assertTrue(order.filled)
        self.assertTrue(order.stop_trigger)
        
        # Create another order
        order2 = StopOrder(
            symbol="AAPL",
            direction=OrderDirection.LONG,
            quantity=10,
            stop_price=145.0,
            open_price=150.0
        )
        
        # Price above stop, should not execute
        result2 = order2.execute_order(148.0)
        self.assertFalse(result2)
        self.assertFalse(order2.filled)

    def test_stop_order_short_execution(self):
        """Test stop order execution for SHORT position"""
        order = StopOrder(
            symbol="AAPL",
            direction=OrderDirection.SHORT,
            quantity=10,
            stop_price=155.0,
            open_price=150.0
        )
        
        # Price hits stop, should execute
        result = order.execute_order(155.0)
        self.assertTrue(result)
        self.assertTrue(order.filled)
        self.assertTrue(order.stop_trigger)
        
        # Create another order
        order2 = StopOrder(
            symbol="AAPL",
            direction=OrderDirection.SHORT,
            quantity=10,
            stop_price=155.0,
            open_price=150.0
        )
        
        # Price below stop, should not execute
        result2 = order2.execute_order(152.0)
        self.assertFalse(result2)
        self.assertFalse(order2.filled)

    def test_get_order(self):
        """Test get_order method"""
        order = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=10,
            open_price=150.0
        )
        order_dict = order.get_order()
        
        self.assertIn('order_id', order_dict)
        self.assertEqual(order_dict['symbol'], "AAPL")
        self.assertEqual(order_dict['order_type'], OrderType.MARKET)
        self.assertEqual(order_dict['direction'], OrderDirection.LONG)
        self.assertEqual(order_dict['quantity'], 10)


class TestPortfolio(unittest.TestCase):
    """Test cases for Portfolio class"""

    def setUp(self):
        """Set up test portfolio before each test"""
        self.portfolio = Portfolio(initial_capital=10000)

    def test_portfolio_initialization(self):
        """Test portfolio initialization"""
        self.assertEqual(self.portfolio.initial_capital, 10000)
        self.assertEqual(self.portfolio.current_cash, 10000)
        self.assertTrue(self.portfolio.position_df.empty)
        self.assertTrue(self.portfolio.open_orders_df.empty)
        self.assertTrue(self.portfolio.filled_orders_df.empty)

    def test_add_order(self):
        """Test adding an order to portfolio"""
        order = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=10,
            open_price=150.0
        )
        self.portfolio.add_order(order)
        
        self.assertEqual(len(self.portfolio.open_orders_df), 1)
        self.assertEqual(self.portfolio.open_orders_df.iloc[0]['symbol'], "AAPL")
        self.assertEqual(self.portfolio.open_orders_df.iloc[0]['quantity'], 10)

    def test_execute_market_order_long(self):
        """Test executing a LONG market order"""
        order = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=10,
            open_price=150.0
        )
        
        current_price = 150.0
        success = self.portfolio.execute_market_order(order, current_price)
        
        self.assertTrue(success)
        self.assertEqual(self.portfolio.current_cash, 10000 - 10 * 150.0)
        self.assertEqual(len(self.portfolio.position_df), 1)
        self.assertEqual(self.portfolio.position_df.loc["AAPL"]['quantity'], 10)
        self.assertEqual(len(self.portfolio.filled_orders_df), 1)

    def test_execute_market_order_short(self):
        """Test executing a SHORT market order"""
        order = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.SHORT,
            quantity=10,
            open_price=150.0
        )
        
        current_price = 150.0
        success = self.portfolio.execute_market_order(order, current_price)
        
        self.assertTrue(success)
        self.assertEqual(self.portfolio.current_cash, 10000 + 10 * 150.0)
        self.assertEqual(len(self.portfolio.position_df), 1)
        self.assertEqual(self.portfolio.position_df.loc["AAPL"]['quantity'], -10)

    def test_insufficient_cash(self):
        """Test that insufficient cash raises error"""
        order = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=100,
            open_price=150.0
        )
        
        current_price = 150.0  # Would need 15000, only have 10000
        
        with self.assertRaises(ValueError):
            self.portfolio.execute_market_order(order, current_price)

    def test_multiple_positions(self):
        """Test managing multiple positions"""
        # Buy AAPL
        order1 = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=10,
            open_price=150.0
        )
        self.portfolio.execute_market_order(order1, 150.0)
        
        # Buy GOOGL
        order2 = Order(
            symbol="GOOGL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=5,
            open_price=200.0
        )
        self.portfolio.execute_market_order(order2, 200.0)
        
        self.assertEqual(len(self.portfolio.position_df), 2)
        self.assertEqual(self.portfolio.position_df.loc["AAPL"]['quantity'], 10)
        self.assertEqual(self.portfolio.position_df.loc["GOOGL"]['quantity'], 5)
        self.assertEqual(self.portfolio.current_cash, 10000 - 1500 - 1000)

    def test_averaging_positions(self):
        """Test averaging into a position"""
        # Buy AAPL at 150
        order1 = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=10,
            open_price=150.0
        )
        self.portfolio.execute_market_order(order1, 150.0)
        
        # Buy more AAPL at 160
        order2 = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=10,
            open_price=160.0
        )
        self.portfolio.execute_market_order(order2, 160.0)
        
        self.assertEqual(self.portfolio.position_df.loc["AAPL"]['quantity'], 20)
        # Average price should be (150*10 + 160*10) / 20 = 155
        self.assertEqual(self.portfolio.position_df.loc["AAPL"]['avg_price'], 155.0)

    def test_closing_position(self):
        """Test closing a position"""
        # Buy AAPL
        order1 = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=10,
            open_price=150.0
        )
        self.portfolio.execute_market_order(order1, 150.0)
        
        # Sell AAPL (close position)
        order2 = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.SHORT,
            quantity=10,
            open_price=160.0
        )
        self.portfolio.execute_market_order(order2, 160.0)
        
        # Position should be closed (quantity = 0)
        self.assertEqual(self.portfolio.position_df.loc["AAPL"]['quantity'], 0)

    def test_check_pending_orders(self):
        """Test checking and executing pending orders"""
        # Add a limit order
        limit_order = LimitOrder(
            symbol="AAPL",
            direction=OrderDirection.LONG,
            quantity=10,
            limit_price=150.0,
            open_price=155.0
        )
        self.portfolio.add_order(limit_order, limit_price=150.0)
        
        # Market price is above limit, should not execute
        market_data = {"AAPL": 152.0}
        executed = self.portfolio.check_pending_orders(market_data)
        self.assertEqual(len(executed), 0)
        
        # Market price hits limit, should execute
        market_data = {"AAPL": 150.0}
        executed = self.portfolio.check_pending_orders(market_data)
        self.assertEqual(len(executed), 1)
        self.assertTrue(executed[0].filled)

    def test_update_portfolio_value(self):
        """Test updating portfolio value"""
        # Buy AAPL
        order = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=10,
            open_price=150.0
        )
        self.portfolio.execute_market_order(order, 150.0)
        
        # Update portfolio value with new market data
        timestamp = datetime.now()
        market_data = {"AAPL": 160.0}
        self.portfolio.update_portfolio_value(market_data, timestamp)
        
        # Check portfolio history
        self.assertEqual(len(self.portfolio.portfolio_history_df), 1)
        
        # Total value = cash + positions value
        # cash = 10000 - 1500 = 8500
        # positions = 10 * 160 = 1600
        # total = 10100
        total_value = self.portfolio.portfolio_history_df.iloc[0]['total_value']
        self.assertEqual(total_value, 8500 + 1600)
        
        # Check unrealized PnL
        # Bought at 150, now at 160, quantity = 10
        # Unrealized PnL = (160 - 150) * 10 = 100
        self.assertEqual(self.portfolio.position_df.loc["AAPL"]['unrealized_pnl'], 100.0)

    def test_get_portfolio_summary(self):
        """Test getting portfolio summary"""
        # Buy AAPL
        order = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=10,
            open_price=150.0
        )
        self.portfolio.execute_market_order(order, 150.0)
        
        # Update portfolio value
        timestamp = datetime.now()
        market_data = {"AAPL": 160.0}
        self.portfolio.update_portfolio_value(market_data, timestamp)
        
        summary = self.portfolio.get_portfolio_summary()
        
        self.assertEqual(summary['initial_capital'], 10000)
        self.assertEqual(summary['current_cash'], 8500)
        self.assertEqual(summary['positions_count'], 1)
        self.assertEqual(summary['filled_orders_count'], 1)
        self.assertAlmostEqual(summary['total_return_pct'], 1.0, places=2)

    def test_get_position_analysis(self):
        """Test getting position analysis"""
        # Buy AAPL
        order = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=10,
            open_price=150.0
        )
        self.portfolio.execute_market_order(order, 150.0)
        
        # Update portfolio value
        timestamp = datetime.now()
        market_data = {"AAPL": 160.0}
        self.portfolio.update_portfolio_value(market_data, timestamp)
        
        analysis = self.portfolio.get_position_analysis()
        
        self.assertEqual(len(analysis), 1)
        self.assertIn('weight_pct', analysis.columns)
        self.assertIn('cost_basis', analysis.columns)
        self.assertIn('pnl_pct', analysis.columns)
        
        # Cost basis = 10 * 150 = 1500
        self.assertEqual(analysis.loc["AAPL"]['cost_basis'], 1500.0)
        
        # PnL % = (100 / 1500) * 100 = 6.67%
        self.assertAlmostEqual(analysis.loc["AAPL"]['pnl_pct'], 6.67, places=2)

    def test_complex_trading_scenario(self):
        """Test a complex trading scenario with multiple orders"""
        # Day 1: Buy AAPL and GOOGL
        order1 = Order(
            symbol="AAPL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=10,
            open_price=150.0
        )
        self.portfolio.execute_market_order(order1, 150.0)
        
        order2 = Order(
            symbol="GOOGL",
            order_type=OrderType.MARKET,
            direction=OrderDirection.LONG,
            quantity=5,
            open_price=200.0
        )
        self.portfolio.execute_market_order(order2, 200.0)
        
        # Update portfolio value
        market_data = {"AAPL": 155.0, "GOOGL": 205.0}
        self.portfolio.update_portfolio_value(market_data, datetime.now())
        
        # Day 2: Add limit orders
        limit_order = LimitOrder(
            symbol="MSFT",
            direction=OrderDirection.LONG,
            quantity=8,
            limit_price=300.0,
            open_price=305.0
        )
        self.portfolio.add_order(limit_order, limit_price=300.0)
        
        # Check if limit order executes
        market_data = {"AAPL": 155.0, "GOOGL": 205.0, "MSFT": 300.0}
        executed = self.portfolio.check_pending_orders(market_data)
        
        self.assertEqual(len(executed), 1)
        self.assertEqual(len(self.portfolio.position_df), 3)
        
        # Update portfolio value
        self.portfolio.update_portfolio_value(market_data, datetime.now())
        
        # Day 3: Place stop loss on AAPL
        stop_order = StopOrder(
            symbol="AAPL",
            direction=OrderDirection.SHORT,
            quantity=10,
            stop_price=150.0,
            open_price=155.0
        )
        self.portfolio.add_order(stop_order, stop_price=150.0)
        
        # Price drops to stop
        market_data = {"AAPL": 150.0, "GOOGL": 205.0, "MSFT": 310.0}
        executed = self.portfolio.check_pending_orders(market_data)
        
        # Stop should trigger
        self.assertEqual(len(executed), 1)
        
        # Get final summary
        self.portfolio.update_portfolio_value(market_data, datetime.now())
        summary = self.portfolio.get_portfolio_summary()
        
        self.assertEqual(summary['positions_count'], 3)
        self.assertTrue(summary['filled_orders_count'] >= 3)


def run_tests():
    """Run all tests and print results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestOrder))
    suite.addTests(loader.loadTestsFromTestCase(TestPortfolio))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

