from django.db.models import Prefetch
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.models import Page, PageContent
from api.paginator import StandardPageNumberPaginator
from api.serializers import PageSerializer, DetailPageSerializer
from api.tasks import update_content_views_by_page_task


class PageView(ListAPIView, RetrieveAPIView, GenericViewSet):
    queryset = Page.objects.prefetch_related(
        Prefetch('page_contents', queryset=PageContent.objects.select_related('content').order_by('order'))
    ).all()
    pagination_class = StandardPageNumberPaginator

    def get_serializer_class(self):
        if self.action == 'list':
            return PageSerializer
        return DetailPageSerializer

    def retrieve(self, request, *args, **kwargs):
        page = self.get_object()
        update_content_views_by_page_task.delay(page.pk)
        serializer = self.get_serializer(page)
        return Response(serializer.data)
