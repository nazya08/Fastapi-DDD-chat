from abc import abstractmethod, ABC
from dataclasses import dataclass, field

from logic.queries.base import QueryHandler, QT, QR, BaseQuery


@dataclass(eq=False)
class QueryMediator(ABC):
    queries_map: dict[QT, QueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    @abstractmethod
    def register_query(self, query: QT, query_handler: QueryHandler[QT, QR]):
        ...

    @abstractmethod
    async def handle_query(self, query: BaseQuery) -> QR:
        ...
