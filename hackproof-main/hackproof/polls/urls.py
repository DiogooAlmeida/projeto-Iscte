from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('tables/', views.tables, name='tables'),
    path('dicas/', views.dicas, name='dicas'),
    path('forgot-password/', views.password, name='password'),
    path('charts/', views.charts, name='charts'),
    path('401/', views.page_401, name='error_401'),
    path('404/', views.page_404, name='error_404'),
    path('500/', views.page_500, name='error_500'),
    path('definicoes/', views.definicoes, name='definicoes'),
    path('logout/', views.logout, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('main_page/', views.main_page, name='main_page'),
    path('files/', views.files, name='files'),

]