from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    message_text: str
    message_id: str
    chat_id: str
