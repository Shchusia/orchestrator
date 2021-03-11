"""
Service exceptions
"""
# pylint: disable=unnecessary-pass


class ServiceException(Exception):
    """
    Class for Service exceptions
    """
    pass


class ServiceBlockException(BaseException):
    """
    Class for exceptions in ServiceBlock
    """


class ServiceBuilderException(BaseException):
    """
    Class for exceptions in BuilderService
    """
    pass


class NotUniqueCommandError(BaseException):
    """
    Class error if user add the same commands
    """
    pass


class UnknownCommandWarning(Warning):
    """
    Class Warning if handler got msg with incorrect command
    """
    pass


class DoublePostProcessFunctionDeclaredError(ServiceException):
    """
    Exception if many default postprocess handlers
    """

    def __init__(self):
        self.message = "Several postprocessors specified"
        Exception.__init__(self, self.message)
