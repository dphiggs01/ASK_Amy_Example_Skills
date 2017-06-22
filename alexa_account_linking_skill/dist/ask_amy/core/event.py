import logging

from ask_amy.core.session import Session
from ask_amy.core.request import Request, IntentRequest


logger = logging.getLogger()


class Event(object):
    def __init__(self, event_dict):
        self._request = Request.factory(event_dict['request'])
        self._session = Session(event_dict['session'])

    def session(self):
        return self._session

    def request(self):
        return self._request

    def get_user_id(self):
        return self._session.user_id()

    def is_new_session(self):
        return self._session.is_new_session()

    def get_request_type(self):
        return self._request.request_type()

    def get_intent_name(self):
        return self._request.intent_name()

    def value_for_slot_name(self, slot_name):
        return self._request.value_for_slot_name(slot_name)

    def get_session_attributes(self):
        return self._session.attributes()

    def get_value_in_session(self, path):
        return self._session.get_attribute(path)

    def set_value_in_session(self, name, value):
        return self._session.put_attribute(name, value)

    def slot_data_to_session_attributes(self):
        logger.debug("**************** entering Event.slot_data_to_session_attributes")
        # If we have an Intent Request map the slot values to the session
        if isinstance(self._request, IntentRequest):
            slots_dict = self._request.slots()
            for name in slots_dict.keys():
                # get the value for this name if available
                value = self.value_for_slot_name(name)
                if value is not None:
                    # Is this is a 'requested_value' and do we have a field to map to?
                    if name == 'requested_value':
                        requested_value_nm = self.get_value_in_session(['requested_value_nm'])
                        if requested_value_nm is not None:
                            self.set_value_in_session(requested_value_nm, value)
                        else:
                            self.set_value_in_session(name, value)
                    else:
                        self.set_value_in_session(name, value)

    def __str__(self):
        output = 'Event[\n\tsession = {}\n\trequest = {}\n]'.format(
            self._session,
            self._request)
        return output
