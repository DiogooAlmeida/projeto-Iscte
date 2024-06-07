from django.urls import path
from .views import start_logging_view

urlpatterns = [
    path('start_logging/', start_logging_view, name='start_logging'),
]