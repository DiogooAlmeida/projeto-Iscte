from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('login/register/', views.register, name='register'),
    path('tables/', views.tables, name='tables'),
    path('dicas/', views.dicas, name='dicas'),
    path('password/', views.password, name='password'),
    path('charts/', views.charts, name='charts'),
    path('401/', views.page_401, name='error_401'),
    path('404/', views.page_404, name='error_404'),
    path('500/', views.page_500, name='error_500'),
]