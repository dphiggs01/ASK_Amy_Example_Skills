"""
Global exception and warning classes.
"""


class ApplicationIdError(Exception):
    """The application id provided does not match application id for the skill_fwk"""
    pass


class SessionError(Exception):
    """Error in session """
    pass
