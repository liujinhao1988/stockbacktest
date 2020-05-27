#股票持仓类
class Position:

    def __init__(self, order_book_id, direction, init_quantity=0):
        self._env = None

        self._order_book_id = order_book_id
        self._instrument = self._env.data_proxy.instruments(order_book_id)  # type: Instrument
        self._direction = direction

        self._old_quantity = init_quantity
        self._logical_old_quantity = 0
        self._today_quantity = 0

        self._avg_price = 0
        self._trade_cost = 0
        self._transaction_cost = 0
        self._prev_close = None
        self._last_price = float("NaN")

        self._direction_factor = 1 if direction == POSITION_DIRECTION.LONG else -1

   

    def order_book_id(self):
        # type: () -> str
        return self._order_book_id



    def direction(self):
        # type: () -> POSITION_DIRECTION
        return self._direction

 

    def quantity(self):
        # type: () -> int
        return self._old_quantity + self._today_quantity

  

    def transaction_cost(self):
        # type: () -> float
        return self._transaction_cost

 

    def avg_price(self):
        # type: () -> float
        return self._avg_price



    def trading_pnl(self):
        # type: () -> float
        trade_quantity = self._today_quantity + (self._old_quantity - self._logical_old_quantity)
        if trade_quantity == 0:
            return 0
        return (trade_quantity * self.last_price - self._trade_cost) * self._direction_factor

  

    def position_pnl(self):
        # type: () -> float
        if self._logical_old_quantity == 0:
            return 0
        return self._logical_old_quantity * (self.last_price - self.prev_close) * self._direction_factor

 

    def pnl(self):
        # type: () -> float
        """
        返回该持仓的累积盈亏
        """
        if self.quantity == 0:
            return 0
        return (self.last_price - self.avg_price) * self.quantity * self._direction_factor

  

    def market_value(self):
        # type: () -> float
        return self.last_price * self.quantity if self.quantity != 0 else 0



    def margin(self):
        # type: () -> float
        return 0


    def equity(self):
        # type: () -> float
        return self.last_price * self.quantity if self.quantity != 0 else 0


    def prev_close(self):


        return self._prev_close



    def last_price(self):



        return self._last_price


    def closable(self):
        # type: () -> int
        """
        可平仓位
        """
       
        return self.quantity


    def closable(self):
        # type: () -> int
        return self._today_quantity - sum(
            o.unfilled_quantity for o in self._open_orders if o.position_effect == None
        )

    def get_state(self):
        """"""
        return {
            "old_quantity": self._old_quantity,
            "logical_old_quantity": self._logical_old_quantity,
            "today_quantity": self._today_quantity,
            "avg_price": self._avg_price,
            "trade_cost": self._trade_cost,
            "transaction_cost": self._transaction_cost,
            "prev_close": self._prev_close
        }

    def set_state(self, state):
        """"""
        self._old_quantity = state.get("old_quantity", 0)
        self._logical_old_quantity = state.get("logical_old_quantity", self._old_quantity)
        self._today_quantity = state.get("today_quantity", 0)
        self._avg_price = state.get("avg_price", 0)
        self._trade_cost = state.get("trade_cost", 0)
        self._transaction_cost = state.get("transaction_cost", 0)
        self._prev_close = state.get("prev_close")

    def before_trading(self, trading_date):
        # type: (date) -> float
        # 返回该阶段导致总资金的变化量
        return 0

    def apply_trade(self, trade):
        # type: (Trade) -> float
        # 返回总资金的变化量
        self._transaction_cost += trade.transaction_cost
        if trade.position_effect == None:
            if self.quantity < 0:
                self._avg_price = trade.last_price if self.quantity + trade.last_quantity > 0 else 0
            else:
                cost = self.quantity * self._avg_price + trade.last_quantity * trade.last_price
                self._avg_price = cost / (self.quantity + trade.last_quantity)
            self._today_quantity += trade.last_quantity
            self._trade_cost += trade.last_price * trade.last_quantity
            return (-1 * trade.last_price * trade.last_quantity) - trade.transaction_cost
        elif trade.position_effect == None:
            self._today_quantity -= max(trade.last_quantity - self._old_quantity, 0)
            self._old_quantity -= min(trade.last_quantity, self._old_quantity)
            self._trade_cost -= trade.last_price * trade.last_quantity
            return trade.last_price * trade.last_quantity - trade.transaction_cost
        else:
            raise NotImplementedError("{} does not support position effect {}".format(
                self.__class__.__name__, trade.position_effect
            ))

    def settlement(self, trading_date):
        # type: (date) -> float
        # 返回该阶段导致总资金的变化量以及反映该阶段引起其他持仓变化的虚拟交易，虚拟交易用于换代码，转股等操作
        self._old_quantity += self._today_quantity
        self._logical_old_quantity = self._old_quantity
        self._today_quantity = self._trade_cost = self._transaction_cost = self._non_closable = 0
        self._prev_close = self.last_price
        return 0

    def update_last_price(self, price):
        self._last_price = price

    def calc_close_today_amount(self, trade_amount):
        return 0


    def _open_orders(self):
        # type: () -> Iterable[Order]
        for order in self.order_book_id:
            if order.position_direction == self._direction:
                yield order


