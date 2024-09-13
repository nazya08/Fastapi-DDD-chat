from infrastructure.repositories.messages import MemoryChatRepository, BaseChatRepository
from logic.mediator import Mediator
from logic.commands.messages import CreateChatCommandHandler, CreateChatCommand


def init_mediator(
        mediator: Mediator,
        chat_repository: BaseChatRepository,
):
    mediator.register_command(
        CreateChatCommand,
        [CreateChatCommandHandler(chat_repository=chat_repository)],
    )
