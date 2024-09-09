from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from domain.value_objects.messages import Text, Title


@dataclass
class Message:
    id: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )
    text: Text
    created_at: str = field(
        default_factory=datetime.now,
        kw_only=True,
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: 'Message') -> bool:
        return self.id == __value.id


@dataclass
class Chat:
    id: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )
    title: Title
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True,
    )
    created_at: str = field(
        default_factory=datetime.now,
        kw_only=True,
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: 'Chat') -> bool:
        return self.id == __value.id

    def add_message(self, message: Message) -> None:
        self.messages.add(message)
