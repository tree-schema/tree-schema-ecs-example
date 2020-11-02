
FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update --allow-releaseinfo-change  \
&& apt-get install gcc libsnappy-dev -y \
# dependencies for building Python packages
&& apt-get install -y build-essential \
# psycopg2 dependencies
&& apt-get install -y libpq-dev default-libmysqlclient-dev python-mysqldb git \
# Translations dependencies
&& apt-get install -y gettext \
# cleaning up unused files
&& apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
&& rm -rf /var/lib/apt/lists/* \
&& apt-get clean

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
    && rm -rf /requirements.txt

# Run the application from the "app" directory and as the "django" user
COPY ./deployment/django/cmds/* /cmds/
RUN sed -i 's/\r$//g' /cmds/*
RUN chmod -R +x /cmds
RUN chown -R django /cmds
COPY --chown=django:django . /app

USER django

WORKDIR /app