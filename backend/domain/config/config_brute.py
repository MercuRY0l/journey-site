import os
from dotenv import load_dotenv

load_dotenv()

TRUSTED_PROXIES = os.getenv(key="TRUSTED_PROXIES")

MAX_ATTEMPTS = int(os.getenv("MAX_ATTEMPTS", 5))
BLOCK_TIME = int(os.getenv("BLOCK_TIME", 15 * 60))
ATTEMPT_TIMEOUT = int(os.getenv("ATTEMPT_TIMEOUT", 10 * 60))

REDIS_URL = os.getenv("REDIS_URL")
