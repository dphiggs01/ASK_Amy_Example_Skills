from ask_amy.state_mgr.stack_dialog_mgr import StackDialogManager
from ask_amy.core.reply import Reply
import logging
import json
import random

logger = logging.getLogger()

class AlexaWiseGuySkill(StackDialogManager):

    def tell_me_a_joke_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        who, joke = WiseGuy.get_joke()
        self.session.attributes['who'] = who
        self.session.attributes['joke_speech'] = joke['speech']
        self.session.attributes['joke_text'] = joke['text']
        self.session.attributes['expect_intent'] = 'whos_there_intent'
        return self.handle_default_intent()

    def whos_there_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        if self.session.attributes['expect_intent'] != 'whos_there_intent':
            condition = 'unexpected'
        else:
            self.session.attributes['expect_intent'] = 'setup_name_who_intent'
            condition = 'expected'

        reply_dialog = self.reply_dialog[self.intent_name]
        reply_dialog = reply_dialog['conditions'][condition]
        return Reply.build(reply_dialog, self.event)


    def setup_name_who_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        if self.session.attributes['expect_intent'] != 'setup_name_who_intent':
            condition = 'unexpected'
        else:
            setup_name = self.request.value_for_slot_name('SetupName')
            who = self.session.attributes['who']
            if setup_name != who:
                condition = 'unexpected'
            else:
                condition = 'expected'

        reply_dialog = self.reply_dialog[self.intent_name]
        reply_dialog = reply_dialog['conditions'][condition]
        return Reply.build(reply_dialog, self.event)


class WiseGuy(object):
    JOKES_FILE = "./jokes.json"

    @staticmethod
    def get_joke():
        with open(WiseGuy.JOKES_FILE, 'r') as file_ptr:
            jokes = json.load(file_ptr)
            who = random.choice(list(jokes.keys()))
        return who, jokes[who]
