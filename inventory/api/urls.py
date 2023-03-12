from django.urls import path, include

urlpatterns = [
    path("mobile/", include("inventory.api.mobile.urls")),
    path("admin/", include("inventory.api.web.urls"))
]
