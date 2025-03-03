from os import getenv

API_BASE_URL = getenv("API_BASE_URL")
assert API_BASE_URL, "API_BASE_URL environment variable is not set."

API_API_KEY = getenv("API_API_KEY")
assert API_API_KEY, "API_API_KEY environment variable is not set."