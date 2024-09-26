from pydantic import BaseModel

from domain.entities.messages import Chat, Message


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    id: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> 'CreateChatResponseSchema':
        return cls(
            id=chat.id, title=chat.title.as_generic_type()
        )


class CreateMessageSchema(BaseModel):
    text: str
    # chat_id: str


class CreateMessageResponseSchema(BaseModel):
    id: str
    text: str

    @classmethod
    def from_entity(cls, message: Message):
        return cls(
            id=message.id, text=message.text.as_generic_type()
        )
