# Canflag

## Enoncé 
Lors d'une séance de tuning de votre voiture de compétition, la malette de votre ami garagiste a enregistré des trames dans canflag.pcap. On dirait que votre bolide veut vous parler...

## Résolution
Bon petite recherche sur le protocole CAN... Pas grand chose d'intéressant on s'en tamponne.

On ouvre le fichier avec WireShark en toute tranquilité. On remarque le petit paquet qui contien `FCSC`. 

Un peu plus d'investigation et on se rend compte que les paquets sont ordonés différement que par simple temporalité. Ils sont ordonnés par leur `Identifier` qu'on peut voir dans la case info.

On va donc chercher le petit filtre pour prendre les paquets 2 par 2 : `can.id == 0x00000002` en incluant du coup les XTD et les STD.

Maintenant c'est la partie chiante, on copie d'abord le contenu de XTD, puis de STD, puis on augmente le filtre de 2 : `can.id == 0x00000004`. Puis on recommence.... Evidemment quand pas de caractères ASCII on copie pas ça sert à rien. 

Et puis après avoir fais 20 000 paquets à la main : pouf le flag ! C'est pas le challenge le plus marrant mais faut savoir faire c'est des points à prendre :)
