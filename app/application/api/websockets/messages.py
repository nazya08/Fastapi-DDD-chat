from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket

router = APIRouter(tags=['chats'],)


@router.websocket('{chat_id}')
async def messages_handler(chat_id: str, websocket: WebSocket):
    await websocket.accept()
