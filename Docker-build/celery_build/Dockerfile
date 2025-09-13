FROM python:3.13.5-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR celery_services/

RUN pip install --upgrade pip wheel "poetry==2.1.4"

RUN poetry config virtualenvs.create false

COPY celery_services/pyproject.toml celery_services/poetry.lock ./

RUN poetry install

COPY celery_services .

CMD ["python", "celery.py"]