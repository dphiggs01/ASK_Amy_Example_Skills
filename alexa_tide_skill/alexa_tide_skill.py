import urllib.request
from urllib.error import URLError
from urllib.parse import urlencode
import logging
import datetime
import json

from ask_amy.state_mgr.stack_dialog_mgr import StackDialogManager
from ask_amy.state_mgr.stack_dialog_mgr import required_fields
from ask_amy.core.reply import Reply

logger = logging.getLogger()


class AlexaTideSkill(StackDialogManager):
    def launch_request(self):
        logger.debug("**************** entering {}.launch_request".format(self.__class__.__name__))
        # Recall that a LaunchRequest is not == to an IntentRequest and does not have an intent_name
        # If we want to simulate the same behavior we need to add our own intent name
        self._intent_name = 'launch_request'
        return self.handle_default_intent()

    def supported_cities_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        self.session.attributes['coastal_cities'] = TideInfo.valid_cities()
        return self.handle_default_intent()

    @required_fields(['City', 'Date'])
    def dialog_tide_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))

        # required_fields decorator will redirect us if we do not have all the needed fields
        tides = TideInfo.tide_http_call(
            self.request.attributes['City'],
            self.request.attributes['Date']
        )
        condition = 'failed_to_find_tides'
        if tides is not None:
            for key in tides.keys():
                self.session.attributes[key] = tides[key]
                condition = 'found_tides'

        reply_dialog = self.reply_dialog[self.intent_name]['conditions'][condition]
        return Reply.build(reply_dialog, self.event)

    def oneshot_tide_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))

        # With ask_amy we really do not need two intents as the DialogTideIntent will do the same thing
        # if it has all the required fields. This is maintained to keep compatibility with the sample
        # intent_schema.json provided by Java sample apps
        return self.redirect_to_initialize_dialog('dialog_tide_intent')


class TideInfo(object):
    URI_PATH = "http://tidesandcurrents.noaa.gov/api/datagetter"

    LOCATIONS = {"seattle": "9447130", "san francisco": "9414290", "monterey": "9413450", "los angeles": "9410660",
                 "san diego": "9410170", "boston": "8443970", "new york": "8518750", "virginia beach": "8638863",
                 "wilmington": "8658163", "charleston": "8665530", "beaufort": "8656483", "myrtle beach": "8661070",
                 "miami": "8723214", "tampa": "8726667", "new orleans": "8761927", "galveston": "8771341"}

    @staticmethod
    def valid_cities():
        locations = ''
        for key in TideInfo.LOCATIONS.keys():
            locations += key + ', '
        return locations

    @staticmethod
    def tide_http_call(city, date_str):
        tide_info = None
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        station = TideInfo.LOCATIONS.get(city.lower())
        query_params = {'station': station, 'product': 'predictions', 'datum': 'MLLW', 'units': 'english',
                        'time_zone': 'lst_ldt', 'format': 'json'
                        }

        if date == datetime.date.today():
            query_params['date'] = 'today'
        else:
            query_params['begin_date'] = date.strftime('%Y%m%d')
            query_params['range'] = 24

        response_obj = TideInfo._http_call(TideInfo.URI_PATH, query_params)
        if response_obj is not None:
            if 'predictions' in response_obj:
                predictions = response_obj['predictions']
                tide_info = TideInfo._high_low(predictions)
        # print(tide_info)
        return tide_info

    @staticmethod
    def _high_low(predictions):
        ret_val = {}
        tides = {}
        for e in predictions:
            tides[e['t']] = float(e['v'])

        found_first_low_tide = False
        found_first_high_tide = False
        found_second_low_tide = False
        found_second_high_tide = False
        times = sorted(tides)
        for t in range(0, len(times) - 1):
            tide1 = tides[times[t]]
            tide2 = tides[times[t + 1]]

            if not found_first_low_tide and tide2 > tide1:
                t_am_pm = datetime.datetime.strptime(times[t][11:], "%H:%M")
                ret_val['first_low_tide_time'] = t_am_pm.strftime("%I:%M %p")
                ret_val['first_low_tide_height'] = round(float(tide1), 1)
                found_first_low_tide = True
            if found_first_low_tide and not found_first_high_tide and tide2 < tide1:
                t_am_pm = datetime.datetime.strptime(times[t][11:], "%H:%M")
                ret_val['first_high_tide_time'] = t_am_pm.strftime("%I:%M %p")
                ret_val['first_high_tide_height'] = round(float(tide1), 1)
                found_first_high_tide = True

            if found_first_high_tide and not found_second_low_tide and tide2 > tide1:
                t_am_pm = datetime.datetime.strptime(times[t][11:], "%H:%M")
                ret_val['second_low_tide_time'] = t_am_pm.strftime("%I:%M %p")
                ret_val['second_low_tide_height'] = round(float(tide1), 1)
                found_second_low_tide = True
            if found_second_low_tide and not found_second_high_tide and tide2 < tide1:
                t_am_pm = datetime.datetime.strptime(times[t][11:], "%H:%M")
                ret_val['second_high_tide_time'] = t_am_pm.strftime("%I:%M %p")
                ret_val['second_high_tide_height'] = round(float(tide1), 1)
                found_second_high_tide = True

        return ret_val

    @staticmethod
    def _http_call(uri_path, query_params=None, ret_json=True):
        url = uri_path
        if query_params is not None:
            url += "?" + urlencode(query_params)

        try:
            request_url = urllib.request.Request(url)
            with urllib.request.urlopen(request_url) as response:
                data = response.read()
                encoding = response.info().get_content_charset('utf-8')
                ret_val = data.decode(encoding)
                if ret_json:
                    ret_val = json.loads(ret_val)
        except URLError as e:
            ret_val = None
            if hasattr(e, 'reason'):
                logger.critical('We failed to reach a server.')
                logger.critical('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                logger.critical('The server couldn\'t fulfill the request.')
                logger.critical('Error code: ', e.code)
        return ret_val

