from __future__ import print_function
import logging
from ask_amy.skill_factory import SkillFactory
from ask_amy.exceptions import ApplicationIdError

logger = logging.getLogger()
logger.setLevel(logging.WARN)


def lambda_handler(event_dict, context):
    logger.warn("**************** entering NEW lambda_handler")
    try:
        dialog_obj = SkillFactory.build()
        response = dialog_obj.begin(event_dict)
    except ApplicationIdError:
        # todo return response specific error
        response = None

    return response
