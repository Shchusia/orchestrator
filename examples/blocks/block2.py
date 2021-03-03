"""
Example second block
"""
from orchestrator import Block
from orchestrator import Message


class BlockSecond(Block):
    """
    second block
    """
    name_block = 'second'
    name_queue = ''

    def process(self, message: Message) -> None:
        """
        process function
        :param Message message:
        :return: Nothing
        """
        print(self.name_block)
        print(message)
