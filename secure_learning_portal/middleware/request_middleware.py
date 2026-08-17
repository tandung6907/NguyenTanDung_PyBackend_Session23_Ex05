import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        if request.method == "OPTIONS":
            response = await call_next(request)
        else:
            response = await call_next(request)

        duration = time.perf_counter() - start_time

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{duration:.6f}"

        print(
            f"{request.method} {request.url.path} "
            f"{response.status_code} request_id={request_id} "
            f"time={duration:.6f}s"
        )

        return response
