from django.contrib import admin

from api.models import Page, Content


class ContentAdmin(admin.ModelAdmin):
    search_fields = ['title']


class PageContentInline(admin.TabularInline):
    model = Page.content.through


class PageAdmin(admin.ModelAdmin):
    inlines = [
        PageContentInline
    ]
    search_fields = ['title']


admin.site.register(Content, ContentAdmin)
admin.site.register(Page, PageAdmin)
