"""
Example second block
"""
from orchestrator_service import Block
from orchestrator_service import Message


class BlockSecond(Block):
    """
    second block
    """
    name_block = 'second'

    def process(self, message: Message) -> None:
        """
        process function
        :param Message message:
        :return: Nothing
        """
        print(self.name_block)
        print(message)
