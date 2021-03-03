"""
Message for work with aio_pika messages
"""

import json

from aio_pika import IncomingMessage

from .message import Message


class MessageAioPika(Message):
    """
    Class for processing messages from aio_pika handler
    """

    def __init__(self, message: IncomingMessage):
        """
        Init MessageAioPika
        :param IncomingMessage message: message from queue
        """
        super().__init__()
        self._queue_message = message
        self.body = json.loads(message.body, )  # type: dict
        self.body = dict(message.headers)  # type: dict

    def get_queue_message(self) -> IncomingMessage:
        """
        Method for get IncomingMessage
        :return: IncomingMessage from aio_pika
        """
        return self._queue_message
