from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.views import serve

from .settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("delivery.urls")),
    path('static/', serve, {'document_root': MEDIA_ROOT}),
]
