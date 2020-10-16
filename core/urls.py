from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import views
from core.views import buscaviews

urlpatterns = [
    path('',views.index, name='index'),
    path('ajuda/', views.ajuda, name="ajuda"),
    path('contato/', views.contato, name="contato"),
    path('main/', views.main, name='main'),
    path('publicar/', views.publicar, name="publicar"),
    path('post/<int:post_id>',views.post, name="post"),
    path('comentar/',views.comentar, name="comentar"),
    path('edita_post', views.edita_post, name="edita_post"),
    path('atualiza_post/', views.atualiza_post, name="atualiza_post"),
    path('remove_post/', views.remove_post, name="remove_post"),
    path('buscar/', buscaviews.busca, name="buscar"),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)