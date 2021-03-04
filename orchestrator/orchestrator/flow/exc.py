"""
Flow module exceptions
"""


class FlowBlockException(Exception):
    """
    Class custom exception
    for wrong type of flow block
    """

    def __init__(self, message: str = ''):
        self.message = f"Incorrect type block handler. " \
                       f"The block must inherit from the class 'Block'," \
                       f" and not : {message}"
        Exception.__init__(self, self.message)


class FlowBuilderException(Exception):
    """
    Class custom exception
    for wrong types
    """

    def __init__(self, message: str = ''):
        self.message = f'Incorrect type in builder arguments {message}'
        Exception.__init__(self, self.message)
