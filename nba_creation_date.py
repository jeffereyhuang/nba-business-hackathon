import datetime

# NBA_Date class with relevant functions
class CreationDate:
    def __init__(self, dt):
        self.dt = dt
        self.date = dt.date()
        self.time = dt.time()

    def get_date(self):
        return self.date

    def get_time(self):
        return self.time

    def get_month(self):
        return self.date.strftime("%B")

    def get_month_int(self):
        return self.date.month

    def get_year(self):
        return self.date.year

    def get_weekday(self):
        return self.date.strftime("%A")

    def get_day_section(self):
        if self.time >= datetime.time(1, 0, 0) and self.time < datetime.time(7, 0, 0):
            return "deadzone"
        elif self.time >= datetime.time(7, 0, 0) and self.time < datetime.time(
            11, 0, 0
        ):
            return "morning"
        elif self.time >= datetime.time(11, 0, 0) and self.time < datetime.time(
            13, 0, 0
        ):
            return "lunch"
        elif self.time >= datetime.time(13, 0, 0) and self.time < datetime.time(
            17, 0, 0
        ):
            return "afternoon"
        elif self.time >= datetime.time(17, 0, 0) and self.time < datetime.time(
            21, 0, 0
        ):
            return "evening"
        elif self.time >= datetime.time(21, 0, 0) and self.time < datetime.time(
            23, 30, 0
        ):
            return "night"
        else:
            return "postgame"

    def is_playoffs(self):
        return (
            (self.date.month == 5)
            or (self.date.month == 4 and self.date.day >= 10)
            or (self.date.month == 6 and self.date.day <= 15)
        )


# Functions to convert string into datetime object
def strip_timezone(datetime_str):
    return datetime_str[:-4]


def get_datetime(datetime_str_no_tz):
    return datetime.datetime.strptime(datetime_str_no_tz, "%Y-%m-%d %H:%M:%S")


def date_string_to_datetime(datetime_str, has_timezone=True):
    if has_timezone:
        return get_datetime(strip_timezone(datetime_str))
    else:
        get_datetime(datetime_str)
