from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .viewsets import LutadorViewset

router = DefaultRouter()
# Rota para o viewset lutador
router.register("lutador", LutadorViewset)

urlpatterns = [
    path("", include(router.urls))
]