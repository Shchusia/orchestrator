"""
Example how setup service
"""
from orchestrator_service import Message
from orchestrator_service.service import CommandHandlerPostStrategy
from orchestrator_service.service import CommandHandlerStrategy
from orchestrator_service.service import ServiceBlock, ServiceBuilder, Service


class FirstCommand(CommandHandlerStrategy):
    """
    Example first command
    """
    target_command = 'first_command'

    def process(self, msg: Message) -> Message:
        print('process 1')
        # set to global scope
        self.set_to_swap_scope('val', 1)
        return msg


class SecondCommand(CommandHandlerStrategy):
    """
    Example second command
    """
    target_command = 'second_command'

    def process(self, msg: Message) -> Message:
        print('process 2')
        # get value from scope
        print(self.get_from_swap_scope('val'))
        return msg


class ThirdCommand(CommandHandlerStrategy):
    """
    Example third command
    """
    target_command = 'third_command'

    def process(self, msg: Message) -> Message:
        print('process 3')
        return msg


class PPFirstCommand(CommandHandlerPostStrategy):
    """
    Example first post process handler
    """

    def post_process(self, msg: Message) -> None:
        print('post_process 1')


class PPSecondCommand(CommandHandlerPostStrategy):
    """
    Example second post process handler
    """

    def post_process(self, msg: Message) -> None:
        print('post_process 2')


# example builder
example_service_builder = ServiceBuilder(
    ServiceBlock(process=FirstCommand(),
                 post_process=PPFirstCommand()),
    ServiceBlock(process=SecondCommand()),
    ServiceBlock(process=ThirdCommand),
    default_post_process=PPSecondCommand())


class MyService(Service):
    """
    Custom service
    second use case
    """
    _default_command = 'first_command'
    service_commands = example_service_builder


if __name__ == '__main__':
    service = Service(example_service_builder,
                      default_command='first_command')
    my_service = MyService()
    msg_1 = Message(body={'val': 1}, header={'command': 'first_command'})
    msg_2 = Message(body={'val': 1}, header={'command': 'second_command'})
    msg_3 = Message(body={'val': 1}, header={'command': 'third_command'})
    msg_4 = Message(body={'val': 1}, header={})
    # running correct with there is both a handler
    # and a post handler and a command is specified
    service.handle(msg_1)
    # >>> process 1
    # >>> post_process 1

    # running command with default PP handlers
    service.handle(msg_2)
    # >>> process 2
    # >>> post_process 2
    service.handle(msg_3)
    # >>> process 3
    # >>> post_process 2

    # running default command
    service.handle(msg_4)
    # >>> process 1
    # >>> post_process 1

    # Run overridden service

    my_service.handle(msg_1)
    # >>> process 1
    # >>> post_process 1

    my_service.handle(msg_2)
    # >>> process 2
    # >>> post_process 2
    my_service.handle(msg_3)
    # >>> process 3
    # >>> post_process 2

    my_service.handle(msg_4)
    # >>> process 1
    # >>> post_process 1
