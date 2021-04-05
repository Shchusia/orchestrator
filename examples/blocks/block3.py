"""
Example third block
"""
from service_orchestrator import Block
from service_orchestrator import Message


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
