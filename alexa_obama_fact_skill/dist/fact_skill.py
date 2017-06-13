from ask_amy.default_dialog import DefaultDialog
import json
import random


class ObamaDialog(DefaultDialog):

    def get_new_fact_intent(self, method_name=None):
        file_ptr_r = open("./facts.json", 'r')
        facts = json.load(file_ptr_r)
        obama_facts = facts['obama_facts']
        file_ptr_r.close()
        index = random.randint(0,len(obama_facts))
        self.event().set_value_in_session('obama_fact', obama_facts[index])
        return self.handle_default_intent(method_name)
