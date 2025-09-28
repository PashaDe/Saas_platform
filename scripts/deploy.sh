#!/usr/bin/env bash
set -euo pipefail

docker compose -f docker-compose.prod.yml pull || true
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec -T api alembic upgrade head


