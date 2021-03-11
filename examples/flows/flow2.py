"""
Second flow example
"""
from orchestrator import Flow, FlowBlock, FlowBuilder
from ..blocks import *


class ExampleSecondFlow(Flow):
    """
    Example flow
    """
    name_flow = 'example2'
    steps_flow = FlowBuilder(
        FlowBlock(BlockFirst()),
        FlowBlock(BlockSecond),
    )
