import urllib.request
import time
import shutil
import os,fnmatch
import os.path
import zipfile
from bs4 import BeautifulSoup
import uuid

#bajar novelas en el formato https://translations.gocreateme.com/my-girlfriend-is-a-zombie-chapter-234-part-1/
url_base = "https://translations.gocreateme.com/"
url_novela ="my-girlfriend-is-a-zombie-chapter-"
listaArchivos=[]

def url_generator(base,capitulo):
	cap_base=f"{base}{capitulo}"
	cap1=f"{cap_base}-part-1/"
	cap2=f"{cap_base}-part-2/"
	try:
		print(f"bajando capitulo {capitulo}")
		download(f"{cap_base}/",f"{capitulo}.xhtml")
		time.sleep(1)
	except Exception as e:
		print(f"Capitulo {capitulo} dividido, bajando en dos partes")
		download(cap1,f"{capitulo}-1.xhtml")
		time.sleep(2)
		download(cap2,f"{capitulo}-2.xhtml")
		time.sleep(3)

def url_generator2(base,capitulo):
	cap_base=f"{base}{capitulo}"
	
	cap2=f"{cap_base}-part-2/"
	try:
		print(f"bajando capitulo {capitulo}")
		download(cap2,f"{capitulo}-2.xhtml")
		time.sleep(1)
	except Exception as e:
		pass

