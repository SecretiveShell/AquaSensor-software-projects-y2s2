from aiocache import Cache
from aiocache.serializers import BaseSerializer
import os

from loguru import logger
from pydantic import BaseModel

from typing import Type, TypeVar

T = TypeVar("T", bound=BaseModel)

__all__ = ["cache"]

CACHE_URL = os.getenv("CACHE_URL")
if CACHE_URL is None:
    CACHE_URL = "memory://"
    logger.warning("CACHE_URL is not set. Using in-memory cache. This is not stateless.")


class PydanticSerializer(BaseSerializer):
    def dumps(self, obj: "BaseModel") -> bytes:
        return obj.model_dump_json().encode("utf-8")
    
    def loads(self, data: bytes, model: "BaseModel") -> "BaseModel":
        return model.model_validate_json(data.decode("utf-8"))

cache = Cache.from_url(CACHE_URL)
cache.serializer = PydanticSerializer()