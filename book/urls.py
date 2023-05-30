from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Books

router = DefaultRouter()

# register Books view wit router
router.register('book', Books, basename='book')
urlpatterns = router.urls
