VALID_HISTORY_FIELDS = [
    "datetime",
    "open",
    "close",
    "high",
    "low",
    "total_turnover",
    "volume",
    "acc_net_value",
    "discount_rate",
    "unit_net_value",
    "limit_up",
    "limit_down",
    "open_interest",
    "basis_spread",
    "settlement",
    "prev_settlement",
]

VALID_TENORS = [
    "0S",
    "1M",
    "2M",
    "3M",
    "6M",
    "9M",
    "1Y",
    "2Y",
    "3Y",
    "4Y",
    "5Y",
    "6Y",
    "7Y",
    "8Y",
    "9Y",
    "10Y",
    "15Y",
    "20Y",
    "30Y",
    "40Y",
    "50Y",
]

VALID_INSTRUMENT_TYPES = [
    "CS",
    "Future",
    "INDX",
    "ETF",
    "LOF",
    "SF",
    "FenjiA",
    "FenjiB",
    "FenjiMu",
    "Stock",
    "Fund",
    "Index",
]

VALID_XUEQIU_FIELDS = [
    "new_comments",
    "total_comments",
    "new_followers",
    "total_followers",
    "sell_actions",
    "buy_actions",
]

VALID_MARGIN_FIELDS = [
    "margin_balance",
    "buy_on_margin_value",
    "short_sell_quantity",
    "margin_repayment",
    "short_balance_quantity",
    "short_repayment_quantity",
    "short_balance",
    "total_balance",
]

VALID_SHARE_FIELDS = [
    "total",
    "circulation_a",
    "management_circulation",
    "non_circulation_a",
    "total_a",
]

VALID_TURNOVER_FIELDS = (
    "today",
    "week",
    "month",
    "three_month",
    "six_month",
    "year",
    "current_year",
    "total",
)


VALID_STOCK_CONNECT_FIELDS = [
    'shares_holding',
    'holding_ratio',
]


VALID_CURRENT_PERFORMANCE_FIELDS = [
    'operating_revenue',
    'gross_profit',
    'operating_profit',
    'total_profit',
    'np_parent_owners',
    'net_profit_cut',
    'net_operate_cashflow',
    'total_assets',
    'se_without_minority',
    'total_shares',
    'basic_eps',
    'eps_weighted',
    'eps_cut_epscut',
    'eps_cut_weighted',
    'roe',
    'roe_weighted',
    'roe_cut',
    'roe_cut_weighted',
    'net_operate_cashflow_per_share',
    'equity_per_share',
    'operating_revenue_yoy',
    'gross_profit_yoy',
    'operating_profit_yoy',
    'total_profit_yoy',
    'np_parent_minority_pany_yoy',
    'ne_t_minority_ty_yoy',
    'net_operate_cash_flow_yoy',
    'total_assets_to_opening',
    'se_without_minority_to_opening',
    'basic_eps_yoy',
    'eps_weighted_yoy',
    'eps_cut_yoy',
    'eps_cut_weighted_yoy',
    'roe_yoy',
    'roe_weighted_yoy',
    'roe_cut_yoy',
    'roe_cut_weighted_yoy',
    'net_operate_cash_flow_per_share_yoy',
    'net_asset_psto_opening',
]

