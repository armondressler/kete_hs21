#!/bin/bash
set -e

gunicorn -b 127.0.0.1:8000 kete_hs21.wsgi:application
