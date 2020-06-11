from ask_amy.core.default_dialog import DefaultDialog
import json
import random
import logging

logger = logging.getLogger()

class AlexaCoffeeFactsSkill(DefaultDialog):

    def get_new_fact_intent(self):
        logger.debug("**************** entering {}.{}".format(self.__class__.__name__, self.intent_name))
        # Setting fun_fact as a request.attribute(s) means that this attribute is only in scope for the
        # duration of the request. i.e. Once the reply is sent back to the user the variable is no longer available
        self.request.attributes['fun_fact'] = FactsDB.random_fact()

        # handle_default_intent() builds an Alexa Reply JSON based on the data provided in get_new_fact_intent of the
        # amy_dialog_model.json.
        return self.handle_default_intent()

# Note: Our FactsDB has no Alexa specific code or functionality
# This simple fact generator could be used just as easily in a UI.
# We call this design feature a "Separation of Concern" and it gives our
# code an additional robustness.

class FactsDB(object):
    FACTS_FILE = "facts.json"
    FACTS = "facts"

    @staticmethod
    def random_fact():
        with open(FactsDB.FACTS_FILE, 'r') as file_ptr:
            facts_json = json.load(file_ptr)
            facts = facts_json[FactsDB.FACTS]
            index = random.randint(0, len(facts)-1)
        return facts[index]
