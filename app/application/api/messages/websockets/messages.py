from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket
from punq import Container

from infrastructure.message_brokers.base import BaseMessageBroker
from logic.init import init_container
from settings.config import Config

router = APIRouter(tags=['chats'],)


@router.websocket("/{chat_id}/")
async def websocket_endpoint(
        chat_id: UUID,
        websocket: WebSocket,
        container: Container = Depends(init_container),
):
    await websocket.accept()
    config: Config = container.resolve(Config)
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)

    await message_broker.start_consuming(
            topic=config.new_message_received_event_topic.format(chat_id=chat_id)
    )
    while True:
        try:
            await websocket.send_json(await message_broker.consume())
        finally:
            break

    await message_broker.stop_consuming()
    await websocket.close(reason="Chat closed")
