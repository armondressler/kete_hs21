#!/bin/bash
set -e

gunicorn -b 0.0.0.0:8080 kete_hs21.wsgi:application
