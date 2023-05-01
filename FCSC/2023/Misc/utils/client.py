#!/usr/bin/env python3

# python3 -m pip install pwntools
from pwn import *

# Paramètres de connexion
HOST, PORT = "challenges.france-cybersecurity-challenge.fr", 2052

def comparer(x, y):
	io.sendlineafter(b">>> ", f"comparer {x} {y}".encode())
	return int(io.recvline().strip().decode())

def echanger(x, y):
	io.sendlineafter(b">>> ", f"echanger {x} {y}".encode())

def longueur():
	io.sendlineafter(b">>> ", b"longueur")
	return int(io.recvline().strip().decode())

def verifier():
	io.sendlineafter(b">>> ", b"verifier")
	r = io.recvline().strip().decode()
	if "flag" in r:
		print(r)
	else:
		print(io.recvline().strip().decode())
		print(io.recvline().strip().decode())

def trier(N):
	quicksort()
	pass

def quicksort(lo=0, hi=None):

    if hi is None:
        hi = longueur()-1

    # Il nous faut au moins 2 éléments.
    if lo < hi:

        # `p` est la position du pivot dans le tableau après partition.
        p = partition(lo, hi)

        # Tri récursif des 2 parties obtenues.
        quicksort(lo, p - 1)
        quicksort(p + 1, hi)

def partition(lo, hi):

    # Choisir le dernier élément en tant que pivot.
    pivot_index = hi

    # `l` (comme less) sert à trouver la place du pivot dans le tableau.
    l = lo

    # Bien exclure `hi` lors de l'itération car c'est le pivot.
    for i in range(lo, hi):
        if comparer(i, pivot_index):
            # Les éléments plus petit que le pivot passent à gauche.
            echanger(i, l)
            l = l + 1

    # Déplacer le pivot à sa bonne position.
    echanger(l, pivot_index)

    return l

# Ouvre la connexion au serveur
io = remote(HOST, PORT)

# Récupère la longueur du tableau
N = longueur()

# Appel de la fonction de tri que vous devez écrire
trier(N)

# Verification
verifier()

# Fermeture de la connexion
io.close()
