class TradingEngine:

    def __init__(self, start_balance: float):
        """
        Simulates a simple trading engine that allows buying and selling of shares, tracking the balance and portfolio value for a single stock.

        Args:
            start_balance (float): The initial amount of money available for trading.

        Raises:
            ValueError: If the starting balance is negative.
        """
        if start_balance < 0:
            raise ValueError("Balance cannot be negative.")
        self.balance = start_balance
        self.shares = 0
        self.transactions = []

    def buy(self, price: float, shares: int):
        """
        Buys a specified number of shares at a given price.

        Args:
            price (float): The price per share.
            shares (int): The number of shares to buy.

        Raises:
            ValueError: If the price is not positive, shares is not a whole number or positive, or if there are insufficient funds.
        """
        if not isinstance(shares, int):
            raise ValueError("Shares must be a whole number.")
        if price <= 0:
            raise ValueError("Price must be positive.")
        if shares <= 0:
            raise ValueError("Shares must be positive.")
        total_cost = price * shares
        if total_cost > self.balance:
            raise ValueError("Insufficient balance to complete the purchase.")
        self.balance -= total_cost
        self.shares += shares
        self.transactions.append({'type': 'buy', 'price': price, 'shares': shares})

    def sell(self, price: float, shares: int):
        """
        Sells a specified number of shares at a given price.

        Args:
            price (float): The price per share.
            shares (int): The number of shares to sell.

        Raises:
            ValueError: If the price is not positive, shares is not a whole number or positive, or if there are insufficient shares.
        """
        if not isinstance(shares, int):
            raise ValueError("Shares must be a whole number.")
        if price <= 0:
            raise ValueError("Price must be positive.")
        if shares <= 0:
            raise ValueError("Shares must be positive.")
        if shares > self.shares:
            raise ValueError("Insufficient shares to complete the sale.")
        total_revenue = price * shares
        self.balance += total_revenue
        self.shares -= shares
        self.transactions.append({'type': 'sell', 'price': price, 'shares': shares})

    def get_portfolio_value(self, current_price: float) -> float:
        """
        Calculates the total value of the portfolio based on the current price of the stock and the current remaining balance.

        Args:
            current_price (float): The current price per share.

        Returns:
            float: The total value of the portfolio.

        Raises:
            ValueError: If the current price is negative.
        """
        if current_price < 0:
            raise ValueError("Current price cannot be negative.")
        return self.balance + (self.shares * current_price)