from uuid import uuid4

import pytest

from datetime import datetime

from domain.entities.messages import Message, Chat
from domain.events.messages import NewMessageReceivedEvent
from domain.exceptions.messages import TitleTooLongException
from domain.value_objects.messages import Text, Title


def test_create_message_success_short_text():
    text = Text("hello world")
    message = Message(text=text, chat_id=str(uuid4()))

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_message_text_too_long():
    text = Text("a" * 400)
    message = Message(text=text, chat_id=str(uuid4()))

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_chat_success():
    title = Title("title")
    chat = Chat(title=title)

    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()


def test_create_chat_title_too_long():
    with pytest.raises(TitleTooLongException):
        Title("a" * 400)


def test_add_message_to_chat():
    text = Text("hello world")
    message = Message(text=text, chat_id=str(uuid4()))

    title = Title("title")
    chat = Chat(title=title)

    chat.add_message(message)

    assert message in chat.messages
    assert chat.messages == {message}


def test_new_message_event():
    text = Text("hello world")
    message = Message(text=text, chat_id=str(uuid4()))

    title = Title("title")
    chat = Chat(title=title)

    chat.add_message(message)
    events = chat.pull_events()
    pulled_events = chat.pull_events()

    assert not pulled_events
    assert len(events) == 1, events

    new_event = events[0]

    assert isinstance(new_event, NewMessageReceivedEvent)
    assert new_event.message_text == message.text.as_generic_type()
    assert new_event.chat_id == chat.id
    assert new_event.message_id == message.id
