import os

from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from garmin_client import get_client

load_dotenv()

mcp = MCPServer("garmin-activities")


@mcp.tool()
def list_activities(limit: int = 5) -> list[dict]:
    """Devuelve las últimas actividades registradas en Garmin Connect."""
    client = get_client()
    activities = client.get_activities(0, limit)
    assert isinstance(activities, list)

    return [
        {"date": activity["startTimeLocal"], "name": activity["activityName"]}
        for activity in activities
    ]


class BearerTokenMiddleware(BaseHTTPMiddleware):
    """Rechaza cualquier petición que no traiga la clave compartida en la cabecera Authorization."""

    async def dispatch(self, request: Request, call_next):
        expected = os.environ["MCP_AUTH_TOKEN"]
        if request.headers.get("authorization") != f"Bearer {expected}":
            return JSONResponse({"error": "unauthorized"}, status_code=401)
        return await call_next(request)


if __name__ == "__main__":
    if os.getenv("MCP_TRANSPORT") == "http":
        import uvicorn

        app = mcp.streamable_http_app()
        app.add_middleware(BearerTokenMiddleware)
        uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
    else:
        mcp.run()
