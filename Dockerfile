FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN cp .env.example .env
RUN pip install -r requirements.txt

RUN python populate_db.py

CMD ["python", "run.py"]
