from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
my_url = "https://arkmachinetranslations.wordpress.com/ark-table-of-contents/?fbclid=IwAR0Ubwhcj5QvCLfCiD7wj1ZFC0GZL7oK-p2qigJOmesfmvm_stFkM-FlSpw"
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html,"html.parser")
#print(page_soup.a)
containers = page_soup.find("div",{"class":"entry-content"})
#print(containers[0])
lista={}
for item in containers.findAll("p"):
	#print(item)
	for enlaces in item.findAll("a",href=True):
		link = enlaces['href']
		if (link.contains("volume")):
			print(f'evitando {link}')
			next()
        print(f'añadiendo {link}')
		lista.add(link)
	
    #for parrafo in item.findAll("p"):
    #    print(parrafo)
