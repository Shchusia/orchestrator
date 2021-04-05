"""
Module with custom msg
"""
from .message import Message


class MessageCustom(Message):
    """
    Class for build custom messages
    """

    def __init__(self, body: dict, header: dict = None):
        """
        Init MessageCustom
        :param dict body:
        :param dict header:
        """
        if header is None:
            header = dict()
        self.body = body  # type: dict
        self.header = header  # type: dict
