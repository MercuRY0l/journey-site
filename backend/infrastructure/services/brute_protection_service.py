import redis.asyncio as redis

from domain.config.config_brute import MAX_ATTEMPTS, ATTEMPT_TIMEOUT, TRUSTED_PROXIES, BLOCK_TIME, REDIS_URL

from domain.interfaces.brute_interface import IBruteService
from ipaddress import ip_address, ip_network

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

class BruteService(IBruteService):
    
    def __init__(self, ip=None):
        self.ip = ip

    def get_client_ip(self, request):
        remote_addr = request.client.host
        
        if not any(ip_address(remote_addr) in ip_network(p) for p in TRUSTED_PROXIES):
            return remote_addr
        
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            self.ip = x_forwarded_for.split(',')[0]
        else:
            self.ip = remote_addr
        return self.ip

    def _attempts_cache_key(self): 
        return f'login_attempts{self.ip}'

    def _blocked_cache_key(self):
        return f'blocked_{self.ip}'

    async def is_blocked(self):
        return await redis_client.get(self._blocked_cache_key())
 
    async def record_failed_attempt(self):
        key = self._attempts_cache_key()
        attempts = await redis_client.get(key)
        attempts = int(attempts) + 1 if attempts else 1
        
        await redis_client.set(key, attempts, ex=ATTEMPT_TIMEOUT)
        
        if attempts >= MAX_ATTEMPTS:
            await redis_client.set(self._blocked_cache_key(), "1", ex=BLOCK_TIME)
            return attempts
        return attempts

    async def reset_attempts(self):
        await redis_client.delete(self._attempts_cache_key())
        await redis_client.delete(self._blocked_cache_key())
