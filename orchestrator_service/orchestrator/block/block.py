"""
Module with base class blocks
"""
from __future__ import annotations

import asyncio
import types
from abc import ABC, abstractmethod
from inspect import iscoroutinefunction
from typing import Optional, Callable

from orchestrator_service.message import Message
from .exc import FlowException


class BlockHandler(ABC):
    """
    The Handler interface declares a method for building a chain of handlers.
    It also declares a method to fulfill the request.
    """
    pre_handler_function = None
    post_handler_function = None
    is_async_pre_handler = False
    is_async_post_handler = False

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
    async def ahandle(self,
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
    async def aprocess(self,
                       message: Message) -> None:
        """
        method for executing the logic of a given block
        in it, only send messages to other services
        :param MessageQueue message: msg to process
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

    @property
    def pre_handler_function(self):
        """
        function which call before send to handler
        :return:
        """
        return self._pre_handler_function

    @property
    def post_handler_function(self):
        """
        function which call after received from source
        :return:
        """
        return self._post_handler_function

    @property
    def name_block(self):
        """
        Unique name to identify block
        for override in subclass   name_block
        """
        raise NotImplementedError

    # @property
    # def name_queue(self):
    #     """
    #     Name of the queue that the service is listening on for this block
    #     for override in subclass name_queue
    #     """
    #     raise NotImplementedError

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
        self.pre_handler_function = pre_handler_function
        self.post_handler_function = post_handler_function

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
        in source have name block from which orchestrator_service get msg
        :return: None
        """
        if not message.get_source():
            # if message don't have source
            # we start from first chain flow
            self.process(message)
        elif message.get_source() == self.name_block:
            if self.post_handler_function:
                # apply post function
                if self.is_async_post_handler:
                    message = asyncio.get_event_loop() \
                        .run_until_complete(self.post_handler_function(message))
                else:
                    message = self.post_handler_function(message)
            if not message:
                # if not exist message
                return
            if not self._next_handler:
                # last handler in chain
                return
            if self._next_handler.pre_handler_function:
                if self._next_handler.is_async_pre_handler:
                    message = asyncio.get_event_loop() \
                        .run_until_complete(self._next_handler.pre_handler_function(message))
                else:
                    message = self._next_handler.pre_handler_function(message)
            if not message:
                return
            self._next_handler.process(message)

        elif self._next_handler:
            self._next_handler.handle(message)
        else:
            raise FlowException(f'Not found block for source: {message}')

    async def ahandle(self,
                      message: Message) -> None:
        """
        Flow chain management method
        check step by step
        :param MessageQueue message: msg to process
        in source have name block from which orchestrator_service get msg
        :return: None
        """
        if not message.get_source():
            # if message don't have source
            # we start from first chain flow
            await self.aprocess(message)
        elif message.get_source() == self.name_block:
            if self.post_handler_function:
                # apply post function
                if self.is_async_post_handler:
                    message = await self.post_handler_function(message)
                else:
                    message = self.post_handler_function(message)
            if not message:
                # if not exist message
                return
            if not self._next_handler:
                # last handler in chain
                return
            if self._next_handler.pre_handler_function:
                if self._next_handler.is_async_pre_handler:
                    message = await self._next_handler.pre_handler_function(message)
                else:
                    message = self._next_handler.pre_handler_function(message)
            if not message:
                return
            await self._next_handler.aprocess(message)

        elif self._next_handler:
            await self._next_handler.ahandle(message)
        else:
            raise FlowException(f'Not found block for source: {message}')

    def process(self, message: Message):
        """
        Method for executing the logic of a given block
        in it, only send messages to other services
        :param message:
        :return:
        """
        raise NotImplementedError('Not Implemented method for processing messages')

    async def aprocess(self, message: Message):
        """
        Method for executing the logic of a given block
        in it, only send messages to other services
        :param message:
        :return:
        """
        raise NotImplementedError('Not Implemented method for async processing messages')

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

    @pre_handler_function.setter
    def pre_handler_function(self, func: Callable = None):
        if not func:
            pass
        elif isinstance(func, (types.FunctionType,
                               types.MethodType)):
            self._pre_handler_function = func
            if iscoroutinefunction(func):
                self.is_async_pre_handler = True
        else:
            raise TypeError('Incorrect type pre_handler_function,'
                            ' the attribute must be a function or None')

    @post_handler_function.setter
    def post_handler_function(self, func: Callable = None):
        if not func:
            pass
        elif isinstance(func, (types.FunctionType,
                               types.MethodType)):
            self._post_handler_function = func
            if iscoroutinefunction(func):
                self.is_async_post_handler = True
        else:
            raise TypeError('Incorrect type post_handler_function,'
                            ' the attribute must be a function or None')
