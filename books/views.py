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
