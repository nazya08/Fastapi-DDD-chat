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