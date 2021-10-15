from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import PageView

router = DefaultRouter()
router.register(r'pages', PageView, basename='pages')

urlpatterns = [
    path('', include(router.urls)),
]
