from typing import Mapping, Any

from domain.entities.messages import Chat, Message


def convert_message_entity_to_document(message: Message) -> dict:
    return {
        'id': message.id,
        'text': message.text.as_generic_type(),
        'created_at': message.created_at,
    }


def convert_chat_entity_to_document(chat: Chat) -> dict:
    return {
        'id': chat.id,
        'title': chat.title.as_generic_type(),
        'created_at': chat.created_at,
        'messages': [convert_message_entity_to_document(message) for message in chat.messages],
    }


def convert_message_document_to_entity(message_document: Mapping[str, Any]) -> Message:
    return Message(
        id=message_document['id'],
        text=message_document['text'],
        created_at=message_document['created_at'],
    )


def convert_chat_document_to_entity(chat_document: Mapping[str, Any]) -> Chat:
    return Chat(
        id=chat_document['id'],
        title=chat_document['title'],
        created_at=chat_document['created_at'],
        messages={
            convert_message_document_to_entity(message_document)
            for message_document in chat_document['messages']
        },
    )
