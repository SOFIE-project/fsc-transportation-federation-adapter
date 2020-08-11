FROM ubuntu:18.04

# Project directory
ENV PROJECT_ROOT=/opt/app

WORKDIR $PROJECT_ROOT

# Install libindy
RUN apt update
RUN apt install -y gnupg2 software-properties-common git
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CE7709D068DB5E88
RUN add-apt-repository "deb https://repo.sovrin.org/sdk/deb bionic stable"
RUN apt update
RUN apt install -y libindy

# Install python requirements
RUN apt install -y python3-pip

# Copy python requirements
COPY requirements.txt $PROJECT_ROOT/

# Install required python packages
RUN pip3 install -r requirements.txt

# Copy the application code
COPY . .

# Collect static files
RUN python3 manage.py collectstatic --no-input

# Gunicorn configuration
# Full settings can be found here: http://docs.gunicorn.org/en/stable/settings.html
ENV GUNICORN_CMD_ARGS="--bind 0.0.0.0:8000 --workers 4 --worker-class gevent --user 0 -- group 0 --error-logfile - --access-logfile -"

# Django settings module
ENV DJANGO_SETTINGS_MODULE="transportation_adapter.settings.prod"

CMD ["sh", "./config/scripts/server.sh"]

# Gunicorn will listen to this port
EXPOSE 8000
