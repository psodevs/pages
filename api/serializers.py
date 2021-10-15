from rest_framework import serializers
from rest_framework.reverse import reverse

from api.models import Page, PageContent, Content


class ContentSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='content.title')
    count_views = serializers.IntegerField(source='content.count_views')
    type = serializers.ChoiceField(source='content.type', choices=Content.ContentType.choices)
    additional_attributes = serializers.JSONField(source='content.additional_attributes')

    class Meta:
        fields = (
            'title',
            'count_views',
            'type',
            'order',
            'additional_attributes',
        )
        model = PageContent


class PageSerializer(serializers.ModelSerializer):
    content = ContentSerializer(many=True, source='page_contents')
    link = serializers.SerializerMethodField()

    def get_link(self, page_object: Page) -> str:
        return reverse('pages-detail', args=[page_object.pk], request=self.context.get('request'))

    class Meta:
        fields = (
            'title',
            'content',
            'link',
        )
        model = Page


class DetailPageSerializer(PageSerializer):
    class Meta:
        fields = ('title', 'content')
        model = Page
