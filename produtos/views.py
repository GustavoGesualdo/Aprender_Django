from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import NovaPessoa, Doador
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date
from django.shortcuts import render
from django.http import JsonResponse # ESSENCIAL para retornar JSON
from django.db.models import Q        # ESSENCIAL para pesquisas complexas
from django.contrib.auth.decorators import login_required
from .models import Doador            # Seus modelos de banco de dados
# from .models import NovaPessoa      # Seus outros modelos

def minha_pagina(request):
    return render(request, 'index.html')

def contato_projeto(request):
    return render(request, 'contato.html')

def logout(request):
    auth_logout(request)  # Encerra a sessão do usuário
    return redirect('/')  # Redireciona para a página inicial (ou outra página desejada)

def login(request):
    if request.method == 'POST':
        # Obtém o username e password do formulário enviado via POST
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentica o usuário com as credenciais fornecidas
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Se o usuário for autenticado com sucesso, faz o login
            auth_login(request, user)
            # Redireciona para a página inicial (ajuste a URL conforme necessário)
            return redirect('/') # Ou para outra URL como 'home'
        else:
            # Se a autenticação falhar, exibe uma mensagem de erro (opcional)
            messages.error(request, 'Usuário ou senha inválidos.')
            # Renderiza a página de login novamente
            return render(request, 'login.html')
    else:
        # Se a requisição for GET, apenas renderiza a página de login
        return render(request, 'login.html')
  
class ResetSenhaForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nome de Usuário')
    new_password = forms.CharField(widget=forms.PasswordInput, label='Nova Senha')
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Nova Senha')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        new_password = self.cleaned_data['new_password']
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return True
        except User.DoesNotExist:
            self.add_error('username', 'Usuário não encontrado.')
            return False

def resetar_senha(request):
    if request.method == 'POST':
        form = ResetSenhaForm(request.POST)
        if form.is_valid():
            if form.save():
                messages.success(request, 'Senha alterada com sucesso!')
                return redirect('login')  # Redirecione para a página de login após o sucesso
            else:
                messages.error(request, 'Erro ao alterar a senha. Verifique o nome de usuário.')
    else:
        form = ResetSenhaForm()
    return render(request, 'reset_senha.html', {'form': form})

@login_required
def cadastro_crianca(request):
    if request.method == "GET":
        crianca_id = request.GET.get('id')
        crianca = None
        if crianca_id:
            crianca = get_object_or_404(NovaPessoa, id=crianca_id)
        return render(request, 'cadastro.html', {'crianca': crianca})

    elif request.method == "POST":
        acao = request.POST.get('acao')

        if acao == "criar":
            nome = request.POST.get('nome')
            data_nascimento = request.POST.get('data_nascimento')
            rua = request.POST.get('rua')
            numero = request.POST.get('numero')
            bairro = request.POST.get('bairro')
            responsavel = request.POST.get('responsavel')
            telefone = request.POST.get('telefone')

            pessoa = NovaPessoa(
                nome=nome,
                data_nascimento=data_nascimento,
                rua=rua,
                numero=numero,
                bairro=bairro,
                nome_responsavel=responsavel,
                telefone=telefone
            )
            pessoa.save()
            messages.success(request, 'Criança cadastrada com sucesso.')
            return redirect('cadastro_crianca') # Redireciona de volta para a página de cadastro

        else:
            messages.error(request, 'Ação inválida.') # Adiciona a mensagem de erro
            return redirect('cadastro_crianca') # Redireciona de volta para a página de cadastro

@login_required # Mantendo o decorator para consistência
def cadastro_doador(request):
    if request.method == "GET":
        # Usa o nome do template que você estava tentando usar antes: 'cadastro_doador.html'
        return render(request, 'cadastrodoador.html', {}) 

    elif request.method == "POST":
        # Como não estamos usando Form, pegamos os dados diretamente
        nome_doador = request.POST.get('nome')
        email_doador = request.POST.get('email')
        telefone_doador = request.POST.get('telefone')
        
        # --- Validação Manual Simples (Baseada no que foi sugerido antes) ---
        erros = {}
        if not nome_doador:
            erros['nome'] = 'O nome é obrigatório.'
        if not email_doador or '@' not in email_doador:
            erros['email'] = 'O email é inválido ou obrigatório.'
        
        
        if not erros:
            try:
                # Salvando no modelo Doador
                Doador.objects.create(
                    nome=nome_doador,
                    email=email_doador,
                    telefone=telefone_doador
                )
                messages.success(request, 'Doador cadastrado com sucesso.')
                # Redireciona de volta para a página de cadastro
                return redirect('cadastrodoador') 

            except Exception as e:
                # Captura erro de DB, como email duplicado
                erros['geral'] = f'Erro ao salvar: {e}'

        # Se houver erros, renderiza novamente com os dados preenchidos
        contexto = {
            'erros': erros,
            'dados_preenchidos': request.POST, # Mantém os dados no formulário
        }
        
        # Se houver erro ou GET, renderiza o template simples 'cadastro_doador.html'
        return render(request, 'cadastrodoador.html', contexto)

