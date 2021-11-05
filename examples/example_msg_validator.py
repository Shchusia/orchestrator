"""
Example how setup service
"""
from typing import Any, Dict, Optional, TypeVar, Tuple

from pydantic import BaseModel, ValidationError

from orchestrator_service import Message
from orchestrator_service.service import (
    CommandHandlerPostStrategy,
    CommandHandlerStrategy,
    MessageValidator,
    Service,
    ServiceBlock,
    ServiceBuilder,
)


class MessageBodyStructure1(BaseModel):
    val: int


class MessageHeaderStructure1(BaseModel):
    command: str


class MessageBodyStructure2(BaseModel):
    val: str


class MessageHeaderStructure2(BaseModel):
    command: int


SubPydanticBaseModel = TypeVar("SubPydanticBaseModel", bound=BaseModel)


class MyMessageValidator1(MessageValidator):
    @staticmethod
    def validate(data_to_validate: Dict, validator) -> bool:
        try:
            validator(**data_to_validate)
            return True
        except ValidationError as exc:  # noqa
            return False
        except Exception as exc:  # noqa
            return False

    def validate_function(self, msg_to_validate: Message) -> bool:
        return self.validate(
            msg_to_validate.body, MessageBodyStructure1
        ) and self.validate(msg_to_validate.header, MessageHeaderStructure1)


class MyMessageValidator2(MessageValidator):
    @staticmethod
    def validate(data_to_validate: Dict, validator) -> bool:
        try:
            validator(**data_to_validate)
            return True
        except ValidationError as exc:  # noqa
            return False
        except Exception as exc:  # noqa
            return False

    def validate_function(self, msg_to_validate: Message) -> bool:
        return self.validate(
            msg_to_validate.body, MessageBodyStructure2
        ) and self.validate(msg_to_validate.header, MessageHeaderStructure2)


class FirstCommand(CommandHandlerStrategy):
    """
    Example first command
    """

    target_command = "first_command"

    def process(self, message: Message) -> Tuple[Message, Optional[Any]]:
        print("process 1")
        self.set_to_swap_scope("test_val", 1)

        return message, None


class SecondCommand(CommandHandlerStrategy):
    """
    Example second command
    """

    target_command = "second_command"

    def process(self, message: Message) -> Tuple[Message, Optional[Any]]:
        print("process 2")
        self.set_to_swap_scope("test_val", 1)

        return message, None


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
    is_catch_exceptions = True
    is_validate_msgs = True

    service_commands = ServiceBuilder(
        ServiceBlock(FirstCommand, msg_validator=MyMessageValidator1),
        ServiceBlock(
            SecondCommand,
        ),
        default_post_process=PPFirstCommand,
        default_msg_validator=MyMessageValidator2,
    )


if __name__ == "__main__":
    msg_1 = Message(body={"val": 1}, header={"command": "first_command"})
    msg_2 = Message(body={"val": 1}, header={"command": "second_command"})
    service = MyService()

    # valid
    processed = service.handle(msg_1)
    # >>> processed None
    print("processed:", processed)

    # invalid
    not_processed = service.handle(msg_2)
    # >>> not_processed <Message body: `{'val': 1}`
    #       header: `{'command': 'second_command'}`>
    print("not_processed:", not_processed)
