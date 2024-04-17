from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src import handlers, middleware


def get_app() -> Dispatcher:
    memory_storage = MemoryStorage()
    dp = Dispatcher(storage=memory_storage)
    handlers.setup(dp)
    middleware.setup(dp)
    return dp
