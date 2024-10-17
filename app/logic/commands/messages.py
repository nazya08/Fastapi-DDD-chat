from dataclasses import dataclass

from domain.entities.messages import Chat, Message
from domain.value_objects.messages import Title, Text
from infrastructure.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.messages import ChatWithThatTitleAlreadyExistsException, ChatNotFoundException


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chats_repository: BaseChatsRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chats_repository.check_chat_exists_by_title(command.title):
            raise ChatWithThatTitleAlreadyExistsException(command.title)

        title = Title(value=command.title)
        new_chat = Chat.create_chat(title=title)

        await self.chats_repository.add_chat(new_chat)
        await self._mediator.publish(new_chat.pull_events())

        return new_chat


@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    text: str
    chat_id: str


@dataclass(frozen=True)
class CreateMessageCommandHandler(CommandHandler[CreateMessageCommand, Message]):
    messages_repository: BaseMessagesRepository
    chats_repository: BaseChatsRepository

    async def handle(self, command: CreateMessageCommand) -> Message:
        chat = await self.chats_repository.get_chat_by_id(chat_id=command.chat_id)

        if not chat:
            raise ChatNotFoundException(chat_id=command.chat_id)
        message = Message(text=Text(value=command.text), chat_id=command.chat_id)
        chat.add_message(message=message)

        await self.messages_repository.add_message(message=message)

        return message
