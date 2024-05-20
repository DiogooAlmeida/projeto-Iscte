from django.contrib import admin
from django.urls import path, include

from django.conf.urls import handler404
from . import views
handler404 = 'setup.views.custom_404_view'  # Ajuste para o caminho correto do módulo e view

# Create your urls here.

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('index.urls')),
    path('clientes/', include('clientes.urls')),
]