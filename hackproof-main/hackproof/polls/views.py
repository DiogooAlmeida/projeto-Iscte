from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def tables(request):
    return render(request, "tables.html")

def dicas(request):
    return render(request, "dicas.html")

def password(request):
    return render(request, "password.html")

def charts(request):
    return render(request, "charts.html")

def dicas(request):
    return render(request, "dicas.html")

def page_401(request):
    return render(request, "401.html")

def page_404(request):
    return render(request, "404.html")

def page_500(request):
    return render(request, "500.html")