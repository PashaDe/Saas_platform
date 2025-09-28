from celery import Celery
import os


celery_app = Celery(
    "moysklad_saas",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
)


