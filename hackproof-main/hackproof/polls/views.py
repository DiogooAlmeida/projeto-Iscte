from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from django.contrib import messages
from django.http import HttpResponseRedirect
from newsapi import NewsApiClient
from collections import Counter
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Path
import os
import datetime
import json

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

def get_event_counts():
    logs = []
    log_folder = 'log_folder'
    today = datetime.date.today()
    filename = f'folder_access_{today}.log'
    if os.path.exists(os.path.join(log_folder, filename)):
        with open(os.path.join(log_folder, filename), 'r') as f:
            for line in f:
                parts = line.strip().split(' - ')
                if len(parts) >= 5:
                    date_time, event_name, folder_path, destination_path, user = parts[:5]
                    logs.append({
                        'date_time': date_time,
                        'event_name': event_name,
                        'folder_path': folder_path,
                        'destination_path': destination_path,
                        'user': user,
                    })

    event_counts = Counter(log['event_name'] for log in logs)
    event_counts_dict = dict(event_counts)  # Convert to regular dictionary
    return event_counts_dict

@login_required
def charts(request):
    event_counts_dict = get_event_counts()
    print('event_counts:', event_counts_dict)
    return render(request, 'charts.html', {'event_counts': json.dumps(event_counts_dict)})

@login_required
def dicas(request):
    newsapi = NewsApiClient(api_key='c9669e9e1bed456eb08fc9f887a5054a')
    news = newsapi.get_everything(q='cybersecurity tips',
                                  language='en',
                                  sort_by='relevancy',
                                 )
    articles = news['articles']

    return render(request, "dicas.html", {'articles': articles})

def page_401(request):
    return render(request, "401.html")


def page_404(request):
    return render(request, "404.html")


def page_500(request):
    return render(request, "500.html")

@login_required
def definicoes(request):
    return render(request, "definicoes.html")

@login_required
def logout(request):
    return render(request, "logout.html")

@login_required
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
    event_counts_dict = get_event_counts()

    context = {
        'page_obj': page_obj,
        'event_counts': json.dumps(event_counts_dict)
    }

    return render(request, "main_page.html", context)


@login_required
def tables(request):
    logs = []
    log_folder = 'log_folder'
    today = datetime.date.today()
    filename = f'folder_access_{today}.log'
    if os.path.exists(os.path.join(log_folder, filename)):
        with open(os.path.join(log_folder, filename), 'r') as f:
            for line in f:
                parts = line.strip().split(' - ')
                if len(parts) >= 5:
                    date_time, event_name, folder_path, destination_path, user = parts[:5]
                    logs.append({
                        'date_time': date_time,
                        'event_name': event_name,
                        'folder_path': folder_path,
                        'destination_path': destination_path,
                        'user': user,
                    })
    return render(request, 'tables.html', {'logs': logs})

@login_required
def save_path(request):
    path_obj = Path.objects.first()
    if path_obj is None:
        path_obj = Path.objects.create(path='your default path here')
    current_path = path_obj.path
    form_submitted = False
    if request.method == 'POST':
        new_path = request.POST['path']
        if new_path != current_path:
            path_obj.path = new_path
            path_obj.save()
            messages.success(request, 'Diretório alterado com sucesso.')
            form_submitted = True
            current_path = new_path
            current_path = current_path.replace("\\", "/")
    return render(request, 'files.html', {'form_submitted': form_submitted, 'path': current_path})