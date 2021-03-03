"""
Module with class Flow
"""
from orchestrator.message import Message
from .flow_builder import FlowBuilder
from ..block import Block


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
