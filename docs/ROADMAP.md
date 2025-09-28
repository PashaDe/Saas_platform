## Roadmap (живой план с чеклистами)

### Состояние на сегодня
- [x] Репозиторий GitHub создан и заполнен каркасом
- [x] Документация (README, ARCHITECTURE, API_DESIGN, DATA_MODELS, TECHNICAL_SPEC, DEVELOPMENT, DEPLOYMENT)
- [x] Dockerfile и docker-compose (dev/prod), Nginx конфиг
- [x] VPS Beget: SSH по ключу, Docker/Compose установлены
- [x] Деплой стека на VPS в `/opt/moysklad-saas`, `/health` доступен
- [x] Alembic исполняется (синхронный движок для миграций)
- [x] Справочник экспортёров добавлен в `docs/ARCHITECTURE.md`

### Этап 1 — Фундамент (текущая неделя)
- [ ] Модели БД и миграции
  - [ ] `Company`, `User`, `ProviderToken`
  - [ ] `ExportConfig`, `ExportTask`
  - [ ] `AuditLog`, `ApiKey` (базово)
- [ ] Ядро API
  - [ ] `deps` (tenant из JWT/заглушки), мидлварь контекста
  - [ ] `companies`, `integrations`, `export-configs`, `export-tasks` (CRUD)
  - [ ] Стандартизированные ответы ошибок
- [ ] Клиенты и сервисы (заглушки)
  - [ ] `moysklad_client`, `google_sheets_client`
  - [ ] `export_service` (черновик)
- [ ] Наблюдаемость
  - [ ] Структурные логи JSON, базовые метрики Prometheus

### Этап 2 — Первые экспортёры и интеграции
- [ ] Экспортёры: `orders`, `demand` (инкремент + батчи в Sheets)
- [ ] Планировщик (Celery Beat) и ретраи
- [ ] Настройка домена и HTTPS (Let’s Encrypt)
- [ ] Google OAuth (test credentials, redirect: staging/prod)

### Этап 3 — Масштабирование
- [ ] Остальные экспортёры из каталога (приоритет по требованиям)
- [ ] Биллинг/лимиты (soft/hard)
- [ ] Админ‑панель платформы

### Тестирование (как и когда)
- [ ] Unit‑тесты (модели, трансформации, валидации)
- [ ] Контрактные тесты экспортёров (фикстуры JSON → ожидаемый диапазон в Sheets)
- [ ] Интеграционные тесты с моками API (httpx/mock + fake Sheets/MoySklad)
- [ ] E2E на staging (VPS):
  - [ ] OAuth Google (test client, redirect на домен/staging)
  - [ ] MoySklad: API‑токен/тест‑аккаунт (без логина/пароля)
  - [ ] “Dry‑run” режим (без записи) и “replace sheet” для безопасной записи
- [ ] Нагрузочные мини‑тесты (батчи, квоты)
- [ ] Безопасность (ключи, шифрование, роли)

### Рабочий процесс
1) Локальная разработка (Cursor) → коммиты → GitHub (main/feature‑ветки).
2) Автопроверки локально (lint/tests), затем деплой на VPS:
   - `ssh root@<ip> && cd /opt/moysklad-saas && git pull`
   - `docker compose -f docker-compose.prod.yml up -d --build`
   - `docker compose -f docker-compose.prod.yml exec -T api alembic upgrade head`
3) После этапа интеграций — проверка на домене с HTTPS, затем публикация в каталоге МойСклад.

### Примечания
- Для ранних E2E используем API‑токен МойСклад или тестовый аккаунт, а не логин/пароль. OAuth МС подключим при готовности домена/SSO.
- Список экспортёров и их статус ведём в `docs/ARCHITECTURE.md` и в чекбоксах задач выше.