def download(link, file_name):
	url = urllib.request.Request(link,data=None,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
	with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
		shutil.copyfileobj(response, out_file)

def lista_archivos():
	listOfFiles = os.listdir('.')  
	pattern = "*.xhtml"  
	for entry in listOfFiles:  
		if fnmatch.fnmatch(entry, pattern):
		    listaArchivos.append(entry)

def lista_html():
	listOfFiles = os.listdir('.')  
	pattern = "*.html"  
	for entry in listOfFiles:  
		if fnmatch.fnmatch(entry, pattern):
		    listaArchivos.append(entry)



def clean(file_name_in, file_name_out, start):
	raw = open(file_name_in, "r", encoding = "utf8")
	soup = BeautifulSoup(raw, 'lxml')
	chapter_title = soup.find(class_="entry-title")
	chapter_title = chapter_title.text.replace("My Girlfriend is a Zombie Chapter ","")
	soup = soup.find(class_="entry-content")
	for a in soup.find_all(class_="cb_p6_patreon_button"):
		a.decompose()
	for a in soup.find_all("script"):
		a.decompose()
	for a in soup.find_all("ins"):
		a.decompose()
	raw.close()
	file = open(file_name_out + ".html", "w", encoding = "utf8")
	file.write('<html xmlns="http://www.w3.org/1999/xhtml">')
	file.write("\n<head>")
	file.write("\n<title>" + chapter_title + "</title>")
	file.write("\n</head>")
	file.write("\n<body>")
	file.write("\n<h1>" + chapter_title + "</h1>")
	file.write(str(soup))
	file.write("\n</body>")
	file.write("\n</html>")
	os.remove(file_name_in)
	file.close

def find_between(file):
    f = open(file, "r", encoding = "utf8")
    soup = BeautifulSoup(f, 'html.parser')
    return soup.title

def generate(html_files, novelname, author, chaptername, chapter_s, chapter_e):
    epub = zipfile.ZipFile(novelname + "_" + chapter_s + "-" + chapter_e + ".epub", "w")
    # The first file must be named "mimetype"
    epub.writestr("mimetype", "application/epub+zip")

     # The filenames of the HTML are listed in html_files
    # We need an index file, that lists all other HTML files
    # This index file itself is referenced in the META_INF/container.xml
    # file
    epub.writestr("META-INF/container.xml", '''<container version="1.0"
                  xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
          <rootfiles>
            <rootfile full-path="OEBPS/Content.opf" media-type="application/oebps-package+xml"/>
          </rootfiles>
        </container>''')

    # The index file is another XML file, living per convention
    # in OEBPS/Content.xml
    uniqueid = uuid.uuid1().hex
    index_tpl = '''<package version="3.1"
    xmlns="http://www.idpf.org/2007/opf" unique-identifier="''' + uniqueid + '''">
            <metadata>
                %(metadata)s
            </metadata>
            <manifest>
                %(manifest)s
                <item href="cover.png" id="cover" media-type="image/jpeg" properties="cover-image"/>
            </manifest>
            <spine>
                <itemref idref="toc"/>
                %(spine)s
            </spine>
        </package>'''

    manifest = ""
    spine = ""
    metadata = '''<dc:title xmlns:dc="http://purl.org/dc/elements/1.1/">%(novelname)s</dc:title>
        <dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:ns0="http://www.idpf.org/2007/opf" ns0:role="aut" ns0:file-as="Unbekannt">%(author)s</dc:creator>
        <dc:language xmlns:dc="http://purl.org/dc/elements/1.1/">en</dc:language>
        <dc:identifier xmlns:dc="http://purl.org/dc/elements/1.1/">%(uuid)s"</dc:identifier>''' % {
        "novelname": novelname + ": " + chapter_s + "-" + chapter_e, "author": author, "uuid": uniqueid}
    toc_manifest = '<item href="toc.xhtml" id="toc" properties="nav" media-type="application/xhtml+xml"/>'

    # Write each HTML file to the ebook, collect information for the index
    for i, html in enumerate(html_files):
        basename = os.path.basename(html)
        manifest += '<item id="file_%s" href="%s" media-type="application/xhtml+xml"/>' % (
                      i+1, basename)
        spine += '<itemref idref="file_%s" />' % (i+1)
        epub.write(html, "OEBPS/"+basename)

    # Finally, write the index
    epub.writestr("OEBPS/Content.opf", index_tpl % {
        "metadata": metadata,
        "manifest": manifest + toc_manifest,
        "spine": spine,
        })

 #Generates a Table of Contents + lost strings
    toc_start = '''<?xml version='1.0' encoding='utf-8'?>
        <!DOCTYPE html>
        <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
        <head>
            <title>%(novelname)s</title>
        </head>
        <body>
            <section class="frontmatter TableOfContents">
                <header>
                    <h1>Contents</h1>
                </header>
                <nav id="toc" role="doc-toc" epub:type="toc">
                    <ol>
                    %(toc_mid)s
            %(toc_end)s'''
    toc_mid = ""
    toc_end = '''</ol></nav></section></body></html>'''

    for i,y in enumerate(html_files):
        chapter = find_between(html_files[i])
        chapter = str(chapter)
        toc_mid += '''<li class="toc-Chapter-rw" id="num_%s">
            <a href="%s">%s</a>
            </li>''' % (i, html_files[i], chapter)

    epub.writestr("OEBPS/toc.xhtml", toc_start % {"novelname": novelname, "toc_mid": toc_mid, "toc_end": toc_end})
    epub.write("cover.png", "OEBPS/cover.png")
    epub.close()
    os.remove("cover.png")


    #removes all the temporary files
    for x in html_files:
        os.remove(x)

if __name__=="__main__":
	#for n in range(1, 235):
	#	clean(f"{n}.xhtml",n,1)
	#	url_generator(url_base+url_novela,n)
	#	url_generator2(url_base+url_novela,n)	
	#lista_archivos()
	#i=1
	#for archivo in listaArchivos:
	#	nombre = archivo.split(".")[0]
	#	if len(nombre.split("-")) > 1:
	#		nombre=str(nombre.split("-")[0].zfill(3)+"1")+".xhtml"
	#	else:
	#		nombre=str(nombre.split("-")[0].zfill(3)+"0")+".xhtml"
	#	print(f"Procesando {archivo} a {nombre}")
	#	os.rename(archivo,nombre)
	#	#clean(archivo,f"{str(i).zfill(3)}",1)
	#	i=i+1
	#lista_archivos()	
	#for archivo in listaArchivos:
	#	clean(archivo,archivo.split(".")[0],1)
	novelname="My Girlfriend is a Zombie"
	lista_html()
	generate(listaArchivos,novelname, "Dark lichi","","1","234")



