## Дизайн API (черновик)

Аутентификация: JWT после SSO из МойСклад. Все запросы в контексте `company_id`.

Заголовки: `Idempotency-Key`, `X-Request-Id`.

### Области
- `/health`, `/me`
- `/integrations/*` (google/moysklad: connect/status/refresh)
- `/export-configs` (CRUD, preview, schedule)
- `/export-tasks` (create/run, list, details, cancel)
- `/automations` (rules CRUD, test)
- `/dealers` (CRUD, bindings)
- `/billing` (subscription, usage)
- `/admin/*`

### Компания↔Компания (pairing)
- `POST /company-links` — предложить связь (target_company_id)
- `POST /company-links/{id}/confirm` — подтверждение второй стороной
- `GET /company-links` — список активных связей
- `POST /automations/rules` — правило с `target_company_id` из активной связи и перечнем допустимых сущностей/действий

Вебхуки: `/webhooks/moysklad`, `/webhooks/outgoing` (подтверждения доставки).


