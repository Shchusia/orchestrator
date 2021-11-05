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
        super(Message, self).__init__(body=body, header=header)
