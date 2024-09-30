from dataclasses import dataclass

from domain.entities.messages import Chat
from infrastructure.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from logic.exceptions.messages import ChatNotFoundException
from logic.queries.base import BaseQuery, QueryHandler


@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_id: str


@dataclass(frozen=True)
class GetChatDetailQueryHandler(QueryHandler[GetChatDetailQuery, Chat]):
    chats_repository: BaseChatsRepository
    messages_repository: BaseMessagesRepository  # TODO: get messages separately

    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat = await self.chats_repository.get_chat_by_id(chat_id=query.chat_id)

        if not chat:
            raise ChatNotFoundException(chat_id=query.chat_id)

        return chat
