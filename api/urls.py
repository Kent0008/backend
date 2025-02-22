from django.urls import path, include
from rest_framework import routers
from .views import BookViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r"books", BookViewSet, basename="book")

router_v2 = routers.DefaultRouter()
router_v2.register(r"books", BookViewSet, basename="book")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v2/", include(router_v2.urls)),
]
