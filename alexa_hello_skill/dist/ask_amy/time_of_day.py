from datetime import datetime, timedelta
import re
import logging

logger = logging.getLogger()


class TimeOfDay(object):
    Breakfast, Lunch, Dinner, Daytime, Nighttime = range(5)

    @staticmethod
    def current_time(time_adj):
        if time_adj is None:
            return None
        now = datetime.now() - timedelta(hours=int(time_adj))
        return now.strftime('%I:%M %p')

    @staticmethod
    def meal_time(time_adj):
        if time_adj is None:
            return None
        now = datetime.now() - timedelta(hours=int(time_adj))
        # now = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
        today1130 = now.replace(hour=11, minute=30, second=0, microsecond=0)
        today430 = now.replace(hour=12 + 4, minute=30, second=0, microsecond=0)
        if now < today1130:
            return TimeOfDay.Breakfast
        elif today1130 < now < today430:
            return TimeOfDay.Lunch
        else:
            return TimeOfDay.Dinner

    @staticmethod
    def day_night(time_adj):
        if time_adj is None:
            return None
        now = datetime.now() - timedelta(hours=int(time_adj))
        # now = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
        # logger.debug("********** day_night ************[{}]************".format(now))
        today5am = now.replace(hour=5, minute=0, second=0, microsecond=0)
        today8pm = now.replace(hour=12 + 8, minute=0, second=0, microsecond=0)
        logger.debug("today5am={}".format(today5am))
        logger.debug("today8pm={}".format(today8pm))
        logger.debug("now={}".format(now))
        if today5am < now < today8pm:
            return TimeOfDay.Daytime
        else:
            return TimeOfDay.Nighttime

    @staticmethod
    def time_adj(time_str, time_am_pm):
        logger.debug("**************** entering TimeOfDay.time_adj")
        if time_str is None:
            return None
        if time_am_pm is None:
            return None
        if time_am_pm.lower() == "pm":
            am_pm_shift = 12
        else:
            am_pm_shift = 0
        time_difference_in_hours = None
        pattern = re.compile("^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")
        if pattern.match(time_str):
            hours, minutes = time_str.split(':')
            server_time = datetime.now()
            users_time = server_time.replace(hour=int(hours)+am_pm_shift, minute=int(minutes), second=0, microsecond=0)
            time_difference = server_time - users_time
            time_difference_in_hours = int(round(time_difference / timedelta(minutes=60), 0))
            logger.debug("Time on Server [{}] User stated time [{}] difference {}".format(server_time, time_str,
                                                                                          time_difference_in_hours))
        return time_difference_in_hours
