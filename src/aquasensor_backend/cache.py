from aiocache import Cache
import os

__all__ = ["cache"]

CACHE_URL = os.getenv("CACHE_URL", "memory://")

cache = Cache.from_url(CACHE_URL)
