from ask_amy.tests.utility import TestCaseASKAmy
from ask_amy.utilities.time_of_day import TimeOfDay
from unittest.mock import MagicMock
from unittest import mock

from datetime import datetime, date

class DatetimeWrapper(datetime):
    "A wrapper for datetime that can be mocked for testing."

    def __new__(cls, *args, **kwargs):
        return datetime.__new__(datetime, *args, **kwargs)

# @mock.patch('datetime.datetime', FakeDatetime)
# datetime.now = MagicMock(return_value=datetime.now())
# from datetime import datetime
# FakeDatetime.now = classmethod(lambda cls: datetime(2017, 7, 4, 12, 00, 00))

class TestTimeOfDay(TestCaseASKAmy):
    def setUp(self):
        pass

    def test_day_night(self):
        base_time = datetime(2017, 7, 4, 8, 00, 00)
        back_two_hr = TimeOfDay.current_time(-2, base_time)
        forward_one_hr = TimeOfDay.current_time(1, base_time)
        self.assertEquals('06:00 AM',back_two_hr)
        self.assertEquals('09:00 AM',forward_one_hr)
        print(back_two_hr)
        print(forward_one_hr)

    def test_mealtime(self):
        time_desc=['Breakfast', 'Lunch', 'Dinner', 'Daytime', 'Nighttime']
        base_time = datetime(2017, 7, 4, 12, 22, 00)
        time_adj = TimeOfDay.time_adj("05:22","AM",base_time)
        tod = TimeOfDay.meal_time(time_adj,base_time)
        self.assertEquals(TimeOfDay.Breakfast,tod)

        time_adj = TimeOfDay.time_adj("12:22","PM",base_time)
        tod = TimeOfDay.meal_time(time_adj,base_time)
        self.assertEquals(TimeOfDay.Lunch,tod)

        time_adj = TimeOfDay.time_adj("05:22","PM",base_time)
        tod = TimeOfDay.meal_time(time_adj,base_time)
        self.assertEquals(TimeOfDay.Dinner,tod)
        print("adj={} time_desc={}".format(time_adj,time_desc[tod]))



    def test_day_night(self):
        time_desc=['Breakfast', 'Lunch', 'Dinner', 'Daytime', 'Nighttime']
        base_time = datetime(2017, 7, 4, 12, 22, 00)
        time_adj = TimeOfDay.time_adj("04:22","AM",base_time)
        tod = TimeOfDay.day_night(time_adj,base_time)
        # print("adj={} time_desc={}".format(time_adj,time_desc[tod]))
        self.assertEquals(TimeOfDay.Nighttime,tod)

        time_adj = TimeOfDay.time_adj("06:22","AM",base_time)
        tod = TimeOfDay.day_night(time_adj,base_time)
        self.assertEquals(TimeOfDay.Daytime,tod)

        time_adj = TimeOfDay.time_adj("08:22","PM",base_time)
        tod = TimeOfDay.day_night(time_adj,base_time)
        self.assertEquals(TimeOfDay.Nighttime,tod)

        # print("adj={} time_desc={}".format(time_adj,time_desc[tod]))


    def test_time_adj(self):
        lunch = datetime(2017, 7, 4, 12, 22, 00)
        time_adj = TimeOfDay.time_adj("11:22","AM",lunch)
        self.assertEquals(1,time_adj)
        time_adj = TimeOfDay.time_adj("01:22","PM",lunch)
        self.assertEquals(-1,time_adj)
