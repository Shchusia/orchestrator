"""
Flow exceptions module
"""


class FlowException(Exception):
    """
    Class custom exception
    for incorrect type flow
    """

    def __init__(self, message: str):
        self.message = f"The flow chain ended without finding a single handler: {message}"
        Exception.__init__(self, self.message)
