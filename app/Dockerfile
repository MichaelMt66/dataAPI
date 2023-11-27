FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./common /code/common
COPY ./data /code/data
COPY ./schemas /code/schemas
COPY ./service /code/service
COPY main.py /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]