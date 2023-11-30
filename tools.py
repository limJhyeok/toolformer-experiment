def Calendar():
    import datetime
    from calendar import day_name, month_name
    now = datetime.datetime.now()
    return f'Today is {day_name[now.weekday()]}, {month_name[now.month]} {now.day}, {now.year}.'