from django.shortcuts import render, redirect
from django.contrib import messages
from newsapi import NewsApiClient
from collections import Counter
from django.contrib.auth.decorators import login_required
from .models import Path
import os
import datetime
import json
import glob
from cryptography.fernet import Fernet

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

def get_all_event_counts():
    logs = []
    log_folder = 'log_folder'
    filenames = glob.glob(os.path.join(log_folder, 'folder_access_*.log'))
    for filename in filenames:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
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
    total_event_count = sum(event_counts.values())  # Sum up all the counts
    return total_event_count

@login_required
def charts(request):
    event_counts_dict = get_event_counts()
    all_event_counts = get_all_event_counts()
    return render(request, 'charts.html', {
        'event_counts': json.dumps(event_counts_dict),
        'all_event_counts': all_event_counts
    })

@login_required
def dicas(request):
   
    articles = get_news()

    return render(request, "dicas.html", {'articles': articles})

def page_401(request):
    return render(request, "401.html")


def page_404(request):
    return render(request, "404.html")


def page_500(request):
    return render(request, "500.html")

@login_required
def definicoes(request):
    if request.method == 'POST':
        new_email = request.POST.get('newEmail')
        new_username = request.POST.get('newUsername')
        new_first_name = request.POST.get('firstName')
        new_last_name = request.POST.get('lastName')
        if new_email:
            # Change the user's email
            request.user.email = new_email
            messages.success(request, 'Email changed to {}'.format(new_email))

        if new_username:
            # Change the user's username
            request.user.username = new_username
            messages.success(request, 'Username changed to {}'.format(new_username))

        if new_first_name:
            # Change the user's first name
            request.user.first_name = new_first_name
            messages.success(request, 'First name changed to {}'.format(new_first_name))

        if new_last_name:
            # Change the user's last name
            request.user.last_name = new_last_name
            messages.success(request, 'Last name changed to {}'.format(new_last_name))

        # Save all changes to the user
        request.user.save()

        return redirect('definicoes')
    else:
        return render(request, 'definicoes.html')

@login_required
def logout(request):
    return render(request, "logout.html")

@login_required
def perfil(request):
    return render(request, "perfil.html")


def get_news():
    newsapi = NewsApiClient(api_key='c9669e9e1bed456eb08fc9f887a5054a')
    news = newsapi.get_everything(q='cybersecurity tips',
                                  language='en',
                                  sort_by='relevancy',
                                 )    
    return news['articles']  # Get the first 5 articles

@login_required 
def main_page(request):
    articles = get_news()
    event_counts_dict = get_event_counts()

    context = {
        'articles': articles,
        'event_counts': json.dumps(event_counts_dict),
    }

    return render(request, "main_page.html", context)



@login_required
def tables(request):
    logs = []
    log_folder = 'log_folder'
    #today = datetime.date.today()
    filename = f'folder_access_2024-06-10.enc' #f'folder_access_{today}.enc'
    
    # Recupere a chave da variável de ambiente
    key = os.environ['FERNET_KEY'].encode()

    with open(filename, "rb") as f:
        encrypted_data = f.read()
    
    # Verifique se a chave existe e se o arquivo existe
    if key and os.path.exists(os.path.join(log_folder, filename)):
        with open(os.path.join(log_folder, filename), "rb") as f:
            encrypted_data = f.read()
        
        # Desencriptar 
        decrypted_data = decrypt_data(key, encrypted_data)

        for line in decrypted_data.splitlines():
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


""""
@login_required
def tables(request):
    logs = []
    log_folder = 'log_folder'
    today = datetime.date.today()
    filename = f'folder_access_{today}.log'
    file_path = os.path.join(log_folder, filename)
    
    # Verificar se o arquivo existe antes de tentar ler
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        
        # Recuperar a chave da variável de ambiente
        key = os.environ.get('FERNET_KEY')
        
        if key:
            key = key.encode()
            
            # Desencriptar os dados
            cipher_suite = Fernet(key)
            original_data = cipher_suite.decrypt(encrypted_data)
            
            # Decodificar os dados desencriptados
            decoded_data = original_data.decode()
            
            # Processar os dados decodificados
            for line in decoded_data.splitlines():
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

"""

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

# Define the decryption function
def decrypt_data(key, encrypted_data):
    cipher_suite = Fernet(key)
    original_data = cipher_suite.decrypt(encrypted_data).decode()
    return original_data