from api.service import update_content_views_by_page
from pages.celery import app


@app.task()
def update_content_views_by_page_task(page_id: int):
    update_content_views_by_page(page_id)
