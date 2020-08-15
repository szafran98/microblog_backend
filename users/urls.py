from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import UserViewSet


router = DefaultRouter()
router.register('users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]