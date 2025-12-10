from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class DecisionEnum(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    MONITOR = "MONITOR"

class ThreatCategory(str, Enum):
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    ANOMALY = "anomaly"
    BOT_BEHAVIOR = "bot_behavior"
    RATE_LIMIT = "rate_limit"
    UNKNOWN = "unknown"

class RequestMetadata(BaseModel):
    ip: str
    method: str
    url: str
    headers: Dict[str, str] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ThreatScore(BaseModel):
    total_score: float = Field(..., ge=0, le=100) # 0 = safe, 100 = critical
    breakdown: Dict[str, float] = {} # e.g. {"vector_anomaly": 40.0, "sqli": 50.0}
    categories: List[ThreatCategory] = []

class InspectionResult(BaseModel):
    decision: DecisionEnum
    score: ThreatScore
    request_id: str
    reason: Optional[str] = None
    action_taken: str = "forwarded" # or "blocked"

# Rule Management
class RuleType(str, Enum):
    IP_BLOCK = "ip_block"
    IP_ALLOW = "ip_allow"
    KEYWORD_BLOCK = "keyword_block"
    GEO_BLOCK = "geo_block"

class Rule(BaseModel):
    id: str
    type: RuleType
    value: str # IP address or keyword
    expiration: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
