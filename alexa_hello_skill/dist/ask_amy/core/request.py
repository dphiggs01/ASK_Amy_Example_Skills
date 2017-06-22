import logging

from ask_amy.core.object_dictionary import ObjectDictionary

logger = logging.getLogger()


class Request(ObjectDictionary):
    def __init__(self, request_dict):
        super().__init__(request_dict)
        self.logger.debug("Request __init__")

    def request_type(self):
        return self.get_value_from_dict(['type'])

    def request_id(self):
        return self.get_value_from_dict(['requestId'])

    def locale(self):
        return self.get_value_from_dict(['locale'])

    def timestamp(self):
        return self.get_value_from_dict(['timestamp'])

    @staticmethod
    def factory(request_dict):
        logger.debug("**************** entering Request.factory")
        request_type = request_dict['type']
        if request_type == "LaunchRequest": return LaunchRequest(request_dict)
        if request_type == "IntentRequest": return IntentRequest(request_dict)
        if request_type == "SessionEndedRequest": return SessionEndedRequest(request_dict)
        assert 0, "Bad Request creation: " + request_type


class LaunchRequest(Request):
    def __init__(self, request_dict):
        super().__init__(request_dict)
        self.logger.debug("LaunchRequest __init__")


class IntentRequest(Request):
    CONFIRMATION_STATUSES = ['NONE', 'CONFIRMED', 'DENIED']
    DIALOG_STATES = ['STARTED', 'IN_PROGRESS', 'COMPLETED']

    def __init__(self, request_dict):
        super().__init__(request_dict)
        self.logger.debug("IntentRequest __init__")

    def dialog_state(self):
        return self.get_value_from_dict(['dialogState'])

    def intent_name(self):
        return self.get_value_from_dict(['intent', 'name'])

    def confirmation_status(self):
        return self.get_value_from_dict(['intent', 'confirmationStatus'])

    def slots(self):
        return self.get_value_from_dict(['intent', 'slots'])

    def value_for_slot_name(self, name):
        path = ['intent', 'slots', name, 'value']
        return self.get_value_from_dict(path)


class SessionEndedRequest(Request):
    REASONS = ['USER_INITIATED', 'ERROR', 'EXCEEDED_MAX_REPROMPTS']
    ERROR_TYPES = ['INVALID_RESPONSE', 'DEVICE_COMMUNICATION_ERROR', 'INTERNAL_ERROR']

    def __init__(self, request_dict):
        super().__init__(request_dict)
        self.logger.debug("SessionEndedRequest __init__")

    def reason(self):
        return self.get_value_from_dict(['reason'])

    def error_type(self):
        return self.get_value_from_dict(['error', 'type'])

    def error_message(self):
        return self.get_value_from_dict(['error', 'message'])


class Slot(ObjectDictionary):
    CONFIRMATION = ['NONE', 'CONFIRMED', 'DENIED']

    def __init__(self, slot_dict):
        super().__init__(slot_dict)
        self.logger.debug("Slot __init__")

    def name(self):
        return self.get_value_from_dict(['name'])

    def value(self):
        return self.get_value_from_dict(['value'])

    def confirmation_status(self):
        return self.get_value_from_dict(['confirmationStatus'])
