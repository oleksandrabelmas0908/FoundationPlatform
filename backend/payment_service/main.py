from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from prometheus_client import make_asgi_app

from shared.core.logs.logger import setup_logging, get_logger
from shared.core.logs.middleware import ErrorLoggingMiddleware, LoggingMiddleware
from routes import router


setup_logging(service_name="payment-service")
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 50)
    logger.info("Payment Service starting up...")
    logger.info("=" * 50)    
    
    yield
    
    logger.info("Shutting down application...")


app = FastAPI(debug=True, title="Payment servicd", lifespan=lifespan)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(router)


app.add_middleware(ErrorLoggingMiddleware)
app.add_middleware(LoggingMiddleware)


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, log_level="info")