@login_required
def visualizar_doador(request):
    # Pegar parâmetros sem .lower() — icontains já cuida do case
    nome_param = request.GET.get('nome', '').strip()
    email_param = request.GET.get('email', '').strip()

    # Validação: nome é obrigatório (exceto se for "todos")
    if not nome_param:
        return JsonResponse({
            'sucesso': False,
            'mensagem_erro': 'O campo "nome" é obrigatório.',
            'doadores': []
        })

    # Inicializa com todos
    doadores_query = Doador.objects.all().order_by('nome')

    # Lógica de filtro
    if nome_param.lower() == 'todos':
        if email_param:
            doadores_query = doadores_query.filter(email__icontains=email_param)
        # else: mostra todos
    else:
        # Filtros normais
        filtros = Q()
        if nome_param:
            filtros &= Q(nome__icontains=nome_param)
        if email_param:
            filtros &= Q(email__icontains=email_param)
        doadores_query = doadores_query.filter(filtros)

    # Serialização
    doadores_list = [
        {
            'id': d.id,
            'nome': d.nome,
            'email': d.email,
            'telefone': d.telefone or 'N/A',
        }
        for d in doadores_query
    ]

    return JsonResponse({
        'sucesso': True,
        'total': len(doadores_list),
        'doadores': doadores_list
    })

@login_required
def atualizar_crianca(request):
    if request.method == "GET":
        crianca_id = request.GET.get('id')
        crianca = None
        if crianca_id:
            crianca = get_object_or_404(NovaPessoa, id=crianca_id)
        return render(request, 'atualizar.html', {'crianca': crianca})

    elif request.method == "POST":
        acao = request.POST.get('acao')

        if acao == "deletar":
            crianca_id_deletar = request.POST.get('id_deletar')
            if crianca_id_deletar:
                try:
                    crianca = NovaPessoa.objects.get(id=crianca_id_deletar)
                    crianca.delete()
                    messages.success(request, 'Apagado cadastrado da Criança com sucesso.')
                    return redirect('atualizar_crianca') # Redireciona de volta para a página de cadastro
                except NovaPessoa.DoesNotExist:
                    messages.error(request, 'Criança não encontrada para apagar.')
                    return redirect('atualizar_crianca') # Redireciona de volta para a página de cadastro
            else:
                return HttpResponse("ID da criança para deletar não fornecido.")

        elif acao == "editar":
            crianca_id_editar = request.POST.get('id_editar')
            if crianca_id_editar:
                try:
                    crianca = NovaPessoa.objects.get(id=crianca_id_editar)
                    crianca.nome = request.POST.get('nome')
                    crianca.data_nascimento = request.POST.get('data_nascimento')
                    crianca.rua = request.POST.get('rua')
                    crianca.numero = request.POST.get('numero')
                    crianca.bairro = request.POST.get('bairro')
                    crianca.nome_responsavel = request.POST.get('responsavel')
                    crianca.telefone = request.POST.get('telefone')
                    crianca.save()
                    messages.success(request, 'Atualizado cadastrado da Criança com sucesso.')
                    crianca_id = request.GET.get('id')
                    crianca = None
                    if crianca_id:
                        crianca = get_object_or_404(NovaPessoa, id=crianca_id)
                    return render(request, 'atualizar.html', {'crianca': crianca})
                except NovaPessoa.DoesNotExist:
                    messages.error(request, 'Criança não encontrada para editar.')
                    return render(request, 'atualizar.html', {'crianca': crianca})
            else:
                return HttpResponse("ID da criança para editar não fornecido.")

        else:
            return HttpResponse("Ação inválida.")
        
@login_required
def pesquisa_crianca(request):
    nome_param = request.GET.get('nome', '').strip().lower()
    responsavel_param = request.GET.get('nome_responsavel', '').strip()
    resultados = []

    if nome_param == 'todos':
        if responsavel_param:
            # Todas as crianças com esse responsável
            resultados = NovaPessoa.objects.filter(
                nome_responsavel__icontains=responsavel_param
            ).order_by('-data_nascimento')
        else:
            # Todas as crianças
            resultados = NovaPessoa.objects.all().order_by('-data_nascimento')
    elif nome_param:
        if responsavel_param:
            # Nome E responsável
            resultados = NovaPessoa.objects.filter(
                Q(nome__icontains=nome_param) & Q(nome_responsavel__icontains=responsavel_param)
            ).order_by('-data_nascimento')
        else:
            # Apenas nome
            resultados = NovaPessoa.objects.filter(
                nome__icontains=nome_param
            ).order_by('-data_nascimento')
    else:
        # Nenhum nome fornecido
        mensagem_erro = "O nome da criança é obrigatório para a pesquisa."
        return render(request, 'pesquisa.html', {'mensagem_erro': mensagem_erro})

    if not resultados.exists():
        mensagem_erro = "Nenhuma criança encontrada com os critérios fornecidos."
        return render(request, 'pesquisa.html', {'mensagem_erro': mensagem_erro})

    maiores_18 = sum([crianca.idade >= 18 for crianca in resultados])
    
    context = {
    'resultados': resultados,
    'maiores_18': maiores_18,
    }
    return render(request, 'pesquisa.html', context)