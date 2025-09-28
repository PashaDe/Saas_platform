## Пошаговая разработка и деплой

### Коммуникация
- Всегда думаю и проектирую на английском, общаюсь и пишу ответы на русском.

### GitHub и Beget
1) Создайте приватный репозиторий GitHub и добавьте проект.
2) На Beget настройте SSH‑ключ и доступ по git/ssh.
3) На сервере держите две директории: `staging` и `prod`.

### Поток
1) Разработка локально → коммиты → push.
2) На Beget (staging): `git pull` или rsync, `docker compose -f docker-compose.prod.yml up -d --build`, `alembic upgrade head`, проверка `/health`.
3) Перекат на prod через `scripts/deploy.sh` после проверки.
4) Бэкапы по cron: `scripts/backup.sh`.

### Правила
- Не редактировать прод напрямую; всё через Git.
- Обязательные ревью PR (минимум себя же).
- Семантические версии релизов и changelog.

### Настройка GitHub (шаги)
1) Локально:
   - `git init`
   - `git remote add origin git@github.com:<ORG>/<REPO>.git`
   - `git add . && git commit -m "chore: initial scaffold" && git push -u origin main`
2) Создайте доступ по SSH (см. ниже) и добавьте ключ на GitHub.

### Настройка SSH и Beget (шаги)
1) На локальной машине: `ssh-keygen -t ed25519 -C "beget-deploy"`
2) Публичный ключ (`.pub`) добавить в панель Beget → SSH‑ключи.
3) Подключение проверка: `ssh user@beget.host`.
4) На сервере:
   - `mkdir -p ~/apps/moysklad-saas && cd ~/apps/moysklad-saas`
   - `git clone git@github.com:<ORG>/<REPO>.git .`
   - `cp .env.example .env` и заполнить секреты
   - `docker compose -f docker-compose.prod.yml up -d --build`
   - `docker compose -f docker-compose.prod.yml exec -T api alembic upgrade head`

### Обновление версии (деплой)
- `git pull`
- `./scripts/deploy.sh`



