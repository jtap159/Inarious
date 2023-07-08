FROM python:3.9

ENV PYTHONBUFFERED 1
ENV PYTHONPATH /app

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock* ./

RUN pip install --no-cache-dir poetry
RUN poetry install

COPY ./Inarious /app/Inarious

CMD ["faust", "-A", "Inarious.faust_main", "worker", "-l", "info"]
