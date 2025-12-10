from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from app.services.inspector import inspector
from app.core.proxy import proxy_service
from app.models.schemas import DecisionEnum

async def firewall_middleware(request: Request, call_next):
    # Skip health checks and internal endpoints
    # Note: root path can be either "/" or "" depending on the request
    internal_paths = ["", "/", "/health", "/docs", "/openapi.json", "/redoc"]
    if request.url.path in internal_paths:
        return await call_next(request)

    # Skip Inspection for Internal Management API & Dashboard
    # We trust these endpoints (protected by Auth or are Read-Only UI)
    if request.url.path.startswith("/firewall") or request.url.path == "/dashboard":
         return await call_next(request)

    # 1. Read Body (Need to cache it because consuming stream once empties it)
    body = await request.body()

    # 2. Inspect
    result = await inspector.inspect_request(request, body)

    # 3. Act
    # Log to DB
    from app.services.db_logger import db_logger
    db_logger.log(
        ip=request.client.host,
        path=request.url.path,
        method=request.method,
        decision=result.decision,
        score=result.score.total_score,
        reasons=result.reason,
        metadata={"request_id": result.request_id, "categories": result.score.categories}
    )

    if result.decision == DecisionEnum.BLOCK:
        return JSONResponse(
            status_code=403,
            content={
                "error": "Forbidden",
                "reason": result.reason,
                "request_id": result.request_id,
                "score": result.score.dict()
            }
        )

    # 4. Proxy (Forward to Upstream)
    # Forward to Upstream
    return await proxy_service.forward_request(request, body)
