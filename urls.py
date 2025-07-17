from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path
from .views import orderviewset




router =DefaultRouter()
router.register('Order', orderviewset)


urlpatterns = router.urls