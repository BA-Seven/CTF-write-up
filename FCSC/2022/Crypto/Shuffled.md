# Shuffled
## Enoncé
Oops, nous avons mélangé les caractères du flag. Pourrez-vous les remettre dans l'ordre ?
## Découverte
On nous donne 2 fichiers avec l'énoncé :
- [shuffled.py](./utils/shuffled.py)
- [output.txt](./utils/output.txt)

Après une rapide analyse, on constate que `output.txt` est un fichier qui contient le flag mélangé. Tandis que le script python est celui utilisé pour mélanger les caractères du flag original.

## Résolution
Le script utilise la fonction `random.shuffle()` pour mélanger les caractères. On cherche donc à inverser cette fonction. [Ce lien](https://crypto.stackexchange.com/questions/78309/how-to-get-the-original-list-back-given-a-shuffled-list-and-seed) semble aider beaucoup à comprendre les enjeux. Après adaptation du snippet à la situation, on obtient donc un script de ce genre : [decode.py](./utils/decode.py).

On a en sortie une liste de 257 flag possibles, il suffit de lancer un grep sur le mot "flag" et obtient alors le bon déchiffrement.
