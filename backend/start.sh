#!/bin/bash

uv run alembic upgrade head
uv run gunicorn -b 0.0.0.0:8000 app:app