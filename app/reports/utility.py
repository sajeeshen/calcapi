from datetime import datetime


def get_current_month():
    now = datetime.now()
    return now.month


def get_current_year():
    now = datetime.now()
    return now.year
