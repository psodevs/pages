from unittest.mock import patch

from rest_framework.test import APITestCase

from api.models import Page, Content, PageContent
from api.service import update_content_views_by_page


class TestPageView(APITestCase):
    def test_all_pages(self):
        response = self.client.get('/pages/')
        self.assertEqual(response.status_code, 200)

    def test_app_pages_pagination(self):
        response = self.client.get('/pages/?page_size=3')
        self.assertTrue(response.json()['results'], 3)

    def test_detail_page(self):
        with patch('api.tasks.update_content_views_by_page_task.delay') as mock_task:
            response = self.client.get('/pages/1/')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(mock_task.called)

    def test_update_count_content_views(self):
        content_1 = Content.objects.create(title='Test content 1', type=Content.ContentType.TEXT)
        content_2 = Content.objects.create(title='Test content 2', type=Content.ContentType.TEXT)
        page = Page.objects.create(title='Test')
        PageContent.objects.create(page=page, content=content_1, order=1)
        PageContent.objects.create(page=page, content=content_2, order=2)

        update_content_views_by_page(page.pk)

        self.assertEqual(Content.objects.get(pk=content_1.pk).count_views, 1)
        self.assertEqual(Content.objects.get(pk=content_2.pk).count_views, 1)
