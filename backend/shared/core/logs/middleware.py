import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next):
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Start time
        start_time = time.time()
        
        # Extract request info
        method = request.method
        url = str(request.url)
        client_host = request.client.host if request.client else "unknown"
        
        # Log request
        logger.info(
            f"Request started: {method} {url}",
            extra={
                "request_id": request_id,
                "method": method,
                "endpoint": url,
                "client_ip": client_host,
            }
        )
        
        # Process request
        try:
            response: Response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            logger.info(
                f"Request completed: {method} {url} - Status: {response.status_code}",
                extra={
                    "request_id": request_id,
                    "method": method,
                    "endpoint": url,
                    "status_code": response.status_code,
                    "duration_ms": round(duration * 1000, 2),
                }
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            # Calculate duration
            duration = time.time() - start_time
            
            # Log error
            logger.error(
                f"Request failed: {method} {url} - Error: {str(e)}",
                extra={
                    "request_id": request_id,
                    "method": method,
                    "endpoint": url,
                    "duration_ms": round(duration * 1000, 2),
                },
                exc_info=True
            )
            raise


class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to catch and log unhandled exceptions"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(
                f"Unhandled exception: {str(e)}",
                extra={
                    "method": request.method,
                    "endpoint": str(request.url),
                },
                exc_info=True
            )
            raise