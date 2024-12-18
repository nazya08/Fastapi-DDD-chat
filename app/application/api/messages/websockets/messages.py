from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket
from punq import Container

from application.api.common.websockets.managers import BaseConnectionManager
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
    config: Config = container.resolve(Config)
    connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)
    print(connection_manager.connections_map)

    await connection_manager.accept_connection(websocket=websocket, key=chat_id)

    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)

    try:
        async for message in message_broker.start_consuming(
            topic=config.new_message_received_event_topic
        ):

            await connection_manager.send_all(key=chat_id, json_message=message)
    finally:
        await connection_manager.remove_connection(websocket=websocket, key=chat_id)
        await message_broker.stop_consuming()

    await message_broker.stop_consuming()
    await websocket.close(reason="Chat closed")
