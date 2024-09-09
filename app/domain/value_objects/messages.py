from dataclasses import dataclass

from domain.value_objects.base import BaseValueObject
from domain.exceptions.messages import TitleTooLongException, EmptyTextException


@dataclass(frozen=True)
class Text(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyTextException()

    def as_generic_type(self):
        return str(self.value)


@dataclass(frozen=True)
class Title(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyTextException()
        if len(self.value) > 255:
            raise TitleTooLongException(text=self.value)

    def as_generic_type(self):
        return str(self.value)
