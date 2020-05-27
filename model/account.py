
#股票账户类



class Account:
    """
    账户，多种持仓和现金的集合。

    不同品种的合约持仓可能归属于不同的账户，如股票、转债、场内基金、ETF 期权归属于股票账户，期货、期货期权归属于期货账户
    """



    def __init__(self, type, total_cash, init_positions):
        # type: (str, float, Dict[str, int]) -> None
        self._type = type
        self._total_cash = total_cash  # 包含保证金的总资金

        self._positions = {}
        self._backward_trade_set = set()
        self._frozen_cash = 0

      

   




    def get_state(self):
        return {
           
            'frozen_cash': self._frozen_cash,
            "total_cash": self._total_cash,
            'backward_trade_set': list(self._backward_trade_set),
        }

    def set_state(self, state):
        self._frozen_cash = state['frozen_cash']
        self._backward_trade_set = set(state['backward_trade_set'])

        self._positions.clear()
        
        if "total_cash" in state:
            self._total_cash = state["total_cash"]
        else:
            # forward compatible
            total_cash = state["static_total_value"]
            for p in self._iter_pos():
                if p._instrument.type == None:
                    continue
                # FIXME: not exactly right
                try:
                    total_cash -= p.equity
                except RuntimeError:
                    total_cash -= p.prev_close * p.quantity

   

    def fast_forward(self, orders=None, trades=None):
        if trades:
            close_trades = []
            # 先处理开仓
            for trade in trades:
                if trade.exec_id in self._backward_trade_set:
                    continue
                if trade.position_effect == None:
                    self.apply_trade(trade)
                else:
                    close_trades.append(trade)
            # 后处理平仓
            for trade in close_trades:
                self.apply_trade(trade)

        # 计算 Frozen Cash
        if orders:
            self._frozen_cash = sum(self._frozen_cash_of_order(order) for order in orders if order.is_active())

    def get_positions(self):
        # type: () -> Iterable[Position]
        """
        获取所有持仓对象列表，
        """
        return self._iter_pos()

    def get_position(self, order_book_id, direction):
        # type: (str, POSITION_DIRECTION) -> Position
        """
        获取某个标的的持仓对象

        :param order_book_id: 标的编号
        :param direction: 持仓方向

        """
        try:
            return self._positions[order_book_id][direction]
        except KeyError:
            return order_book_id, direction

    def calc_close_today_amount(self, order_book_id, trade_amount, position_direction):
        return self._get_or_create_pos(order_book_id, position_direction).calc_close_today_amount(trade_amount)

   
    def type(self):
        return self._type


    def positions(self):
        return self._positions

  
    def frozen_cash(self):
        # type: () -> float
        """
        冻结资金
        """
        return self._frozen_cash
    def cash(self):
        # type: () -> float
        """
        可用资金
        """
        return self._total_cash - self.margin - self._frozen_cash


    def market_value(self):
        # type: () -> float
        """
        [float] 市值
        """
        return sum(p.market_value * (1 if p.direction == None else -1) for p in self._iter_pos())



    def transaction_cost(self):
        # type: () -> float
        """
        总费用
        """
        return sum(p.transaction_cost for p in self._iter_pos())

 

    def margin(self):
        # type: () -> float
        """
        总保证金
        """
        return sum(p.margin for p in self._iter_pos())

 

    def buy_margin(self):
        # type: () -> float
        """
        多方向保证金
        """
        return sum(p.margin for p in self._iter_pos(None))



    def sell_margin(self):
        # type: () -> float
        """
        空方向保证金
        """
        return sum(p.margin for p in self._iter_pos(None))



    def daily_pnl(self):
        # type: () -> float
        """
        当日盈亏
        """
        return self.trading_pnl + self.position_pnl - self.transaction_cost



    def equity(self):
        # type: () -> float
        """
        总权益
        """
        return sum(p.equity for p in self._iter_pos())

 

    def total_value(self):
        # type: () -> float
        """
        账户总权益
        """
        return self._total_cash + self.equity

 

    def total_cash(self):
        # type: () -> float
        """
        账户总资金
        """
        return self._total_cash - self.margin

  

    def position_pnl(self):
        # type: () -> float
        """
        昨仓盈亏
        """
        return sum(p.position_pnl for p in self._iter_pos())



    def trading_pnl(self):
        # type: () -> float
        """
        交易盈亏
        """
        return sum(p.trading_pnl for p in self._iter_pos())

    def _on_before_trading(self, _):
        trading_date = None
        for position in self._iter_pos():
            self._total_cash += position.before_trading(trading_date)



    def _on_order_pending_new(self, event):
        if event.account != self:
            return
        order = event.order
        self._frozen_cash += self._frozen_cash_of_order(order)

    def _on_order_unsolicited_update(self, event):
        if event.account != self:
            return
        order = event.order
        if order.filled_quantity != 0:
            self._frozen_cash -= order.unfilled_quantity / order.quantity * self._frozen_cash_of_order(order)
        else:
            self._frozen_cash -= self._frozen_cash_of_order(event.order)

    def apply_trade(self, trade, order=None):
        # type: (Trade, Optional[Order]) -> None
        if trade.exec_id in self._backward_trade_set:
            return
        order_book_id = trade.order_book_id
        if trade.position_effect == None:
            delta_cash = self._get_or_create_pos(
                order_book_id
            ).apply_trade(trade) + self._get_or_create_pos(
                order_book_id
            ).apply_trade(trade)
            self._total_cash += delta_cash
        else:
            delta_cash = self._get_or_create_pos(order_book_id, trade.position_direction).apply_trade(trade)
            self._total_cash += delta_cash
        self._backward_trade_set.add(trade.exec_id)
        if order and trade.position_effect != None:
            if trade.last_quantity != order.quantity:
                self._frozen_cash -= trade.last_quantity / order.quantity * self._frozen_cash_of_order(order)
            else:
                self._frozen_cash -= self._frozen_cash_of_order(order)

    def _iter_pos(self, direction=None):
        # type: (Optional[POSITION_DIRECTION]) -> Iterable[Position]
        if direction:
            return (p[direction] for p in self._positions)
        else:
            return self._positions



    def _update_last_price(self, _):
        env = None
        for order_book_id, positions in self._positions:
            price = env.get_last_price(order_book_id)
            if price == price:
                for position in positions:
                    position.update_last_price(price)

    def _frozen_cash_of_order(self, order):
        env = None
        if order.position_effect == None:
            instrument = env.data_proxy.instruments(order.order_book_id)
            order_cost = instrument.calc_cash_occupation(order.frozen_price, order.quantity, order.position_direction)
        else:
            order_cost = 0
        return order_cost + env.get_order_transaction_cost(order)


