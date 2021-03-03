"""
Module with a flow builder
"""
# pylint: disable=too-few-public-methods
from .exc import FlowBuilderException
from .flow import Flow
from .flow_block import FlowBlock
from ..block import Block


class FlowBuilder:
    """
    Flow building class
    build chain flow from flow blocks
    """

    def __init__(self,
                 step: FlowBlock,
                 *args):
        """
        Init FlowBuilder
        :param FlowBlock step: first block in flow
        :param List[FlowBlock] args:  other steps  if value exsst
        """
        self.steps = list(args)
        self.steps.insert(0, step)
        for _index, _step in enumerate(self.steps):
            if not isinstance(_step, FlowBlock):
                raise FlowBuilderException(f'on index {_index}')

    def build_flow(self, instance_main: Flow) -> Block:
        """
        Byild chain flow for StrategyFlow
        :param instance_main:
        :return:
        """
        flow = self.steps[0].init_block(instance_main)
        cur_step = flow
        for step in self.steps[1:]:
            cur_step = cur_step.set_next(step.init_block(instance_main))
        return flow
