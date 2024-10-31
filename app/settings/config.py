import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    mongodb_connection_uri: str = os.getenv("MONGODB_CONNECTION_URI")
    mongodb_chat_database: str = os.getenv("MONGODB_CHAT_DATABASE", "chat")
    mongodb_chat_collection: str = os.getenv("MONGODB_CHAT_COLLECTION", "chat")
    mongodb_messages_collection: str = os.getenv("MONGODB_MESSAGES_COLLECTION", "messages")

    new_chats_event_topic: str = os.getenv("NEW_CHATS_EVENT_TOPIC", "new-chats-topic")
    new_message_received_event_topic: str = os.getenv("NEW_MESSAGE_RECEIVED_EVENT_TOPIC", "chat-{chat_id}-new-messages")

    kafka_url: str = os.getenv("KAFKA_URL")
