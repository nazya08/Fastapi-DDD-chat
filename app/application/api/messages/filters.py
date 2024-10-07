from pydantic import BaseModel

from infrastructure.repositories.filters.messages import GetMessagesFilters as GetMessagesInfraFilters


class GetMessagesFiltersSchema(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infra(self):
        return GetMessagesInfraFilters(
            limit=self.limit,
            offset=self.offset
        )
