#!/usr/bin/env bash
set -euo pipefail

DIR=${1:-backups}
mkdir -p "$DIR"

docker compose -f docker-compose.prod.yml exec -T postgres \
  pg_dump -U postgres app | gzip > "$DIR/backup_$(date +%Y%m%d_%H%M%S).sql.gz"


