from bs4 import BeautifulSoup
import requests
import random
import sys
import os
import re
from urllib.parse import urlparse
from guardarFichero import Fichero

from modelos.web import Web

def resource_path(relative_path):
    """ To get resources path for creating the .exe with PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def getUrl(url, pagina):
    if(pagina == ''):
        return url
    else:
        parsed_uri = urlparse(url)
        result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return result + pagina
        

def scrapearEmail(url,user_agent_list, contador):
    contacto = Web(url,'')
    try:        
        user_agent = random.choice(user_agent_list)
        
        headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com",
        "ONT": "1",
        "Sec-Ch-Ua": "\"Chromium\";v=\"88\", \"Google Chrome\";v=\"88\", \";Not A Brand\";v=\"99\"", 
        "Sec-Ch-Ua-Mobile": "?0", 
        "Sec-Fetch-Dest": "document", 
        "Sec-Fetch-Mode": "navigate", 
        "Sec-Fetch-Site": "none", 
        "Sec-Fetch-User": "?1", 
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": user_agent
      }
        
        r = requests.get(url, headers=headers)
        encoding = r.encoding if "charset" in r.headers.get("content-type", "").lower() else None
        soup = BeautifulSoup(r.content, 'lxml', from_encoding=encoding)
        
        containsEmail = soup.find_all(text=re.compile("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"))
        match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', str(containsEmail))
        newemails = match.group(0)
        contacto.email = str(newemails)
        print(str(contador) + '- ' + str(newemails))
    except:
        pass
    return contacto

def main():
    
    listaUrls=[]
    with open('webpages.txt') as f:
        listaUrls = f.read().splitlines()

    archivo = open(resource_path('useragents.txt'),'r')
    user_agent_list = archivo.read().splitlines()
    archivo.close()

    listaContactos=[]
    contUrl = 0
    for url in listaUrls:
        contUrl += 1
        
        contacto = scrapearEmail(url,user_agent_list, contUrl)
        if(contacto.email != ''):
            listaContactos.append(contacto)

    guardar = Fichero(listaContactos)
    guardar.guardarExcel("emails_output.xls")

if __name__ == "__main__":
    main()