from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _
from utils.token import Token
from django.utils import timezone
from utils.auth import verifica_email
import requests


def cadastro( request ):
    if request.user.is_authenticated:
        return redirect('main')
    if request.method == 'POST':
        usuario = request.POST['username']
        email = request.POST['email']
        email2 = request.POST['email2']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']
        password2 = request.POST['password2']
        datadenascimento = request.POST['datanascimento']

        if not usuario.strip():
            menssagem = _('O campo usuario não pode ficar em branco')
            messages.error(request, menssagem)
            return redirect('cadastro')
        elif not email.strip():
            menssagem = _('O campo email não pode ficar em branco')
            messages.error(request, menssagem)
            return redirect('cadastro')
        elif not firstname.strip():
            menssagem = _('O campo primeiro nome não pode ficar em branco')
            messages.error(request, menssagem)
            return redirect('cadastro')
        elif not lastname.strip():
            menssagem = _('O campo ultimo nome não pode ficar em brancos')
            messages.error(request, menssagem)
            return redirect('cadastro')
        elif password != password2:
            menssagem = _('as senhas não coincidem')
            messages.error(request, menssagem)
            return redirect('cadastro')
        elif email != email2:
            menssagem = _('Os emails não coincidem')
            messages.error(request, menssagem)
            return redirect('cadastro')
        elif not verifica_email(email):
            menssagem = _('Insira um email valido')
            messages.error(request, menssagem)
            return redirect('cadastro')
        """
        elif User.objects.filter(email = email).exists():
            menssagem = _('Úsuario já cadastrado')
            messages.error(request,menssagem)
            return redirect('cadastro')
        elif User.objects.filter(username = usuario).exists():
            menssagem = _('Úsuario já cadastrado')
            messages.error(request,menssagem)
            return redirect('cadastro')
        """
        dados = {
            "username":usuario,
            "email":email,
            "password":password, 
            "first_name":firstname, 
            "last_name":lastname, 
            "is_trusty":0 ,
            "data_de_nascimento":datadenascimento,
        }

        r = requests.post("https://papersound-api.herokuapp.com/usuarios/",data=dados, auth=("julio","15052005"))
        print(r.json())

        #token = Token(request, email)
        #token.make_token()
        #token.envia_token_por_email()

        menssagem = _('Usuario cadastrado com sucesso')
        messages.success(request,menssagem)
        menssagem = _('Confirme seu email para ter acesso completo ao site')
        messages.success(request,menssagem)    
        return redirect('login')
    else:
        return render(request, 'pages/cadastro.html')

    return render(request ,'pages/cadastro.html')

def login( request ):
    if request.user.is_authenticated:
        return redirect('main')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email == "" or password == "":
            menssagem = _("Os campos email e senha não podem ficar em branco")
            messages.error(request, menssagem)
            return redirect('login')
        if User.objects.filter(username = email).exists():
            nome = email
        elif User.objects.filter(email = email).exists():
            nome=User.objects.filter(email=email).values_list('username',flat=True).get()
        else:
            messages.error(request,"Usuario não encontrado")
            return redirect('login')

        user = auth.authenticate(request, username=nome, password=password)
        if user is not None:
            auth.login(request, user)
            menssagem = _('login realizado com sucesso')
            messages.success(request, menssagem)

            
            if not user.is_trusty:
                menssagem = _('Confirme seu email para ter acesso')
                messages.error(request,menssagem)

            return redirect('main')
            
        else:
            menssagem = _("Usuario ou senha invalidos")
            messages.error(request, menssagem)
            return redirect('login')

    return render(request ,'pages/login.html')

def logout( request ):
    auth.logout(request)
    return redirect('index')

def confirma_email( request , token):
    token_verifi = Token( token=token)
    id = token_verifi.check_token()
    user = User.objects.get(pk=id)
    user.is_trusty = 1
    user.save()
    messages.success(request,'Email confirmado com sucesso')
    return redirect('login')

def perfil( request , usuario ):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=usuario)
        if user:
            seguidores = Seguidor.objects.filter(user=user).order_by("-datetime")
            segue = Seguidor.objects.filter(seguid=user).order_by("-datetime")
            posts = Post.objects.filter(postador=user).order_by("-datetime")
            dados = {
                "usuario":user,
                "posts":posts,
                "lensegui":len(seguidores),
                "lensegue":len(segue),
                "lenposts":len(posts),
            }

            if user == request.user:
                if not user.audio or not user.descricao:
                    mensagem = _("Parece que você não completou seu perfil, clique aqui para completar")
                    messages.success(request, mensagem)
            else:
                if Seguidor.objects.filter(seguid_id=request.user.id, user_id=user.id).exists():
                    dados.update({"segue": True})
                else:
                    dados.update({"segue": False})

            return render(request, 'pages/perfil.html', dados)
        else:
            mensagem = _("Usuario não encontrado")
            messages.error(request, mensagem)
            return redirect('main')
    else:
        return redirect('login')

def seguir(request):
    if request.user.is_authenticated:
        if request.user.is_trusty:
            if request.method == 'POST':
                seguidor = request.POST['seguidor']
                user = request.POST['user']

                seguidor = get_object_or_404(User, username=seguidor)
                user = get_object_or_404(User, username=user)
                retorno = "/user/"+user.username
                if seguidor == request.user:
                    if not Seguidor.objects.filter(seguid_id=seguidor.id, user_id=user.id).exists():
                        seguir = Seguidor(user=user, seguid=seguidor)
                        seguir.save()
                return redirect(retorno)
            
            
        else:
            menssagem = _('Confirme seu email para ter acesso completo ao site. Caso seu email tenha expirado <a href="{% url "renova_token" %}">Clique aqui</a>')
            messages.error(request, menssagem)

            return redirect('main')
    else:
        return redirect('login')

def deseguir(request):
    if request.user.is_authenticated:
        if request.user.is_trusty:
            if request.method == 'POST':
                seguidor = request.POST['seguidor']
                user = request.POST['user']

                seguidor = get_object_or_404(User, username=seguidor)
                user = get_object_or_404(User, username=user)
                retorno = "/user/"+user.username
                if seguidor == request.user:
                    if Seguidor.objects.filter(seguid_id=seguidor.id, user_id=user.id).exists():
                        seguir = Seguidor.objects.get(user=user, seguid=seguidor)
                        seguir.delete()
                return redirect(retorno)
            else:
                return redirect('main')

        else:
            menssagem = _('Confirme seu email para ter acesso completo ao site. Caso seu email tenha expirado <a href="{% url "renova_token" %}">Clique aqui</a>')
            messages.error(request, menssagem)

            return redirect('main')
    else:
        return redirect('login')
