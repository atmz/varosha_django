#!/bin/bash
python manage.py migrate && gunicorn --workers 2 varosha.wsgi
