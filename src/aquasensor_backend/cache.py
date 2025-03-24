import json
from aiocache import Cache
from aiocache.serializers import BaseSerializer
import os

from loguru import logger
from pydantic import BaseModel

from typing import Any, TypeVar

T = TypeVar("T", bound=BaseModel)

__all__ = ["cache"]

CACHE_URL = os.getenv("CACHE_URL")
if CACHE_URL is None:
    CACHE_URL = "memory://"
    logger.warning(
        "CACHE_URL is not set. Using in-memory cache. This is not stateless."
    )


class PydanticSerializer(BaseSerializer):
    def dumps(self, value: "BaseModel" | Any) -> str:
        if not isinstance(value, BaseModel):
            return json.dumps(value)
        
        return value.model_dump_json()

    def loads(self, value: bytes | str | None) -> dict | None:
        if value is None:
            return None
        return json.loads(value)


cache = Cache.from_url(CACHE_URL)
cache.serializer = PydanticSerializer()
