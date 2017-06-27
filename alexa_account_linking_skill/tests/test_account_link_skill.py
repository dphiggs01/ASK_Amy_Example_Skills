import logging
from alexa_account_linking_skill.tests.test_alexa_skill_base import TestAlexaSkillBase
from ask_amy.core.skill_factory import SkillFactory
from ask_amy.core.event import Event

logger = logging.getLogger()

class AccountLinkTest(TestAlexaSkillBase):
    def setUp(self):
        BASE_DIR=".."
        CONFIG=BASE_DIR+"/skill_configuration.json"
        self.dialog = SkillFactory.build(CONFIG)

    def test_get_user_name(self):
        self.logger.debug("AccountLinkTest.test_get_user_name")
        event_dict, response = self.get_request_response('open_request.json')
        self.dialog.set_event(Event(event_dict))
        profile = self.dialog.amazon_profile()
        print(profile)

        # print(access_token)


