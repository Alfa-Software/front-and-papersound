from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from user import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('confirm/<str:token>', views.confirma_email, name="confirma"),
    path('user/<str:usuario>', views.perfil, name="user"),
    path('seguir/',views.seguir, name="seguir"),
    path('deseguir/',views.deseguir, name="deseguir"),
    #path('buscar/', buscaviews.busca, name="buscar"),
]