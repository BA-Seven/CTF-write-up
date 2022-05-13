# Chatpristi 1/2
## Enoncé
Un ami m'a fourni un site pour stocker mes memes, et il me dit qu'il y a deux flags cachés dedans. Pouvez-vous m'aider à les trouver ?

Pour cette première épreuve, votre but est de trouver un meme caché.
## Découverte
On découvre un site très simple contenant plusieurs memes (6 au total) parfois regroupés par un système de tags. Un champ de recherche peut être utilisé pour trouver les memes à partir de leurs tags. Cependant, les noms de fichiers sont inintelligibles donc impossible de deviner le nom du 7e meme.

## Réflexion
Le seul point d'entrée viable du site semble être le champ de recherche. On essaye donc de provoquer une erreur avec le caractère `'`. Parfait ! `https://chatpristi.france-cybersecurity-challenge.fr/?search=%27` retourne une erreur :
`pq: operator is not unique: unknown % unknown`
Le site est donc probablement vulnérable aux SQLi et tourne avec PostgreSQL.

## Exploitation
Après plusieurs essais de payloads POC. On obtient un payload `');--` URLencoded (qui devient `%27%29%3b--` pour éviter les erreurs) qui ne provoque pas de dysfonctionnement.

On utilise donc cette approche pour réaliser une injection UNION based. Après plusieurs essais de repérage, on parvient à lister les tables avec `test')UNION select 1,'',tablename from pg_tables;--`. En circulant rapidement sur la page, on repère la table `memes` (et la table `___youw1lln3verfindmyfl4g___` si on est pas stupide comme moi :/).

Il suffit alors de lister les colonnes de cette table avec `test')UNION select 1,'',column_name from information_schema.columns where table_name='memes';--` :
- tags
- filename
- id
La colonne intéressante est bien entendu `filename` qu'on extrait gentiment avec `test')UNION select 1,filename,'' from memes;--` ce qui nous donne 7 memes dont un contenant le flag à recopier pour notre plus grand plaisir.
