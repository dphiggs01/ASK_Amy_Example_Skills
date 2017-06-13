import logging
from ask_amy.event import Event
from ask_amy.object_dictionary import ObjectDictionary
from ask_amy.exceptions import ApplicationIdError

logger = logging.getLogger()


class Dialog(ObjectDictionary):
    def __init__(self, dialog_dict=None):
        super().__init__(dialog_dict)
        self._event = None

        self._sc_application_id = self.get_value_from_dict(['applicationId'])
        self._sc_request_control = self.get_value_from_dict(['requestControl'])
        self._sc_intent_control = self.get_value_from_dict(['intentControl'])

    def set_event(self, event):
        self._event = event

    def event(self):
        return self._event

    def get_prompt_for_data(self, data_name):
        return self.get_value_from_dict(['slots', data_name, 'prompt'])

    def get_expected_intent_for_data(self, data_name):
        return self.get_value_from_dict(['slots', data_name, 'expected_intent'])

    def get_re_prompt_for_data(self, data_name):
        return self.get_value_from_dict(['slots', data_name, 're_prompt_text'])

    def get_intent_details(self, intent_name):
        return self.get_value_from_dict([intent_name])

    def begin(self, event_dict):
        logger.debug("**************** entering Dialog.begin")
        self._event = Event(event_dict)
        logger.debug("####### event={}".format(self._event))

        # If we have and application id in our configuration see if it matches the
        # application id in the event
        session = self._event.session()
        if self._sc_application_id:
            if session.application_id() != self._sc_application_id:
                raise ApplicationIdError("Invalid Application ID")

        # If we are starting a new session then call the method in the request
        # control. This methods may be overridden on the skills derived class
        if session.is_new_session():
            method_name = self._sc_request_control['NewSession']
            self.execute_method(method_name)

        # Get the request type from the event and execute the mapped method
        # This methods may be overridden on the skills derived class
        # Current request may be  "LaunchRequest", "IntentRequest", "SessionEndedRequest"
        request = self._event.request()
        request_type = request.request_type()
        method_name = self._sc_request_control[request_type]
        return self.execute_method(method_name)

    def peek_established_dialog(self):
        logger.debug("**************** entering Dialog.peek_established_dialog")
        dialog_stack = self._event.get_value_in_session(['established_conversation'])
        ret_val = None
        if dialog_stack is not None:
            ret_val = dialog_stack[len(dialog_stack) - 1]
        return ret_val

    def push_established_dialog(self, intent_name):
        logger.debug("**************** entering Dialog.push_established_dialog")
        dialog_stack = self._event.get_value_in_session(['established_conversation'])
        if dialog_stack is None:
            dialog_stack = []
        dialog_stack.append(intent_name)
        self._event.set_value_in_session('established_conversation', dialog_stack)
        return dialog_stack

    def pop_established_dialog(self):
        logger.debug("**************** entering Dialog.pop_established_dialog")
        dialog_stack = self._event.get_value_in_session(['established_conversation'])
        ret_val = None
        if dialog_stack is not None:
            ret_val = dialog_stack.pop()
        return ret_val

    def execute_method(self, method_name):
        method = getattr(self, method_name)
        return method(method_name)
