#importer les packages
from bs4 import BeautifulSoup
import requests
import pandas as pd 

#collecte du contenu de la page URL
url = 'https://www.basketball-reference.com/leagues/NBA_2022_per_game.html'
page = requests.get(url)
#print(page.content)   #affiche le contenu de la page

#Utiliser beautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify) prettify permet d'afficher le HTML de façon structuré

tableau = soup.find_all(class_='full_table')
#prend toute les valeurs du tableau en 'brut'
joueurs = []
for i in range(len(tableau)):
    joueur = []
    for j in tableau[i].find_all('td'):
        joueur.append(j.text)
    joueurs.append(joueur)

#permet de scrapper les nom des colomnes
head = soup.find(class_='thead')
column_name = [head.text for item in head][0]
column_name_clean = column_name.split('\n')[2:-1]

df = pd.DataFrame(joueurs, columns = column_name_clean).set_index('Player')
#df.shape()  #permet d'afficher la taille du tableau
#df['Pos'].value_counts() #permet d'afficher le nombre de joueurs par poste
#df['Age'] = df['Age'].astype(str).astype(int) #permis de convertir la colonne 'Age' en int
# print(df['Age'].mean()) #permet de faire la moyenne de la colonne 'Age'
#print(df['Age'].describe()) #donne toute les info de la colonne 'Age'
df.to_csv('../out/NBA.csv', index = True) #permet d'exporter en format csvd
df.iloc()