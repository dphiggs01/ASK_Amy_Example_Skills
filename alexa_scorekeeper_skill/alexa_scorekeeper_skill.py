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
        logger.debug("**************** entering {}.launch_request".format(self.__class__.__name__))
        self._intent_name = 'welcome_request'
        scorekeeper = Scorekeeper(self.session.attributes['game'])
        condition = 'no_players'
        if scorekeeper.number_of_players > 0:
            payer_players = lambda players: '1 player' if players == 1 else str(players) + ' players'
            self.request.attributes['players_text'] = payer_players(scorekeeper.number_of_players)
            condition = 'has_players'

        reply_dialog = self.reply_dialog[self.intent_name]
        return Reply.build(reply_dialog['conditions'][condition], self.event)

    def reset_players_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        scorekeeper = Scorekeeper(self.session.attributes['game'])
        self.session.attributes['game'] = scorekeeper.reset_game()
        self.session.save()
        return self.handle_default_intent()

    def new_game_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        scorekeeper = Scorekeeper(self.session.attributes['game'])
        self.session.attributes['game'] = scorekeeper.new_game()
        self.session.save()
        condition = 'no_players'
        if scorekeeper.number_of_players > 0:
            payer_players = lambda players: '1 player' if players == 1 else str(players) + ' players'
            self.request.attributes['players_text'] = payer_players(scorekeeper.number_of_players)
            condition = 'has_players'

        reply_dialog = self.reply_dialog[self.intent_name]
        return Reply.build(reply_dialog['conditions'][condition], self.event)

    def tell_scores_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        scorekeeper = Scorekeeper(self.session.attributes['game'])

        condition = 'no_players'
        if scorekeeper.number_of_players > 0:
            leader_board = ''
            condition = 'has_players'
            for player, score in scorekeeper.leader_board():
                point_or_points = lambda score: ' point \n' if score == 1 else ' points \n'
                leader_board += player + ' has ' + str(score) + point_or_points(score)
                self.request.attributes['leader_board'] = leader_board

        reply_dialog = self.reply_dialog[self.intent_name]
        return Reply.build(reply_dialog['conditions'][condition], self.event)

    @required_fields(['PlayerName'])
    def add_player_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        scorekeeper = Scorekeeper(self.session.attributes['game'])
        scorekeeper.add_player(self.request.attributes['PlayerName'])
        self.session.attributes['game'] = scorekeeper.game
        self.session.save()

        reply_dialog = self.reply_dialog[self.intent_name]
        return Reply.build(reply_dialog, self.event)

    @required_fields(['ScoreNumber','ScoreName'])
    def add_score_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        scorekeeper = Scorekeeper(self.session.attributes['game'])

        score_str = self.request.attributes['ScoreNumber']
        player_name = self.request.attributes['ScoreName']
        if not scorekeeper.is_player(player_name):
            condition = 'invalid_player_provided'
        else:
            condition = 'score_added'
            scorekeeper.add_score(player_name, score_str)
            self.session.attributes['game'] = scorekeeper.game
            score_points = lambda score: '1 point' if score == 1 else str(score) + ' points'
            self.request.attributes['score_points'] = score_points(int(score_str))
            self.session.save()

        reply_dialog = self.reply_dialog[self.intent_name]
        return Reply.build(reply_dialog['conditions'][condition], self.event)



class Scorekeeper(object):
    def __init__(self, game=None):
        if game:
            self._game = game
        else:
            self._game = {}

    def add_player(self, player):
        self._game[player] = 0

    def is_player(self, player_name):
        return player_name in self._game.keys()

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

    def leader_board(self):
        return sorted(self._game.items(), key=itemgetter(1), reverse=True)