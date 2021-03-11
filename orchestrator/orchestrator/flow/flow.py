"""
Module with Flow
"""
# pylint: disable=too-few-public-methods
from __future__ import annotations

from typing import Union

from orchestrator.message import Message
from .exc import FlowBlockException
from .exc import FlowBuilderException
from ..block import Block


class FlowBlock:
    """
    Block for FlowBuilder
    """
    obj_block: Union[Block, type] = None

    def __init__(self,
                 obj_block,
                 pre_handler_function=None,
                 post_handler_function=None):
        """
        Init FlowBlock
        :param obj_block: type stepBlock
        :param pre_handler_function
        :param  post_handler_function
        """
        try:
            if isinstance(obj_block, type):
                if getattr(obj_block, '__base__'):
                    if obj_block.__base__.__name__ == 'Block':
                        self.obj_block = obj_block

                        self.pre_handler_function = str(pre_handler_function)
                        self.post_handler_function = str(post_handler_function)
                        return

            elif issubclass(type(obj_block), Block):
                self.obj_block = obj_block

                self.pre_handler_function = str(pre_handler_function)
                self.post_handler_function = str(post_handler_function)
                return

            raise FlowBlockException(type(obj_block))
        except FlowBlockException as exc:
            raise exc
        except Exception as exc :
            raise TypeError("Incorrect type `obj_block`")

    def init_block(self, instance_main: Flow) -> Block:
        """
        Method init instance subclass MainBlock
        :param instance_main:
        :return: object subclass MainBlock
        """
        if not isinstance(instance_main, Flow):
            raise TypeError("Value `instance_main` must be a Flow")
        if isinstance(self.obj_block, type):
            self.obj_block = self.obj_block(
                pre_handler_function=getattr(instance_main, self.pre_handler_function, None),
                post_handler_function=getattr(instance_main, self.post_handler_function, None),
            )
        else:
            self.obj_block.pre_handler_function = getattr(instance_main,
                                                          self.pre_handler_function,
                                                          None)
            self.obj_block.post_handler_function = getattr(instance_main,
                                                           self.post_handler_function,
                                                           None)
        return self.obj_block


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
        Build chain flow for StrategyFlow
        :param instance_main:
        :return:
        """
        flow = self.steps[0].init_block(instance_main)
        cur_step = flow
        for step in self.steps[1:]:
            cur_step = cur_step.set_next(step.init_block(instance_main))
        return flow


class Flow:
    """
    Class for inheritance for a specific flow
    """
    flow_chain: Block = None

    @property
    def name_flow(self):
        """
        Name current flow
        :return: name flow
        """
        raise NotImplementedError

    @property
    def steps_flow(self):
        """
        Steps current flow
        :return:
        """
        raise NotImplementedError

    @steps_flow.setter
    def steps_flow(self,
                   flow: FlowBuilder):
        """
        check the set value to property `steps_flow` value
        :param FlowBuilder flow: builder flow for current flow
        :return: None or exception
        """
        if isinstance(flow, FlowBuilder):
            self.steps_flow = flow
        else:
            raise TypeError('incorrect type flow builder')

    def __init__(self):
        """
        Init Flow
        """

        if isinstance(self.steps_flow, FlowBuilder):
            self.flow_chain = self.steps_flow.build_flow(self)
        else:
            raise TypeError(f"Incorrect type 'steps_flow' - it must be 'FlowBuilder',"
                            f" and not {type(self.steps_flow)}")

    def to_go_with_the_flow(self,
                            message: Message) -> None:
        """
        Method that starts flow execution from the first block
        :param message:
        :return: None
        """
        self.flow_chain.handle(message)

    def get_steps(self) -> str:
        """
        Print steps flow
        :return:
        """
        return self.flow_chain.get_list_flow()
