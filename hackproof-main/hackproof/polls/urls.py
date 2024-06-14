from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tables/', views.tables, name='tables'),
    path('dicas/', views.dicas, name='dicas'),
    path('charts/', views.charts, name='charts'),
    path('401/', views.page_401, name='error_401'),
    path('404/', views.page_404, name='error_404'),
    path('500/', views.page_500, name='error_500'),
    path('definicoes/', views.definicoes, name='definicoes'),
    path('perfil/', views.perfil, name='perfil'),
    path('main_page/', views.main_page, name='main_page'),
    path('save_path/', views.save_path, name='save_path'),
]