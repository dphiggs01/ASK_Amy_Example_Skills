from ask_amy.tests.utility import TestCaseASKAmy
from ask_amy.core.dialog import Dialog


class TestDialog(TestCaseASKAmy):
    def setUp(self):
        pass

    def test_dialog_constr(self):
        skill_dict = self.load_json_file('skill_configuration_test.json')
        dialog_obj =  Dialog(skill_dict['Dialog'])
        print(dialog_obj)