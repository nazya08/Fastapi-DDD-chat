from dataclasses import dataclass
from typing import ClassVar

from domain.events.base import BaseEvent


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    message_text: str
    message_id: str
    chat_id: str

    title: ClassVar[str] = "New Message Received"


@dataclass
class NewChatCreatedEvent(BaseEvent):
    chat_id: str
    chat_title: str

    title: ClassVar[str] = "New Chat Created"

