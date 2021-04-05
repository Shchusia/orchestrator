"""
Service exceptions
"""


# pylint: disable=unnecessary-pass,non-parent-init-called


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


class IncorrectDefaultCommand(ServiceException):
    """
    among the available commands, there is no default command
    """

    def __init__(self, command: str, list_command: list):
        self.message = f"The `{command}` command which is the default " \
                       f"command is not among the valid commands : {str(list_command)}"
        Exception.__init__(self, self.message)


class EmptyCommandsException(ServiceException):
    """
    Empty list of commands for service operation
    """

    def __init__(self, ):
        self.message = "Empty list of commands for service operation"
        Exception.__init__(self, self.message)


class CommandHandlerNotFoundException(ServiceException):
    """
    if not exist handler and not exist default handler
    """

    def __init__(self, command: str):
        self.message = f'No handler for `{command}` command'
        Exception.__init__(self, self.message)
