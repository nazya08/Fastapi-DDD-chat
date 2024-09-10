from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar, Any

V = TypeVar("V", bound=Any)


@dataclass(frozen=True)
class BaseValueObject(ABC, Generic[V]):
    value: V

    def __post_init__(self) -> None:
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        ...

    @abstractmethod
    def as_generic_type(self) -> str:
        ...
