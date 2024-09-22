from functools import lru_cache

from punq import Container, Scope

from infrastructure.repositories.messages import MemoryChatRepository, BaseChatRepository
from logic.mediator import Mediator
from logic.commands.messages import CreateChatCommandHandler, CreateChatCommand


@lru_cache(maxsize=1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)
    container.register(CreateChatCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
