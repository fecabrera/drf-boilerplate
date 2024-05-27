FROM python:3.12 AS base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# installs postgresql-client
RUN apt-get update && apt-get install -y wget lsb-release gnupg
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb https://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list
RUN apt-get update && apt-get install -y postgresql-client-14

FROM base

# installs pipenv
RUN pip install pipenv

# installs dependencies
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system

# sets up a non-root user
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /home/appuser
USER appuser

COPY . .

CMD ["gunicorn", "--worker-tmp-dir", "/dev/shm", "api.wsgi"]