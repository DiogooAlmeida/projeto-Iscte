from django.shortcuts import render, redirect
from .services import cliente_services
from .entidades import cliente
from .models import Cliente
from .forms import ClienteForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='index')
def listar_clientes(request):
    clientes = cliente_services.listar_cliente()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})

@login_required(login_url='index')
def inserir_cliente(request):
    if request.method == "POST":
        # instancia do formulario recebendo os dados da requisição
        form = ClienteForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data["nome"]
            sexo = form.cleaned_data["sexo"]
            data_nascimento = form.cleaned_data["data_nascimento"]
            email = form.cleaned_data["email"]
            profissao = form.cleaned_data["profissao"]
            cliente_novo = cliente.Cliente(nome=nome, sexo=sexo, data_nascimento=data_nascimento, email=email, profissao=profissao)

            cliente_services.cadastrar_cliente(cliente_novo)
            return redirect('listar_clientes')  # REDIRECIONA PARA A LISTAGEM
    else:
        form = ClienteForm()
    return render(request, 'clientes/form_cliente.html', {'form': form})

@login_required(login_url='index')
def listar_cliente_id(request, id):
    cliente = cliente_services.listar_cliente_id(id)
    return render(request, 'clientes/listar_cliente_id.html', {'cliente': cliente})

@login_required(login_url='index')
def editar_cliente(request, id):
    cliente_antigo = cliente_services.listar_cliente_id(id)
    form = ClienteForm(request.POST or None, instance=cliente_antigo)
    if form.is_valid():
        nome = form.cleaned_data["nome"]
        sexo = form.cleaned_data["sexo"]
        data_nascimento = form.cleaned_data["data_nascimento"]
        email = form.cleaned_data["email"]
        profissao = form.cleaned_data["profissao"]
        cliente_novo = cliente.Cliente(nome=nome, sexo=sexo, data_nascimento=data_nascimento, email=email, profissao=profissao)

        cliente_services.editar_cliente(cliente_antigo, cliente_novo)
        return redirect('listar_clientes')
    return render(request, 'clientes/form_cliente.html', {'form': form})

@login_required(login_url='index')
def remover_cliente(request, id):
    cliente = cliente_services.listar_cliente_id(id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'clientes/confirma_exclusao.html', {'cliente': cliente})
