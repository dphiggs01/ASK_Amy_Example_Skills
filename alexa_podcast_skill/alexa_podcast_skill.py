from ask_amy.state_mgr.stack_dialog_mgr import StackDialogManager
from ask_amy.core.reply import Reply
import logging

logger = logging.getLogger()

class AlexaPodcastSkill(StackDialogManager):

    def play_audio(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        self.session.attributes['active_url'] = "https://feeds.soundcloud.com/stream/274166909-amazon-web-services-306355661-aws-podcast-episode-139.mp3"
        self.session.attributes['offset'] = 0
        self.request.attributes['command'] = "play"
        self.session.save()
        reply_dialog = self.reply_dialog[self.intent_name]
        return Reply.build_audio(reply_dialog, self.event)

    def pause_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        offset = self.event.context.audio_player.offset_in_milliseconds
        self.session.attributes['offset'] = offset
        self.request.attributes['command'] = "stop"
        self.session.save()
        reply_dialog = self.reply_dialog[self.intent_name]
        return Reply.build_audio(reply_dialog, self.event)

    def resume_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        active_url = self.session.attributes['active_url']
        offset = self.session.attributes['offset']
        self.request.attributes['command'] = "play"
        reply_dialog = self.reply_dialog[self.intent_name]
        return Reply.build_audio(reply_dialog, self.event)

    def next_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        return self.handle_default_intent()

    def previous_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        return self.handle_default_intent()

