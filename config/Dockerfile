FROM python:3.6-alpine

# Project directory
ENV PROJECT_ROOT=/opt/app

WORKDIR $PROJECT_ROOT

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step. Correct the path to your production requirements file, if needed.
RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
            gcc \
            make \
            libc-dev \
            musl-dev \
            linux-headers \
            pcre-dev \
            postgresql-dev \
            zlib-dev \
            jpeg-dev \
            python3-dev

# Copy python requirements
COPY requirements.txt $PROJECT_ROOT/

# Install required python packages
RUN LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "pip3 install -r requirements.txt"

# Copy the application code
COPY . .

# Collect static files
RUN python3 manage.py collectstatic --no-input

# Delete all package cache
RUN rm -rf /root/.cache

# Gunicorn configuration
# Full settings can be found here: http://docs.gunicorn.org/en/stable/settings.html
ENV GUNICORN_CMD_ARGS="--bind 0.0.0.0:8000 --workers 4 --worker-class gevent --user 1001 -- group 1001 --error-logfile - --access-logfile -"

# Django settings module
ENV DJANGO_SETTINGS_MODULE="transportation_adapter.settings.prod"

CMD ["sh", "./config/scripts/server.sh"]

# Gunicorn will listen to this port
EXPOSE 8000
