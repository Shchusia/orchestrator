"""
Orchestrator
"""
# pylint: disable=too-few-public-methods, broad-except,too-many-arguments,logging-fstring-interpolation
import inspect
from logging import Logger
from types import ModuleType
from typing import Union, List, Dict, Optional

from .block import Block
from .exc import NoDateException
from .exc import UniqueNameException
from .exc import WrongTypeException
from .flow import Flow
from .utils import StrategyIncorrectMessages, IgnoreIncorrectMessage
from ..message import Message


class Orchestrator:
    """
    Orchestrator class for build service
    """
    _flows = dict()
    _targets = dict()

    def __init__(self,
                 flows: Union[ModuleType, List],
                 blocks: Union[ModuleType, List] = None,
                 incorrect_messages_handler: StrategyIncorrectMessages = None,
                 flow_field: str = 'flow',
                 block_field: str = 'target',
                 log: Logger = None,
                 flows_to_ignore: List[str] = None,
                 blocks_to_ignore: List[str] = None):
        """
        Init Orchestrator
        :param flows:
        :param blocks:
        :param incorrect_messages_handler:
        :param flow_field:
        :param block_field:
        :param log:
        :param List[str] flows_to_ignore: names classes to ignore
        (Attention) applies only if a module flows is passed
        :param List[str] blocks_to_ignore: names classes to ignore
        (Attention) applies only if a module blocks is passed

        """
        if not log:
            log = Logger(__name__)
        self._logger = log

        if incorrect_messages_handler \
                and not isinstance(incorrect_messages_handler,
                                   StrategyIncorrectMessages):
            raise TypeError(f"Incorrect_messages_handler must "
                            f"be a subclass of `StrategyIncorrectMessages`"
                            f"and not {type(StrategyIncorrectMessages)}")
        if not incorrect_messages_handler:
            incorrect_messages_handler = IgnoreIncorrectMessage()
        self._incorrect_messages_handler = incorrect_messages_handler

        if not isinstance(flow_field, str):
            raise TypeError('Flow_field field must be a string')
        if not isinstance(block_field, str):
            raise TypeError('Target_field field must be a string')
        self._flow_field = flow_field
        self._block_field = block_field

        self._flows = self._generate_data(data_to_process=flows,
                                          _type_to_compare=Flow,
                                          attribute_to_get='name_flow',
                                          names_to_ignore=flows_to_ignore,
                                          _type_data='flow')
        if blocks:
            self._targets = self._generate_data(data_to_process=blocks,
                                                _type_to_compare=Block,
                                                attribute_to_get='name_block',
                                                names_to_ignore=blocks_to_ignore,
                                                _type_data='block')

    @staticmethod
    def _generate_data(data_to_process: Union[ModuleType, List],
                       _type_to_compare: type,
                       attribute_to_get: str,
                       names_to_ignore: List[str] = None,
                       _type_data: str = 'flow') -> Dict:
        """

        :param data_to_process:
        :param _type_to_compare:
        :param attribute_to_get:
        :param names_to_ignore:
        :param _type_data:
        :return:
        """
        if not names_to_ignore:
            names_to_ignore = list()

        _data = dict()
        if inspect.ismodule(data_to_process):
            for class_name, clazz in inspect.getmembers(data_to_process,
                                                        inspect.isclass):
                if class_name in names_to_ignore:
                    continue

                if not issubclass(clazz.__base__, _type_to_compare):
                    raise TypeError(f'flow is not inheritor {_type_to_compare.__name__}')
                if _data.get(getattr(clazz, attribute_to_get)):
                    raise UniqueNameException(getattr(clazz, attribute_to_get), _type_data)
                # class is not initialized
                _data[getattr(clazz, attribute_to_get)] = clazz
        elif isinstance(data_to_process, list):
            for flow in data_to_process:
                if isinstance(flow, type):
                    if issubclass(flow.__base__, _type_to_compare):
                        if _data.get(getattr(flow, attribute_to_get)):
                            raise UniqueNameException(getattr(flow, attribute_to_get),
                                                      _type_data)
                        _data[getattr(flow, attribute_to_get)] = flow
                    else:
                        raise TypeError(f'flow: `{flow}` is not'
                                        f' inheritor {_type_to_compare.__name__}')
                elif isinstance(flow, _type_to_compare):
                    if _data.get(getattr(flow, attribute_to_get)):
                        raise UniqueNameException(getattr(flow, attribute_to_get), _type_data)
                    _data[getattr(flow, attribute_to_get)] = flow
                else:
                    raise TypeError(f'flow: `{flow}` is not '
                                    f'inheritor {_type_to_compare.__name__}')
        else:
            raise WrongTypeException('flows', type(data_to_process))
        if not _data:
            raise NoDateException(_type_data)
        return _data

    def handle(self, message: Message) -> Optional[Message]:
        """

        :param Message message: message to process
        :return: message if don't have information for processing or incorrect
        """
        self._logger.debug(str(message))
        is_correct, message = self._incorrect_messages_handler.message_checker(message)
        if not is_correct:
            self._incorrect_messages_handler.process_incorrect_message(message)
            if not self._incorrect_messages_handler.is_process_incorrect_messages:
                return message
        msg_header = message.header
        if self._flow_field in msg_header:
            flow = self._flows.get(msg_header[self._flow_field])  # type: Flow
            if flow:
                if isinstance(flow, type):
                    flow = flow()
                    self._flows[msg_header[self._flow_field]] = flow
                flow.to_go_with_the_flow(message=message)
            else:
                self._logger.error(f'No flow `{msg_header[self._flow_field]}` for processing')
                return message
        elif self._block_field in msg_header:
            target = self._targets.get(msg_header[self._block_field])  # type: Block
            if target:
                if isinstance(target, type):
                    target = target()
                    self._targets[msg_header[self._block_field]] = target
                target.process(message=message)
            else:
                self._logger.error(f'No blocks `{msg_header[self._block_field]}` for processing')
                return message
        else:
            self._logger.error(f"Message don't have information for process {message}")
            return message
