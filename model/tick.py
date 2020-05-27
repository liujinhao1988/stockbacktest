
#股票期货期权tick数据


import datetime

import numpy as np



class Tick:
    def __init__(self, instrument, tick_dict):
        """
        Tick 对象
        :param instrument: Instrument
        :param tick_dict: dict
        """
        self._instrument = instrument
        self._tick_dict = tick_dict

    
    def order_book_id(self):
        """
        [str] 标的代码
        """
        return self._instrument.order_book_id

    
    def datetime(self):
        """
        [datetime.datetime] 当前快照数据的时间戳
        """
        try:
            dt = self._tick_dict['datetime']
        except (KeyError, ValueError):
            return datetime.datetime.min
        else:
            if not isinstance(dt, datetime.datetime):
                if dt > 10000000000000000:  # ms
                    return dt

            return dt

 
    def open(self):
        """
        [float] 当日开盘价
        """
        return self._tick_dict['open']

    
    def last(self):
        """
        [float] 当前最新价
        """
        return self._tick_dict['last']

    
    def high(self):
        """
        [float] 截止到当前的最高价
        """
        return self._tick_dict['high']

  
    def low(self):
        """
        [float] 截止到当前的最低价
        """
        return self._tick_dict['low']

   
    def prev_close(self):
        """
       [float] 昨日收盘价
       """
        try:
            return self._tick_dict['prev_close']
        except (KeyError, ValueError):
            return 0


    def volume(self):
        """
        [float] 截止到当前的成交量
        """
        try:
            return self._tick_dict['volume']
        except (KeyError, ValueError):
            return 0


    def total_turnover(self):
        """
        [float] 截止到当前的成交额
        """
        try:
            return self._tick_dict['total_turnover']
        except (KeyError, ValueError):
            return 0

  
    def open_interest(self):
        """
        [float] 截止到当前的持仓量（期货专用）
        """
        try:
            return self._tick_dict['open_interest']
        except (KeyError, ValueError):
            return 0

   
    def prev_settlement(self):
        """
        [float] 昨日结算价（期货专用）
        """
        try:
            return self._tick_dict['prev_settlement']
        except (KeyError, ValueError):
            return 0


    def asks(self):
        """
        [list] 卖出报盘价格，asks[0]代表盘口卖一档报盘价
        """
        try:
            return self._tick_dict['asks']
        except (KeyError, ValueError):
            return [0] * 5

   
    def ask_vols(self):
        """
        [list] 卖出报盘数量，ask_vols[0]代表盘口卖一档报盘数量
        """
        try:
            return self._tick_dict['ask_vols']
        except (KeyError, ValueError):
            return [0] * 5

  
    def bids(self):
        """
        [list] 买入报盘价格，bids[0]代表盘口买一档报盘价
        """
        try:
            return self._tick_dict['bids']
        except (KeyError, ValueError):
            return [0] * 5

  
    def bid_vols(self):
        """
        [list] 买入报盘数量，bids_vols[0]代表盘口买一档报盘数量
        """
        try:
            return self._tick_dict['bid_vols']
        except (KeyError, ValueError):
            return [0] * 5


    def limit_up(self):
        """
        [float] 涨停价
        """
        try:
            return self._tick_dict['limit_up']
        except (KeyError, ValueError):
            return 0


    def limit_down(self):
        """
        [float] 跌停价
        """
        try:
            return self._tick_dict['limit_down']
        except (KeyError, ValueError):
            return 0

   
    def isnan(self):
        return np.isnan(self.last)

    def __repr__(self):
        items = []
        for name in dir(self):
            if name.startswith("_"):
                continue
            items.append((name, getattr(self, name)))
        return "Tick({0})".format(', '.join('{0}: {1}'.format(k, v) for k, v in items))

    def __getitem__(self, key):
        return getattr(self, key)
