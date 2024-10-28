# Guia de instalação e configuração do projeto
- Este guia fornece um passo a passo para criar e configurar o projeto desenvolvido
- O projeto usa django para receber a solicitação do usuário via navegador e então chamar uma tarefa com o uso do Selenium para: 
  - Abrir uma página específica no navegador Chrome
  - Encontrar a tabela de livros
  - Extrair as informações como título, autor, ano, descrição
  - Salvar essas informações em arquivo, no formato json
  - A url espera um parâmetro com o ano dos livros que deseja filtrar, para não filtrar informe o valor 0

## Requisitos

- Python 3.x
- `pip` para gerenciar pacotes Python

## Passo 1: Instalar o Django

Primeiro, instale o Django usando `pip`. Abra seu terminal e execute:

```bash
python3 -m pip install django
#OU
pip install django
```

## Passo 2: Criar um Projeto Django

Após instalar o Django, crie o projeto com o comando:

```bash
django-admin startproject rpa
#OU
python3 -m django startproject rpa

# se você já clonou o projeto vazio do git, adicione um ponto ao final do comando, para não criar outra subpasta, assim:

django-admin startproject rpa .
#OU
python3 -m django startproject rpa .
```

## Passo 3: Navegar para o Diretório do Projeto
Siga esse passo apenas se você não usou o `.` no final do comando anterior

Entre no diretório do projeto que foi criado:

```bash
cd rpa
```

## Passo 4: Criar um Aplicativo Django

Dentro do projeto, crie um aplicativo. O Django organiza funcionalidades em "apps". Para criar o primeiro app, use:

```bash
python3 manage.py startapp books
```

## Passo 5: Configurar o Aplicativo no Projeto

1. No arquivo `settings.py`, adicione o nome do aplicativo na lista `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # outras apps
    'books',
]
```

2. Salve o arquivo.

## Passo 6: Reconfigurar o BASE_DIR
No arquivo `settings.py` do seu projeto, vamos reconfigurar o BASE_DIR para permitir importações e montagens de caminhos de arquivos

Onde tem:
```bash
from pathlib import Path
```
Troque por:
```bash
import os
```

Onde tem:
```bash
BASE_DIR = Path(__file__).resolve().parent.parent
```
Troque por:
```bash
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

Onde tem:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
Troque por:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

## Passo 7: Criar uma View para executar a chamada da tarefa com o selenium
No arquivo `views.py` do seu aplicativo, adicione a seguinte view:

```bash
import os
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
import datetime
from rpa.settings import BASE_DIR


def coletar_dados_livros(request, year_to_filter):
    if not year_to_filter or year_to_filter == "0":
        year_to_filter = None
    # URL onde a tabela de livros está localizada
    books_url = "https://api.vrltech.com.br/books"

    # Inicialização do WebDriver
    driver = webdriver.Chrome()  # Altere para o WebDriver do navegador que você usa

    try:
        # Passo 1: Acessar a URL com a tabela de livros
        driver.get(books_url)
        time.sleep(2)  # Aguardar a página carregar

        # Passo 2: Coletar dados da tabela de livros
        books = []
        rows = driver.find_elements(By.XPATH, "//table/tbody/tr")  # XPath do elemento

        for row in rows:
            title = row.find_element(By.XPATH, "./td[1]").text
            author = row.find_element(By.XPATH, "./td[2]").text
            year = row.find_element(By.XPATH, "./td[3]").text
            description = row.find_element(By.XPATH, "./td[4]").text

            if not year_to_filter or int(year_to_filter) == int(year):
                books.append({
                    "title": title,
                    "author": author,
                    "description": description,
                    "year": year,
                })

        # Passo 3: Salvar dados coletados em arquivo JSON
        date_now = datetime.datetime.now().strftime("%Y%m%d-%H-%M-%S")
        year_filtrado = '' if not year_to_filter else f"_{year_to_filter}"
        file_name = f"{date_now}_books{year_filtrado}_data.json"
        path_to_file = os.path.join(BASE_DIR, 'books', 'files', file_name)
        with open(path_to_file, "w") as file:
            json.dump(books, file, indent=4, ensure_ascii=False)

        return JsonResponse({"message": "Dados coletados com sucesso."})
    except Exception as e:
        return JsonResponse({"error": f"Erro ao coletar dados: {str(e)}"}, status=500)
    finally:
        # Encerrar o WebDriver
        driver.quit()
```

## Passo 8: Configurar o roteamento no `urls.py` no seu app
- No diretório do seu app, crie o arquivo `urls.py`
- Adicione a importação da view e configure a URL:

```bash
from django.urls import path
from .views import coletar_dados_livros

urlpatterns = [
    path('coletar-dados-livros/<int:year_to_filter>', coletar_dados_livros, name='coletar-dados-livros'),
]
```

## Passo 9: Incluir no seu projeto o roteamento feito 
- No diretório do seu projeto, abra o arquivo `urls.py`
- Inclua o arquivo de rotas criado anteriormente

```bash
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
]
```

## Passo 10: Executar o Servidor
Agora, você pode iniciar o servidor local para testar o projeto

```bash
python3 manage.py runserver
```

Acesse o servidor em seu navegador pelo endereço `http://127.0.0.1:8000/`.

## Conclusão

Pronto! Você criou e configurou o projeto, agora faça os testes e veja os arquivos gerados em `books/files`
