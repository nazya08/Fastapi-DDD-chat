from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mongodb_connection_uri: str = Field(default="mongodb://localhost:27017", alias="MONGODB_CONNECTION_URI")  # TODO: remove default
    mongodb_chat_database: str = Field(default="chat", alias="MONGODB_CHAT_DATABASE")
    mongodb_chat_collection: str = Field(default="chat", alias="MONGODB_CHAT_COLLECTION")
