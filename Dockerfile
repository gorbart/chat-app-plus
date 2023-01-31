FROM python:3.10.9

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.11 \
  POETRY_VIRTUALENVS_CREATE=false \
  FORWARDED_ALLOW_IPS=* \
  AGILEAPI_ENV=PRODUCTION

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY poetry.lock pyproject.toml /code

RUN poetry config virtualenvs.create false && \
  poetry install --no-dev --no-interaction --no-ansi

COPY ./chatappplus /code

RUN ["chmod", "+x", "./docker-entrypoint.sh"]
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
