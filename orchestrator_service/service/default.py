"""
module with default classes
"""
from typing import Optional, Any

from .to_extends import CommandHandlerPostStrategy
from ..message import Message


class DoNothingStrategy(CommandHandlerPostStrategy):
    """
    Default post-processing strategy that does nothing
    """

    def post_process(self, msg: Message, additional_data: Optional[Any] = None) -> None:
        return

    async def apost_process(self, msg: Message, additional_data: Optional[Any] = None) -> None:
        return
