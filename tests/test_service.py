"""
Tests for service builder
"""
# pylint: disable=missing-class-docstring,missing-function-docstring,invalid-name
from unittest import TestCase

from orchestrator import Message
from orchestrator.exc import DoublePostProcessFunctionDeclaredError
from orchestrator.exc import EmptyCommandsException
from orchestrator.exc import NotUniqueCommandError
from orchestrator.exc import ServiceBlockException
from orchestrator.service import CommandHandlerPostStrategy, CommandHandlerStrategy
from orchestrator.service import ServiceBlock, ServiceBuilder


class FirstCommand(CommandHandlerStrategy):
    """
    Example first command
    """
    target_command = 'first_command'

    def process(self, message: Message) -> Message:
        print('process 1')
        return message


class SecondCommand(CommandHandlerStrategy):
    """
    Example second command
    """
    target_command = 'second_command'

    def process(self, message: Message) -> Message:
        print('process 2')
        return message


class PPFirstCommand(CommandHandlerPostStrategy):
    """
    Example first post process handler
    """

    def post_process(self, msg: Message) -> None:
        print('post_process 1')


class TestServiceBlock(TestCase):

    def test_insufficient_args(self) -> None:
        self.assertRaises(TypeError, ServiceBlock, )
        self.assertRaises(ServiceBlockException, ServiceBlock, PPFirstCommand)
        self.assertRaises(ServiceBlockException, ServiceBlock, FirstCommand, SecondCommand)
        self.assertRaises(ServiceBlockException, ServiceBlock, FirstCommand, list)

    def test_correct(self) -> None:
        fc = FirstCommand()
        pp_fc = PPFirstCommand()
        sb_1 = ServiceBlock(FirstCommand, )
        self.assertTrue(isinstance(sb_1.process, CommandHandlerStrategy))
        self.assertIsNone(sb_1.post_process)
        sb_2 = ServiceBlock(process=fc,
                            post_process=pp_fc)
        self.assertEqual(fc, sb_2.process)
        self.assertEqual(pp_fc, sb_2.post_process)


class TestServiceBuilder(TestCase):
    def test_insufficient_args(self) -> None:
        self.assertRaises(TypeError, ServiceBuilder, list)
        self.assertRaises(EmptyCommandsException, ServiceBuilder)
        self.assertRaises(DoublePostProcessFunctionDeclaredError,
                          ServiceBuilder,
                          PPFirstCommand,
                          ServiceBlock(FirstCommand, PPFirstCommand),
                          default_post_process=PPFirstCommand
                          )

    def test_build(self):
        sb = ServiceBuilder(ServiceBlock(FirstCommand),
                            ServiceBlock(SecondCommand))

        self.assertRaises(NotUniqueCommandError,
                          ServiceBuilder(
                              ServiceBlock(FirstCommand),
                              ServiceBlock(FirstCommand)).build)
        dict_commands = sb.build()
        self.assertIn(FirstCommand.target_command, dict_commands.keys())
        self.assertIn(SecondCommand.target_command, dict_commands.keys())
        self.assertEqual(len(dict_commands.keys()), 2)

    def test_check_default_pp(self):
        self.assertIsNone(ServiceBuilder._check_default_pp())
        self.assertRaises(ServiceBlockException, ServiceBuilder._check_default_pp, FirstCommand)
        self.assertRaises(ServiceBlockException, ServiceBuilder._check_default_pp, FirstCommand())
        pp_fc = PPFirstCommand()
        self.assertEqual(pp_fc, ServiceBuilder._check_default_pp(pp_fc))
        self.assertTrue(isinstance(ServiceBuilder._check_default_pp(PPFirstCommand),
                                   PPFirstCommand))
