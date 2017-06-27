from ask_amy.core.default_dialog import DefaultDialog
import json
import random


class ObamaDialog(DefaultDialog):

    def get_new_fact_intent(self):
        """
        Called to generate an Obama fact
        """
        obama_facts = self._load_facts()
        index = random.randint(0,len(obama_facts))
        self.session.attributes['obama_fact'] = obama_facts[index]
        return self.handle_default_intent()

    def _load_facts(self):
        facts_file = open("./facts.json", 'r')
        facts_json = json.load(facts_file)
        facts = facts_json['obama_facts']
        facts_file.close()
        return facts

