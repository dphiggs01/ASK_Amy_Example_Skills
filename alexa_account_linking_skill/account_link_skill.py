from ask_amy.core.default_dialog import DefaultDialog
from ask_amy.core.reply import Reply
import logging
import urllib.request
from urllib.error import URLError
import json
from pydblite.pydblite import Base
import utilities

logger = logging.getLogger()


class AccountLinkDialog(DefaultDialog):

    @utilities.timing
    def launch_request(self, method_name=None):
        logger.debug("**************** entering AccountLinkDialog.launch_request")
        access_token = self.session.access_token()
        if access_token is None:
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
        zip_code = self.get_zip_code_from_profile()
        user_timezone = self.get_timezone(zip_code)
        self.session.put_attribute("user_timezone", user_timezone)
        intent_dict = self.get_intent_details('timezone_intent')
        return Reply.build(intent_dict,self.session)

    @utilities.timing
    def get_timezone(self, zip_code):
        logger.debug("**************** entering AccountLinkDialog.get_timezone")

        ret_val = 'No timezone found for '+zip_code
        data = self.query_zipcode_db_by_zip_code(zip_code)
        logger.debug("**   data={}".format(data))
        timezone = data['data']['timezone']
        dst = data['data']['dst']
        tz_dic = {'-5+1':'US/Eastern', '-5+0':'US/East-Indiana', '-6+1':'US/Central', '-7+1':'US/Mountain',
                  '-7+0':'US/Arizona', '-8+1':'US/Pacific', '-9+1':'US/Alaska', '-10+0':'US/Hawaii',
                  '-10+1':'US/Aleutian'}
        key=timezone+'+'+dst
        logger.debug("**   timezone={} dst={} tz_dic={}".format(timezone, dst, tz_dic))
        if key in tz_dic:
            ret_val = tz_dic[key]

        return ret_val

    @utilities.timing
    def query_zipcode_db_by_zip_code(self, zip_cd):
        logger.debug("**************** entering AccountLinkDialog.query_zipcode_db_by_zip_code")
        pydblite_db_file = './zipcode.db'
        record = 'Zip not found'
        db = Base(pydblite_db_file)
        db.open()
        records = db(zip_cd=zip_cd)
        logger.debug("**   zip={} records={}".format(zip_cd, records))
        if len(records)==1:
            record = records[0]
        return record

    @utilities.timing
    def get_zip_code_from_profile(self):
        zip_code = 'not known'
        amazon_profile = self.amazon_profile()
        if amazon_profile is not None:
            if 'postal_code' in amazon_profile.keys():
                zip_code = amazon_profile['postal_code']
                if len(zip_code) > 5:
                    zip_code = zip_code[:5]
        return zip_code

    @utilities.timing
    def amazon_profile(self):
        access_token = self.session.access_token()
        url = "https://api.amazon.com/user/profile?access_token={}".format(access_token)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        try:
            req = urllib.request.Request(url,headers=headers)
            with urllib.request.urlopen(req) as response:
                data = response.read()
                encoding = response.info().get_content_charset('utf-8')
                found = json.loads(data.decode(encoding))
                logger.critical('amazon_profile found {}'.format(found))
        except URLError as e:
            found = None
            if hasattr(e, 'reason'):
                logger.critical('We failed to reach a server.')
                logger.critical('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                logger.critical('The server couldn\'t fulfill the request.')
                logger.critical('Error code: ', e.code)
        return found


