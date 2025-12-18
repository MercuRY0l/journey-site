
import hmac
import hashlib
import os

from dotenv import load_dotenv

from domain.interfaces.hash_tokens_service import IHashTokenService

load_dotenv()

SECRET_KEY = os.environ.get(key="SECRET_KEY")
SECRET_KEY_BYTES = SECRET_KEY.encode()

class HashTokenService(IHashTokenService):
    def hash(self, token: str) -> str:
        return hmac.new(SECRET_KEY_BYTES, token.encode(), hashlib.sha256).hexdigest()

