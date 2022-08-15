# Extractor

## Enoncé
We are under emergency. Enemy is ready with its nuclear weapon we need to activate our gaurds but chief who had password is dead. There is portal at URL below which holds key within super-user account, can you get the key and save us.

## Découverte
On arrive sur site bien dégueulasse avec deux fonctions principales : "register" et "login". Trois champs découlent de ces fonctions : "Username", "Password" et "Signature". On crée un utilisateur "test" avec pour password "test" et pour signature "123456". On tente alors au hasard une SQLi login bypass (`test';--`) par hasard et tient, ça fonctionne...

## Exploitation 
On est donc à peu près certain d'avoir affaire à une SQLi. Seulemen, nous n'avons aucun user donné dont on doit exfiltrer le mot de passe
