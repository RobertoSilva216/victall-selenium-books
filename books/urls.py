from django.urls import path
from .views import coletar_dados_livros

urlpatterns = [
    path('coletar-dados-livros/<int:year_to_filter>', coletar_dados_livros, name='coletar-dados-livros'),
]
