"""Entry point. Run: make run  (or: uvicorn app.main:app --reload)"""

import logging
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.config import get_settings

settings = get_settings()
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)

# Readiness checks: name -> function that raises if the dependency is unusable.
# Register one per dependency as you add it, e.g.
#   READINESS_CHECKS["database"] = lambda: engine.connect().close()
#   READINESS_CHECKS["redis"] = lambda: redis_client.ping()
READINESS_CHECKS: dict[str, Callable[[], object]] = {}
READINESS_TIMEOUT_S = settings.readiness_timeout_seconds

# Checks run in their own threads so a hung dependency can't stall /ready past the timeout.
# (A hung check's thread keeps running in the background; Python can't kill threads, but the
# endpoint still answers 503 in time, which is what the load balancer needs.)
_check_pool = ThreadPoolExecutor(max_workers=8, thread_name_prefix="ready")


@app.get("/health")
def health() -> dict:
    """Liveness: the process is up. No dependency checks, so a slow DB never restarts the pod."""
    return {"status": "ok", "environment": settings.environment}


@app.get("/ready")
def ready() -> JSONResponse:
    """Readiness: can we serve traffic right now? 503 tells the load balancer to skip this pod."""
    failed = {}
    # One time budget shared by all checks, since they run in parallel.
    deadline = time.monotonic() + READINESS_TIMEOUT_S
    futures = {name: _check_pool.submit(check) for name, check in READINESS_CHECKS.items()}
    for name, future in futures.items():
        try:
            future.result(timeout=max(0.0, deadline - time.monotonic()))
        except Exception as e:  # any failure, including TimeoutError, means "not ready"
            log.warning("readiness check %s failed: %s", name, e)
            failed[name] = type(e).__name__  # error type only; details stay in the logs
    if failed:
        return JSONResponse(status_code=503, content={"status": "not ready", "failed": failed})
    return JSONResponse(content={"status": "ready", "checks": sorted(READINESS_CHECKS)})
