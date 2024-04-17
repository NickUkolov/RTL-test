from aiogram import Dispatcher, html, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from src import core
from src.db import Database


async def start(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


async def aggregate_handler(message: Message, db: Database) -> None:
    await core.aggregate_data(message, db)


def setup(dp: Dispatcher):
    dp.message.register(start, CommandStart())
    dp.message.register(aggregate_handler, F.text)
