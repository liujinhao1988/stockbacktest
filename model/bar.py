import numpy as np
NAMES = ['open', 'close', 'low', 'high', 'settlement', 'limit_up', 'limit_down', 'volume', 'total_turnover',
         'discount_rate', 'acc_net_value', 'unit_net_value', 'open_interest',
         'basis_spread', 'prev_settlement', 'datetime']

#获取数据切片

class Bar:
    def __init__(self, instrument, df, dt=None):
        self._dt = dt
        self._df = df
        self._instrument = instrument

    
    def open(self):
        """
        [float] 开盘价
        """
        return self._df["open"]

    
    def close(self):
        """
        [float] 收盘价
        """
        return self._df["close"]

    
    def low(self):
        """
        [float] 最低价
        """
        return self._df["low"]

    
    def high(self):
        """
        [float] 最高价
        """
        return self._df["high"]

   
    def limit_up(self):
        """
        [float] 涨停价
        """
        try:
            v = self._df['limit_up']
            return v if v != 0 else np.nan
        except (KeyError, ValueError):
            return np.nan

    
    def limit_down(self):
        """
        [float] 跌停价
        """
        try:
            v = self._df['limit_down']
            return v if v != 0 else np.nan
        except (KeyError, ValueError):
            return np.nan

    
    def prev_close(self):
        """
        [float] 昨日收盘价
        """
        try:
            return self._df['prev_close']
        except (ValueError, KeyError):
            trading_dt = self.trading_dt
            df_proxy = self.df_proxy
            return df_proxy.get_prev_close(self._instrument.order_book_id, trading_dt)

    
    def last(self):
        """
        [float] 当前最新价
        """
        return self.close

    
    def volume(self):
        """
        [float] 截止到当前的成交量
        """
        return self._df["volume"]

    
    def total_turnover(self):
        """
        [float] 截止到当前的成交额
        """
        return self._df['total_turnover']

    
    def discount_rate(self):
        return self._df['discount_rate']

   
    def acc_net_value(self):
        return self._df['acc_net_value']

 
    def unit_net_value(self):
        return self._df['unit_net_value']

    INDEX_MAP = {
        'IF': '000300.XSHG',
        'IH': '000016.XSHG',
        'IC': '000905.XSHG',
    }

    def basis_spread(self):
        try:
            return self._df['basis_spread']
        except (ValueError, KeyError):
            if self._instrument.type != 'Future':
                raise
            if self._instrument.underlying_symbol in ['IH', 'IC', 'IF']:
                order_book_id = self.INDEX_MAP[self._instrument.underlying_symbol]
                bar = order_book_id
                return self.close - bar.close
            else:
                return np.nan

    def settlement(self):
        """
        [float] 结算价（期货专用）
        """
        return self._df['settlement']

    def prev_settlement(self):
        """
        [float] 昨日结算价（期货专用）
        """
        try:
            return self._df['prev_settlement']
        except (ValueError, KeyError):
            trading_dt = self.trading_dt
            df_proxy =self.df_proxy
            return df_proxy.get_prev_settlement(self._instrument.order_book_id, trading_dt)


    def open_interest(self):
        """
        [float] 截止到当前的持仓量（期货专用）
        """
        return self._df['open_interest']


    def datetime(self):
        """
        [datetime.datetime] 时间戳
        """
        if self._dt is not None:
            return self._dt
        return self._df['datetime']

    def instrument(self):
        return self._instrument

    def order_book_id(self):
        """
        [str] 交易标的代码
        """
        return self._instrument.order_book_id

    def symbol(self):
        """
        [str] 合约简称
        """
        return self._instrument.symbol

    def is_trading(self):
        """
        [bool] 是否有成交量
        """
        return self._df['volume'] > 0


    def isnan(self):
        return np.isnan(self._df['close'])

    def suspended(self):
        if self.isnan:
            return True

        return self._instrument.order_book_id

    def mavg(self, intervals, frequency='1d'):
        if frequency == 'day':
            frequency = '1d'
        if frequency == 'minute':
            frequency = '1m'

        # copy form history
        env = None
        dt = env.calendar_dt

        if (env.config.base.frequency == '1m' and frequency == '1d'):
            # 在分钟回测获取日线数据, 应该推前一天
            dt = env.df_proxy.get_previous_trading_date(env.calendar_dt.date())
        bars = env.df_proxy.fast_history(self._instrument.order_book_id, intervals, frequency, 'close', dt)
        return bars.mean()

    def vwap(self, intervals, frequency='1d'):
        if frequency == 'day':
            frequency = '1d'
        if frequency == 'minute':
            frequency = '1m'

        # copy form history
        env = None
        dt = env.calendar_dt

        if (env.config.base.frequency == '1m' and frequency == '1d'):
            # 在分钟回测获取日线数据, 应该推前一天
            dt = env.df_proxy.get_previous_trading_date(env.calendar_dt.date())
        bars = env.df_proxy.fast_history(self._instrument.order_book_id, intervals, frequency, ['close', 'volume'], dt)
        sum = bars['volume'].sum()
        if sum == 0:
            # 全部停牌
            return 0

        return np.dot(bars['close'], bars['volume']) / sum

    def __repr__(self):
        base = [
            ('symbol', repr(self._instrument.symbol)),
            ('order_book_id', repr(self._instrument.order_book_id)),
            ('datetime', repr(self.datetime)),
        ]

        if self.isnan:
            base.append(('error', repr('df UNAVAILABLE')))
            return 'Bar({0})'.format(', '.join('{0}: {1}'.format(k, v) for k, v in base) + ' NaN BAR')

        if isinstance(self._df, dict):
            # in pt
            base.extend((k, v) for k, v in self._df if k != 'datetime')
        else:
            base.extend((n, self._df[n]) for n in self._df.dtype.names if n != 'datetime')
        return "Bar({0})".format(', '.join('{0}: {1}'.format(k, v) for k, v in base))

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, item):
        try:
            return self._df[item]
        except KeyError:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, item))



