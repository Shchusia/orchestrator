"""
Module with Base class for orchestrator operation
"""
import json
from pprint import pprint
from typing import Dict, Any, Optional, Union


class Message:
    """
    Class for working with a received message from the queue
    """

    __body = None
    __header = None

    @property
    def body(self):
        """
        Property class message - body
        :return: dict body: message
        """
        return self.__body

    @property
    def header(self):
        """
        Property class message - header
        :return: dict header: message
        """
        return self.__header

    @body.setter
    def body(self, body):
        if not isinstance(body, dict):
            raise TypeError("Body msg must be a dict")
        self.__body = body

    @header.setter
    def header(self, header):
        if not isinstance(header, dict):
            raise TypeError("Header msg must be a dict")
        self.__header = header

    def __init__(self, body: dict, header: dict = None):
        self.body = body
        if header is None:
            header = dict()
        self.header = header

    def __str__(self) -> str:
        return f'<Message body: `{self.__body}` header: `{self.__header}`>'

    def print_message(self) -> None:
        """
        Method print message
        :return: None
        """
        print('Header:')
        pprint(self.__header)
        print("Body")
        pprint(self.__body)

    def update_body(self, date_to_add: Union[Dict, Any],
                    key: Optional[str] = None) -> None:
        """
        Method add value to body
        if a `key` exists, then the date_to_add will be added by this `key`
        if the key doesn't exist then date_to_add must be a dictionary
         and the current __body will be updated
        :param date_to_add:
        :param str key:
        :return: None
        """
        try:
            if key is None:
                if isinstance(date_to_add, dict):
                    self.__body.update(date_to_add)
                else:
                    raise TypeError("date_to_add must be a dictionary if no key is specified")
            else:
                self.__body[key] = date_to_add
        except Exception as exc:
            raise exc

    def update_header(self, date_to_add: Union[Dict, Any],
                      key: Optional[str] = None) -> None:
        """
        Method add value to body
        if a `key` exists, then the date_to_add will be added by this `key`
        if the key doesn't exist then date_to_add must be a dictionary
         and the current __header will be updated
        :param date_to_add:
        :param key:
        :return: None
        """
        try:
            if key is None:
                if isinstance(date_to_add, dict):
                    self.__header.update(date_to_add)
                else:
                    raise TypeError("date_to_add must be a dictionary if no key is specified")
            else:
                self.__header[key] = date_to_add
        except Exception as exc:
            raise exc

    def get_body(self, returned_type_str: bool = True) -> Union[str, Dict]:
        """
        The method returns the body of the message str or dict for future processing
        :param bool returned_type_str: type string may be needed if send to queue
        :return: body in str or dict type
        """
        if returned_type_str:
            return json.dumps(self.__body)
        return self.__body

    def get_header(self, returned_type_str: bool = True) -> Union[str, Dict]:
        """
        The method returns the header of the message str or dict for future processing
        :param bool returned_type_str: type string may be needed if send to rabbit queue
        :return: header in str or dict type
        """
        if returned_type_str:
            return json.dumps(self.__header)
        return self.__header

    def get_source(self) -> str:
        """

        :return:
        """
        return self.__header.get('source', None)

    def set_source(self, new_source: str) -> None:
        """

        :param new_source:
        :return:
        """
        self.__header['source'] = new_source
