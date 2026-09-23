import time
from fastapi import Request

async def timing_middleware(req: Request, call_next):
    start = time.perf_counter()
    res = await call_next(req)
    res.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}s"
    return res