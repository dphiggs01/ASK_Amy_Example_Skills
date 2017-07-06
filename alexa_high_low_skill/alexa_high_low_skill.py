import logging
from ask_amy.core.default_dialog import DefaultDialog
from ask_amy.core.reply import Reply
import random

logger = logging.getLogger()


class AlexaHighLowSkill(DefaultDialog):

    def new_session_started(self):
        """
        This method is called when Alexa starts a new session
        This happens when the session objects 'new' attribute is set to True
        """
        logger.debug("**************** entering {}.new_session_started".format(self.__class__.__name__))
        if not self.session.attribute_exists('games_played'):
            self.session.attributes['games_played'] = 0

        high_low_game = HighLowGame()
        self.session.attributes['winning_number'] = high_low_game.peek_winning_number

    def number_guess_intent(self):
        """
        This method is called when we provide Alexa with a guess
        Note: That even though the slot type is defined as an AMAZON.NUMBER it is not guaranteed
        to be one so you should do some checking before processing
        """
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))

        # 1. Get the processing details for this intent from skill_configuration Dialog
        reply_dialog = self.reply_dialog[self.intent_name]

        # 2. See if we have any slots filled
        guessed_number_str = self.request.value_for_slot_name('number')
        if guessed_number_str is not None:
            self.session.attributes['guessed_number'] = guessed_number_str

            # 3. Take a turn at the game
            high_low_game = HighLowGame(self.session.attributes['winning_number'])
            guess_result = high_low_game.guess(guessed_number_str)

            # 4. Process results
            if guess_result == HighLowGame.Winner:
                reply_dialog = reply_dialog['conditions']['winner']
                games_played = self.session.attributes['games_played']
                self.session.attributes['games_played']= games_played + 1
                self.session.save()
            else:
                if guess_result == HighLowGame.ToLow:
                    self.session.attributes['to_high_to_low'] = 'low'
                else: # It must be to High
                    self.session.attributes['to_high_to_low'] = 'high'

                reply_dialog = reply_dialog['conditions']['to_high_to_low']

        return Reply.build(reply_dialog, self.event.session)


class HighLowGame(object):
        Winner, ToLow, ToHigh = range(3)
        def __init__(self, seed_winning_number=None):
            if seed_winning_number:
                self._winning_number = seed_winning_number
            else:
                self._winning_number = random.randint(0, 100)

        def get_winning_number(self):
            return self._winning_number
        peek_winning_number = property(get_winning_number)

        def guess(self,guessed_number_str):
            guessed_number = int(guessed_number_str)
            if guessed_number == self._winning_number:
                return HighLowGame.Winner
            elif guessed_number < self._winning_number:
                return HighLowGame.ToLow
            else:
                return HighLowGame.ToHigh

