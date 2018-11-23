import requests
import os
from bs4 import BeautifulSoup
base = "https://www.wuxiaworld.com"
lista =[]
indice = requests.get("https://www.wuxiaworld.com/novel/stop-friendly-fire").text
soup = BeautifulSoup(indice,"lxml")
[x.extract() for x in soup.findAll('script')] #no es necesario , pero mejor quitar los scripts  
contenidos = soup.findAll("li",{"class":"chapter-item"})
for item in contenidos:
  enlaces=item.find("a",href=True)
  link = enlaces['href']
  lista.append(base+link) #queremos enlaces tipo : https://www.wuxiaworld.com/novel/stop-friendly-fire/sff-chapter-4-5
#Ahora tenemos que procesar la lista de enlaces para quitar la paja.
#Queremos solo el contenido del div class fr-view
salida ="<html><head></head><body>"
for capitulo in lista:
  pagina = requests.get(capitulo).text
  contenido = BeautifulSoup(pagina,"lxml")
  texto = contenido.find("div",{"class":"fr-view"})
  salida = salida + texto.prettify()
salida = salida + "</body></html>"
with open("sff.html", encoding='utf-8',mode="w+") as f:
 f.write(salida)
 f.close()
os.system("ebook-convert sff.html sff.epub")