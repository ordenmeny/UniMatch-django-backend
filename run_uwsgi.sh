#!/bin/sh

set -e

uv run manage.py wait_for_db
uv run manage.py migrate
uv run manage.py collectstatic --noinput

exec uwsgi \
  --chdir /djangoapp \
  --module djangoProject.wsgi \
  --master \
  --workers 1 \
  --threads 2 \
  --enable-threads \
  --socket :9000 \
  --vacuum \
  --die-on-term \
  --buffer-size 32768


# --buffer-size 16384 \      # 16KB
# --post-buffering 8192 \    # 8KB
# --max-request-size 52428800 # 50MB
