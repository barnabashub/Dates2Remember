from datetime import datetime, timedelta

class DatesHark:
    @staticmethod
    def is_jubilee(date1, date2):
        dt1 = datetime.strptime(date1, "%Y-%m-%d")
        if isinstance(date2, str):
            dt2 = datetime.strptime(date2, "%Y-%m-%d")
        else:
            dt2 = date2
        return dt1.month == dt2.month and dt1.day == dt2.day

    @staticmethod
    def is_month_jubilee(date1, date2):
        dt1 = datetime.strptime(date1, "%Y-%m-%d")
        if isinstance(date2, str):
            dt2 = datetime.strptime(date2, "%Y-%m-%d")
        else:
            dt2 = date2
        return dt1.day == dt2.day

    @staticmethod
    def is_divisible_by_100_or_250(date1, date2):
        dt1 = datetime.strptime(date1, "%Y-%m-%d")
        if isinstance(date2, str):
            dt2 = datetime.strptime(date2, "%Y-%m-%d")
        else:
            dt2 = date2
        delta = abs((dt2 - dt1).days)
        return delta % 100 == 0 or delta % 250 == 0

    @staticmethod
    def any_jubilee(date1, date2):
        if DatesHark.is_jubilee(date1, date2):
            return True
        elif DatesHark.is_month_jubilee(date1, date2):
            return True
        elif DatesHark.is_divisible_by_100_or_250(date1, date2):
            return True
        else:
            return False
        
    @staticmethod
    def get_next_dates(date, quantity):
        found_dates = []
        original_date = date
        while len(found_dates) < quantity:
            dateobj = datetime.strptime(date, "%Y-%m-%d")
            dateobj += timedelta(days=1)
            date = f"{dateobj.year}-{dateobj.month}-{dateobj.day}"
            if DatesHark.any_jubilee(date, original_date):
                found_dates.append(date)
        print(found_dates)
        return found_dates

    @staticmethod
    def get_howold_indays(date1, date2):
        dt1 = datetime.strptime(date1["date"], "%Y-%m-%d")
        dt2 = date2
        delta = abs((dt2 - dt1).days)
        return delta

    @staticmethod
    def get_howold_inmonths(date1, date2):
        dt1 = datetime.strptime(date1["date"], "%Y-%m-%d")
        dt2 = date2
        return (dt2.year - dt1.year) * 12 + dt2.month - dt1.month
    
    @staticmethod
    def when_will_day_basedon_day(date, days):
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")
        date += timedelta(days=int(days))
        return date.strftime("%Y-%m-%d")
