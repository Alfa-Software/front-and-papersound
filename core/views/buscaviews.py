from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import auth, messages
from django.utils.translation import ugettext as _
import requests

def busca(request):
    users = User.objects.order_by('-date_joined').filter(is_trusty=True)
    if 'busca' in request.GET:
        nome_a_buscar = request.GET['busca']
        users = users.filter(username=nome_a_buscar)
    
    dados = {
        "users": users,
    }

    return render(request, 'pages/busca.html', dados)