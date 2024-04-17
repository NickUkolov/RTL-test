"""
`core.py` - Core-functionality of bot
"""

import json

from aiogram.types import Message
from pydantic import ValidationError

from src.db import Database
from src.models import AggregateIn


async def aggregate_data(message: Message, db: Database):
    try:
        data_in = AggregateIn.model_validate_json(message.text)
        result = await db.aggregate_data(
            dt_from=data_in.dt_from,
            dt_upto=data_in.dt_upto,
            group_type=data_in.group_type,
        )
        await message.answer(json.dumps(result))
    except ValidationError:
        await message.answer(
            "Message validation error\n"
            "it has to be a json of such type:\n"
            '{"dt_from": "2022-10-01T00:00:00", - isoformat\n'
            '"dt_upto": "2023-10-01T00:00:00", - isoformat\n'
            '"group_type": "day"} - possible variants: month, day, hour\n'
            "and dt_from must be less then dt_upto"
        )
    except Exception:
        await message.answer(
            'Oops, can not send message to Telegram due to it"s huge size etc'
        )
