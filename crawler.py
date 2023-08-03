import urllib.request
from bs4 import BeautifulSoup
from datetime import date
import json
import csv

publish_news = dict()
livros_mes = dict()

livros_meses = []
livros = []

posicao = ""
nome = ""
volume = ""
autor = ""
editora = ""
resumo = ""
isbn = ""
categoria = ""
num_paginas = ""

data_atual = date.today()

url = "https://www.publishnews.com.br/ranking/mensal/0/"
year =2020
month =1
month_limit = 13

while year <= data_atual.year:
    month = 1

    if  year == data_atual.year:
        month_limit = data_atual.month
    print(month_limit)
    
    for m in range(1,month_limit):
        month=m
        page = urllib.request.urlopen(url+str(year)+"/"+str(month)+"/0/0")
        html = str(page.read().decode('utf-8'))
        soup = BeautifulSoup(html, 'lxml')

        for book in soup.find_all('div', class_='pn-ranking-livros-posicao'):

            posicao = ""
            nome = ""
            volume = ""
            autor = ""
            editora = ""
            resumo = ""
            isbn = ""
            categoria = ""
            num_paginas = ""

            if book:
                posicao = book.find("div",  class_="pn-ranking-livros-posicao-numero")
                nome = book.find("div",  class_="pn-ranking-livro-nome")
                volume = book.find("div",  class_="pn-ranking-livros-posicao-volume")
                autor = book.find("div",  class_="pn-ranking-livro-autor")
                editora = book.find("div",  class_="pn-ranking-livro-editora")
                resumo = book.find("div",  class_="pn-ranking-livro-resumo")
                isbn = book.find("div",  class_="pn-ranking-livro-isbn")
                categoria = book.find("div",  class_="pn-ranking-livro-categoria")
                num_paginas = book.find("div",  class_="pn-ranking-livro-paginas")
                capa = book.find("div", class_="pn-ranking-livro-capa")
                #print(capa.img['src'])

                livro =dict()
                livro["nome"] = nome.text
                livro["autor"] = autor.text
                livro["editora"] = editora.text
                if resumo:
                    livro["resumo"] = resumo.p.text
                livro["isbn"] = isbn.strong.text
                livro["categoria"] = categoria.strong.text
                livro["numero_paginas"] = num_paginas.strong.text
                livro["capa"] = capa.img['src']

                exemplar = dict()
                exemplar["isbn_livro"] = isbn.strong.text
                exemplar["posicao"] = posicao.text
                exemplar["copias_vendidas"] = volume.text
                exemplar["mes_ano"] = str(month)+"//"+str(year)

                #livro["exemplar"] = exemplar
                livro["exemplar"] = isbn.strong.text

                livros.append(livro)  

                with open('exemplares.csv', 'a', newline='') as csvfile:
                    header_key = ['isbn_livro', 'posicao', 'copias_vendidas', 'mes_ano']
                    writer = csv.DictWriter(csvfile, fieldnames=header_key)
                    #writer.writeheader()
                    writer.writerow(exemplar)
                
            
                with open('livros.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    header_key = ["nome", "autor", "editora", "resumo", "isbn", "categoria","numero_paginas", "exemplar", "capa"]
                    writer = csv.DictWriter(csvfile, fieldnames=header_key)
                    #writer.writeheader()
                    writer.writerow(livro)
                    
        livros_mes = dict()
        livros_mes["mes_ano"] = str(month)+"/"+str(year)
        livros_mes["livros"] = livros
        livros_meses.append(livros_mes)
        livros = []
    year+=1

publish_news["livros_por_mes"] = livros_meses
jsonStr = json.dumps(publish_news, indent=4, ensure_ascii=False) 
with open("teste.json", "w", encoding='utf-8') as outfile:
  outfile.write(jsonStr)