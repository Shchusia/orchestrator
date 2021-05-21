"""
ExampleFlow
"""
from orchestrator_service import Block
from orchestrator_service import Flow, FlowBlock, FlowBuilder
from orchestrator_service import Message, MessageCustom


class StepFirst(Block):
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


class StepSecond(Block):
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


class StepThird(Block):
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


class ExampleFlow(Flow):
    """
    Example flow
    """
    name_flow = 'example'
    steps_flow = FlowBuilder(
        FlowBlock(StepFirst()),
        FlowBlock(StepSecond,
                  post_handler_function='add_blocks'),
        FlowBlock(StepThird),
    )

    @staticmethod
    async def add_blocks(message: Message) -> Message:
        """
        Function for example how add process
        :param Message message:
        :return: Message
        """
        message.update_body('block', 'block')
        return message


if __name__ == '__main__':
    msg_2 = MessageCustom(body={}, header={'source': 'second'})
    msg_3 = MessageCustom(body={}, header={'source': 'third'})
    ef = ExampleFlow()
    print(ef.get_steps())
    ef.to_go_with_the_flow(msg_2)
    ef.to_go_with_the_flow(msg_3)
