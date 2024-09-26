import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    mongodb_connection_uri: str = os.getenv("MONGODB_CONNECTION_URI")
    mongodb_chat_database: str = os.getenv("MONGODB_CHAT_DATABASE", "chat")
    mongodb_chat_collection: str = os.getenv("MONGODB_CHAT_COLLECTION", "chat")
