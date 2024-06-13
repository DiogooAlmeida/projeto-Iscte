from django.shortcuts import render, redirect
from django.contrib import messages
from newsapi import NewsApiClient
from collections import Counter
from django.contrib.auth.decorators import login_required
from .models import Path
from django.core.mail import send_mail
import os
import datetime
import json
import glob
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from .models import LogFilesEncrypted
from datetime import date
from django.utils import timezone
from django.core.files import File
from django.contrib.auth import get_user_model
from allauth.account.forms import ChangePasswordForm, AddEmailForm
from .forms import UserUpdateForm


def index(request):
    return render(request, "index.html")

def dicas(request):
    return render(request, "dicas.html")

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
def perfil(request):
    if request.method == 'POST':
        send_emails(request)
        return redirect('perfil')
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
    today = datetime.date.today()
    filename = f'folder_access_{today}.log'
    file_path = os.path.join('log_folder', filename)

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            logs = [
                dict(zip(['date_time', 'event_name', 'folder_path', 'destination_path', 'user'], line.strip().split(' - ')[:5]))
                for line in f if len(line.strip().split(' - ')) >= 5
            ]
    else:
        logs = []
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

def send_emails(request):
    user_email = request.user.email

    folder_path = 'archive_folder'  # replace with your folder path
    files_in_folder = os.listdir(folder_path)

    if files_in_folder:
        email = EmailMessage(
            'Your monthly logs',  # subject
            'Body of the message',  # message
            'letter.1alert@gmail.com',  # from email
            [user_email],  # recipient list
        )

        for file_name in files_in_folder:
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'rb') as file:
                email.attach(file_name, file.read())

        email.send()
    else:
        messages.error(request, 'No files found in the selected folder.')


User = get_user_model()

@login_required
def account_settings(request):

    email_form = AddEmailForm(user=request.user)
    password_form = ChangePasswordForm(request.user)
    user_form = UserUpdateForm(instance=request.user)
    

    if request.method == 'POST':
        if 'change_password' in request.POST:
            password_form = ChangePasswordForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()  
                messages.success(request, 'Sua senha foi alterada com sucesso.')
                return redirect('definicoes')
            
        elif 'delete_account' in request.POST:
            password = request.POST.get('password')
            if request.user.check_password(password):
                request.user.delete()
                messages.success(request, 'Sua conta foi excluída com sucesso.')
                return redirect('account_login')
            else:
                messages.error(request, 'Senha incorreta.')

        elif 'update_user' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Seu perfil foi atualizado com sucesso.')
                return redirect('definicoes')

    else:
        email_form = AddEmailForm(user=request.user)
        password_form = ChangePasswordForm(request.user)

    return render(request, 'definicoes.html', {
        'email_form': email_form,
        'password_form': password_form,
        'user_form': user_form,
        
    })
