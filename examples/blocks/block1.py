"""
Example first block
"""
from orchestrator import Block
from orchestrator import Message


class BlockFirst(Block):
    """
    first block
    """
    name_block = 'first'
    name_queue = ''

    def process(self, message: Message) -> None:
        """
        process function
        :param Message message:
        :return: Nothing
        """
        print(self.name_block)
        print(message)
