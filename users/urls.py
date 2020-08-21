from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import UserViewSet, CustomAuthToken


router = DefaultRouter()
router.register('', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', CustomAuthToken.as_view()),
]