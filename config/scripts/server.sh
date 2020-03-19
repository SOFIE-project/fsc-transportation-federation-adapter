#!/bin/sh

python3 manage.py migrate
gunicorn transportation_adapter.wsgi:application
