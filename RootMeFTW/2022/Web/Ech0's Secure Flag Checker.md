# Ech0's Secure Flag Checker

## Enoncé 

> Ech0 has developed his own flag checker... A shady staff member from the team informs you that Ech0, the author of the tool and the website that presents it isn't as good at security as he pretends.

>   The admin is currently running the FlagChecker on his server. There is a vulnerability that allows you to read the flag from the next obfuscation challenge (Javascript - Obfuscation 6).

>   Everyone hates obfuscation so just get that flag so that you don't need to do it when it'll come out.

 Authors : `AnthoLaMalice#7246` and ``\`#0001``

## Découverte

Cliquons sur le lien du challenge. On est face à un site basique quoique assez sympa (en fait il nous explose pas les yeux c'est assez cool). On trouve deux pages principales. D'abord la page home :

![[./images/home.png]](./images/home.png)

Puis la page app :

![[./images/app.png]](./images/app.png)

On est bon élève donc on fait ce qu'on nous dit : on télécharge [le script](./utils/flagChecker.py).

## Exploration

### Le script
Rien de bien intéressant dans le script. Il vérifie simplement la complexité du flag proposé. 
![[./images/script.png]](./images/script.png)

Juste bizarre qu'il nous donne son PID à chaque lancement. Ce genre d'éléments est rarement un hasard.
Comme on est malin, on a bien vu la ligne de l'énoncé :
> The admin is currently running the FlagChecker on his server.

Et on a même pas galeré.

### La LFI
Deuxième trouvaille : les pages affichées dans le site sont gérées par le paramètre `view` qui pue la Local File Inclusion (LFI).

![[./images/param.png]](./images/param.png)

Petit test rapide avec `?view=/etc/passwd` :

![[./images/hey.png]](./images/hey.png)

Ici on passe en mode mauvais élève parce qu'on a définitivement un truc intéressant. Time to exloit !

## Exploitation

Vous vous rappelez l'histoire du PID et du fait que le script est en train de tourner côté serveur ? Et bah bravo. (Nan en vrai gardez le en tête)

Qu'est-ce qu'on peut faire de marrant avec une LFI ? Dans le monde merveilleux de Linux où tout est fichier on peut lister les processus en cours d'exécution. Je dis ça je dis rien.
Pour le faire il suffit d'inclure le fichier /proc/X/cmdline avec X le PID du processus. Ce fichier cmdline renvoie en fait la ligne de commande avec laquelle le programme a été lancé. Evidemment on va pas s'amuser à checker tous les PID à la main donc pour l'occasion j'ai fait un petit script que vous pouvez retrouver [ici](./utils/lfi_process_checker.py). 

On peut tenter de leak le premier processus avec `?view=/proc/1/cmdline` qui nous renvoie un très sympathique : 
![[./images/cmdline.png]](./images/cmdline.png)

Plus qu'à tester sur les autres PID... No spoil mais celui qui marche c'est le 8. On voit alors apparaître sous nos yeux ébahis cette sainte ligne :

      python3/var/www/html/flagChecker.py--flagRM{Thx...0bfu6}

## Conclusion
Petit chall bien fun qui sort de l'ordinaire. Un grand merci aux créateurs et à RootMe pour le CTF.
