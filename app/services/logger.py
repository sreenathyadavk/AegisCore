import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if hasattr(record, "extra_info"):
            log_obj.update(record.extra_info)
        return json.dumps(log_obj)

def setup_logger():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    
    root_logger = logging.getLogger("aegis")
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    
    # Also capture uvicorn access logs if possible or let them be
    return root_logger

logger_service = setup_logger()

def log_audit(decision: str, score: float, request_id: str, metadata: Dict[str, Any]):
    logger = logging.getLogger("aegis.audit")
    logger.info("Decision Made", extra={"extra_info": {
        "event_type": "audit",
        "decision": decision,
        "score": score,
        "request_id": request_id,
        "metadata": metadata
    }})
