from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'company', views.CompanyAPI, basename='company')
router.register(r'employee', views.EmployeeAPI, basename='employee')
router.register(r'device', views.DeviceAPI, basename='device')
router.register(r'deligate', views.DeligateAPI, basename='deligate')
router.register(r'device-history', views.DeviceHistoryAPI, basename='device-history')


urlpatterns = [
]
urlpatterns += router.urls
