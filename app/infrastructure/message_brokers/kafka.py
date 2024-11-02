from dataclasses import dataclass, field
from typing import AsyncIterator

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from orjson import orjson

from infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer
    consumer_map: dict[str, AIOKafkaConsumer] = field(
        default_factory=dict, kw_only=True
    )

    async def start(self) -> None:
        await self.producer.start()
        await self.consumer.start()

    async def send_message(self, topic: str, key: bytes, value: bytes) -> None:
        await self.producer.send(topic=topic, key=key, value=value)

    async def close(self) -> None:
        await self.producer.stop()
        await self.consumer.stop()

    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            yield orjson.loads(message.value)

    async def stop_consuming(self) -> None:
        self.consumer.unsubscribe()
