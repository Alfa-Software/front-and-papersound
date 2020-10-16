from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from  django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _
from utils.token import Token
from django.utils import timezone
from utils.auth import verifica_email
import requests

def index( request ):
    if request.user.is_authenticated:
        return redirect('main')
    return render(request ,'pages/index.html')

def ajuda( request ):
    return render(request, 'pages/ajuda.html')

def contato( request ):
    return render(request, 'pages/contato.html')

def main( request ):
    if request.user.is_authenticated:
        posts = Post.objects.order_by('-datetime')
        user = get_object_or_404(User, pk=request.user.id)

        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts_por_pagina = paginator.get_page(page)

        dados = {
            "posts":posts_por_pagina,
        }

        return render(request, 'pages/main.html', dados)

    else:
        return redirect('login')

def publicar( request ):
    if request.user.is_authenticated:
        if request.user.is_trusty:
            if request.method == 'POST':
                titulo = request.POST['titulo']
                descricao = request.POST['descricao']

                if 'audio' in request.FILES:
                    audio = request.FILES['audio']
                else:
                    audio = ''

                if not titulo.strip():
                    messages.error(request,"O campo titulo, não pode ficar vazio")
                    return redirect('publicar')
                elif not descricao.strip():
                    messages.error(request,"O campo descricao, não pode ficar vazio")
                    return redirect('publicar')
                user = get_object_or_404(User, pk=request.user.id)

                publicacao = Post(titulo=titulo, descricao = descricao, audio=audio,postador=user)
                publicacao.save()

                return redirect('main')
        else:
            menssagem = _('Confirme seu email para ter acesso completo ao site.')
            messages.error(request, menssagem)

            return redirect('main')

        return render(request, 'pages/publicar.html')
    else:
        menssagem = _ ('Você precisar estar logado para realizar esta ação.')
        messages.error(request, menssagem)
        return redirect('login')

def post( request, post_id ):
    if request.user.is_authenticated:
        if request.user.is_trusty:
            post = get_object_or_404(Post, pk=post_id)
            comentarios = Comentario.objects.order_by('-datetime').filter(post_id=post_id)

            dados = {
                "post":post,
                "comentarios":comentarios,
            }

            return render(request, 'pages/post.html', dados)
        else:
            menssagem = _('Confirme seu email para ter acesso completo ao site.')
            messages.error(request, menssagem)

            return redirect('main')

    else:
        return redirect('login')
        
def comentar(request):
    if request.user.is_authenticated:
        if request.user.is_trusty:
            if request.method == 'POST':
                user = get_object_or_404(User, pk=request.user.id)
                conteudo = request.POST['conteudo']
                post_id = request.POST['post']
                post = get_object_or_404(Post, pk=post_id)

                comentario = Comentario(conteudo=conteudo, postador=user, post=post)
                comentario.save()

                retorno = '/post/'+str(post_id)

                return redirect(retorno)
        else:
            menssagem = _('Confirme seu email para ter acesso completo ao site. Caso seu email tenha expirado <a href="{% url "renova_token" %}">Clique aqui</a>')
            messages.error(request, menssagem)

            return redirect('main')

    return redirect('login')

def edita_post(request):
    if request.user.is_authenticated:
        if request.user.is_trusty:
            if request.method == 'POST':
                post = request.POST['post']
                post = get_object_or_404(Post, pk=post)
                dados = {
                    'post':post,
                }
                return render(request, 'pages/editpost.html', dados)
            else:
                return redirect('main')
        else:
            menssagem = _('Confirme seu email para ter acesso completo ao site. Caso seu email tenha expirado <a href="{% url "renova_token" %}">Clique aqui</a>')
            messages.error(request, menssagem)

            return redirect('main')
    else:
        return redirect('login')

def atualiza_post(request):
    if request.user.is_authenticated:
        if request.user.is_trusty:
            if request.method == 'POST':
                post = request.POST['post']
                post = Post.objects.get(pk=post)

                post.titulo = request.POST['titulo']
                post.descricao = request.POST['descricao']
                post.editado = timezone.now()

                if 'audio' in request.FILES:
                    post.audio = request.FILES['audio']

                post.save()
                return redirect('main')
            else:
                return redirect('main')
        else:
            menssagem = _('Confirme seu email para ter acesso completo ao site. Caso seu email tenha expirado <a href="{% url "renova_token" %}">Clique aqui</a>')
            messages.error(request, menssagem)

            return redirect('main')
    else:
        return redirect('login')

def remove_post(request):
    if request.user.is_authenticated:
        if request.user.is_trusty:
            if request.method == 'POST':
                post = request.POST['post']
                post = get_object_or_404(Post, pk=post)
                post.delete()

                return redirect('main')
            else:
                return redirect('main')
        else:
            menssagem = _('Confirme seu email para ter acesso completo ao site. Caso seu email tenha expirado <a href="{% url "renova_token" %}">Clique aqui</a>')
            messages.error(request, menssagem)

            return redirect('main')
    else:
        return redirect('login')