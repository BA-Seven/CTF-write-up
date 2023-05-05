# ENISA Flag Store 1/2

# ENISA Flag Store 1/2

## Enoncé

L'ENISA a décidé de mettre en place un nouveau service en ligne disponible à l'année pour les équipes qui participent à l'ECSC. Ce service permet aux joueurs des différentes équipes nationales de se créer des comptes individuels en utilisant des tokens secrets par pays. Une fois le compte créé, les joueurs peuvent voir les flags capturés dans différents CTF.

Les données personnelles des utilisateurs (mot de passe et pays) sont protégées dans la base de données, seuls les noms d'utilisateurs sont stockés en clair.

Le token pour la Team France est ohnah7bairahPh5oon7naqu1caib8euh.

Pour cette première épreuve, on vous met au défi d'aller voler un flag FCSC{...} à l'équipe suisse :-)

## Découverte

Le site propose de s'inscrire, on est alors obligé d'entrer un nom d'utilisateur, un mot de passe, un token et un pays. Une fois enregistré, l'endpoint `/flags` nous offre une panoplie de fake flags. Aucune vuln ne saute aux yeux.

## Étude du code source

Il va bien falloir se mettre à lire sinon on risque pas d'arriver à grand chose. Le seul point d'entrée envisageable semble être les différentes requêtes SQL mais malheureusement, elles sont toutes bien préparées et ne peuvent pas être injectées :

Wait... Toutes ? La requête qui s'occupe du pays n'est pas sécurisée, voici notre point d'entrée !

## Exploitation

L'exploitation est maintenant triviale, plus qu'à se munir d'un proxy et ajouter dans le champ pays `fr' OR 1=1 ;--` au moment de la création du compte (en prenant garde à bien encoder). 

Maintenant `/flags` nous retourne l'intégralité des flags stockés, y compris celui au format FCSC{...}.
