import httpx
from fastapi import Request, Response
from app.config import settings
import logging

logger = logging.getLogger("aegis.proxy")

class ProxyService:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=settings.UPSTREAM_URL)

    async def forward_request(self, request: Request, body: bytes) -> Response:
        """
        Forwards the incoming request to the upstream service.
        """
        path = request.url.path
        target_base = settings.UPSTREAM_URL

        # 1. Check for specific route overrides
        for prefix, upstream in settings.API_ROUTES.items():
            if path.startswith(prefix):
                target_base = upstream
                break

        # 2. Build final URL
        # If target_base is "http://localhost:8080", and path is "/api/foo", result is "http://localhost:8080/api/foo"
        # We need to handle stripping prefixes if necessary, but for now we'll append standard reverse proxy style.
        
        # httpx client is initialized with base_url, but we might be changing it per request.
        # So we use a generic client or override the url fully.
        
        target_url = f"{target_base.rstrip('/')}{path}"
        if request.url.query:
            target_url += f"?{request.url.query}"

        # Filter headers we don't want to forward strictly or need to modify
        headers = dict(request.headers)
        headers.pop("host", None) 
        headers["X-Aegis-Gate"] = "Protected"

        try:
            upstream_response = await httpx.AsyncClient().request(
                method=request.method,
                url=target_url,
                content=body,
                headers=headers,
                timeout=30.0
            )

            return Response(
                content=upstream_response.content,
                status_code=upstream_response.status_code,
                headers=dict(upstream_response.headers)
            )
        except httpx.RequestError as exc:
            logger.error(f"Proxy error: {exc}")
            return Response(content="Upstream Service Unavailable", status_code=503)

proxy_service = ProxyService()
