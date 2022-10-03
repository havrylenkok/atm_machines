FROM python:3.10-slim

WORKDIR /app

ENV PYTHONBUFFERED 1

COPY requirements ./requirements

RUN pip install -r requirements/base.txt

COPY . .

CMD ["uvicorn", "main:app", "--host=0.0.0.0"]
EXPOSE 8000
