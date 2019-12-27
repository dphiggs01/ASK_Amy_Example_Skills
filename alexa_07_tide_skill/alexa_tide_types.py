from ask_amy.utilities.slot_validator import Slot_Validator
import logging
from datetime import datetime

logger = logging.getLogger()


class LIST_OF_CITIES(Slot_Validator):
    VALID = 0  # Passed validation
    MSG_01_TEXT = 1  # Failed Validation

    _valid_values = [
        'seattle', 'los angeles', 'monterey', 'san diego', 'san francisco', 'boston', 'new york', 'miami', 'wilmington',
        'tampa', 'galveston', 'morehead', 'new orleans', 'beaufort', 'myrtle beach', 'virginia beach', 'charleston']

    def is_valid_value(self, value):
        status_code = LIST_OF_CITIES.MSG_01_TEXT
        if isinstance(value, str):
            if value.lower() in LIST_OF_CITIES._valid_values:
                status_code = LIST_OF_CITIES.VALID
        return status_code


class DATE(Slot_Validator):
    VALID = 0  # Passed validation
    MSG_01_TEXT = 1  # Failed Validation

    def is_valid_value(self, value):
        status_code = DATE.MSG_01_TEXT
        if isinstance(value, str):
            try:
                datetime.strptime(value, "%Y-%m-%d")
                status_code = DATE.VALID
            except ValueError:
                logger.debug("Failed to convert date value {}".format(value))
        return status_code
