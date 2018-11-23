from bs4 import BeautifulSoup
import requests
import os

principal = requests.get("https://arkmachinetranslations.wordpress.com/ark-table-of-contents/?fbclid=IwAR0Ubwhcj5QvCLfCiD7wj1ZFC0GZL7oK-p2qigJOmesfmvm_stFkM-FlSpw").text
page_soup= BeautifulSoup(principal,'lxml')
containers = page_soup.find("div",{"class":"entry-content"})
lista=[]
cuerpo=""
for item in containers.findAll("p"):
    for enlaces in item.findAll("a",href=True):
        link = enlaces['href']
        if (not "volume" in link and not "japtem" in link):            
            lista.append(link)    
for enlace in lista:
  pagina = requests.get(enlace).text
  texto = BeautifulSoup(pagina,'lxml')
  [x.extract() for x in texto.findAll('script')]
  [x.extract() for x in texto.findAll("div",{"class":"comments-area"})]
  [x.extract() for x in texto.findAll("div",{"class":"sharedaddy"})]
  [x.extract() for x in texto.findAll("div",{"class":"wpcnt"})]
  contenido = texto.find("div",{"class":"entry-content"})
  cuerpo = cuerpo + contenido.prettify()
with open('ark.html', encoding='utf-8', mode='w+') as f:
    f.write("<html><body>")
    f.write(cuerpo)
    f.write("</body></html>")
    f.close
os.system("ebook-convert ark.html ark.epub")
