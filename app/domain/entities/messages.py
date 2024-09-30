from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.events.messages import NewMessageReceivedEvent, NewChatCreated
from domain.value_objects.messages import Text, Title


@dataclass(eq=False)
class Message(BaseEntity):
    text: Text
    chat_id: str


@dataclass(eq=False)
class Chat(BaseEntity):
    title: Title
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True,
    )

    @classmethod
    def create_chat(cls, title: Title) -> 'Chat':
        new_chat = cls(title=title)
        new_chat.register_event(NewChatCreated(chat_id=new_chat.id, chat_title=new_chat.title.as_generic_type()))

        return new_chat

    def add_message(self, message: Message) -> None:
        self.messages.add(message)
        self.register_event(NewMessageReceivedEvent(
            message_text=message.text.as_generic_type(), chat_id=self.id, message_id=message.id)
        )
