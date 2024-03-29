"""
Tests for service builder
"""
# pylint: disable=missing-class-docstring,missing-function-docstring,invalid-name
from typing import Any, Optional
from unittest import TestCase

from orchestrator_service import Message
from orchestrator_service.exc import (
    DoublePostProcessFunctionDeclaredError,
    EmptyCommandsException,
    NotUniqueCommandError,
    ServiceBlockException,
)
from orchestrator_service.service import (
    CommandHandlerPostStrategy,
    CommandHandlerStrategy,
    Service,
    ServiceBlock,
    ServiceBuilder,
)


class FirstCommand(CommandHandlerStrategy):
    """
    Example first command
    """

    target_command = "first_command"

    def process(self, message: Message) -> Message:
        print("process 1")
        self.set_to_swap_scope("test_val", 1)

        return message

    async def aprocess(self, message: Message) -> Message:
        print("process 1")
        return message


class SecondCommand(CommandHandlerStrategy):
    """
    Example second command
    """

    target_command = "second_command"

    def process(self, message: Message) -> Message:
        print("process 2")
        val = self.get_from_swap_scope("test_val")
        if not val:
            raise ValueError
        if val == 1:
            raise AttributeError("not error just for test")
        return message

    async def aprocess(self, message: Message) -> Message:
        print("process 2")
        return message


class ThirdCommand(CommandHandlerStrategy):
    """
    Example third command
    """

    target_command = "third_command"

    def process(self, message: Message) -> Message:
        print("process 3")
        command = self.get_service_command(self.target_command)
        assert command == self
        return message

    async def aprocess(self, message: Message) -> Message:
        print("process 3")
        return message


class FourthCommand(CommandHandlerStrategy):
    """
    Example third command
    """

    target_command = "fourth_command"

    def process(self, message: Message) -> Message:
        print("process 4")
        command = self.get_service_command(self.target_command)
        print("com", command)
        assert command == "other object"
        return message

    async def aprocess(self, message: Message) -> Message:
        print("process 4")
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


class MyService(Service):
    _default_command = FirstCommand.target_command
    service_commands = ServiceBuilder(
        ServiceBlock(FirstCommand),
        ServiceBlock(SecondCommand),
        ServiceBlock(ThirdCommand),
        ServiceBlock(FourthCommand),
        default_post_process=PPFirstCommand,
    )


class TestServiceBlock(TestCase):
    def test_insufficient_args(self) -> None:
        self.assertRaises(
            TypeError,
            ServiceBlock,
        )
        self.assertRaises(ServiceBlockException, ServiceBlock, PPFirstCommand)
        self.assertRaises(
            ServiceBlockException, ServiceBlock, FirstCommand, SecondCommand
        )
        self.assertRaises(ServiceBlockException, ServiceBlock, FirstCommand, list)

    def test_correct(self) -> None:
        fc = FirstCommand()
        pp_fc = PPFirstCommand()
        sb_1 = ServiceBlock(
            FirstCommand,
        )
        self.assertTrue(isinstance(sb_1.process, CommandHandlerStrategy))
        self.assertIsNone(sb_1.post_process)
        sb_2 = ServiceBlock(process=fc, post_process=pp_fc)
        self.assertEqual(fc, sb_2.process)
        self.assertEqual(pp_fc, sb_2.post_process)


class TestServiceBuilder(TestCase):
    def test_insufficient_args(self) -> None:
        self.assertRaises(TypeError, ServiceBuilder, list)
        self.assertRaises(EmptyCommandsException, ServiceBuilder)
        self.assertRaises(
            DoublePostProcessFunctionDeclaredError,
            ServiceBuilder,
            PPFirstCommand,
            ServiceBlock(FirstCommand, PPFirstCommand),
            default_post_process=PPFirstCommand,
        )

    def test_build(self):
        sb = ServiceBuilder(ServiceBlock(FirstCommand), ServiceBlock(SecondCommand))

        self.assertRaises(
            NotUniqueCommandError,
            ServiceBuilder(
                ServiceBlock(FirstCommand), ServiceBlock(FirstCommand)
            ).build,
        )
        dict_commands = sb.build()
        self.assertIn(FirstCommand.target_command, dict_commands.keys())
        self.assertIn(SecondCommand.target_command, dict_commands.keys())
        self.assertEqual(len(dict_commands.keys()), 2)

    def test_check_default_pp(self):
        self.assertIsNone(ServiceBuilder._check_default_pp())
        self.assertRaises(
            ServiceBlockException, ServiceBuilder._check_default_pp, FirstCommand
        )
        self.assertRaises(
            ServiceBlockException, ServiceBuilder._check_default_pp, FirstCommand()
        )
        pp_fc = PPFirstCommand()
        self.assertEqual(pp_fc, ServiceBuilder._check_default_pp(pp_fc))
        self.assertTrue(
            isinstance(ServiceBuilder._check_default_pp(PPFirstCommand), PPFirstCommand)
        )


class TestService(TestCase):
    def setUp(self) -> None:
        self.service = MyService(is_catch_exceptions=False)
        self.msg_first = Message(
            body={}, header={"command": FirstCommand.target_command}
        )
        self.msg_second = Message(
            body={}, header={"command": SecondCommand.target_command}
        )
        self.msg_third = Message(
            body={}, header={"command": ThirdCommand.target_command}
        )
        self.msg_fourth = Message(
            body={}, header={"command": FourthCommand.target_command}
        )

    def test_single_scope(self):
        self.assertRaises(ValueError, self.service.handle, self.msg_second)

        self.service.handle(self.msg_first)
        self.assertRaises(AttributeError, self.service.handle, self.msg_second)

    def test_get_service_command(self):
        self.service.handle(self.msg_third)

        self.assertRaises(AssertionError, self.service.handle, self.msg_fourth)
