"""
Module with base class blocks
"""
from __future__ import annotations

import types
from abc import ABC, abstractmethod
from typing import Optional, Callable

from orchestrator.message import Message
from .exc import FlowException


class BlockHandler(ABC):
    """
    The Handler interface declares a method for building a chain of handlers.
    It also declares a method to fulfill the request.
    """

    @abstractmethod
    def set_next(self,
                 handler: BlockHandler) -> BlockHandler:
        """
        method for adding a new handler
        :param BlockHandler handler: object next handler in chain flow
        :return: BlockHandler
        """
        raise NotImplementedError

    @abstractmethod
    def handle(self,
               message: Message) -> Optional[Exception]:
        """
        flow chain management method
        :param MessageQueue message:
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def process(self,
                message: Message) -> None:
        """
        method for executing the logic of a given block
        in it, only send messages to other services
        :param MessageQueue message: msg to process
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def hidden_process(self, message: Message) -> None:
        """
        Method execute hidden_process
        :param MessageQueue message:
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def get_list_flow(self) -> str:
        """
        Method return str steps flow
        :return: str
        """
        raise NotImplementedError


class Block(BlockHandler):
    """
    The main class for inheriting the blocks that make up the flow of tasks execution
    """
    _next_handler: BlockHandler = None
    # if the function returns None then you do not need to perform the following steps
    _pre_handler_function: Callable = None
    _post_handler_function: Callable = None
    rabbit = None

    @property
    def name_block(self):
        """
        Unique name to identify block
        for override in subclass   name_block
        """
        raise NotImplementedError

    @property
    def name_queue(self):
        """
        Name of the queue that the service is listening on for this block
        for override in subclass name_queue
        """
        raise NotImplementedError

    def __init__(self,
                 pre_handler_function: Callable = None,
                 post_handler_function: Callable = None):
        """
        Init Block
        :param pre_handler_function: function should accept and return objects of type Message
        which be run before call method
        :param post_handler_function: function should accept and return objects of type Message
        which be run after got msg from source

        """
        if pre_handler_function is None:
            pass
        elif isinstance(pre_handler_function, (types.FunctionType,
                                               types.MethodType)):
            self._pre_handler_function = pre_handler_function
        if post_handler_function is None:
            pass
        elif isinstance(post_handler_function, (types.FunctionType,
                                                types.MethodType)):
            self._post_handler_function = post_handler_function
        else:
            raise TypeError('Incorrect type additional_function, the attribute must be a function')

    def set_next(self,
                 handler: BlockHandler) -> Optional[BlockHandler, None]:
        """
        Save Next handler after this handler
        :param handler:
        :return: Optional[BlockHandler, None]
        """
        self._next_handler = handler
        return handler

    def handle(self,
               message: Message) -> None:
        """
        Flow chain management method
        check step by step
        :param MessageQueue message: msg to process
        in source have name block from which orchestrator get msg
        :return: None
        """
        # TODO
        if not message.get_source():
            self.process(message)
        # check where the message came from and the current block
        if message.get_source() == self.name_block:
            # perform the post processing function for this block, if any
            if self._post_handler_function:
                message = self._post_handler_function(message)

            # send for execution to the next block
            if self._next_handler:
                if not message:
                    return
                if self._pre_handler_function:
                    message = self._pre_handler_function(message)
                if message is not None:
                    self.process(message)
                else:
                    print('message don\'t send')
            # no next handler
            else:
                pass
        # looking for the required handler
        elif self._next_handler:
            self._next_handler.handle(message)
        # passed all flows and did not find the required handler
        else:
            raise FlowException(f'Not found block for source: {message}')

    def hidden_process(self,
                       message: Message) -> None:
        """
        method apply _pre_handler_function to msg
        :param MessageQueue message: msg to process
        :return:  None
        """
        if self._pre_handler_function:
            message = self._pre_handler_function(message)
        if message is not None:
            self.process(message)
        else:
            print('message don\'t send')

    def process(self, message: Message):
        """
        Method for executing the logic of a given block
        in it, only send messages to other services
        :param message:
        :return:
        """
        raise NotImplementedError

    def get_list_flow(self) -> str:
        """
        Method return str flow
        :return: str
        """
        if self._next_handler:
            next_blocks = self._next_handler.get_list_flow()
        else:
            next_blocks = 'end'
        return f'{self.name_block} -> {next_blocks}'
