"""
Module Service with help classes for build service
"""
# pylint: disable=too-few-public-methods
from __future__ import annotations

import logging
import os
import warnings
from typing import Dict, Optional

from .exc import *
from .to_extends import CommandHandlerPostStrategy, \
    CommandHandlerStrategy
from ..message import Message

default_logger = logging.Logger(__name__)


class ServiceBlock(object):
    """
    Class ServiceBlock for ServiceBuilder
    """
    __process = None  # type: CommandHandlerStrategy
    __post_process = None  # type: CommandHandlerPostStrategy

    @property
    def process(self):
        """
        process instance CommandHandlerStrategy
        """
        return self.__process

    @property
    def post_process(self):
        """
        post_process instance CommandHandlerPostStrategy
        """
        return self.__post_process

    @process.setter
    def process(self, val: CommandHandlerStrategy):
        """
        process setter
        """
        if not isinstance(val, CommandHandlerStrategy):
            raise ServiceBlockException(
                f"`process` object must be of type `CommandHandlerStrategy` and not {type(val)}")
        self.__process = val

    @post_process.setter
    def post_process(self, val: CommandHandlerPostStrategy):
        """
        post_process setter
        """
        if val:
            if not isinstance(val, CommandHandlerPostStrategy):
                raise ServiceBlockException(
                    f"`post_process` object must be of type "
                    f"`CommandHandlerPostStrategy` and not {type(val)}")
            self.__post_process = val

    def __init__(self,
                 process: CommandHandlerStrategy,
                 post_process: CommandHandlerPostStrategy = None
                 ):
        """
        Init ServiceBlock
        :param CommandHandlerStrategy process:
        :param CommandHandlerPostStrategy post_process:
        """
        self.process = process
        self.post_process = post_process


class ServiceBuilder(object):
    """
    Class for build and aggregate handlers
    """
    _default_post_process = None  # type: CommandHandlerPostStrategy

    def __init__(self, *args,
                 default_post_process: CommandHandlerPostStrategy = None):
        """
        Init ServiceBuilder
        :param List[CommandHandlerStrategy] args:  list CommandHandlerStrategy
         objects for current service
        :param CommandHandlerPostStrategy default_post_process: default post process handler
            if not exist handler for concrete ProcessHandler
        :param kwargs: other args for future
        """
        if default_post_process and not isinstance(default_post_process,
                                                   CommandHandlerPostStrategy):
            msg = f"`default_post_process` object must be of type `CommandHandlerPostStrategy`" \
                  f" and not {type(default_post_process)}"
            raise ServiceBlockException(msg)
        self._default_post_process = default_post_process
        list_blocks = list()
        for block in args:
            if isinstance(block, CommandHandlerPostStrategy):
                if not self._default_post_process:
                    self._default_post_process = block
                else:
                    raise DoublePostProcessFunctionDeclaredError

            if not isinstance(block, ServiceBlock):
                raise TypeError(f"block must be instance class `ServiceBlock`."
                                f" Not {type(block)}")
            list_blocks.append(block)
        self._list_blocks = list_blocks

    def build(self,
              log: logging.Logger) -> Dict[str:Dict[str:object]]:
        """
        Method build dict handler
        :param logging.Logger log: log application for set into services
        :return: {'command':{'process': CommandHandlerStrategy,
        'post_process': CommandHandlerPostStrategy}
        """
        dict_commands = dict()
        if self._default_post_process:
            self._default_post_process.set_logger(log)
        for block in self._list_blocks:
            process = block.process
            post_process = block.post_process
            process.set_logger(log)
            if post_process:
                post_process.set_logger(log)
            else:
                post_process = self._default_post_process
            if not dict_commands.get(process.target_command):
                dict_commands[process.target_command] = {
                    'process': process,
                    'post_process': post_process
                }
            else:
                raise NotUniqueCommandError(f"Command `{process.target_command}`"
                                            f" is not unique for current service")
        return dict_commands


class Service(object):
    """
    Class Service for handle msg-s from queue
    """

    _command_field: str = os.getenv('NameCommandInHandler', 'command')
    _default_command: str = os.getenv('DefaultCommand', 'run')
    _dict_handlers = dict()  # type: Dict[str: CommandHandlerStrategy]
    _is_run_default: bool = True

    def __init__(self,
                 service_builder: ServiceBuilder,
                 log: logging.Logger = None,
                 command_field: str = 'command',
                 default_command: str = 'run'):
        """
        Init Service
        :param ServiceBuilder service_builder: instance builder with handlers command
        :param logging.Logger log: logger
        """
        if not isinstance(service_builder, ServiceBuilder):
            raise ServiceBuilderException('Incorrect type `service_builder` variable.')
        if log:
            self.logger = log
        else:
            self.logger = default_logger
        if self._command_field == 'command' and command_field != 'command':
            self._command_field = command_field
        if self._default_command == 'run' and default_command != 'run':
            self._default_command = default_command
        self._dict_handlers = service_builder.build(self.logger)

    def handle(self,
               msg: Message) -> Optional[Message]:
        """
        Method handle msgs from queue for this service
        if only one handler service run this handler
        if don't found handler and exist default command
        :param MessageQueue msg:
        :return:
        """
        try:
            command = msg.header.get(self._command_field)
            handler = self._dict_handlers.get(command)  # get handler without keys
            if not handler:
                if len(self._dict_handlers) == 1:
                    handler = self._dict_handlers[list(self._dict_handlers.keys())[0]]
                elif self._is_run_default:
                    handler = self._dict_handlers.get(self._default_command)
            if not handler:
                warnings.warn("deprecated", UnknownCommandWarning)
                self.logger.warning("don't process message")
                return msg
            process_handler, post_process_handler = handler['process'], handler['post_process']
            resp_msg = process_handler.process(msg)
            if post_process_handler:
                post_process_handler.post_process(resp_msg)
        except Exception as exc:
            self.logger.warning(str(exc), exc_info=True)
            return msg
