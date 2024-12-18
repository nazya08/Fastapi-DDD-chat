from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class TitleTooLongException(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        return f'Text "{self.text[:255]}..." is too long'


@dataclass(eq=False)
class EmptyTextException(ApplicationException):

    @property
    def message(self) -> str:
        return 'Text cannot be empty'
