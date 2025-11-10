from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from prometheus_client import make_asgi_app

from shared.db.engine import lifespan
from routes import router


app = FastAPI(debug=True, title="Auth service", lifespan=lifespan)
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(router)




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, log_level="info")