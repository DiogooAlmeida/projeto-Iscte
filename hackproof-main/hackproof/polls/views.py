from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def home(request):
    return render(request, "home.html")
 
    

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username = username,  password = password)

        if user:
            login_django(request, user)
            return render(request, "home.html")
            
        else:
            return HttpResponse(f"não autenticado")
            


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    else: 
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password1")

        create_username = f"{firstname} {lastname}"
        username = create_username

        user = User.objects.filter(email = email).first()

        if user:
            return HttpResponse("Já existe uma conta com esse email!")
        
        user = User.objects.create(first_name= firstname, last_name= lastname, email= email, password = password, username = username)  
        user.save()

        return HttpResponse("Resgisto feito com sucesso!")



def tables(request):
    return render(request, "tables.html")

def dicas(request):
    return render(request, "dicas.html")

def password(request):
    return render(request, "forgot-password.html")

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