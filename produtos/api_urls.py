from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api_views import NovaPessoaViewSet, DoadorViewSet

router = DefaultRouter()
router.register(r'criancas', NovaPessoaViewSet, basename='criancas')
router.register(r'doadores', DoadorViewSet, basename='doadores')

urlpatterns = [
    path('', include(router.urls)),
]
