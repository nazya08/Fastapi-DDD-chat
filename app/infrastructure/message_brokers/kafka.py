from dataclasses import dataclass

from aiokafka import AIOKafkaProducer

from infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer

    async def send_message(self, topic: str, key: bytes, value: bytes) -> None:
        await self.producer.send(topic=topic, key=key, value=value)

    async def consume(self, topic: str) -> None:
        pass
