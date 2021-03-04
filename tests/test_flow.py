"""

"""
from unittest import TestCase

from orchestrator import Block
from orchestrator import Message
from orchestrator.exc import FlowBlockException,FlowBuilderException
from orchestrator.orchestrator.flow import FlowBlock, Flow, FlowBuilder


class FirstBlockForTesting(Block):
    name_block = 'first_test_block'

    def process(self, message: Message):
        pass


class TestClass():
    pass


class TestFlow(Flow):
    name_flow = 'test'
    steps_flow = FlowBuilder(FlowBlock(FirstBlockForTesting))

    @staticmethod
    def func(message: Message):
        return message


class TestFlowBlock(TestCase):
    def test_insufficient_args(self) -> None:
        self.assertRaises(FlowBlockException, FlowBlock, "Block")
        self.assertRaises(FlowBlockException, FlowBlock, TestClass())
        self.assertRaises(FlowBlockException, FlowBlock, Block)

    def test_init_block(self):
        test_flow = TestFlow()
        first_test_flow_block = FlowBlock(FirstBlockForTesting)
        second_test_flow_block = FlowBlock(FirstBlockForTesting())
        self.assertRaises(TypeError, first_test_flow_block.init_block, TestClass())
        self.assertRaises(TypeError, second_test_flow_block.init_block, TestClass())

        first_block = first_test_flow_block.init_block(test_flow)
        self.assertTrue(isinstance(first_block, Block))
        self.assertIsNone(first_block.pre_handler_function)
        self.assertIsNone(first_block.post_handler_function)

        second_block = second_test_flow_block.init_block(test_flow)
        self.assertTrue(isinstance(second_block, Block))

        third_test_flow_block = FlowBlock(FirstBlockForTesting, post_handler_function='func')
        third_block = third_test_flow_block.init_block(test_flow)
        self.assertTrue(isinstance(third_block, Block))
        self.assertTrue(callable(third_block.post_handler_function))
        self.assertFalse(callable(third_block.pre_handler_function))
        self.assertIsNone(third_block.pre_handler_function)

        fourth_test_flow_block = FlowBlock(FirstBlockForTesting, post_handler_function='list')
        fourth_block = fourth_test_flow_block.init_block(test_flow)
        self.assertTrue(isinstance(fourth_block, Block))
        self.assertIsNone(fourth_block.pre_handler_function)
        self.assertIsNone(fourth_block.post_handler_function)


class TestFlowBuilder(TestCase):
    def test_insufficient_args(self) -> None:
        self.assertRaises(TypeError, FlowBuilder)
        self.assertRaises(FlowBuilderException, FlowBuilder, TestClass)
        self.assertRaises(FlowBuilderException, FlowBuilder, FirstBlockForTesting)
        self.assertRaises(FlowBuilderException, FlowBuilder, FlowBlock(FirstBlockForTesting), TestClass)
        self.assertRaises(FlowBuilderException, FlowBuilder, FlowBlock(FirstBlockForTesting), FirstBlockForTesting)

    def test_build_flow(self) -> None:
        test_flow = TestFlow()
        first_block = FirstBlockForTesting()
        first_builder = FlowBuilder(FlowBlock(first_block),
                                    FlowBlock(FirstBlockForTesting))
        block = first_builder.build_flow(test_flow)
        self.assertTrue(block == first_block)

