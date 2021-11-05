"""
Tests for service builder
"""
# pylint: disable=missing-class-docstring,missing-function-docstring,invalid-name
from typing import Any, Optional
from unittest import TestCase

from orchestrator_service import Message
from orchestrator_service.exc import ServiceBlockException
from orchestrator_service.service import (
    CommandHandlerPostStrategy,
    CommandHandlerStrategy,
    MessageValidator,
    Service,
    ServiceBlock,
    ServiceBuilder,
)


class AllValidMsgs(MessageValidator):
    def validate_function(self, msg_to_validate: Message) -> bool:
        return True


class AllInvalidMsgs(MessageValidator):
    def validate_function(self, msg_to_validate: Message) -> bool:
        return False


class FirstCommand(CommandHandlerStrategy):
    """
    Example first command
    """

    target_command = "first_command"

    def process(self, message: Message) -> Message:
        print("process 1")
        self.set_to_swap_scope("test_val", 1)

        return message


class SecondCommand(CommandHandlerStrategy):
    """
    Example second command
    """

    target_command = "second_command"

    def process(self, message: Message) -> Message:
        print("process 2")
        self.set_to_swap_scope("test_val", 1)

        return message


class PPFirstCommand(CommandHandlerPostStrategy):
    """
    Example first post process handler
    """

    def post_process(self, msg: Message, additional_data: Optional[Any] = None) -> None:
        print("post_process 1")

    async def apost_process(
        self, msg: Message, additional_data: Optional[Any] = None
    ) -> None:
        print("post_process 1")


class MyFirstService(Service):
    _default_command = FirstCommand.target_command
    is_catch_exceptions = True
    is_validate_msgs = True

    service_commands = ServiceBuilder(
        ServiceBlock(FirstCommand, msg_validator=AllValidMsgs),
        ServiceBlock(SecondCommand, msg_validator=AllValidMsgs),
        default_post_process=PPFirstCommand,
        default_msg_validator=AllInvalidMsgs,
    )


class MySecondService(Service):
    _default_command = FirstCommand.target_command
    is_validate_msgs = True
    is_catch_exceptions = True

    service_commands = ServiceBuilder(
        ServiceBlock(FirstCommand, msg_validator=AllValidMsgs),
        ServiceBlock(SecondCommand),
        default_post_process=PPFirstCommand,
        default_msg_validator=AllInvalidMsgs,
    )


class MyThirdService(Service):
    _default_command = FirstCommand.target_command
    is_validate_msgs = True
    is_catch_exceptions = True
    _default_msg_validator = AllInvalidMsgs

    service_commands = ServiceBuilder(
        ServiceBlock(FirstCommand, msg_validator=AllValidMsgs),
        ServiceBlock(
            SecondCommand,
        ),
        default_post_process=PPFirstCommand,
        default_msg_validator=AllValidMsgs,
    )


class MyFourthService(Service):
    _default_command = FirstCommand.target_command
    is_validate_msgs = True
    is_catch_exceptions = True
    _default_msg_validator = AllInvalidMsgs

    service_commands = ServiceBuilder(
        ServiceBlock(FirstCommand, msg_validator=AllValidMsgs),
        ServiceBlock(
            SecondCommand,
        ),
        default_post_process=PPFirstCommand,
    )


# class MyFifthService(Service):
#     default_command = FirstCommand.target_command
#     is_validate_msgs = True
#     is_catch_exceptions = True
#     _default_msg_validator = AllInvalidMsgs
#
#     service_commands = ServiceBuilder(
#         ServiceBlock(FirstCommand, msg_validator=AllValidMsgs),
#         ServiceBlock(SecondCommand, ),
#         default_post_process=PPFirstCommand)


class TestMessageValidator(TestCase):
    def setUp(self):
        self.msg_1 = Message(body={"val": 1}, header={"command": "first_command"})
        self.msg_2 = Message(body={"val": 1}, header={"command": "second_command"})

        self.first_service = MyFirstService()
        self.second_service = MySecondService()
        self.third_service = MyThirdService()
        self.fourth_service = MyFourthService()

    def test_insufficient_args(self) -> None:
        self.assertRaises(TypeError, ServiceBlock)
        self.assertRaises(ServiceBlockException, ServiceBlock, PPFirstCommand)
        self.assertRaises(
            ServiceBlockException, ServiceBlock, FirstCommand, SecondCommand
        )
        self.assertRaises(
            ServiceBlockException,
            ServiceBlock,
            FirstCommand,
            msg_validator=SecondCommand(),
        )
        self.assertRaises(
            ServiceBlockException,
            ServiceBlock,
            FirstCommand,
            msg_validator=PPFirstCommand,
        )

    def test_first_scenario(self):
        """
        Without errors
        """
        self.assertIsNone(self.first_service.handle(self.msg_1))
        self.assertIsNone(self.first_service.handle(self.msg_2))

    def test_second_scenario(self):
        """
        With errors
        """
        self.assertIsNone(self.second_service.handle(self.msg_1))
        self.assertIsNotNone(self.second_service.handle(self.msg_2))

    def test_third_scenario(self):
        self.assertIsNone(self.third_service.handle(self.msg_1))
        self.assertIsNone(self.third_service.handle(self.msg_2))

    def test_fourth_scenario(self):
        self.assertIsNone(self.fourth_service.handle(self.msg_1))
        self.assertIsNotNone(self.fourth_service.handle(self.msg_2))
