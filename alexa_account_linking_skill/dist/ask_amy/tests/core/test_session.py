from ask_amy.tests.utility import TestCaseASKAmy
from ask_amy.core.session import Session


class TestSession(TestCaseASKAmy):
    def setUp(self):
        pass

    def test_session_constr(self):
        session_dict = self.load_json_file('session_w_attributes.json')
        session_obj =  Session(session_dict['session'])
        self.assertEquals('SessionId.0069cc54-2641-4c0d-a5f3-63e4d9fc2f07',session_obj.session_id())
        self.assertEquals('amzn1.ask.skill.c6fbf52b-8714-48f2-9fc3-20dec4f20b47',session_obj.application_id())
        user_id_expected = 'amzn1.ask.account.AH5IOJ4HZXJARKXBUSO2JJOVLD2E4XSNXKGIXO6XNFPHXYYH25TNVGF26RLWQWROXHEQEYQXDR52RLWODP4EP62P2VC3IB2522RZPE3IQXJYJHD3RNPC32VDVA4GU44S5YKTT4HXQQLPXWTSF6TVWAF3MRCPZMJYD5X4I6GUTEI2LHNGEYGWHTG23DVSVKCWYX6UODI6LJRSXHY'
        self.assertEquals(user_id_expected,session_obj.user_id())
        # print(session_obj)

    def test_session_config(self):
        session_dict = self.load_json_file('session_w_attributes.json')
        session_obj =  Session(session_dict['session'])
        print(session_obj._persistence)