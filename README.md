# SOFIE Food Supply Chain Transportation Federation Adapter

The following project contains the Federation Adapter (F.A) module for the Transportation IoT platform derived for the SOFIE H2020 project.
The F.A. module exposes the functionality of the underlying Transportation IoT platform using the Web Of Things Thing Description model.
The model can be accessed by visiting the root webpage of the F.A. (e.g. ```localhost:8000``` when running in development) or ```https://<server>/transportation``` when running in production.


## Required software

The following are required for development.

*   Python 3.6.2+
*   Django framework (2.2.x)
*   Redis
*   Docker
*   docker-compose

## Installation

In a new python virtualenv, execute:

```bash
pip3 install -r requirements.txt
```

## Running the client locally

File ```transportation_adapter.settings.dev``` holds the settings to be used in development.

Make sure that access to a redis server & the **mongodb of the underlying KAA IoT platform** is present, then run:

```bash
export DJANGO_SETTINGS_MODULE=transportation_adapter.settings.dev
python3 manage.py migrate
python3 manage.py runserver 0:8000
```

The django development server is now running at ```localhost:8000```

## Running the unit tests

To run the unit tests, execute:

```bash
python3 manage.py test --settings=transportation_adapter.settings.test
```

## Deploying with docker

File ```transportation_adapter.settings.prod``` holds the settings to be used in production.

To build & run the containers, execute:

```bash
cd config
docker-compose up -d --build
```

### API swagger

In addition, the F.A. also exposes a swagger page under ```api/swagger/```.
