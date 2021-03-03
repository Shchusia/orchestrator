"""
Module with flow block
"""
# pylint: disable=too-few-public-methods
from .exc import FlowBlockException
from .flow import Flow
from ..block import Block


class FlowBlock:
    """
    Block for FlowBuilder
    """

    def __init__(self,
                 obj_block,
                 pre_handler_function=None,
                 post_handler_function=None,
                 **kwargs):
        """
        Init FlowBlock
        :param obj_block: type stepBlock
        :param pre_handler_function
        :param post_handler_function
        :param kwargs: additional arguments for future
        """
        if isinstance(obj_block, type):
            if obj_block.__base__.__name__ == 'MainBlock':
                self.obj_block = obj_block

                self.pre_handler_function = str(pre_handler_function)
                self.post_handler_function = str(post_handler_function)
                self.kwargs = kwargs
                return

        raise FlowBlockException(f'{obj_block.__base__.__name__}. '
                                 f'Name incorrect block {obj_block.__name__}')

    def init_block(self, instance_main: Flow) -> Block:
        """
        Method init instance subclass MainBlock
        :param instance_main:
        :return: object subclass MainBlock
        """
        return self.obj_block(
            pre_handler_function=getattr(instance_main, self.pre_handler_function, None),
            post_handler_function=getattr(instance_main, self.post_handler_function, None),
            **self.kwargs
        )
