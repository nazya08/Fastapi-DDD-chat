from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseMessageBroker(ABC):
    @abstractmethod
    async def start(self) -> None:
        ...

    @abstractmethod
    async def send_message(self, topic: str, key: bytes, value: bytes) -> None:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...

    @abstractmethod
    async def start_consuming(self, topic: str):
        ...

    @abstractmethod
    async def consume(self) -> dict:
        ...

    @abstractmethod
    async def stop_consuming(self) -> None:
        ...
