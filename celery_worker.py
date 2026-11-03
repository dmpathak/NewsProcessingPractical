from celery import Celery
import time

# Configure Celery to use Redis as the message broker
celery = Celery(
    "worker",  # This is the name of your Celery application
    broker="redis://localhost:6379/0",  # This is the Redis connection string
    backend="redis://localhost:6379/0",  # Optional, for storing task results
)