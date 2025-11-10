FROM python:3.11-slim

WORKDIR /app

COPY ./backend/foundation_service /app/
COPY ./requirements.txt requirements.txt
COPY ./backend/shared /app/shared
COPY ./.env /app/

RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]