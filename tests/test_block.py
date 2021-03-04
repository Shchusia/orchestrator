"""

"""
from unittest import TestCase

from orchestrator import Block
from orchestrator.message import Message


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
