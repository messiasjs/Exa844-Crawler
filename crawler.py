import urllib.request
from bs4 import BeautifulSoup
import json



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

url = "https://www.publishnews.com.br/ranking/mensal/0/"
year =2022
month =1
while year <= 2022:
    month = 1
    for m in range(1,13):
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


                livro =dict()
                livro["nome"] = nome.text
                livro["autor"] = autor.text
                livro["editora"] = editora.text
                if resumo:
                    livro["resumo"] = resumo.p.text
                livro["isbn"] = isbn.strong.text
                livro["categoria"] = categoria.strong.text
                livro["numero_paginas"] = num_paginas.strong.text

                exemplar = dict()
                exemplar["isbn_livro"] = isbn.text
                exemplar["posicao"] = posicao.text
                exemplar["copias_vendidas"] = volume.text
                exemplar["mes_ano"] = str(month)+"/"+str(year)

                livro["exemplar"] = exemplar

                livros.append(livro)  

   
        livros_mes = dict()
        livros_mes["mes_ano"] = str(month)+"/"+str(year)
        livros_mes["livros"] = livros
        livros_meses.append(livros_mes)
        livros = []
    year+=1

publish_news["livros_por_mes"] = livros_meses
jsonStr = json.dumps(publish_news, indent=4, ensure_ascii=False) 
with open("publish.json", "w", encoding='utf-8') as outfile:
  outfile.write(jsonStr)