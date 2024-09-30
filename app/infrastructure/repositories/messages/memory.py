from dataclasses import dataclass, field

from domain.entities.messages import Chat
from infrastructure.repositories.messages.base import BaseChatsRepository


@dataclass
class MemoryChatsRepository(BaseChatsRepository):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return bool(next(
                chat for chat in self._saved_chats if chat.title.as_generic_type() == title
            ))
        except StopIteration:
            return False

    async def get_chat_by_id(self, chat_id: str) -> Chat | None:
        try:
            return next(
                chat for chat in self._saved_chats if chat.id == chat_id
            )
        except StopIteration:
            return None

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)
