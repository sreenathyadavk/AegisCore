import redis.asyncio as redis
from app.config import settings
from app.models.schemas import Rule, RuleType
from typing import Optional

class RulesEngine:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

    async def add_rule(self, rule: Rule):
        key = f"rule:{rule.type}:{rule.value}"
        await self.redis.set(key, rule.json())
        if rule.expiration:
            # Set TTL
            pass 

    async def check_ip_block(self, ip: str) -> bool:
        key = f"rule:{RuleType.IP_BLOCK}:{ip}"
        exists = await self.redis.get(key)
        return exists is not None

rules_engine = RulesEngine()
