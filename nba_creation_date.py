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
    def season_yr(self):
        if (self.date > datetime.date(2017, 10, 17) and self.date < datetime.date(2018, 6, 8)):
          return "2018"
        elif (self.date > datetime.date(2018, 10, 16) and self.date < datetime.date(2019, 6, 13)):
          return "2019"
        else:
          return ""
    def is_season(self):
        if self.season_yr:
          return True
        return False
    def is_playoffs(self):
      if not is_season:
        return False
      if self.season_yr == "2018":
        return (
            (self.date.month == 5)
            or (self.date.month == 4 and self.date.day >= 14)
            or (self.date.month == 6 and self.date.day <= 8)
        )
      elif self.season_yr == "2019":
        return (
            (self.date.month == 5)
            or (self.date.month == 4 and self.date.day >= 13)
            or (self.date.month == 6 and self.date.day <= 13)
        )

    def is_finals(self):
      if not is_playoffs:
        return False
      if self.season_yr == "2018":
        return (
          (self.date.month == 5 and self.date.day >= 31) and (self.date.month == 6 and self.date.day <= 8)
        )
      elif self.season_yr == "2019":
        return (
          (self.date.month == 5 and self.date.day >= 30) and (self.date.month == 6 and self.date.day <= 13)
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
