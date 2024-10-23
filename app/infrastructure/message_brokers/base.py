from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseMessageBroker(ABC):

    @abstractmethod
    async def send_message(self, topic: str, key: bytes, value: bytes) -> None:
        ...

    @abstractmethod
    async def consume(self, topic: str) -> None:
        ...