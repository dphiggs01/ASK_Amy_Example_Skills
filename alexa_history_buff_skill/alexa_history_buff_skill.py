from ask_amy.state_mgr.stack_dialog_mgr import StackDialogManager
from ask_amy.state_mgr.stack_dialog_mgr import required_fields
from ask_amy.core.reply import Reply
import urllib.request
from urllib.error import URLError
import logging
import datetime
import json
import re

logger = logging.getLogger()

class AlexaHistoryBuffSkill(StackDialogManager):

    @required_fields(['day'])
    def get_first_event_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))

        date_str = self.request.attributes['day']
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            month = date.strftime('%B')
            day = str(date.day)
            history_buff = HistoryBuff()
            events = history_buff.get_history_for_date(month, day)
            if len(events) >= 3:
                self.request.attributes['event_1'] = events.pop()
                self.request.attributes['event_2'] = events.pop()
                self.request.attributes['event_3'] = events.pop()
                self.session.attributes['month'] = month
                self.session.attributes['day_nbr'] = day
                self.session.attributes['events'] = events
                condition = 'have_events'
            else:
                condition = 'no_events'

        except ValueError:
            condition = 'bad_date'

        reply_dialog = self.reply_dialog[self.intent_name]['conditions'][condition]
        return Reply.build(reply_dialog, self.event)


    def get_next_event_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))

        if not self.session.attribute_exists('events'):
            condition = 'no_events'
        else:
            events = self.session.attributes['events']
            if len(events) >= 3:
                self.request.attributes['event_1'] = events.pop()
                self.request.attributes['event_2'] = events.pop()
                self.request.attributes['event_3'] = events.pop()
                condition = 'have_events'
            else:
                condition = 'no_more_events'

        reply_dialog = self.reply_dialog[self.intent_name]['conditions'][condition]
        return Reply.build(reply_dialog, self.event)


class HistoryBuff(object):
    URI_PATH = "https://en.wikipedia.org/w/api.php"
    QUERY_PARAMS = "action=query&prop=extracts&format=json&" \
                   "explaintext=&exsectionformat=plain&redirects=&titles="

    def get_history_for_date(self,month, day):
        query_params = "{}{}_{}".format(HistoryBuff.QUERY_PARAMS, month, day)
        json = self._http_call(HistoryBuff.URI_PATH,query_params)
        return self._parse_event_str(str(json))

    def _http_call(self, uri_path, query_params=None, ret_json=True):
        url = uri_path
        if query_params is not None:
              url += "?" + query_params
        try:
            print(url)
            request_url = urllib.request.Request(url)
            with urllib.request.urlopen(request_url) as response:
                data = response.read()
                encoding = response.info().get_content_charset('utf-8')
                ret_val = data.decode(encoding)
                if ret_json:
                    ret_val = json.loads(ret_val)
        except URLError as e:
            ret_val = {}
            if hasattr(e, 'reason'):
                logger.critical('We failed to reach a server.')
                logger.critical('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                logger.critical('The server couldn\'t fulfill the request.')
                logger.critical('Error code: ', e.code)
        return ret_val

    def _parse_event_str(self, events_str):
        events = []
        try:
            events_str = events_str[
                         events_str.index("\\nEvents\\n") + 10 :
                         events_str.index("\\n\\n\\nBirths")]
            start_index = 0
            print(events_str.count('\\n'))
            num_events = events_str.count('\\n')
            for e in range(num_events):
                if e < num_events:
                    end_index = events_str.index('\\n', start_index + 2)
                    event_text = events_str[start_index:end_index]
                    start_index = end_index + 2
                else:
                    event_text = events_str[start_index:]

                # replace dashes returned in events_str from Wikipedia's API
                event_text = event_text.replace('\u2013', '')
                event_text = event_text.replace('\u005c', '')
                # add comma after year so Alexa pauses before continuing with the sentence
                event_text = re.sub('^\d+', r'\g<0>,', event_text)
                events.append(event_text)
        except ValueError:
                logger.callHandlers('Error while parsing Wikapedia results')
                events = []

        return events
