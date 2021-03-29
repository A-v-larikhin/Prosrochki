import numpy as np
from read_files import holidays


def srok_postavki_fact(postavka_date, svodnay_date):
    maskcal = np.busdaycalendar(holidays=holidays)

    diff_days = np.busday_count(svodnay_date, postavka_date, busdaycal=maskcal)
    return diff_days