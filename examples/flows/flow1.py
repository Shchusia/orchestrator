"""
First flow example
"""
from orchestrator_service import Flow, FlowBlock, FlowBuilder
from orchestrator_service import Message
from ..blocks import *


class ExampleFirstFlow(Flow):
    """
    Example flow
    """
    name_flow = 'example'
    steps_flow = FlowBuilder(
        FlowBlock(BlockFirst()),
        FlowBlock(BlockSecond, post_handler_function='add_blocks'),
        FlowBlock(BlockThird),
    )

    @staticmethod
    def add_blocks(message: Message) -> Message:
        """
        Function for example how add process
        :param Message message:
        :return: Message
        """
        message.update_body('block', 'block')
        return message
