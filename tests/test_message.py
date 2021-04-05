"""
Test Message
"""
from unittest import TestCase

from orchestrator_service.message import Message


class TestMessage(TestCase):

    def setUp(self) -> None:
        self.body = {
            "test_body_value_1": "value",
            "test_body_value_2": 1,
            "test_body_value_3": [1, 2, 3],
            "test_body_value_4": {
                "test_body_value_4_1": 1,
                "test_body_value_4_2": "val"
            },
        }
        self.header = {
            "test_header_value_1": "value",
            "test_header_value_2": 1,
        }
        self.data_to_body_add = {
            "added_body_data": "data"
        }
        self.key_to_body_add_1 = "test_body_added_key_value_1"
        self.key_to_body_add_2 = "test_body_added_key_value_2"
        self.value_to_body_add = "value_body_3"

        self.data_to_header_add = {
            "added_header_data": "data"
        }
        self.key_to_header_add_1 = "test_header_added_key_value_1"
        self.key_to_header_add_2 = "test_header_added_key_value_2"
        self.value_to_header_add = "value_header_3"

        self.test_message = Message(body=self.body,
                                    header=self.header)

    def test_insufficient_args(self) -> None:
        self.assertRaises(TypeError, Message)
        self.assertRaises(TypeError, Message,
                          1)
        self.assertRaises(TypeError, Message,
                          1, dict())
        self.assertRaises(TypeError, Message,
                          "1", dict())
        self.assertRaises(TypeError, Message,
                          dict(), 1)
        self.assertRaises(TypeError, Message,
                          dict(), "1")
        self.assertRaises(TypeError, Message,
                          dict(), dict)
        self.assertRaises(TypeError, Message,
                          dict(), list())

    def test_body_property(self) -> None:
        with self.assertRaises(TypeError):
            self.test_message.body = 12345
        with self.assertRaises(TypeError):
            self.test_message.body = "12345"
        with self.assertRaises(TypeError):
            self.test_message.body = [1, 2, 3, 4, 5]
        with self.assertRaises(TypeError):
            self.test_message.body = None

        self.assertDictEqual(self.test_message.body, self.body)

    def test_header_property(self) -> None:
        with self.assertRaises(TypeError):
            self.test_message.header = 12345
        with self.assertRaises(TypeError):
            self.test_message.header = "12345"
        with self.assertRaises(TypeError):
            self.test_message.header = [1, 2, 3, 4, 5]
        with self.assertRaises(TypeError):
            self.test_message.header = None
        self.assertDictEqual(self.test_message.header, self.header)

    def test_update_body(self) -> None:
        self.test_message.update_body(self.data_to_body_add)
        self.body.update(self.data_to_body_add)
        self.assertDictEqual(self.test_message.body, self.body)

        with self.assertRaises(TypeError):
            self.test_message.update_body("test")
        with self.assertRaises(TypeError):
            self.test_message.update_body(12345)
        with self.assertRaises(TypeError):
            self.test_message.update_body([1, 2, 3, 4, 5])

        self.test_message.update_body(self.value_to_body_add, self.key_to_body_add_1)
        self.body[self.key_to_body_add_1] = self.value_to_body_add
        self.assertDictEqual(self.test_message.body, self.body)

        self.test_message.update_body(self.data_to_body_add, self.key_to_body_add_2)
        self.body[self.key_to_body_add_2] = self.data_to_body_add
        self.assertDictEqual(self.test_message.body, self.body)

    def test_update_header(self) -> None:
        self.test_message.update_header(self.data_to_header_add)
        self.header.update(self.data_to_header_add)
        self.assertDictEqual(self.test_message.header, self.header)

        with self.assertRaises(TypeError):
            self.test_message.update_header("test")
        with self.assertRaises(TypeError):
            self.test_message.update_header(12345)
        with self.assertRaises(TypeError):
            self.test_message.update_header([1, 2, 3, 4, 5])

        self.test_message.update_header(self.value_to_header_add, self.key_to_header_add_1)
        self.header[self.key_to_header_add_1] = self.value_to_header_add
        self.assertDictEqual(self.test_message.header, self.header)

        self.test_message.update_header(self.data_to_header_add, self.key_to_header_add_2)
        self.header[self.key_to_header_add_2] = self.data_to_header_add
        self.assertDictEqual(self.test_message.header, self.header)

    def test_get_body(self) -> None:
        self.assertDictEqual(self.test_message.get_body(returned_type_str=False), self.body)
        self.assertEqual(type(self.test_message.get_body(returned_type_str=False)), dict)
        # strings are not compared
        # self.assertEqual(self.test_message.get_body(returned_type_str=False), json.dumps(self.body))
        self.assertEqual(type(self.test_message.get_body(returned_type_str=True)), str)

    def test_get_header(self) -> None:
        self.assertDictEqual(self.test_message.get_header(returned_type_str=False), self.header)
        self.assertEqual(type(self.test_message.get_header(returned_type_str=False)), dict)
        # strings are not compared
        # self.assertEqual(self.test_message.get_header(returned_type_str=False), json.dumps(self.header))
        self.assertEqual(type(self.test_message.get_header(returned_type_str=True)), str)

    def test_source_methods(self) -> None:
        self.assertIsNone(self.test_message.get_source())

        name_source = "test_source"
        self.test_message.set_source(name_source)
        self.assertEqual(self.test_message.get_source(),
                         name_source)
