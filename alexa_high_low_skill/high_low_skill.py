import logging
from ask_amy.core.default_dialog import DefaultDialog
from ask_amy.core.reply import Reply
import random

logger = logging.getLogger()


class HighLowDialog(DefaultDialog):
    def new_session_started(self, method_name=None):
        """
        This method is called when Alexa starts a new session
        This happens when the session objects 'new' attribute is set to True
        """
        logger.debug("**************** entering HighLowDialog.new_session_started")
        games_played = self.session.get_attribute(['games_played'])
        if games_played is None:
            self.session.put_attribute('games_played', 0)

        winning_number = random.randint(0, 100)
        self.session.put_attribute('winning_number', winning_number)

    def number_guess_intent(self, method_name=None):
        """
        This method is called when we provide Alexa with a guess
        Note: That even though the slot type is defined as an AMAZON.NUMBER it is not guaranteed
        to be one so you should do some checking before processing
        """
        logger.debug('**************** entering HighLowDialog.{}'.format(method_name))

        # 1. Get the processing details and dialog for this intent from skill_configuration
        intent_dict = self.get_intent_details(method_name)

        # 2. See if we got any slots filled
        guessed_number_str = self.request.value_for_slot_name('number')
        if guessed_number_str is not None:
            self.session.put_attribute('guessed_number', guessed_number_str)
            guessed_number = int(guessed_number_str)
            winning_number = self.session.get_attribute(['winning_number'])

            if guessed_number == winning_number:
                reply_intent_dict = intent_dict['conditions']['winner']
                games_played = self.session.get_attribute(['games_played'])
                self.session.put_attribute('games_played', games_played + 1)
                self.session.save()
            else:
                if guessed_number < winning_number:
                    to_high_to_low = 'low'
                else:
                    to_high_to_low = 'high'
                self.session.put_attribute('to_high_to_low', to_high_to_low)
                reply_intent_dict = intent_dict['conditions']['to_high_to_low']
        else:
            reply_intent_dict = intent_dict

        return Reply.build(reply_intent_dict, self.event.session)

