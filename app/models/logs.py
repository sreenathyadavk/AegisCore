from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional

class LogEntry(BaseModel):
    id: Optional[int] = None
    timestamp: datetime
    ip: str
    request_path: str
    method: str
    decision: str
    score: float
    reasons: str
    metadata: str # JSON string
