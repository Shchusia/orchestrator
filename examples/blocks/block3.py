"""
Example third block
"""
from orchestrator import Block
from orchestrator import Message


class BlockThird(Block):
    """
    third block
    """
    name_block = 'third'
    name_queue = ''

    def process(self, message: Message) -> None:
        """
        process function
        :param Message message:
        :return: Nothing
        """
        print(self.name_block)
        print(message)
