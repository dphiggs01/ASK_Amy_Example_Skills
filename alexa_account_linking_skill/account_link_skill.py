from ask_amy.core.default_dialog import DefaultDialog
from ask_amy.core.reply import Reply
from ask_amy.utilities.account_link import AmazonProfile
import logging
from zip_code_db import ZipcodeDB
import utilities

logger = logging.getLogger()


class AccountLinkDialog(DefaultDialog):

    @utilities.timing
    def launch_request(self, method_name=None):
        logger.debug("**************** entering AccountLinkDialog.launch_request")

        if self.session.access_token is None:
            return self.account_link_intent(method_name)
        else:
            return self.timezone_intent(method_name)

    def account_link_intent(self, method_name=None):
        """
        Called to generate an Account Link Card
        """
        intent_dict = self.get_intent_details('account_link_intent')
        return Reply.build(intent_dict)

    @utilities.timing
    def timezone_intent(self, method_name=None):
        """
        Called to speak the time zone
        """
        amazon_profile = AmazonProfile(self.session.access_token)
        zip_code = amazon_profile.get_zip_code()
        zip_code_db = ZipcodeDB()
        user_timezone = zip_code_db.get_timezone_for_zip_code(zip_code)
        self.session.attributes["user_timezone"] = user_timezone
        intent_dict = self.get_intent_details('timezone_intent')
        return Reply.build(intent_dict,self.session)



