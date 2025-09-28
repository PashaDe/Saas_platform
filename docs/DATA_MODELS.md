## Модели данных (верхний уровень)

Базовые:
- Company (tenant)
- User (role: admin|viewer|service)
- ProviderToken (google|moysklad)
- ExportConfig, ExportTask
- Subscription, UsageCounter
- ApiKey, WebhookSubscription, AuditLog

Расширения:
- Dealer: company_id, name, telegram_chat_id, bindings_json
- CompanyLink: owner_company_id, peer_company_id, status (pending|active|rejected), created_at
- AutomationRule: owner_company_id, source_company_id, target_company_id, source_event, action, field_mapping_json, filters_json, enabled
- CrossCompanyJob: rule_id, source_entity/id, target_entity/id, status, idempotency_key, error

Индексы и ограничения:
- Уникальные: (company_id, idempotency_key) на задачах/кросс‑операциях
- Частичные индексы по статусам и created_at
- Внешние ключи на `company_id` и `rule_id`


