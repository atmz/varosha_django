#!/bin/bash
pipenv run python3 manage.py migrate && pipenv run gunicorn --timeout 600 --workers 2 varosha.wsgi