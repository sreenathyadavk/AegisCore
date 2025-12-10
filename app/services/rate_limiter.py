import redis.asyncio as redis
from app.config import settings
from typing import Tuple

class RateLimiter:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
        # Default limits
        self.DEFAULT_LIMIT = 100 # requests
        self.WINDOW_SIZE = 60 # seconds

    async def check_rate_limit(self, ip: str) -> Tuple[bool, int]:
        """
        Returns (is_allowed, current_count)
        """
        key = f"ratelimit:{ip}"
        
        # Simple Fixed Window for now (or Token Bucket in future)
        # INCR returns the new value
        count = await self.redis.incr(key)
        
        if count == 1:
            # First request, set expiry
            await self.redis.expire(key, self.WINDOW_SIZE)
            
        if count > self.DEFAULT_LIMIT:
            return False, count
            
        return True, count

rate_limiter = RateLimiter()
