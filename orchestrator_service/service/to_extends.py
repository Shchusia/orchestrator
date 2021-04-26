"""
Module with classes for inheritance.
And the implementation in these classes of the service logic.
"""
# pylint: disable=too-few-public-methods
from __future__ import annotations

import logging
import logging as log_module
from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple

from ..message import Message

DEFAULT_LOGGER = logging.Logger(__name__)


class CommandHandler(ABC):
    """
    Class with method for all handlers
    """
    _logger = DEFAULT_LOGGER  # for one global handler
    _service_instance = None  # single scope for service_commands
    _is_logged = False

    @property
    def logger(self) -> Optional["logger"]:
        """
        get logger
        :return:  logger or None
        """
        return self._logger

    @logger.setter
    def logger(self, val: Any):
        """
        method checks the set value
        :param Any val: value to set
        """
        _val = val
        if not val:
            return
        if type(val) != type:
            val = type(val)
        if val == log_module:
            pass
        elif issubclass(val, log_module.Filterer):
            pass
        else:
            raise TypeError(f"Type must be logger but not {val}")
        self._logger = _val

    def set_logger(self,
                   log: logging.Logger) -> None:
        """
        method set to service global logger if not inited
        :param logging.Logger log: service logger
        :return: None
        """
        self.logger = log

    def set_service_instance(self, instance: "Service") -> None:
        """
        Added a single scope for sharing data in the service
        :param Service instance: service object
        """
        self._service_instance = instance

    def get_service_command(self,
                            command_name: str,
                            is_process: bool = True) -> Optional[CommandHandler]:
        """
        The method allows you to take command handlers by its `target_command`
        process or post_process handler
        :param str command_name: `target_command` which handler want to get
        :param bool is_process: want to get the process handler or post_process(if var is False)
        :return: if exists then the handler will return None else
        """
        handler = None
        if self._service_instance and self._service_instance._dict_handlers.get(command_name):
            handler = self._service_instance._dict_handlers[command_name]
            if is_process:
                handler = handler['process']
            else:
                handler = handler['post_process']
        else:
            if self.logger and self._is_logged:
                self.logger.warning("You can't use swap because it is not initialized ")
        return handler

    def set_to_swap_scope(self,
                          key: str,
                          data: Any) -> bool:
        """
        Method adds a value to the global scope for access from all services
        :param str key: name key
        :param Any data: data to add
        :return: bool: is_added_value
        """
        is_added = False
        if self._service_instance:
            try:
                setattr(self._service_instance, key, data)
                is_added = True
            except Exception:
                if self.logger and self._is_logged:
                    self.logger.warning(f'Key `{key}` not added', exc_info=True)
        else:
            if self.logger and self._is_logged:
                self.logger.warning("You can't use swap because it is not initialized ")
        return is_added

    def get_from_swap_scope(self, key: str) -> Optional[Any]:
        """
        Method gets from the global scope a value available for all services
        :param str key: name key to get value
        :return: data if exist or None
        """
        data = None
        if self._service_instance:
            try:
                data = getattr(self._service_instance, key)
            except Exception:
                if self.logger and self._is_logged:
                    self.logger.warning('Error while fetching data from swap', exc_info=True)
        else:
            if self.logger and self._is_logged:
                self.logger.warning("You cann't use swap because it is not initialized ")
        return data

    def del_from_swap_scope(self, key: str) -> bool:
        """
        Method removes attribute from swap_scope if was exist
        """
        is_dropped = False
        if self._service_instance:
            try:
                delattr(self._service_instance, key)
                is_dropped = True
            except Exception:
                if self.logger and self._is_logged:
                    self.logger.warning(f'Key `{key}` not added', exc_info=True)
        else:
            if self.logger and self._is_logged:
                self.logger.warning("You can't use swap because it is not initialized ")
        return is_dropped


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
                msg: Message) -> Tuple[Message, Optional[Any]]:
        """
        the main method for executing the logic of this handler, must be overridden in the inheritor
        :param MessageQueue msg: msg from queue
        :return: MessageQueue or None if return None post handler will not be called
        """
        raise NotImplementedError

    @abstractmethod
    async def aprocess(self, msg: Message) -> Tuple[Message, Optional[Any]]:
        """
        the main async method for executing the logic of this handler,
        must be overridden in the inheritor
        :param MessageQueue msg: msg from queue
        :return: MessageQueue or None if return None post handler will not be called
        """
        return self.process(msg=msg)


class CommandHandlerPostStrategy(CommandHandler, ABC):
    """
    Post Process Handler
    """

    @abstractmethod
    def post_process(self, msg: Message, additional_data: Optional[Any] = None) -> None:
        """
        method does post processing
        e.g. sending to another queue
        , must be overridden in the inheritor
        :param MessageQueue msg:
        :param additional_data: optional data got from processing block
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    async def apost_process(self, msg: Message, additional_data: Optional[Any] = None) -> None:
        """
        method does post processing
        e.g. sending to another queue
        , must be overridden in the inheritor
        :param MessageQueue msg:
        :param additional_data: optional data got from processing block

        :return: None
        """
        self.post_process(msg=msg, additional_data=additional_data)
