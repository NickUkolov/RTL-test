from datetime import timedelta, datetime
from typing import Dict

from motor.motor_asyncio import AsyncIOMotorClient


class Database:
    __slots__ = "db_url", "db_name", "collection_name", "_client", "_db", "collection"

    def __init__(self, db_url: str, db_name: str, collection_name: str):
        self.db_url = db_url
        self.db_name = db_name
        self.collection_name = collection_name
        self._client = AsyncIOMotorClient(db_url)
        self._db = self._client.get_database(db_name)
        self.collection = self._db.get_collection(collection_name)

    async def aggregate_data(self, dt_from: datetime, dt_upto: datetime, group_type: str) -> Dict[str, list]:
        pipeline = [
            {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
            {
                "$densify": {
                    "field": "dt",
                    "range": {
                        "step": 1,
                        "unit": group_type,
                        # upper bound is exclusive in mongo $densify,
                        # so we need to add 1 millisecond to densify properly
                        "bounds": [dt_from, dt_upto + timedelta(milliseconds=1)],
                    },
                }
            },
            {
                "$group": {
                    "_id": {
                        "$switch": {
                            "branches": [
                                {
                                    "case": {"$eq": [group_type, "month"]},
                                    "then": {
                                        "$dateToString": {
                                            "format": "%Y-%m",
                                            "date": "$dt",
                                        }
                                    },
                                },
                                {
                                    "case": {"$eq": [group_type, "day"]},
                                    "then": {
                                        "$dateToString": {
                                            "format": "%Y-%m-%d",
                                            "date": "$dt",
                                        }
                                    },
                                },
                                {
                                    "case": {"$eq": [group_type, "hour"]},
                                    "then": {
                                        "$dateToString": {
                                            "format": "%Y-%m-%dT%H",
                                            "date": "$dt",
                                        }
                                    },
                                },
                            ],
                            "default": None,
                        }
                    },
                    "total": {"$sum": "$value"},  # Adjust "value" to your field name
                }
            },
            {"$project": {"_id": 0, "dt": {"$toDate": "$_id"}, "total": "$total"}},
            {"$sort": {"dt": 1}},
        ]
        result = await self.collection.aggregate(pipeline).to_list(length=None)

        dataset = [doc["total"] for doc in result]
        labels = [doc["dt"].isoformat(timespec="seconds") for doc in result]

        return {"dataset": dataset, "labels": labels}
