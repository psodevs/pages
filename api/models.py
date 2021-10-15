from django.core.exceptions import ValidationError
from django.db import models


class Page(models.Model):
    title = models.TextField(verbose_name='Заголовок')
    content = models.ManyToManyField('Content', through='PageContent')

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
        ordering = ['id']

    def __str__(self) -> str:
        return f'Страница "{self.title}"'


class PageContent(models.Model):
    page = models.ForeignKey('Page', on_delete=models.CASCADE, related_name='page_contents', verbose_name='Странца')
    content = models.ForeignKey(
        'Content', on_delete=models.CASCADE, related_name='page_contents', verbose_name='Контент')
    order = models.IntegerField(verbose_name='Порядок отображения')

    class Meta:
        verbose_name = 'Связь страницы и контента'
        unique_together = ['page', 'order']  # Необходимо для вывода контента по порядку

    def __str__(self) -> str:
        return f'Свзязь {self.page.title} - {self.content.title}'


class Content(models.Model):
    class ContentType(models.TextChoices):
        AUDIO = 'AUDIO', 'Аудио'
        VIDEO = 'VIDEO', 'Видео'
        TEXT = 'TEXT', 'Текст'

    title = models.TextField(verbose_name='Заголовок')
    type = models.TextField(choices=ContentType.choices, verbose_name='Тип контента')
    count_views = models.IntegerField(default=0, editable=False, verbose_name='Количество просмотров')
    additional_attributes = models.JSONField(default=dict, verbose_name='Дополнительные атрибуты')

    class Meta:
        verbose_name = 'Контент'
        verbose_name_plural = 'Контент'

    def __str__(self) -> str:
        return f'Контент "{self.get_type_display()}" "{self.title}"'

    def clean(self) -> None:
        if self.type == self.ContentType.AUDIO:
            if 'bit_rate' not in self.additional_attributes:
                raise ValidationError('Для типа аудио необходимо указать параметр bit_rate')
        elif self.type == self.ContentType.VIDEO:
            if 'link' not in self.additional_attributes or 'subs_link' not in self.additional_attributes:
                raise ValidationError('Для типа аудио необходимо указать параметры link, subs_link')
        elif self.type == self.ContentType.TEXT:
            if 'text' not in self.additional_attributes:
                raise ValidationError('Для типа текст необходимо указать параметр text')
