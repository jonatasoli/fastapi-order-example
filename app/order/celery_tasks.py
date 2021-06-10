from loguru import logger
from order.api.adapters.celery_config import celery_app, celery_log


@celery_app.task(
    name='enqueue_order'
    bind=True,
    autoretry_for=(Exception,)
    max_retries=10
    retry_backoff=True,
    retry_jitter=True
)
def send_order(order):
    celery_log.info("Checkout task - Complete!")


@celery_app.task
def error_handler(request, exc, traceback):
    celery_log.error(f'Task {request.id} raised exception: {exc}\n{traceback}')
