from ask_amy.core.default_dialog import DefaultDialog

from ask_amy.core.reply import Reply
import logging

logger = logging.getLogger()

class AlexaSessionSkill(DefaultDialog):

    def my_color_is_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))

        # 1. See if we have the slot filled
        color_name = self.request.value_for_slot_name('Color')

        # 2. Move the value from the slot to the session
        if color_name is not None:
            self.session.attributes['Color'] = color_name

        # 3. We are assuming the slot was filled and has a correct value!

        #    This is NOT a good assumption as we should be checking that the slot has a good value....
        #    It is left as a learning exercise to improve this code.
        #    Hint you can use reply_dialog['conditions']['have_color'] to improve the response
        return self.handle_default_intent()

    def whats_my_color_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        # 1. Get the processing details for this intent from amy_dialog_model
        reply_dialog = self.reply_dialog[self.intent_name]

        # 2. See if we have a session Attribute for Color
        if self.session.attribute_exists('Color'):
            reply_dialog = reply_dialog['conditions']['have_color']
        else:
            reply_dialog = reply_dialog['conditions']['dont_have_color']

        return Reply.build(reply_dialog, self.event)