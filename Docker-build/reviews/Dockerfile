FROM python:3.13.5-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR reviews_service/

RUN pip install --upgrade pip wheel "poetry==2.1.4"

RUN poetry config virtualenvs.create false

COPY reviews_service/pyproject.toml reviews_service/poetry.lock ./

RUN poetry install

COPY reviews_service .

CMD ["python", "main.py"]