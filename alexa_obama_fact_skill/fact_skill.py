from ask_amy.core.default_dialog import DefaultDialog
import json
import random


class ObamaDialog(DefaultDialog):

    def get_new_fact_intent(self, method_name=None):
        """
        Called to generate an Obama fact
        """
        file_ptr_r = open("./facts.json", 'r')
        facts = json.load(file_ptr_r)
        obama_facts = facts['obama_facts']
        file_ptr_r.close()
        index = random.randint(0,len(obama_facts))
        self.session.put_attribute('obama_fact', obama_facts[index])
        return self.handle_default_intent(method_name)
