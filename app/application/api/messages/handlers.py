from fastapi import APIRouter, HTTPException, status, Depends
from punq import Container

from application.api.messages.schemas import CreateChatResponseSchema, CreateChatRequestSchema, \
    CreateMessageResponseSchema, CreateMessageSchema, ChatDetailSchema
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import CreateChatCommand, CreateMessageCommand
from logic.init import init_container
from logic.mediator import Mediator
from logic.queries.messages import GetChatDetailQuery

router = APIRouter(
    tags=['Chat'],
    responses={404: {'description': 'Not found'}},
)


@router.post(
    '/',
    # response_model=CreateChatResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description='Create new chat, if chat with that title exists - raise 400 exception.',
    responses={
        status.HTTP_201_CREATED: {'model': CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    }
)
async def create_chat_handler(
        schema: CreateChatRequestSchema,
        container: Container = Depends(init_container)
) -> CreateChatResponseSchema:
    """Create new chat."""
    mediator: Mediator = container.resolve(Mediator)
    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return CreateChatResponseSchema.from_entity(chat=chat)


@router.post(
    '/{chat_id}/messages',
    status_code=status.HTTP_201_CREATED,
    description='Create new message to chat.',
    responses={
        status.HTTP_201_CREATED: {'model': CreateMessageResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    }
)
async def create_message_handler(
        chat_id: str,
        schema: CreateMessageSchema,
        container: Container = Depends(init_container)
) -> CreateMessageResponseSchema:
    """Create new message to chat."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        message, *_ = await mediator.handle_command(
            CreateMessageCommand(text=schema.text, chat_id=chat_id)
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return CreateMessageResponseSchema.from_entity(message=message)


@router.get(
    '/{chat_id}/',
    status_code=status.HTTP_200_OK,
    description='Get information about chat and all messages.',
    responses={
        status.HTTP_200_OK: {'model': ChatDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    }
)
async def get_chat_handler(
        chat_id: str,
        container: Container = Depends(init_container)
) -> ChatDetailSchema:
    """Get information about chat."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat = await mediator.handle_query(GetChatDetailQuery(chat_id=chat_id))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return ChatDetailSchema.from_entity(chat=chat)
