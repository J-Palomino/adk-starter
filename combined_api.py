from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

# Create main FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service API client
SERVICE_API_URL = "http://localhost:8080"
AGENT_API_URL = "http://localhost:8000"

# Forward requests to the service API
@app.api_route("/service/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def service_proxy(request: Request, path: str):
    url = f"{SERVICE_API_URL}/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=url,
            headers=dict(request.headers),
            params=request.query_params,
            content=await request.body(),
        )
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code,
            headers=dict(response.headers)
        )

# Forward requests to the agent API
@app.api_route("/agent/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def agent_proxy(request: Request, path: str):
    url = f"{AGENT_API_URL}/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=url,
            headers=dict(request.headers),
            params=request.query_params,
            content=await request.body(),
        )
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code,
            headers=dict(response.headers)
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
