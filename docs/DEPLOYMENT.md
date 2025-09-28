## Деплой (Beget + Docker)

Сервисы: api, worker, beat, postgres, redis, nginx.

Переменные: DATABASE_URL, REDIS_URL, SECRET_KEY, ENCRYPTION_KEY, GOOGLE_*, MOYSKLAD_*, SENTRY_DSN, OTEL_*.

Шаги: .env → docker-compose → alembic upgrade → Nginx SSL → бэкапы.


