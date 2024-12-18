from abc import ABC
from dataclasses import dataclass
from typing import Iterable

from motor.core import AgnosticClient

from domain.entities.messages import Chat, Message
from infrastructure.repositories.filters.messages import GetMessagesFilters
from infrastructure.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from infrastructure.repositories.messages.converters import convert_chat_entity_to_document, \
    convert_message_entity_to_document, convert_chat_document_to_entity, convert_message_document_to_entity


@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]


@dataclass
class MongoDBChatsRepository(BaseChatsRepository, BaseMongoDBRepository):
    async def get_chat_by_id(self, chat_id: str) -> Chat | None:
        chat_document = await self._collection.find_one(filter={'id': chat_id})

        if not chat_document:
            return None

        return convert_chat_document_to_entity(chat_document)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        return bool(await self._collection.find_one(filter={'title': title}))

    async def add_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(convert_chat_entity_to_document(chat))


@dataclass
class MongoDBMessagesRepository(BaseMessagesRepository, BaseMongoDBRepository):
    async def add_message(self, message: Message) -> None:
        await self._collection.insert_one(
            convert_message_entity_to_document(message)
        )

    async def get_messages(self, chat_id: str, filters: GetMessagesFilters) -> tuple[Iterable[Message], int]:
        find = {'chat_id': chat_id}

        cursor = self._collection.find(filter=find).skip(filters.offset).limit(filters.limit)
        count = await self._collection.count_documents(filter=find)

        messages = [
            convert_message_document_to_entity(message_document=message_document)
            async for message_document in cursor
        ]

        return messages, count
