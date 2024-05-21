#!/bin/bash
python manage.py migrate && gunicorn --timeout 120 --workers 2 varosha.wsgi
