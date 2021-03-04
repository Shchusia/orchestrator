"""
a module with a strategy for what to do with
incorrect messages and a default solution
"""

from abc import ABC, abstractmethod
from typing import Tuple, Any

from orchestrator.message import Message


class StrategyIncorrectMessages(ABC):
    """
    class strategy for handling messages of wrong structure
    """

    @property
    def is_process_incorrect_messages(self):
        """
        boolean parameter whether to process invalid messages
        True - process
        flow - ignore
        """
        raise NotImplementedError

    @abstractmethod
    def message_checker(self, message: Message) -> Tuple[bool, Any]:
        """
        Method for validating messages
        :param Message message: message to check
        :return: is_correct_message: bool, warning message
        """
        raise NotImplementedError

    @abstractmethod
    def process_incorrect_message(self, message: Message) -> None:
        """
        method for handling messages with incorrect structure
        save for send report or save to log
        :param Message message: message to process
        :return: None
        """
        raise NotImplementedError


class IgnoreIncorrectMessage(StrategyIncorrectMessages):
    """
    Default class if no strategy for handling invalid messages is specified
    """

    @property
    def is_process_incorrect_messages(self):
        return True

    def message_checker(self, message: Message) -> Tuple[bool, Any]:
        """
        consider all messages correct
        :param Message message: message to check
        :return:
        """
        return True, ''

    def process_incorrect_message(self, message: Message) -> None:
        """
        :return: None
        """
        return
