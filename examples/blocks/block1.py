"""
Example first block
"""
from service_orchestrator import Block
from service_orchestrator import Message


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
