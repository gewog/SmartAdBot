FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \


COPY . .

CMD ["poetry", "run", "python", "main.py"]