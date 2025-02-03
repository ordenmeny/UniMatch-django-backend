FROM python:3.12-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

COPY . .

ENV PATH="/app:/django_venv/bin:$PATH"


RUN python -m venv /django_venv && \
    apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get install -y libpq-dev && \
    apt-get install -y build-essential && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r req.txt && \
    pip install "psycopg[c]" && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chmod +x /app/run_uwsgi.sh


CMD ["run_uwsgi.sh"]
