from ask_amy.core.default_dialog import DefaultDialog
import json
import random
import logging

logger = logging.getLogger()

class AlexaObamaFactSkill(DefaultDialog):

    def get_new_fact_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        self.request.attributes['obama_fact'] = FactsDB.random_fact()
        return self.handle_default_intent()


class FactsDB(object):
    FACTS_FILE = "./facts.json"
    FACTS = "facts"

    @staticmethod
    def random_fact():
        with open(FactsDB.FACTS_FILE, 'r') as file_ptr:
            facts_json = json.load(file_ptr)
            facts = facts_json[FactsDB.FACTS]
            index = random.randint(0, len(facts)-1)
        return facts[index]
