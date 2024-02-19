---
title: "Terminale NSI - Labyrinthes"
subtitle: "Génération de Labyrinthes aléatoires, résolution automatique"
author: "qkzk"
date: "2021/05/16"
theme: "metropolis"
geometry: "margin=1.5cm"
header-includes: |
    \usepackage{tcolorbox}
    \newtcolorbox{myquote}{colback=teal!10!white, colframe=teal!55!black}
    \renewenvironment{Shaded}{\begin{myquote}}{\end{myquote}}

---

# Labyrinthes

L'objectif de ce projet est :

* de générer aléatoirement des labyrinthes _parfaits_,
* de les afficher dans la console,
* de les résoudre automatiquement.

On pourra envisager d'en faire un jeu, mais cela demanderait de dessiner
les labyrinthes dans Pygame ou une autre interface et ce n'est pas un objectif.

Un labyrinthe est _parfait_ si toutes les cases sont joignables.

## Génération automatique de labyrinthes

Nous allons utiliser cet algorithme :

![kruksal](https://upload.wikimedia.org/wikipedia/commons/6/69/Yl_maze_ani_algo1.gif)

Il est dû à Joseph Kruskal en 1956.

On débute avec une grille rectangulaire où toutes les cases ont un numéro différent.

Chaque trait dans la grille désigne un mur plein.

Tant qu'il reste plus d'un numéro dans la grille :

* on choisit aléatoirement un mur. Il sépare deux parties ayant des numéros différents,
* on enlève ce mur,
* on donne aux deux parties séparées par le mur le numéro le plus petit des deux.

Il est possible de démontrer qu'on obtient alors un labyrinthe parfait.


Remarquons qu'il est nécessaire d'envisager une structure permettant trois opérations :

* **find** : trouver l'ensemble des éléments qui ont le même numéro.
* **union** : unir deux parties ayant des numéros différents,
* **count** : compter le nombre de parties différentes.

On appelle une telle structure `Union-Find`.

Vous trouverez dans le TP un module [union find](./union_find_forest.py) qui implémente
cette structure. Vous devez juste apprendre à vous en servir.

## Qu'allons nous faire ?

ça :

```
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
│█ █│         │     │ │         │       │ │    █ █│█ █ █│   │     │ │ │ │ │     |
+ + + +-+-+-+ +-+ +-+ + + + +-+-+ + +-+ + +-+-+ + + +-+ + +-+-+ + + + + + +-+ +-+
│ │█ █  │ │   │   │     │ │     │ │   │█ █ █│  █│█ █  │█ █│ │   │     │         |
+-+-+ +-+ +-+ + +-+ +-+-+-+-+-+-+-+-+ + + + + + +-+ + + + + + +-+-+ +-+ +-+-+-+-+
│   │█│     │   │ │ │     │   │ │   │ │█│ │█│ │█│   │ │ │█│ │█ █│         │     |
+ + + + +-+-+ +-+ + + +-+ + + + +-+ +-+ +-+ +-+ +-+ +-+ + + + + +-+-+-+-+-+-+ +-+
│ │  █ █ █  │   │       │ │ │   │ │█ █ █  │█ █ █│     │ │█ █ █│█  │   │ │       |
+ +-+-+-+ + + +-+ +-+ + +-+ +-+-+ + +-+-+ + + + + +-+-+-+ +-+-+ +-+ +-+ +-+ + +-+
│ │    █ █│ │ │     │ │     │   │  █ █│   │ │ │ │ │ │   │ │ │█ █            │ │ |
+ +-+ + +-+ +-+-+ +-+ + +-+-+-+ +-+-+ +-+-+-+-+ + + + +-+-+ + +-+-+-+ +-+-+-+-+ +
│ │   │█│ │   │ │ │   │      █ █ █ █ █│   │     │ │   │ │  █ █│   │ │ │   │     |
+-+-+-+ + + +-+ +-+-+-+ +-+ + +-+-+ +-+ +-+-+-+-+-+ +-+ + + + + + + + + + + +-+-+
│  █ █ █│   │       │   │   │█    │         │ │       │   │█│   │ │   │ │ │     |
+-+ +-+-+-+ +-+ +-+-+ +-+-+-+ + +-+ + + +-+-+ +-+ +-+-+-+-+ +-+-+-+-+ +-+ + +-+ +
│  █  │   │ │   │ │ │   │█ █ █│ │   │ │ │ │   │ │         │█ █ █  │   │ │   │   |
+-+ +-+-+ +-+-+ + + +-+ + +-+ +-+ +-+-+-+ +-+ + +-+-+-+ +-+ +-+ + +-+ + + +-+-+-+
│  █ █ █ █    │     │ │ │█│ │   │ │               │   │     │█ █│   │ │   │     |
+ +-+-+-+ + +-+ +-+ + +-+ + +-+-+-+ + + +-+ + +-+ + +-+-+-+ + + +-+-+-+ +-+-+ +-+
│   │ │  █│   │ │  █ █│  █ █│   │   │ │ │ │ │ │ │ │     │   │█│   │     │   │   |
+-+-+ +-+ +-+-+ + + + +-+-+ +-+ +-+-+-+ + + + + +-+ + + + + + +-+ + +-+-+ +-+-+ +
│        █ █│ │ │ │█│█│ │ │█│   │         │ │   │ │ │ │ │ │ │█│ │ │█ █ █│  █ █│ |
+-+-+-+ +-+ + +-+-+ + + + + + + +-+-+ +-+ + + +-+ + +-+-+ +-+ + +-+ +-+ +-+ + + +
│   │     │█ █ █ █ █│█ █ █│█  │   │ │   │ │ │ │           │ │█│   │█ █│█ █│█│█ █|
+ + +-+-+ +-+-+-+-+ +-+-+ + + +-+ + +-+ +-+ +-+ +-+ + +-+-+ + + +-+-+ + + + +-+ +
│ │               │ │  █ █│█│ │       │ │     │ │   │     │ │█      │█│ │█ █│█ █|
+-+-+-+-+ +-+-+-+-+ +-+ +-+ +-+-+ +-+ +-+ + + +-+ +-+ +-+ + + +-+-+ + + + +-+ +-+
│     │   │     │ │ │  █ █ █    │   │   │ │ │ │ │ │   │   │  █ █ █│ │█│ │ │  █│ |
+ + +-+ +-+ +-+ + +-+-+-+-+ + + + +-+-+ + +-+ + + +-+-+-+ +-+-+ + + + +-+-+ + + +
│ │           │ │ │ │   │   │ │ │ │   │ │ │             │   │   │█│ │█│     │█│ |
+-+-+-+ +-+-+-+-+ + +-+ +-+-+ +-+ +-+ + +-+-+-+ + +-+-+ +-+ + +-+ + + + +-+-+ + +
│ │       │   │     │       │   │   │     │   │ │ │     │   │ │  █│ │█│ │   │█  |
+ + +-+-+ + +-+ +-+-+-+ +-+ +-+ + +-+-+-+ + +-+ +-+-+-+ + +-+-+-+ +-+ +-+-+ + +-+
│     │         │     │ │   │   │     │   │         │ │ │ │ │█ █ █│  █│ │    █ █|
+ +-+ + +-+-+ +-+ + + + +-+ +-+ +-+-+-+-+-+ + +-+ +-+ +-+-+ + +-+-+-+ + + +-+-+ +
│ │   │   │ │     │ │ │ │         │       │ │ │   │ │   │ │  █  │█ █ █│ │   │█ █|
+-+ + +-+ + + + +-+ +-+-+ +-+ + + + +-+-+ +-+ +-+ + + +-+ +-+ +-+ + +-+ + +-+ +-+
│   │   │   │ │ │ │     │   │ │ │   │   │ │   │           │  █│█ █│   │ │ │ │█ █|
+ +-+-+ +-+ + +-+ +-+ +-+-+-+ +-+-+ + + +-+-+-+ + +-+-+ + + + + +-+ + + + + +-+ +
│     │ │   │ │           │     │   │ │         │   │   │ │ │█ █│   │ │     │  █|
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

## Modéliser un labyrinthe.

De nombreuses approches sont possibles. Nous allons choisir :

* La grille est un ensemble de cellules.
* Chaque cellule a 4 murs autour d'elle. (`N, S, E, W`). Ils peuvent être
  vides ou pleins.

On aura donc besoin de différentes classes :

* `Cell` représente une case du labyrinthe.
* `Maze` représente le labyrinthe.

### Méthodes de la classe `Cell`

* constructeur avec pour paramètres `i, j, width, height`. Respectivement, l'absisse,
  l'ordonnée, la largeur et la hauteur du labyrinthe.
* `neighbors` : renvoie la liste des voisins de la cellule (les cellules du bord en ont moins de quatre).
* `is_neighbor` : prend en paramètre une autre cellule et renvoie vraie ssi les cellules sont voisines.
* Quelques méthodes magiques pour comparer et représenter :

  * `__repr__` : afficher dans la console,
  * `__eq__` : vrai si les deux cellules sont égales `cell_a == cell_b`,
  * `__lt__` : vrai si la cellule a est à gauche ou plus haute que la cellule b : `cell_a < cell_b`
  * `__hash__` : renvoie un identifiant unique pour les cellules. C'est nécessaire pour `union_find_forest`.

### Méthodes du labyrinthe `Maze` :

* constructeur avec pour paramètres `width` et `height`,
* `generate` va convertir un labyrinthe plein en un labyrinthe parfait avec l'algorithme de Kruksal.
* `solve` renvoie une solution du labyrinthe parfait. C'est à dire une liste des cases accessibles
  de l'une à l'autre en partant d'en haut à gauche vers en bas à droite.
* `__repr__` : affiche le labyrinthe dans la console.

## Résolution du labyrinthe

Étant donné qu'on dispose de tous les éléments, on peut voir le labyrinthe comme un graphe.

* Les cellules sont les cases,
* les murs _vides_ sont les arêtes.

Résoudre le labyrinthe revient à trouver un chemin reliant la cases initiale (haut gauche)
à la case finale (bas droite).

Nous avons étudié et programmé un tel algorithme qui repose sur une exploration du graphe.
On choisira une exploration en profondeur, conduisant généralement à des solutions
plus lisibles.

D'autres approches, plus efficaces, sont possibles.

## Point de départ

Le projet n'est pas évident et contient des aspects techniques pénibles, vous
débutez avec quelques éléments :

Vous avez tout ce qu'il faut pour afficher un labyrinthe "plein", où toutes les cellules
sont reliées :

```
+-+-+-+-+-+-+-+-+-+-+
│ │ │ │ │ │ │ │ │ │ |
+-+-+-+-+-+-+-+-+-+-+
│ │ │ │ │ │ │ │ │ │ |
+-+-+-+-+-+-+-+-+-+-+
│ │ │ │ │ │ │ │ │ │ |
+-+-+-+-+-+-+-+-+-+-+
│ │ │ │ │ │ │ │ │ │ |
+-+-+-+-+-+-+-+-+-+-+
│ │ │ │ │ │ │ │ │ │ |
+-+-+-+-+-+-+-+-+-+-+
│ │ │ │ │ │ │ │ │ │ |
+-+-+-+-+-+-+-+-+-+-+
│ │ │ │ │ │ │ │ │ │ |
+-+-+-+-+-+-+-+-+-+-+
│ │ │ │ │ │ │ │ │ │ |
+-+-+-+-+-+-+-+-+-+-+
│ │ │ │ │ │ │ │ │ │ |
+-+-+-+-+-+-+-+-+-+-+
│ │ │ │ │ │ │ │ │ │ |
+-+-+-+-+-+-+-+-+-+-+
```

* La classe `Cell` est complète.
* La classe `Maze` est incomplète. Il manque de quoi générer le labyrinthe parfait,
  de quoi l'explorer et construire le chemin.
* De quoi représenter ce chemin.

En exécutant `python eleve.py` vous devriez voir le labyrinthe plein apparaître.

Rien ne vous empêche de les réécrire à votre sauce ou d'adapter le projet final
à une version web / pygame / tkinter etc. et le rendre jouable.

## Étape 1

Générer le labyrinthe. Bizarrement, c'est la plus facile.
En effet, tout le travail est déjà réalisé dans le module [union_find_forest.py](./union_find_forest.py)

Il ne reste qu'à écrire les méthodes de la classe `Maze` permettant de le mettre en oeuvre
et à écrire l'algorithme décrit plus haut.

 ```
+-+-+-+-+-+-+-+-+-+-+
│       │         │ |
+-+-+-+ + + + +-+-+ +
│         │ │ │ │   |
+-+ +-+ +-+ +-+ + +-+
│   │ │ │           |
+-+-+ +-+ +-+ +-+-+ +
│       │   │   │ │ |
+ + + +-+-+-+ +-+ + +
│ │ │   │   │     │ |
+ + + +-+ +-+ + +-+ +
│ │ │         │   │ |
+-+ +-+-+-+-+-+ + +-+
│ │ │     │     │   |
+ +-+-+ +-+ +-+ + + +
│ │     │ │   │ │ │ |
+ +-+ + + +-+-+-+ + +
│ │   │           │ |
+ + +-+-+-+-+ +-+-+ +
│     │       │     |
+-+-+-+-+-+-+-+-+-+-+
```

Vérifiez que la labyrinthe précédent est parfait. Choisissez deux cases, (pas celle
de l'exemple ci-dessous...) et trouvez un chemin qui les relie.

## Étape 2

Résoudre le labyrinthe. 

Cela revient à transcrire l'algorithme de recherche de chemin pour nos classes.
Ce n'est pas _très_ difficile mais nettement plus que l'étape précédente.

```
+-+-+-+-+-+-+-+-+-+-+
│█ █ █ █│█ █      │ |
+-+-+-+ + + + +-+-+ +
│      █ █│█│ │ │   |
+-+ +-+ +-+ +-+ + +-+
│   │ │ │  █ █      |
+-+-+ +-+ +-+ +-+-+ +
│       │   │█  │ │ |
+ + + +-+-+-+ +-+ + +
│ │ │   │   │█ █  │ |
+ + + +-+ +-+ + +-+ +
│ │ │         │█ █│ |
+-+ +-+-+-+-+-+ + +-+
│ │ │     │     │█ █|
+ +-+-+ +-+ +-+ + + +
│ │     │ │   │ │ │█|
+ +-+ + + +-+-+-+ + +
│ │   │           │█|
+ + +-+-+-+-+ +-+-+ +
│     │       │    █|
+-+-+-+-+-+-+-+-+-+-+
```

On reprendra la modélisation par un graphe présenté plus haut :

* Les cellules sont les sommets du graphe,
* deux cellules sont reliées par une arête s'il existe un mur _vide_ entre elles.
  Autrement dit, si elles sont voisines et que le mur les séparant est vide.

_Une chose importante à considérer : trouver la sortie du labyrinthe peut se faire sans
la connaissance complète de celui-ci. Tout ce dont on a besoin, c'est d'accéder aux voisins
d'une cellule, de reconnaître une cellule (afin de savoir si on l'a déjà visité) et
de reconnaître la sortie._

# Compléments

1. Présenter le labyrinthe dans une interface graphique.

    * bien qu'il soit parfaitement possible de le faire dans une page web,
        cela demande d'utiliser d'autres technologies (javascript + éventuellement webassambly)
        et cela dépasse le cadre du programme.

    * Pygame et Pygame zero proposeny tout ce qu'il faut pour représenter le labyrinthe.

2. En faire un jeu. Pour cela il faut déplacer le joueur dans le labyrinthe.
  
    Rien de bien difficile là dedans.

    Créer un objet joueur, lui attribuer une position de départ, l'autoriser à se
    déplacer d'une case à l'autre, vérifier s'il existe une jonction entre les cellules.
    Enfin, tester la victoire après chaque tour.

3. Rendre le jeu multijoueur. Un serveur (web mais pas forécement) muni d'une API
  sera nécessaire. On peut envisage d'utiliser les points d'accès suivants :

    * `[POST] /login` avec un symbole utilisé pour représenter le joueur (un emoji !)
    * `[GET] /game` permet de récupérer le labyrinthe. Est appelé automatiquement après une connexion.
    * `[POST] /move/<Direction>` vérifie que le déplacement est légal et déplace le joueur.
    * `[GET] /players` permet de récupérer la liste des joueurs et leurs positions.

    Cette étape est nettement plus difficile et va nécessiter beaucoup de changements
    dans votre projet. Elle n'est à envisager que si vous êtes parvenu à en faire
    un projet solide !

4. La vrai extension, selon moi, est de réécrire union-find à votre sauce. 
    Cette structure de donnée, décrite plus haut, n'est pas difficile à comprendre.

    On peut la représenter simplement par un `set` python. Cela évite facilement les doublons ! Problème, il n'existe pas d'ordre dans un `set`.
    Ceci se résout sauvagement en en faisant une `list` qu'on trie.

    On y met ce qu'on veut à deux conditions :

    * les éléments doivent être `hashables`, c'est-à-dire qu'ils doivent disposer d'une méthode `__hash__`. C'est le cas de nos `Cell` donc on pourra utiliser
        cette implantation.
    * les éléments doivent être comparables entre eux, c'est aussi le cas de nos `Cell`.

    Donc `UnionFind` :

    * une classe, instanciée avec une collection d'objets `uf = UnionFind([1, 2, 3])`, par exemple
    
    qui dispose des méthodes :

    * `find` renvoyant un élément : `uf.find(1)` renvoie 1... par exemple.
    * `union` qui unit plusieurs éléments : `uf.union(1, 2)` et ensuite `uf.find(2)` renvoie 1.
    * `count` qui compte le nombre de composantes. Dans l'exemple précédent `uf.count()` renvoie 2.

    Exemple complet :

    ```python
    uf = UnionFind([1, 2, 3])
    assert uf.count() == 3
    assert uf.find(1) == 1
    assert uf.find(2) == 2 
    assert uf.find(3) == 3 
    uf.union(1, 2)
    assert uf.count() == 2 
    assert uf.find(2) == 1
    assert uf.find(1) == 1
    assert uf.find(3) == 3
    ```
