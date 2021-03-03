"""
Import exceptions orchestrator
"""
# pylint: disable=unused-import,wildcard-import
from .flow.exc import *
from .block.exc import *


class UniqueNameException(Exception):
    """
    Exception for not unique flows
    """
    def __init__(self, not_unique_flow_name: str, _type: str):
        self.message = f'The {_type} name `{not_unique_flow_name}` ' \
                       f'is not unique to this orchestrator'
        Exception.__init__(self, self.message)


class NoDateException(Exception):
    """
    Exception if dict flow is empty
    """
    def __init__(self, _type):
        self.message = f'No {_type}s for processing'
        Exception.__init__(self, self.message)


class WrongTypeException(Exception):
    """
    Exception for incorrect inputted types
    """
    def __init__(self, variable: str = 'flows', type_variable: str = 'any'):
        self.message = f'Invalid variable type `{variable}`.' \
                       f' There {variable} should be a list and not `{type_variable}`'
