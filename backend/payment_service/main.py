from fastapi import FastAPI
import uvicorn


app = FastAPI(debug=True, title="Payment servicd")


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, log_level="info")