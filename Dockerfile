FROM python:3.13-slim

COPY requirements.txt /build/requirements.txt

RUN pip install --no-cache-dir -r /build/requirements.txt

WORKDIR /code

COPY . /code

CMD python main.py