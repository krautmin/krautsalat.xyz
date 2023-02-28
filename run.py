from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app import create_app


application = create_app()


@application.before_serving
async def init_db():
    client = AsyncIOMotorClient(application.config["MONGODB_URL"])
    await init_beanie(
        database=client.quart_kraut,
        document_models=[
            "app.documents.PostDocument",
            "app.documents.UserDocument",
            "app.documents.ContactMessageDocument",
        ],
    )


if __name__ == "__main__":
    application.run()
