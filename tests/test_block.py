"""

"""
from unittest import TestCase

from orchestrator_service import Block
from orchestrator_service.message import Message


class FirstBlockForTesting(Block):
    name_block = 'first_test_block'

    def process(self, message: Message):
        pass


class SecondBlockForTesting(Block):
    name_block = 'second_test_block'

    def process(self, message: Message):
        pass


class TestBlock(TestCase):

    def setUp(self) -> None:
        pass

    def test_insufficient_args(self) -> None:
        self.assertRaises(TypeError,
                          FirstBlockForTesting,
                          SecondBlockForTesting)

    def test_get_list_flow(self) -> None:
        pass

    def test_set_next(self) -> None:
        f_block = FirstBlockForTesting()
        s_block = SecondBlockForTesting()
        new_block = f_block.set_next(s_block)
        self.assertTrue(new_block == s_block)

    def test_handle(self):
        pass
