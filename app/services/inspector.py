from app.models.schemas import InspectionResult, DecisionEnum, ThreatScore, ThreatCategory
from fastapi import Request
import uuid
import logging
from app.services.rules_engine import rules_engine
from app.services.rate_limiter import rate_limiter
from app.ai.embeddings import embeddings_engine

logger = logging.getLogger("aegis.inspector")

class InspectorService:
    def __init__(self):
        pass

    async def inspect_request(self, request: Request, body: bytes) -> InspectionResult:
        """
        Orchestrates the inspection pipeline.
        """
        request_id = str(uuid.uuid4())
        ip = request.client.host
        score_val = 0.0
        reasons = []
        categories = []

        # 1. Rules Engine (Fast Fail)
        if await rules_engine.check_ip_block(ip):
            return InspectionResult(
                decision=DecisionEnum.BLOCK,
                score=ThreatScore(total_score=100.0, categories=[ThreatCategory.UNKNOWN]),
                request_id=request_id,
                reason="IP Blocklisted"
            )

        # 2. Rate Limiter
        allowed, count = await rate_limiter.check_rate_limit(ip)
        if not allowed:
            return InspectionResult(
                decision=DecisionEnum.BLOCK,
                score=ThreatScore(total_score=50.0, categories=[ThreatCategory.RATE_LIMIT]),
                request_id=request_id,
                reason="Rate Limit Exceeded"
            )

        # 3. AI Inspection (Embeddings & Anomaly)
        # Decode body text safely
        try:
            text_body = body.decode("utf-8")
        except:
            text_body = ""

        anomaly_score = embeddings_engine.calculate_anomaly_score(text_body)
        if anomaly_score > 0.8:
            score_val += (anomaly_score * 100)
            reasons.append("Semantic Anomaly Detected")
            categories.append(ThreatCategory.ANOMALY)
            
        # 4. Aggregation
        total_score = min(max(score_val, 0.0), 100.0)
        
        decision = DecisionEnum.ALLOW
        if total_score > 80:
            decision = DecisionEnum.BLOCK
        elif total_score > 50:
            decision = DecisionEnum.MONITOR # Log but allow
            
        return InspectionResult(
            decision=decision,
            score=ThreatScore(total_score=total_score, breakdown={"anomaly": anomaly_score}, categories=categories),
            request_id=request_id,
            reason=", ".join(reasons) if reasons else "Clean"
        )

inspector = InspectorService()
