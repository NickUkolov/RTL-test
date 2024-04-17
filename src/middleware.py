from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Message

from settings import settings
from src.db import Database


class ResourcesMiddleware(BaseMiddleware):

    def __init__(self):
        self.db = Database(
            db_url=f"mongodb://{settings.DB_HOST}:{settings.DB_PORT}",
            db_name=settings.DB_NAME,
            collection_name=settings.COLLECTION_NAME,
        )
        super().__init__()

    async def _provide_resources(self) -> dict:
        resources = {"db": self.db}
        return resources

    async def on_pre_process_message(self, data: dict) -> dict:
        data.update(await self._provide_resources())
        return data

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        await self.on_pre_process_message(data)
        return await handler(event, data)


def setup(dp: Dispatcher) -> None:
    dp.update.middleware(ResourcesMiddleware())
