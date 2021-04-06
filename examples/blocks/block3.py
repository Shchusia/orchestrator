"""
Example third block
"""
from orchestrator_service import Block
from orchestrator_service import Message


class BlockThird(Block):
    """
    third block
    """
    name_block = 'third'

    def process(self, message: Message) -> None:
        """
        process function
        :param Message message:
        :return: Nothing
        """
        print(self.name_block)
        print(message)
