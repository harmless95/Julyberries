FROM python:3.13.5-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR example_api_services/

RUN pip install --upgrade pip wheel "poetry==2.1.4"

RUN poetry config virtualenvs.create false

COPY example_api_services/pyproject.toml example_api_services/poetry.lock ./

RUN poetry install

COPY example_api_services .

CMD ["python", "main.py"]