import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.errors import AssistantError
from app.routers import assistants

log = logging.getLogger("saep.http")
app = FastAPI(title="AI Assistant Platform")
app.include_router(assistants.router)


@app.exception_handler(AssistantError)
async def handle_domain_error(request: Request, exc: AssistantError) -> JSONResponse:
    """One handler turns any AssistantError into a clean JSON response."""
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Time and log every request — the seed of platform observability."""
    started = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - started) * 1000
    log.info("request", extra={"path": request.url.path,
                               "status": response.status_code,
                               "latency_ms": round(elapsed_ms, 1)})
    return response


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
