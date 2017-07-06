from ask_amy.state_mgr.stack_dialog_mgr import StackDialogManager
from ask_amy.core.reply import Reply
import logging

logger = logging.getLogger()

class AlexaSessionSkill(StackDialogManager):

    def my_color_is_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        # 2. See if we have any slots filled
        self.event.slot_data_to_session_attributes()

        # 3. Do we we have all our required fields
        need_additional_data = self.required_fields_process(['Color'])
        if need_additional_data is not None:
            return need_additional_data

        return self.handle_default_intent()

    def whats_my_color_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))

        need_additional_data = self.required_fields_process(['Color'])
        if need_additional_data is not None:
            return need_additional_data

        return self.handle_default_intent()

