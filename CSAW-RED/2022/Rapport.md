# RED Competition - CSAW2022

## Informations données

Scope : newsX.rednews.media, wwwX.fakebouc.com

Identifiants pour FakeBouc : RED_Inspector:azerty

Le nom du hacker est darkHat et son mot de passe est simple à deviner.

## Début d'exploration

### Rednews

En premier lieu on peut se rendre sur le site rednews :

![News](./news.png)
<br>
<br>
<br>
<br>

En regardant le code source, on se rend compte que l'overlay est changé à partir d'un fichier `overlay.txt`.

![source](./source.png)

### FakeBook
En se connectant sur le site avec les identifiants donnés, on constate l'existence d'un compte appartenant au hacker :

![Fakebook](./fakebook.png)

D'un autre côté, l'administrateur nous donne cet indice intéressant :

![admin](./admin.png)

Le mot de passe du hacker semble alors évident :

![kitty](./kitty.png)

On arrive efffectivement à se connecter avec les identifiants : darkHat:kitty-rex.
A partir de là l'exploration se divise en plusieurs branches.

## Branche 1 : Le mode opératoire

En fouillant dans les messages privés du hacker, on se rend compte qu'un certain Tom Johnson a donné au hacker les identifiants d'un développer docker : dckrdev@dckrdev4.rednews.media:IDL0ialdIq

### Connexion ssh
Au vu du format du nom d'utilisateur, on peut se connecter via ssh et obtenir le premier Flag.

`RED{679ee818d2d337b8e3b0a3d33cd084a2}`

### Escalation de privilèges
La commande `sudo -l` nous renvoie les informations suivantes :

![gdb](./gdb.png)

On exploite donc le binaire `gdb` pour augementer nos privilèges :
`sudo gdb -nx -ex '!bash' -ex quit`

Nous sommes alors utilisateur `root`. Mais seulement sur le container Docker.

### Docker escape
Pour sortir du container on liste les capabilités attribuées. Parmis celles exploitables : 
- cap_net_raw
- cap_sys_chroot
- cap_sys_ptrace
- cap_sys_admin  

Malheureusement, les tentatives d'exploitation par ce biais là n'ont pas fonctionné.

<br>
<br>

## Branche 2 : Le hacker
En fouillant dans les posts FakeBook du hacker, on trouve une image nommée hacker.png :

![hacker](./hacker.png)

A l'aide d'`exiftool`, on retrouve les coordonnées géographiques de la prise de la photo, étrangement proche de l'ESISAR.

![map](./map.png)

Il suffit alors de se rendre sur les lieux, pour trouver la planque du hacker et un autre flag : `RED{A015-ESISAR}` (en QR code). On trouve aussi une malette contenant les affaires du hacker.

## Branche 3 : Le commanditaire 
Dans une autre conversation privée du hacker, on trouve un certain Payday, probablement commanditaire de l'attaque qui propose de payer sur le site suivant.

![secured-market](./secured-market.png)

On se rend donc à l'adresse http://secured-market.sh:3000.

Le site semble complétement inactivé mais on peut trouver ce commentaire dans le code source :

![comments](./comments.png)

On peut donc accéder à la page de login sur http://secured-market.sh:3000/login.

Impossible de se connecter mais on nous laisse penser qu'on possède un statut de guest. On regarde donc dans les cookies avant de trouver un token JWT. On le décode simplement.

![jwt](./jwt.png)

Pour continuer dans cette direction, il faut probablement utiliser une des failles de l'algorithme JWT à savoir :
- (CVE-2015-2951) The alg=none signature-bypass vulnerability
- (CVE-2016-10555) The RS/HS256 public key mismatch vulnerability
- (CVE-2018-0114) Key injection vulnerability
- (CVE-2019-20933/CVE-2020-28637) Blank password vulnerability
- (CVE-2020-28042) Null signature vulnerability

## Conclusion
En résumé, voici les informations concrètes retrouvées :
- Au sujet du commanditaire :
    - Son pseudo est "Payday" sur FakeBook
    - Il souhaite utiliser un site de NFT peu sécurisé pour payer le hacker
- Au sujet du hacker :
    - Sa planque se trouvait à l'intérieur de l'ESISAR
    - Il range ses affaires dans une malette
- Au sujet de la méthode d'intrusion
    - L'overlay a été changé depuis le fichier `overlay.txt`
    - Un informateur a donné les accès d'un développeur au hackeur
    - Le hackeur a réaliser une escalade de privilèges via `gdb` 
    - Il est parvenu a sortir du container Docker et se retrouver sur la machine hôte.

*Compte-rendu par DEVILLE Baptiste (BA-Seven) pour la team St-Barth's goin'2 Valence*