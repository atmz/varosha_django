#!/bin/bash
gunicorn --workers 2 varosha.wsgi
