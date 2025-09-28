## Архитектура

### Компоненты
- API (FastAPI): REST, аутентификация, валидация, мидлвари мультиарендности.
- Workers (Celery): экспорт данных, кросс‑компанийные автоматизации, Telegram‑уведомления.
- Scheduler (Celery Beat): cron‑задания на основе ExportConfig.
- PostgreSQL: данные арендаторов, задания, биллинг, аудит; опционально RLS.
- Redis: брокер Celery, кеши, лимитеры, дедупликация задач.
- Google Sheets API, МойСклад API: внешние провайдеры.
- Observability: Prometheus, OpenTelemetry, Sentry, структурные логи.

### Мультиарендность
- Обязательный `company_id` во всех арендуемых таблицах и индексах.
- Мидлварь выставляет контекст `company_id` для логов/метрик; все запросы проверяют принадлежность.
- (Опция) RLS: политика `USING (company_id = current_setting('app.company_id')::uuid)`; установка `SET app.company_id` на соединении.

### Клиенты и сервисы
- `moysklad_client`: авторизация, пагинация, инкремент `updatedSince`, backoff.
- `google_sheets_client`: batchUpdate, значения, upsert/replace стратегии, троттлинг.
- `telegram_client`: отправка сообщений дилерам с троттлингом и ретраями.
- `export_service`: оркестрация ExportTask, идемпотентность, счётчики.
- `automation_service`: обработка правил между компаниями (см. ниже).
- `notification_service`: шаблоны и доставка Telegram‑уведомлений.

### Экспортёр (плагинная модель)
Контракт `BaseExporter`:
1) discover_schema
2) fetch_pages(updated_since, page_size)
3) transform(mapping, context)
4) write_batch(strategy: append|upsert|replace)
5) finalize → counters/markers

Идемпотентность: ключ `(company_id, exporter, run_id)`; upsert использует скрытый столбец `external_id`.

### Справочник поддерживаемых сущностей (экспортёров)
Для администраторов компании в UI список доступен как чекбоксы. Ниже — канонические слаги экспортёров и отображаемые названия из МойСклад (ориентир для разработки и тестов).

- orders — Заказы покупателей
- order_positions — Заказы покупателей (позиции)
- sales — Продажи
- sales_positions — Продажи (позиции)
- customer_invoices — Счета покупателям
- customer_invoice_positions — Счета покупателям (позиции)
- payments — Платежи
- paid_documents — Платежи (оплаченные документы)
- supplier_orders — Заказы поставщикам
- supplier_order_positions — Заказы поставщикам (позиции)
- supplier_invoices — Счета поставщиков
- supplier_invoice_positions — Счета поставщиков (позиции)
- receipts — Приемки
- receipt_positions — Приемки (позиции)
- returns — Возвраты
- return_positions — Возвраты (позиции)
- supplier_returns — Возвраты поставщикам
- supplier_return_positions — Возвраты поставщикам (позиции)
- moves — Перемещения
- move_positions — Перемещения (позиции)
- writeoffs_inventory — Списания/оприходования
- writeoff_inventory_positions — Списания/оприходования (позиции)
- production_tasks — Производственные задания
- production_techmaps — Производственные задания (техкарты)
- contractor_reports — Полученные отчеты комиссионеров
- contractor_report_positions — Полученные отчеты комиссионеров (позиции)
- payouts_deposits — Выплаты/внесения
- counterparties — Контрагенты
- assortment — Ассортимент

### Кросс‑компанийные автоматизации (парное подключение компаний)
- Новая сущность `CompanyLink`: двусторонняя связка между компаниями платформы по их `company_id`.
- Подключение происходит только при взаимном подтверждении: каждая сторона вводит `company_id` партнёра и включает связь.
- Сущность `AutomationRule` (владелец — компания) описывает:
  - источник: `source_company_id` (обычно владелец) и событие (`order.created`, `demand.created`, и т.п.),
  - получатель: `target_company_id` (из `CompanyLink`),
  - действие: какую сущность создавать у получателя (например, `receiving` при событии `demand.created`),
  - маппинг полей (json),
  - фильтры/условия, идемпотентный ключ.
- Поток: событие → outbox → воркер → в контексте получателя создаётся сущность → запись `CrossCompanyJob` → аудит.
- Безопасность: 
  - активная `CompanyLink` в обе стороны,
  - квоты и тарифные ограничения,
  - чёткий owner у правила, отмена/пауза, журнал запусков.

### Telegram‑уведомления дилерам
- Сущность `Dealer` (company‑scoped) с `telegram_chat_id`; привязки к точкам продаж/контрагентам.
- Триггеры: заказ создан, входящий платёж, отгрузка.
- Доставка: бот API, retry/backoff, журнал доставок, отписка/пауза.

### Надёжность
- Outbox pattern для экспортов, автоматизаций и уведомлений.
- Ретраи с экспоненциальной задержкой, лимиты параллелизма на компанию.
- Защита квот Google/МС: троттлинг в Redis, алерты на 429/5xx.


