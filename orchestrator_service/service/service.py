"""
Module Service with help classes for build service
"""
# pylint: disable=too-few-public-methods
from __future__ import annotations

import logging
import os
import warnings
from typing import Dict, Optional, Union, Tuple

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
    def process(self, val: Union[type, CommandHandlerStrategy]):
        """
        process setter
        """
        if isinstance(val, type):
            if getattr(val, '__base__'):
                if val.__base__.__name__ == 'CommandHandlerStrategy':
                    self.__process = val()
                    return
        elif isinstance(val, CommandHandlerStrategy):
            self.__process = val
            return
        raise ServiceBlockException(
            f"`process` object must be of type `CommandHandlerStrategy` and not {type(val)}")

    @post_process.setter
    def post_process(self, val: Union[type, CommandHandlerPostStrategy] = None):
        """
        post_process setter
        """
        if val is None:
            return
        elif isinstance(val, type):
            if getattr(val, '__base__'):
                if val.__base__.__name__ == 'CommandHandlerPostStrategy':
                    self.__post_process = val()
                    return
        elif isinstance(val, CommandHandlerPostStrategy):
            self.__post_process = val
            return

        raise ServiceBlockException(
            f"`post_process` object must be of type "
            f"`CommandHandlerPostStrategy` and not {type(val)}")

    def __init__(self,
                 process: Union[type, CommandHandlerStrategy],
                 post_process: Union[type, CommandHandlerPostStrategy] = None
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

    @staticmethod
    def _check_default_pp(default_post_process: Union[type, CommandHandlerPostStrategy] = None
                          ) -> Optional[CommandHandlerPostStrategy]:
        if default_post_process is None:
            return None
        elif isinstance(default_post_process, type):
            if getattr(default_post_process, '__base__'):
                if default_post_process.__base__.__name__ == 'CommandHandlerPostStrategy':
                    return default_post_process()

        elif isinstance(default_post_process, CommandHandlerPostStrategy):
            return default_post_process
        msg = f"`default_post_process` object must be of type `CommandHandlerPostStrategy`" \
              f" and not {type(default_post_process)}"
        raise ServiceBlockException(msg)

    def __init__(self, *args,
                 default_post_process: Union[type, CommandHandlerPostStrategy] = None):
        """
        Init ServiceBuilder
        :param List[CommandHandlerStrategy] args:  list CommandHandlerStrategy
         objects for current service
        :param CommandHandlerPostStrategy default_post_process: default post process handler
            if not exist handler for concrete ProcessHandler
        :param kwargs: other args for future
        """

        self._default_post_process = ServiceBuilder._check_default_pp(default_post_process)
        list_blocks = list()
        for block in args:
            try:
                tmp_pp = ServiceBuilder._check_default_pp(block)

                if not self._default_post_process:
                    self._default_post_process = tmp_pp
                    continue
                else:
                    raise DoublePostProcessFunctionDeclaredError
            except ServiceBlockException:
                pass
            if not isinstance(block, ServiceBlock):
                raise TypeError(f"block must be instance class `ServiceBlock`."
                                f" Not {type(block)}")
            list_blocks.append(block)
        if not list_blocks:
            raise EmptyCommandsException
        self._list_blocks = list_blocks

    def build(self,
              log: logging.Logger = None,
              service_instance: Service = None) -> Dict[str:Dict[str:object]]:
        """
        Method build dict handler
        :param logging.Logger log: log application for set into services
        :param Service service_instance: service object
        :return: {'command':{'process': CommandHandlerStrategy,
        'post_process': CommandHandlerPostStrategy}
        """
        if not log:
            log = default_logger
        dict_commands = dict()

        if self._default_post_process:
            self._default_post_process.set_logger(log)
            self._default_post_process.set_service_instance(instance=service_instance)
        for block in self._list_blocks:
            process = block.process
            post_process = block.post_process
            process.set_logger(log)
            process.set_service_instance(instance=service_instance)
            if post_process:
                post_process.set_logger(log)
                post_process.set_service_instance(instance=service_instance)

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
    _is_run_default: bool = False
    _service_commands: ServiceBuilder = None
    is_catch_exceptions: bool = False

    @property
    def service_commands(self) -> Optional[ServiceBuilder]:
        """
        Property _service_commands
        :return: ServiceBuilder
        """
        if not self._service_commands:
            raise NotImplementedError
        return self._service_commands

    @service_commands.setter
    def service_commands(self,
                         service_builder: ServiceBuilder) -> None:
        """
        setter ServiceBuilder
        :param ServiceBuilder service_builder:
        :return: None
        """
        if not isinstance(service_builder, ServiceBuilder):
            raise ServiceBuilderException('Incorrect type `service_builder` variable.')

    def __init__(self,
                 service_builder: ServiceBuilder = None,
                 log: logging.Logger = None,
                 is_run_default: bool = True,
                 command_field: str = 'command',
                 default_command: str = None,
                 is_catch_exceptions: bool = True,
                 ):
        """
        Init Service
        :param ServiceBuilder service_builder: instance builder with handlers command
        :param logging.Logger log: logger
        """
        if is_catch_exceptions:
            self.is_catch_exceptions = True
        if service_builder is None:
            if not isinstance(self.service_commands, ServiceBuilder):
                raise ServiceBuilderException('Incorrect type `service_commands` must be '
                                              'overridden in subclass Service.')
            service_builder = self.service_commands
        elif not isinstance(service_builder, ServiceBuilder):
            raise ServiceBuilderException('Incorrect type `service_builder` variable.')
        if log:
            self.logger = log
        else:
            self.logger = default_logger
        if self._command_field == 'command' and command_field != 'command':
            self._command_field = command_field
        if is_run_default:
            self._is_run_default = True
        if not default_command:
            self._default_command = default_command
        elif self._default_command == 'run' and default_command != 'run':
            self._default_command = default_command
        self._dict_handlers = service_builder.build(log=self.logger,
                                                    service_instance=self)
        if self._is_run_default \
                and self._default_command \
                and self._default_command not in self._dict_handlers:
            if len(self._dict_handlers) > 1:
                raise IncorrectDefaultCommand(self._default_command,
                                              list(self._dict_handlers.keys()))

    def _get_handlers(self, msg) -> Tuple[CommandHandlerStrategy, CommandHandlerPostStrategy]:
        command = msg.header.get(self._command_field)
        handler = self._dict_handlers.get(command)  # get handler without keys
        if not handler:
            if len(self._dict_handlers) == 1:
                handler = self._dict_handlers[list(self._dict_handlers.keys())[0]]
            elif self._is_run_default and self._default_command:
                handler = self._dict_handlers.get(self._default_command)
        if not handler:
            raise CommandHandlerNotFoundException(command)
        return handler['process'], handler['post_process']

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
            process_handler, post_process_handler = self._get_handlers(msg)
            resp_msg = process_handler.process(msg)
            if post_process_handler and resp_msg:
                post_process_handler.post_process(resp_msg)
        except CommandHandlerNotFoundException as exc:
            warnings.warn("deprecated", UnknownCommandWarning)
            self.logger.warning(f"Don't process message. Reason:{exc}", exc_info=True)
            return msg
        except Exception as exc:
            self.logger.warning(str(exc), exc_info=True)
            if not self.is_catch_exceptions:
                raise exc
            return msg

    async def ahandle(self,
                      msg: Message) -> Optional[Message]:
        """
        async Method handle msgs from queue for this service
        if only one handler service run this handler
        if don't found handler and exist default command
        :param MessageQueue msg:
        :return:
        """
        try:
            process_handler, post_process_handler = self._get_handlers(msg)
            resp_msg = await process_handler.aprocess(msg)
            if post_process_handler and resp_msg:
                await post_process_handler.apost_process(resp_msg)
        except CommandHandlerNotFoundException as exc:
            warnings.warn("deprecated", UnknownCommandWarning)
            self.logger.warning(f"Don't process message. Reason:{exc}", exc_info=True)
            return msg
        except Exception as exc:
            self.logger.warning(str(exc), exc_info=True)
            if not self.is_catch_exceptions:
                raise exc
            return msg
