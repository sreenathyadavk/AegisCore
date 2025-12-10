from fastapi import FastAPI, Request

app = FastAPI()

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path_name: str):
    return {
        "status": "received",
        "path": path_name,
        "method": request.method,
        "headers": dict(request.headers),
        "from_firewall": request.headers.get("x-aegis-gate")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
