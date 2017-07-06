from ask_amy.state_mgr.stack_dialog_mgr import StackDialogManager
from ask_amy.state_mgr.stack_dialog_mgr import required_fields
from ask_amy.core.reply import Reply
import logging
from operator import itemgetter


logger = logging.getLogger()

class AlexaScorekeeperSkill(StackDialogManager):
    def new_session_started(self):
        """
        This method is called when Alexa starts a new session
        This happens when the session objects 'new' attribute is set to True
        """
        logger.debug("**************** entering {}.new_session_started".format(self.__class__.__name__))
        if not self.session.attribute_exists('game'):
            self.session.attributes['game'] = {}

    def launch_request(self):
        logger.debug("**************** entering DiabetesDialog.launch_request")
        self._intent_name = 'welcome_request'
        scorekeeper = Scorekeer(self.session.attributes['game'])
        condition='no_players'
        if scorekeeper.number_of_players > 0:
            payer_players = lambda players: '1 player' if players == 1 else str(players)+' players'
            self.session.attributes['players_text'] = payer_players(scorekeeper.number_of_players)
            condition='has_players'

        reply_dialog = self.reply_dialog[self.intent_name]
        return Reply.build(reply_dialog['conditions'][condition], self.session)


    @required_fields(['PlayerName'])
    def add_player_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        scorekeeper = Scorekeer(self.session.attributes['game'])
        scorekeeper.add_player(self.session.attributes['PlayerName'])
        self.session.attributes['game'] = scorekeeper.game
        self.session.save()
        return self.handle_default_intent()

    @required_fields(['PlayerName','ScoreNumber'])
    def add_score_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        scorekeeper = Scorekeer(self.session.attributes['game'])
        player = self.session.attributes['PlayerName']
        score_str = self.session.attributes['ScoreNumber']

        return_code, error_message =scorekeeper.add_score(player,score_str)
        if return_code == 0:
            condition='added'
            self.session.attributes['game'] = scorekeeper.game
            score_points = lambda score: '1 point' if score == 1 else str(score)+' points'
            self.session.attributes['score_points'] = score_points(int(score_str))
            self.session.save()
        else:
            condition='not_added'
            self.session.attributes['error'] = error_message

        reply_dialog = self.reply_dialog[self.intent_name]
        return Reply.build(reply_dialog['conditions'][condition], self.session)

    def reset_players_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        scorekeeper = Scorekeer(self.session.attributes['game'])
        scorekeeper.reset_game()
        self.session.attributes['game'] = scorekeeper.reset_game()
        self.session.save()
        return self.handle_default_intent()

    def new_game_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        scorekeeper = Scorekeer(self.session.attributes['game'])
        self.session.attributes['game'] = scorekeeper.new_game()
        self.session.save()
        condition='no_players'
        if scorekeeper.number_of_players > 0:
            payer_players = lambda players: '1 player' if players == 1 else str(players)+' players'
            self.session.attributes['players_text'] = payer_players(scorekeeper.number_of_players)
            condition='has_players'

        reply_dialog = self.reply_dialog[self.intent_name]
        return Reply.build(reply_dialog['conditions'][condition], self.session)


    def tell_scores_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        scores = self.session.attributes['game']
        leader_board = ''
        for player, score in sorted(scores.items(), key=itemgetter(1), reverse=True):
            point_or_points = lambda score: ' point \n' if score == 1 else ' points \n'
            leader_board += player + ' has ' + str(score) + point_or_points(score)

        self.session.attributes['leader_board'] = leader_board
        return self.handle_default_intent()


class Scorekeer(object):
    def __init__(self, game=None):
            if game:
                self._game = game
            else:
                self._game = {}

    def add_player(self, player):
        self._game[player]=0

    def add_score(self, player, score):
        if player in self._game.keys():
            self._game[player] += int(score)
        else:
            return -1, "invalid player"
        return 0, ""

    def points(self, player):
        return self._game[player]

    @property
    def number_of_players(self):
        return len(self._game)

    def reset_game(self):
        self._game = {}
        return self._game

    def new_game(self):
        for name in self._game.keys():
            self._game[name] = 0
        return self._game

    @property
    def game(self):
        return self._game

