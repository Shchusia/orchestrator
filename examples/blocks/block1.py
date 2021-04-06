"""
Example first block
"""
from orchestrator_service import Block
from orchestrator_service import Message


class BlockFirst(Block):
    """
    first block
    """
    name_block = 'first'

    def process(self, message: Message) -> None:
        """
        process function
        :param Message message:
        :return: Nothing
        """
        print(self.name_block)
        print(message)
