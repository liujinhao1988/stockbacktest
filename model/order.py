#order为每次交易所下单的订单
import time
from decimal import Decimal

import numpy as np


class Order:

   

    def __init__(self):
        self._order_id = None
        self._secondary_order_id = None
        self._calendar_dt = None
        self._trading_dt = None
        self._quantity = None
        self._order_book_id = None
        self._side = None
        self._position_effect = None
        self._message = None
        self._filled_quantity = None
        self._status = None
        self._frozen_price = None
        self._type = None
        self._avg_price = None
        self._transaction_cost = None

 

    def get_state(self):
        return {
            'order_id': self._order_id,
            'secondary_order_id': self._secondary_order_id,
            'calendar_dt': self._calendar_dt,
            'trading_dt': self._trading_dt,
            'order_book_id': self._order_book_id,
            'quantity': self._quantity,
            'side': self._side,
            'position_effect': self._position_effect,
            'message': self._message,
            'filled_quantity': self._filled_quantity,
            'status': self._status,
            'frozen_price': self._frozen_price,
            'type': self._type,
            'transaction_cost': self._transaction_cost,
            'avg_price': self._avg_price,
        }

    def set_state(self, d):
        self._order_id = d['order_id']
        if 'secondary_order_id' in d:
            self._secondary_order_id = d['secondary_order_id']
        self._calendar_dt = d['calendar_dt']
        self._trading_dt = d['trading_dt']
        self._order_book_id = d['order_book_id']
        self._quantity = d['quantity']
        self._side = d["side"]
        self._position_effect = d["position_effect"] if d["position_effect"] else None
        self._message = d['message']
        self._filled_quantity = d['filled_quantity']
        self._status = d["order_status"]
        self._frozen_price = d['frozen_price']
        self._type = d["type"]
        self._transaction_cost = d['transaction_cost']
        self._avg_price = d['avg_price']


    def __from_create__(cls, order_book_id, quantity, side, style, position_effect):
        env = None
        order = cls()
        order._order_id = next(order.order_id_gen)
        order._calendar_dt = env.calendar_dt
        order._trading_dt = env.trading_dt
        order._quantity = quantity
        order._order_book_id = order_book_id
        order._side = side
        order._position_effect = position_effect
        order._message = ""
        order._filled_quantity = 0
        order._status = None
        if isinstance(style):
            if env.config.base.round_price:
                tick_size = env.data_proxy.get_tick_size(order_book_id)
                style.round_price(tick_size)
            order._frozen_price = style.get_limit_price()
            order._type = None
        else:
            order._frozen_price = 0.
            order._type = None
        order._avg_price = 0
        order._transaction_cost = 0
        return order

    def order_id(self):
        """
        [int] 唯一标识订单的id
        """
        return self._order_id

    def secondary_order_id(self):
        """
        [str] 实盘交易中交易所产生的订单ID
        """
        return self._secondary_order_id

    def trading_datetime(self):
        """
        [datetime.datetime] 订单的交易日期（对应期货夜盘）
        """
        return self._trading_dt


    def datetime(self):
        """
        [datetime.datetime] 订单创建时间
        """
        return self._calendar_dt

 
    def quantity(self):
        """
        [int] 订单数量
        """
  
        return self._quantity

  
    def unfilled_quantity(self):
        """
        [int] 订单未成交数量
        """
        return self.quantity - self.filled_quantity


    def order_book_id(self):
        """
        [str] 合约代码
        """
        return self._order_book_id


    def side(self):
        """
        [SIDE] 订单方向
        """
        return self._side


    def position_effect(self):
        """
        [POSITION_EFFECT] 订单开平（期货专用）
        """
 
        return self._position_effect


    def position_direction(self):
        # type: () -> POSITION_DIRECTION
        return self._side, self._position_effect


    def message(self):
        """
        [str] 信息。比如拒单时候此处会提示拒单原因
        """
        return self._message

   
    def filled_quantity(self):
        """
        [int] 订单已成交数量
        """
  
        return self._filled_quantity

 
    def status(self):
        """
        [ORDER_STATUS] 订单状态
        """
        return self._status

   
    def price(self):
        """
        [float] 订单价格，只有在订单类型为'限价单'的时候才有意义
        """
        return  self.frozen_price

  
    def type(self):
        """
        [ORDER_TYPE] 订单类型
        """
        return self._type


    def avg_price(self):
        """
        [float] 成交均价
        """
        return self._avg_price

 
    def transaction_cost(self):
        """
        [float] 费用
        """
        return self._transaction_cost


    def frozen_price(self):
        """
        [float] 冻结价格
        """
       
        return self._frozen_price



    def is_active(self):
        return self.status 

    def active(self):
        self._status 

    def set_pending_cancel(self):
        if not self.is_final():
            self._status

    def fill(self, trade):
        quantity = trade.last_quantity
        assert self.filled_quantity + quantity <= self.quantity
        new_quantity = self._filled_quantity + quantity
        self._transaction_cost += trade.commission + trade.tax
        self._filled_quantity = new_quantity


    def mark_rejected(self, reject_reason):
        if not self.is_final():
            self._message = reject_reason



    def mark_cancelled(self, cancelled_reason, user_warn=True):
        if not self.is_final():
            self._message = cancelled_reason



    def set_frozen_price(self, value):
        self._frozen_price = value

    def set_secondary_order_id(self, secondary_order_id):
        self._secondary_order_id = str(secondary_order_id)




