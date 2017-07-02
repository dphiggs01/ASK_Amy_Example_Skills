from ask_amy.state_mgr.stack_dialog_mgr import StackDialogManager
from ask_amy.core.reply import Reply
import logging

logger = logging.getLogger()

class AlexaSessionSkill(StackDialogManager):

    def my_color_is_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        return self.handle_default_intent()

    def whats_my_color_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        return self.handle_default_intent()

