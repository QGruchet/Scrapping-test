#importer les packages
from bs4 import BeautifulSoup
import requests
import pandas as pd 

joueurs = []
for numpage in range(1, 5):
    url = "https://www.fifaindex.com/fr/players/top/?page=" + str(numpage)
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    tableau = soup.find_all('tr')

    for i in range(1, len(tableau)):
        joueur = []
        for j in tableau[i].find_all('td'):
            #Permet de recuperer la nationalité
            if((str(j).find('link-nation') != -1 )):
                temp = j.find(class_='link-nation')
                temp = str(temp)
                temp = temp.split("=")
                tempo = temp[4]
                joueur.append(tempo[1:-10])

            #Permet de recuperer l'équipe
            if((str(j).find('link-team') != -1 )):
                temp = j.find(class_='link-team')
                temp = str(temp)
                temp = temp.split("=")
                tempo = temp[4]
                joueur.append(tempo[1:-15])
            
            joueur.append(j.text) 
        joueurs.append(joueur)

#permet de supprimer les colonnes vides
for l in joueurs:
    del l[:1]
    del l[1]
    del l[6]

#permet de recuperer les noms des colonnes
head = soup.find('thead')
column_name = [head.text for item in head][0]
column_name_clean = column_name.split('\n')[3:-2]
#On ajoute à la main les deux colonnes parce que c'est codé avec le cul
column_name_clean[0] = 'Nationalité'
column_name_clean[len(column_name_clean) - 1] = 'Club'

df = pd.DataFrame(joueurs, columns=column_name_clean).set_index('Nom')
df = df.sort_values(by=['GEN-POT'], ascending=False)
df.to_csv('../out/FIFA.csv', index = True)