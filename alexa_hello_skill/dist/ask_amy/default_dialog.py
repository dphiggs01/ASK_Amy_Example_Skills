import logging
from ask_amy.dialog import Dialog
from ask_amy.reply import Reply


logger = logging.getLogger()


class DefaultDialog(Dialog):
    def __init__(self, dialog_dict=None):
        super().__init__(dialog_dict)

    def new_session_started(self, method_name=None):
        logger.debug("**************** entering DefaultDialog.new_session_started")
        pass

    def launch_request(self, method_name=None):
        logger.debug("**************** entering DefaultDialog.launch_request")
        method_name = self._sc_intent_control['AMAZON.HelpIntent']
        return self.execute_method(method_name)

    def session_ended_request(self, method_name=None):
        logger.debug("**************** entering DefaultDialog.session_ended_request")
        pass

    def intent_request(self, method_name=None):
        """
        Executes the method related to the intent sent from Alexa.
        The methods are mapped in the skill_configuration.json file under the attribute name 'intentControl'

        Returns: Response object

        """
        logger.debug("**************** entering DefaultDialog.intent_request")
        request = self._event.request()
        intent_name = request.intent_name()
        method_name = self._sc_intent_control[intent_name]
        return self.execute_method(method_name)

    def default_stop_intent(self, method_name=None):
        logger.debug("**************** entering DefaultDialog.default_stop_intent")
        return self.handle_default_intent(method_name)

    def default_cancel_intent(self, method_name=None):
        logger.debug("**************** entering DefaultDialog.default_cancel_intent")
        return self.handle_default_intent(method_name)

    def handle_default_intent(self, method_name=None):
        logger.debug('**************** entering DefaultDialog.handle_default_intent.{}'.format(method_name))
        response_dict = self.get_intent_details(method_name)
        if response_dict is None:
            response_dict = {"card_title": "End Session",
                             "speech_out_text": "Good Bye.",
                             "should_end_session": True}

        reply = Reply.build(response_dict, self.event().session())
        return reply
