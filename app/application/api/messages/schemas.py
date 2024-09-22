from pydantic import BaseModel

from domain.entities.messages import Chat


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    id: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> 'CreateChatResponseSchema':
        return CreateChatResponseSchema(
            id=chat.id, title=chat.title.as_generic_type()
        )
