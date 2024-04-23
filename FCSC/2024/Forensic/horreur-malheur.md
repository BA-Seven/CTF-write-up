# Horreur, malheur

## Enoncé 
Vous venez d'être embauché en tant que Responsable de la Sécurité des Systèmes d'Information (RSSI) d'une entreprise stratégique.

En arrivant à votre bureau le premier jour, vous vous rendez compte que votre prédécesseur vous a laissé une clé USB avec une note dessus : VPN compromis (intégrité). Version 22.3R1 b1647.

Note : La première partie (Archive chiffrée) débloque les autres parties, à l'exception de la seconde partie (Accès initial) qui peut être traitée indépendamment. Nous vous recommandons de traiter les parties dans l'ordre.

## Partie 1/5
> Sur la clé USB, vous trouvez deux fichiers : une archive chiffrée et les journaux de l'équipement. Vous commencez par lister le contenu de l'archive, dont vous ne connaissez pas le mot de passe. Vous gardez en tête un article que vous avez lu : il paraît que les paquets installés sur l'équipement ne sont pas à jour...

> Le flag est le mot de passe de l'archive.
## Partie 2/5
> Sur la clé USB, vous trouvez deux fichiers : une archive chiffrée et les journaux de l'équipement. Vous focalisez maintenant votre attention sur les journaux. L'équipement étant compromis, vous devez retrouver la vulnérabilité utilisée par l'attaquant ainsi que l'adresse IP de ce dernier.

> Le flag est au format : FCSC{CVE-XXXX-XXXXX:<adresse_IP>}.
## Partie 3/5
> Vous avez réussi à déchiffrer l'archive. Il semblerait qu'il y ait dans cette archive une autre archive, qui contient le résultat du script de vérification d'intégrité de l'équipement.

> À l'aide de cette dernière archive et des journaux, vous cherchez maintenant les traces d'une persistance déposée et utilisée par l'attaquant.
## Partie 4/5
> Vous remarquez qu'une fonctionnalité built-in de votre équipement ne fonctionne plus et vous vous demandez si l'attaquant n'a pas utilisé la première persistance pour en installer une seconde, moins "visible"...

> Vous cherchez les caractéristiques de cette seconde persistance : protocole utilisé, port utilisé, chemin vers le fichier de configuration qui a été modifié, chemin vers le fichier qui a été modifié afin d'établir la persistance.

> Le flag est au format : FCSC{<protocole>:<port>:<chemin_absolu>:<chemin_absolu>}.
## Partie 5/5
> Vous avez presque fini votre analyse ! Il ne vous reste plus qu'à qualifier l'adresse IP présente dans la dernière commande utilisée par l'attaquant.

> Vous devez déterminer à quel groupe d'attaquant appartient cette adresse IP ainsi que l'interface de gestion légitime qui était exposée sur cette adresse IP au moment de l'attaque.

> Le flag est au format : FCSC{<UNCXXXX>:<nom du service>}.

> Remarque : Il s'agit d'une véritable adresse IP malveillante, n’interagissez pas directement avec cette adresse IP.
