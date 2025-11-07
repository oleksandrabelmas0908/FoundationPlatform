from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
import asyncio
import logging

from routes import router
from shared.db.engine import lifespan
from consumer import kafka_consumer, start_consumer


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting application...")
    
    # Start Kafka consumer in background
    consumer_task = asyncio.create_task(
        start_consumer_background()
    )
    
    yield
    
    logger.info("Shutting down application...")
    await kafka_consumer.stop()
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass


async def start_consumer_background():
    try:
        await start_consumer(topic="pay_to_found")  
    except Exception as e:
        logger.error(f"Consumer error: {e}")


app = FastAPI(debug=True, title="Foundation service", lifespan=lifespan)
app.include_router(router=router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, log_level="info")