FROM python:3.9

ENV PYTHONBUFFERED 1
ENV PYTHONPATH /app

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock* ./

RUN pip install --no-cache-dir poetry
RUN poetry install

COPY ./inarious /app/inarious

CMD ["poetry", "run", "uvicorn", "inarious.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
