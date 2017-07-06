from ask_amy.core.default_dialog import DefaultDialog
from ask_amy.core.reply import Reply
from ask_amy.utilities.account_link import AmazonProfile
import logging
from zip_code_db import ZipcodeDB

logger = logging.getLogger()

class AlexaAccountLinkingSkill(DefaultDialog):
    def launch_request(self):
        logger.debug("**************** entering {}.launch_request".format(self.__class__.__name__))
        if self.session.access_token is None:
            return self.account_link_intent()
        else:
            return self.timezone_intent()

    def account_link_intent(self):
        """
        Called to generate an Account Link Card
        """
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        reply_dialog = self.reply_dialog['account_link_intent']
        return Reply.build(reply_dialog)

    def timezone_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        amazon_profile = AmazonProfile(self.session.access_token)
        zip_code = amazon_profile.get_zip_code()
        zip_code_db = ZipcodeDB()
        user_timezone = zip_code_db.get_timezone_for_zip_code(zip_code)
        self.session.attributes["user_timezone"] = user_timezone
        reply_dialog = self.reply_dialog['timezone_intent']
        return Reply.build(reply_dialog, self.session)

