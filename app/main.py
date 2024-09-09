from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title='Simple Kafka Chat',
        docs_url='/api/docs',
        description='A simple kafka + ddd example.',
        debug=True,
    )
    # app.include_router(message_router, prefix='/chat')

    return app
