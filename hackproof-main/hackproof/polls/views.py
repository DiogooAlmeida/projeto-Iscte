from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from django.contrib import messages
from newsapi import NewsApiClient
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import os
import time

# Create your views here.

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def dicas(request):
    return render(request, "dicas.html")

def password(request):
    return render(request, "forgot-password.html")

def charts(request):
    return render(request, "charts.html")

def dicas(request):
    newsapi = NewsApiClient(api_key='c9669e9e1bed456eb08fc9f887a5054a')
    news = newsapi.get_everything(q='dicas cibersegurança',
                                      language='pt',
                                      sort_by='relevancy',
                                      page=1)
    
    paginator = Paginator(news['articles'], 5) # Show 5 articles per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "dicas.html", {'page_obj': page_obj})

def page_401(request):
    return render(request, "401.html")

def page_404(request):
    return render(request, "404.html")

def page_500(request):
    return render(request, "500.html")

def definicoes(request):
    return render(request, "definicoes.html")

def logout(request):
    return render(request, "logout.html")

def perfil(request):
    return render(request, "perfil.html")

@login_required 
def main_page(request):
    newsapi = NewsApiClient(api_key='c9669e9e1bed456eb08fc9f887a5054a')
    news = newsapi.get_everything(q='dicas cibersegurança',
                                      language='pt',
                                      sort_by='relevancy',
                                      page=1)
    
    paginator = Paginator(news['articles'], 5) # Show 5 articles per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "main_page.html", {'page_obj': page_obj})

def tables(request):
    # Get the logs from the cache
    list(messages.get_messages(request))
    logs = cache.get('logs', [])
    return render(request, 'tables.html', {'logs': logs})