FROM python:3.13.5-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR catalogs_services/

RUN pip install --upgrade pip wheel "poetry==2.1.4"

RUN poetry config virtualenvs.create false

COPY catalogs_services/pyproject.toml catalogs_services/poetry.lock ./

RUN poetry install

COPY catalogs_services .

COPY catalogs_services/prestart.sh .
COPY catalogs_services/main.py .

RUN chmod +x prestart.sh
RUN chmod +x main.py

ENTRYPOINT ["./prestart.sh"]

CMD ["python", "main.py"]