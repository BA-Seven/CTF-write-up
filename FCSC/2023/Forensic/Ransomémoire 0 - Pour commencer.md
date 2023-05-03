# Ransomémoire 0/3 - Pour commencer

## Enoncé
Vous vous préparez à analyser une capture mémoire et vous notez quelques informations sur la machine avant de plonger dans l'analyse :

    nom d'utilisateur,
    nom de la machine,
    navigateur utilisé.

Le flag est au format FCSC{<nom d'utilisateur>:\<nom de la machine>:\<nom du navigateur>} où :

    <nom d'utilisateur> est le nom de l'utilisateur qui utilise la machine,
    <nom de la machine> est le nom de la machine analysée et
    <nom du navigateur> est le nom du navigateur en cours d'exécution.

Par exemple : FCSC{toto:Ordinateur-de-jojo:Firefox}.

# Résolution
Le fichier donné est un dump de mémoire classique, étudiable avec volatility. Cette simple commande (avec volatility 3) nous donne la liste des processus.
```
python3 vol.py -f ../fcsc.dmp windows.envars.Envars
```

Plus qu'à chercher le navigateur utilisé : Brave, l'utilisateur sur la machine : Admin et enfin le nom de l'ordinateur : DESKTOP-PI234GP
