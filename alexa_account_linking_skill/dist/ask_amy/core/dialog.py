import logging

from ask_amy.core.event import Event
from ask_amy.core.exceptions import ApplicationIdError
from ask_amy.core.object_dictionary import ObjectDictionary

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

    def get_expected_intent_for_data(self, data_name):
        return self.get_value_from_dict(['slots', data_name, 'expected_intent'])

    def get_re_prompt_for_slot_data(self, data_name):
        slot_data_details = self.get_value_from_dict(['slots', data_name])
        if 're_prompt_text' in slot_data_details:
            slot_data_details['speech_out_text'] = slot_data_details['re_prompt_text']
            del slot_data_details['re_prompt_text']
        if 're_prompt_ssml' in slot_data_details:
            slot_data_details['speech_out_text'] = slot_data_details['re_prompt_ssml']
            del slot_data_details['re_prompt_ssml']
        slot_data_details['should_end_session'] = False
        return slot_data_details

    def get_slot_data_details(self, data_name):
        slot_data_details = self.get_value_from_dict(['slots', data_name])
        slot_data_details['should_end_session'] = False
        return slot_data_details

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

    def reset_established_dialog(self):
        logger.debug("**************** entering Dialog.reset_established_dialog")
        dialog_stack = self._event.get_value_in_session(['established_conversation'])
        ret_val = None
        if dialog_stack is not None:
            del dialog_stack[:]
        return ret_val

    def execute_method(self, method_name):
        method = getattr(self, method_name)
        return method(method_name)
