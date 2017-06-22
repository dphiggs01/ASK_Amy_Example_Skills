from ask_amy.core.default_dialog import DefaultDialog
from ask_amy.core.reply import Reply
import logging
import urllib.request
from urllib.error import URLError
import json

logger = logging.getLogger()

class AccountLinkDialog(DefaultDialog):


    def launch_request(self, method_name=None):
        logger.debug("**************** entering AccountLinkDialog.launch_request")

        access_token = self.event().session().access_token()
        if access_token is None:
            return self.account_link_intent(method_name)
        else:
            return self.hello_world_intent(method_name)


    def account_link_intent(self, method_name=None):
        """
        Called to generate an Account Link Card
        """
        intent_dict = self.get_intent_details('account_link_intent')
        return Reply.build(intent_dict)


    def hello_world_intent(self, method_name=None):
        """
        Called to generate an Account Link Card
        """
        amazon_profile = self.amazon_profile()
        self.event().set_value_in_session("user_name", amazon_profile['name'])
        intent_dict = self.get_intent_details('hello_world_intent')
        return Reply.build(intent_dict,self.event().session())


    def amazon_profile(self):
        access_token = self.event().session().access_token()
        url = "https://api.amazon.com/user/profile?access_token={}".format(access_token)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        try:
            req = urllib.request.Request(url,headers=headers)
            with urllib.request.urlopen(req) as response:
                data = response.read()
                encoding = response.info().get_content_charset('utf-8')
                found = json.loads(data.decode(encoding))
        except URLError as e:
            found = None
            if hasattr(e, 'reason'):
                logger.critical('We failed to reach a server.')
                logger.critical('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                logger.critical('The server couldn\'t fulfill the request.')
                logger.critical('Error code: ', e.code)
        return found


