import logging
from ask_amy.core.default_dialog import DefaultDialog
from ask_amy.core.reply import Reply
import random

logger = logging.getLogger()


class HighLowDialog(DefaultDialog):
    def new_session_started(self):
        """
        This method is called when Alexa starts a new session
        This happens when the session objects 'new' attribute is set to True
        """
        logger.debug("**************** entering HighLowDialog.new_session_started")
        if not self.session.attribute_exists('games_played'):
            self.session.attributes['games_played'] = 0

        winning_number = random.randint(0, 100)
        self.session.attributes['winning_number'] = winning_number

    def number_guess_intent(self):
        """
        This method is called when we provide Alexa with a guess
        Note: That even though the slot type is defined as an AMAZON.NUMBER it is not guaranteed
        to be one so you should do some checking before processing
        """
        logger.debug('**************** entering HighLowDialog.number_guess_intent')

        # 1. Get the processing details for this intent from skill_configuration Dialog
        reply_dialog = self.reply_dialog[self.method_name]

        # 2. See if we have any slots filled
        guessed_number_str = self.request.value_for_slot_name('number')
        if guessed_number_str is not None:
            self.session.attributes['guessed_number'] = guessed_number_str
            guessed_number = int(guessed_number_str)
            winning_number = self.session.attributes['winning_number']

            if guessed_number == winning_number:
                reply_dialog = reply_dialog['conditions']['winner']
                games_played = self.session.attributes['games_played']
                self.session.attributes['games_played']= games_played + 1
                self.session.save()
            else:
                if guessed_number < winning_number:
                    to_high_to_low = 'low'
                else:
                    to_high_to_low = 'high'
                self.session.attributes['to_high_to_low'] = to_high_to_low
                reply_dialog = reply_dialog['conditions']['to_high_to_low']

        return Reply.build(reply_dialog, self.event.session)

