from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .viewsets import LutadorViewset

router = DefaultRouter()

router.register("lutador", LutadorViewset)

urlpatterns = [
    path("", include(router.urls))
]