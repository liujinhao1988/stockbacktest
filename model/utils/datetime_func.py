#修改时间格式



import datetime
def convert_date_to_date_int(dt):
    t = dt.year * 10000 + dt.month * 100 + dt.day
    return t


def convert_date_to_int(dt):
    t = dt.year * 10000 + dt.month * 100 + dt.day
    t *= 1000000
    return t


def convert_dt_to_int(dt):
    t = convert_date_to_int(dt)
    t += dt.hour * 10000 + dt.minute * 100 + dt.second
    return t


def convert_int_to_date(dt_int):
    dt_int = int(dt_int)
    if dt_int > 100000000:
        dt_int //= 1000000
    return _convert_int_to_date(dt_int)


def _convert_int_to_date(dt_int):
    year, r = divmod(dt_int, 10000)
    month, day = divmod(r, 100)
    return datetime.datetime(year, month, day)



def convert_int_to_datetime(dt_int):
    dt_int = int(dt_int)
    year, r = divmod(dt_int, 10000000000)
    month, r = divmod(r, 100000000)
    day, r = divmod(r, 1000000)
    hour, r = divmod(r, 10000)
    minute, second = divmod(r, 100)
    return datetime.datetime(year, month, day, hour, minute, second)


def convert_ms_int_to_datetime(ms_dt_int):
    dt_int, ms_int = divmod(ms_dt_int, 1000)
    dt = convert_int_to_datetime(dt_int).replace(microsecond=ms_int * 1000)
    return dt


def convert_date_time_ms_int_to_datetime(date_int, time_int):
    date_int, time_int = int(date_int), int(time_int)
    dt = _convert_int_to_date(date_int)

    hours, r = divmod(time_int, 10000000)
    minutes, r = divmod(r, 100000)
    seconds, millisecond = divmod(r, 1000)

    return dt.replace(hour=hours, minute=minutes, second=seconds,
                      microsecond=millisecond * 1000)



