from django.db.models import F

from api.models import Content


def update_content_views_by_page(page_id: int) -> None:
    Content.objects.filter(page=page_id).update(count_views=F('count_views')+1)
