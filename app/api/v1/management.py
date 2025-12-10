from fastapi import APIRouter, Header, HTTPException, Depends
from app.models.schemas import Rule, RuleType
from app.services.rules_engine import rules_engine
from app.config import settings

router = APIRouter(prefix="/firewall/api/v1", tags=["management"])

def verify_admin_key(x_admin_key: str = Header(...)):
    if x_admin_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid Admin Key")

@router.post("/rules/add", dependencies=[Depends(verify_admin_key)])
async def add_rule(rule: Rule):
    await rules_engine.add_rule(rule)
    return {"status": "added", "rule": rule}

@router.post("/check", dependencies=[Depends(verify_admin_key)])
async def check_simulated_request():
    # Simulation endpoint
    return {"status": "not_implemented_yet"}

from app.services.db_logger import db_logger

@router.get("/logs", dependencies=[Depends(verify_admin_key)])
async def get_logs(limit: int = 50):
    return db_logger.get_recent_logs(limit)

@router.get("/stats", dependencies=[Depends(verify_admin_key)])
async def get_stats():
    return db_logger.get_stats()
