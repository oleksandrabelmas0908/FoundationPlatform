from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from shared.db.engine import init_tables, engine
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_tables()
    yield
    await engine.dispose()


app = FastAPI(debug=True, title="Auth service", lifespan=lifespan)
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, log_level="info")