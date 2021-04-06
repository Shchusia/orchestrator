"""
Example how use with aiopika
"""
import asyncio
import json
from logging import Logger

import aio_pika
from aio_pika import IncomingMessage

import examples.blocks as blocks
import examples.flows as flows
from orchestrator_service import Message
from orchestrator_service import Orchestrator

logger = Logger(__name__)


class MyOrchestrator(Orchestrator):
    """
    inheriting the base class of the orchestrator_service to add a queue handling method
    """

    async def queue_handler(self, message: IncomingMessage) -> None:
        """
        Queue handling method
        :param IncomingMessage message: message received from the queue
        :return: None
        """
        msg_orchestrator = Message(
            body=json.loads(message.body),
            header=dict(message.headers)
        )
        logger.debug(f'got message {msg_orchestrator}')
        self.handle(msg_orchestrator)


async def main(loop_service) -> None:
    """
    Main method service
    :param loop_service:
    :return:
    """
    name_queue = 'test'
    orchestrator_service = MyOrchestrator(flows, blocks)
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
        loop=loop_service
    )
    channel = await connection.channel()
    queue = await channel.declare_queue(name_queue)
    logger.info(f'Started listening to the queue `{name_queue}`')
    await queue.consume(orchestrator_service.queue_handler, no_ack=True)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop))
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info('Stopped listening to the queue')
        loop.call_soon_threadsafe(loop.stop)
