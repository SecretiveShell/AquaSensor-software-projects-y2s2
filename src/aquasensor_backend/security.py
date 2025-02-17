"""all security related functions"""

from hashlib import blake2b
from os import getenv

from loguru import logger

# salt used for hashing passwords. must be a constant
PASSWORD_SALT = getenv("PASSWORD_SALT") or "AQUASENSOR"

if PASSWORD_SALT == "AQUASENSOR":
    logger.warning("PASSWORD_SALT is not set. Using default value. Please set PASSWORD_SALT environment variable.")


def hash_password(password: str) -> str:
    """hash a password"""

    return blake2b(password.encode("utf-8"), digest_size=64, salt=PASSWORD_SALT.encode("utf-8")).hexdigest()
