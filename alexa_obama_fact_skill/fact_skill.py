from ask_amy.core.default_dialog import DefaultDialog
import json
import random


class ObamaDialog(DefaultDialog):

    def get_new_fact_intent(self):
        """
        Called to generate an Obama fact
        """
        self.session.attributes['obama_fact'] = ObamaFacts.random_fact()
        return self.handle_default_intent()


class ObamaFacts(object):
    FACTS_DB="./facts.json"
    OBAMA_FACTS="obama_facts"

    @staticmethod
    def random_fact():
        facts_file = open(ObamaFacts.FACTS_DB, 'r')
        facts_json = json.load(facts_file)
        obama_facts = facts_json[ObamaFacts.OBAMA_FACTS]
        facts_file.close()
        index = random.randint(0,len(obama_facts))
        return obama_facts[index]
