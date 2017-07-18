from ask_amy.state_mgr.stack_dialog_mgr import StackDialogManager
from ask_amy.state_mgr.stack_dialog_mgr import required_fields

from ask_amy.core.reply import Reply
import logging

logger = logging.getLogger()

class AlexaSessionSkill(StackDialogManager):

    @required_fields(['Color'])
    def my_color_is_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        color = self.request.attributes['Color']
        self.session.attributes['Color'] = color
        return self.handle_default_intent()

    @required_fields(['Color'])
    def whats_my_color_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        return self.handle_default_intent()

