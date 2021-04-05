"""
Example second block
"""
from service_orchestrator import Block
from service_orchestrator import Message


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
