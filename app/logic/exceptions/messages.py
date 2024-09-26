from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class ChatWithThatTitleAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f'Chat with title "{self.title}" already exists.'


@dataclass(eq=False)
class ChatNotFoundException(LogicException):
    chat_id: str

    @property
    def message(self):
        return f'Chat with id "{self.chat_id}" not found.'
