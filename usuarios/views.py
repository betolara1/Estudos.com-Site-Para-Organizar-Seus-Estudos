from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib import auth

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    
    
def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não são iguais')
            return redirect('/usuarios/cadastro')
        
        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuário já existente')
            return redirect('/usuarios/cadastro')
        
        try:
            user = User.objects.create_user(
                username = username,
                password = confirmar_senha,
            )

            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso')
            return redirect('/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/usuarios/cadastro')
        

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username=username, password=senha)
        
        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Logado!')
            return redirect('/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidas')
            return redirect('/usuarios/login')
        

def logout(request):
    auth.logout(request)
    return redirect('/')
