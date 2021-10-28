#importer les packages
from bs4 import BeautifulSoup
import requests
import pandas as pd 

#On va récupérer le nombre de page du site
url = "https://www.coingecko.com/fr"
page = requests.get(url)
 
soup = BeautifulSoup(page.content, 'html.parser')

page_item = soup.find_all(class_='page-item')
numpage_text = page_item[len(page_item)-2].text

#On va parcourir toutes les pages et parser l'ensemble de ses données
cryptos = []
for numpage in range(int(numpage_text) + 1):
    url = "https://www.coingecko.com/fr?page=" + str(numpage)
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    tableau = soup.find_all('tr')

    #On récupère toutes les données de la page
    for i in range(1, len(tableau)):
        crypto =[]
        for j in tableau[i].find_all('td'):
            crypto.append(j.text.replace("\n", ""))
        cryptos.append(crypto)

    #On recupère l'intitulé des colonnes une et uniquement une fois
    if(numpage == 1):
        head = soup.find_all('thead')
        column_name = []
        for j in range(len(head)):
            name = head[j].find_all('th')
            for k in range(2, 9):
                if(name[k].find('\xa0') != -1):
                    column_name.append(name[k].text.replace('\n', '').replace('\xa0', ''))
                else:
                    column_name.append(name[k].text.replace('\n', ''))

#On supprime les colonnes inutiles 
for l in cryptos:
    del l[0]
    del l[0]
    del l[7]

df = pd.DataFrame(cryptos, columns = column_name)
df.to_csv('../out/gecko.csv', index=False)