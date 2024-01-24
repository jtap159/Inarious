FROM python:3.9

ENV PYTHONBUFFERED 1
ENV PYTHONPATH /app

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock* ./

RUN pip install --no-cache-dir poetry
RUN poetry install

COPY ./inarious /app/inarious

#CMD ["poetry", "run", "faust", "-A", "inarious.user_consumer", "worker", "-l", "info"]
CMD ["poetry", "run", "python", "inarious/user_consumer.py"]
