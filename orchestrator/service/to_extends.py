"""
Module with classes for inheritance.
And the implementation in these classes of the service logic.
"""
# pylint: disable=too-few-public-methods
import logging
from abc import ABC, abstractmethod

from ..message import Message


class CommandHandler(ABC):
    """
    Class with method for all handlers
    """
    _logger = None  # for one global handler

    def set_logger(self,
                   log: logging.Logger) -> None:
        """
        method set to service global logger if not inited
        :param logging.Logger log: service logger
        :return: None
        """
        if not self._logger:
            self._logger = log


class CommandHandlerStrategy(CommandHandler, ABC):
    """
    handler class
    """

    @property
    def target_command(self):
        """
        this command will determine that the message should be processed by this particular service

        """
        raise NotImplementedError

    @abstractmethod
    def process(self,
                msg: Message) -> Message:
        """
        the main method for executing the logic of this handler, must be overridden in the inheritor
        :param MessageQueue msg: msg from queue
        :return: MessageQueue or None if return None post handler will not be called
        """
        raise NotImplementedError

    @abstractmethod
    async def aprocess(self, msg: Message) -> Message:
        """
        the main async method for executing the logic of this handler,
        must be overridden in the inheritor
        :param MessageQueue msg: msg from queue
        :return: MessageQueue or None if return None post handler will not be called
        """
        raise NotImplementedError


class CommandHandlerPostStrategy(CommandHandler, ABC):
    """
    Post Process Handler
    """

    @abstractmethod
    def post_process(self, msg: Message) -> None:
        """
        method does post processing
        e.g. sending to another queue
        , must be overridden in the inheritor
        :param MessageQueue msg:
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    async def apost_process(self, msg: Message) -> None:
        """
        method does post processing
        e.g. sending to another queue
        , must be overridden in the inheritor
        :param MessageQueue msg:
        :return: None
        """
        raise NotImplementedError
