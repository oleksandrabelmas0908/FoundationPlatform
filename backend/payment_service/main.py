from fastapi import FastAPI
import uvicorn
import logging

from routes import router


app = FastAPI(debug=True, title="Payment servicd")
app.include_router(router)





if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, log_level="info")