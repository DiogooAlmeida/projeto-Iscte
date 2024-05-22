from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login.html", views.login, name="login"),
    path("register.html", views.register, name="register"),
    path("tables.html", views.tables, name="table"),
    path("dicas.html", views.dicas, name="dicas"),
    path("password.html", views.password, name="password"),
    path("charts.html", views.charts, name="charts"),
    path("401.html", views.page_401, name="401"),
    path("404.html", views.page_404, name="404"),
    path("500.html", views.page_500, name="500"),
]