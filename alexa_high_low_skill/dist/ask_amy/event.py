from ask_amy.session import Session
from ask_amy.request import Request
import logging

logger = logging.getLogger()


class Event(object):
    def __init__(self, event_dict):
        self._request = Request.factory(event_dict['request'])
        self._session = Session(event_dict['session'])

    def session(self):
        return self._session

    def request(self):
        return self._request

    # todo candidate for removal
    def get_user_id(self):
        return self._session.user_id()

    def is_new_session(self):
        return self._session.is_new_session()

    def get_request_type(self):
        return self._request.request_type()

    def get_intent_name(self):
        return self._request.intent_name()

    # todo candidate for removal
    def get_timestamp(self, set_session=True):
        timestamp = self._request.timestamp()
        if set_session:
            self.set_value_in_session('timestamp', timestamp)
        return timestamp

    def value_for_slot_name(self, slot_name):
        return self._request.value_for_slot_name(slot_name)

    def get_session_attributes(self):
        return self._session.attributes()

    def get_value_in_session(self, path):
        return self._session.get_attribute(path)

    def set_value_in_session(self, name, value):
        return self._session.put_attribute(name, value)

    def __str__(self):
        output = 'Event[\n\tsession = {}\n\trequest = {}\n]'.format(
            self._session,
            self._request)
        return output
