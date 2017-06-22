from ask_amy.tests.utility import TestCaseASKAmy
from ask_amy.core.request import Request, IntentRequest, LaunchRequest


class TestRequest(TestCaseASKAmy):
    def setUp(self):
        pass

    def test_request_constr(self):
        request_dict = self.load_json_file('intent_request_no_slot_value.json')
        request_obj =  Request(request_dict['request'])
        self.assertEquals('IntentRequest',request_obj.request_type())
        self.assertEquals('EdwRequestId.38cc43e9-fbff-4701-bdbc-97aff27270fb',request_obj.request_id())
        self.assertEquals('en-US',request_obj.locale())
        self.assertEquals('2017-06-12T17:03:34Z',request_obj.timestamp())
        print(request_obj.request_type())
        print(request_obj.request_id())
        print(request_obj.locale())
        print(request_obj.timestamp())

    def test_request_factory(self):
        request_dict = self.load_json_file('intent_request_no_slot_value.json')
        request_obj = Request.factory(request_dict['request'])
        self.assertIsInstance(request_obj,IntentRequest)

    def test_launch_request(self):
        request_dict = self.load_json_file('launch_request.json')
        request_obj = Request.factory(request_dict['request'])
        self.assertIsInstance(request_obj,LaunchRequest)
        self.assertEquals('en-US',request_obj.locale())
        self.assertEquals('2017-06-12T16:40:33Z',request_obj.timestamp())

    def test_intent_request(self):
        request_dict = self.load_json_file('intent_request_w_slot_value.json')
        request_obj = Request.factory(request_dict['request'])
        self.assertEquals('agreeToTerms',request_obj.intent_name())
        self.assertEquals('agree',request_obj.value_for_slot_name('agree'))
        slots_expected = {'agree': {'name': 'agree', 'value': 'agree'}}
        self.assertEquals(slots_expected,request_obj.slots())
        #self.assertEquals()
        #print(request_obj.value_for_slot_name('agree'))
        print(request_obj.slots())

