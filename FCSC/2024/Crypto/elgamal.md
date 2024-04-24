# El Gamal Fait

## Partie 1/2
> On m'a dit qu'on pouvait utiliser RSA pour signer des messages au lieu de les chiffrer. J'ai essayé de faire pareil avec ElGamal. Est-ce que vous pouvez vérifier si ce que j'ai fait est sécurisé ?

Après quelques recherches sur le système de signature El Gamal, on se rend compte qu'il existe un moyen très simple de prédire la signature du message si on a le contrôle de celui-ci. En effet grâce à l'attaque [Existential Forgery](https://en.wikipedia.org/wiki/ElGamal_signature_scheme#Security), il est possible de proposer comme signature valide `r = g^e*y mod p` et `s = −r mod (p − 1)` pour tout `e` avec `1 < e < p − 1`.

Implémentation : 
```python
from pwn import *

# Set up the connection
host = 'challenges.france-cybersecurity-challenge.fr'
port = 2151

# Connect to the remote server
conn = remote(host, port)

e = 3

def parse(resp):
    sp = resp.split('\n')
    p = int(sp[1].split('=')[-1].strip())
    g = int(sp[2].split('=')[-1].strip())
    y = int(sp[3].split('=')[-1].strip())
    return p,g,y


while True:
    received_data = conn.recvuntil('>>>')
    if 'p = ' in str(received_data):
        print("[-] Data received")
        conn.recv()
        p,g,y = parse(received_data.decode())
        r = pow(g,e,p) * y % p
        s = -r % (p-1)
        m = e*s % (p-1)
        conn.send((str(m)+'\n').encode())
        print(conn.recvline())
        conn.send((str(r)+'\n').encode())
        print(conn.recvline())
        conn.send((str(s)+'\n').encode())
        print(conn.recvline())
        print(conn.recvline())

# Close the connection
conn.close()
```

## Partie 2/2
> On m'a dit que dans certains cas, mon service de signature qui utilise ElGamal est encore plus facile à attaquer. À vous de me montrer ça !

La deuxième partie est plus complexe car le message à signer est décidé par le programme et ne nous est fourni qu'après la génération de la clé publique. Cependant, la signature est ici restreinte au cas particulier où le générateur `g` (a.k.a le nombre élevé à la puissance) est 2 et le modulo `p` dans lequel on travaille est choisi tel que `p ≡ 1 mod 4`. J'ai personnellement dû faire un certain nombre de recherches avant de finalement tomber sur [un post stackoverflow cryptique](https://stackoverflow.com/questions/4506618/finding-a-generator-for-elgamal) recommandant de lire la note 11.67 du chapitre 11 du livre [The Handbook of Applied Cryptography](https://cacr.uwaterloo.ca/hac/) de  Alfred J. Menezes, Paul C. van Oorschot et Scott A. Vanstone  (oui oui...). On y lit donc :
> 11.67 Note (security based on parameter selection)
>
> (i) (index-calculus attack) The prime p should be sufficiently large to prevent efficient
use of the index-calculus methods (§3.6.5).
>
> (ii) (Pohlig-Hellman attack) p − 1 should be divisible by a prime number q sufficiently
large to prevent a Pohlig-Hellman discrete logarithm attack (§3.6.4).
>
> (iii) (weak generators) Suppose that p ≡ 1 (mod 4) and the generator α satisfies the
following conditions:
>
> (a) α divides (p − 1); and
>
> (b) computing logarithms in the subgroup S of order α in Z∗
p can be efficiently done
(for example, if a Pohlig-Hellman attack (§3.6.4) can be mounted in S).
It is then possible for an adversary to construct signatures (without knowledge of A’s
private key) which will be accepted by the verification algorithm (step 2 of Algo-
rithm 11.64).
> 
> To see this, suppose that p−1 = αq. To sign a message m the adversary
does the following:
> 
> (a) Compute t = (p − 3)/2 and set r = q.
>
> (b) Determine z such that αqz ≡ yq (mod p) where y is A’s public key. (This is
possible since αq and yq are elements of S and αq is a generator of S.)
>
> (c) Compute s = t · {h(m) − qz} mod (p − 1).
>
> (d) (r, s) is a signature on m which will be accepted by step 2 of Algorithm 11.64.
>
> [...]
> 
> Notice in the case where α = 2 is a generator
that the conditions specified in (iii) above are trivially satisfied.

Ici, `α` est en réalité `g` qui vaut bien 2, cela confirme donc *trivialement* que ce cas est vulnérable...
Plus qu'à implémenter le processus décrit : 

```python
from pwn import *

# Set up the connection
host = 'challenges.france-cybersecurity-challenge.fr'
port = 2152

# Connect to the remote server
conn = remote(host, port)

def parse(resp):
    sp = resp.split('\n')
    p = int(sp[1].split('=')[-1].strip())
    g = int(sp[2].split('=')[-1].strip())
    y = int(sp[3].split('=')[-1].strip())
    m = int(sp[4].split('=')[-1].strip())
    return p,g,y,m

def solve(p,g,y,m):
    t = (p-3)//2
    r = (p-1)//2

    j = pow(y,r,p)
    h = pow(2,r,p)

    for i in range(1,p):
        if pow(h,i,p) == j:
            z = i
            print(z)
            break

    s = t*(m - r*z) % (p-1)
    return r,s

while True:
    received_data = conn.recvuntil(b'>>>')
    if 'p = ' in str(received_data):
        print("[-] Data received")
        conn.recv()
        p,g,y,m = parse(received_data.decode())
        r,s = solve(p,g,y,m)
        conn.send((str(r)+'\n').encode())
        print(conn.recvline())
        conn.send((str(s)+'\n').encode())
        print(conn.recvline())
        print(conn.recvline())
    

# Close the connection
conn.close()
```
