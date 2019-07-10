# GreyFox

Outil de stéganographie qui permet de faire du LSB (Less Significant Bit).  
Fonctionne avec python 3.7 et 3.6 (non testé)

dépendances:
* Pillow
* colorama
* NumPy

## Fonctionnement basique  

Il est possible de faire fonctionner le programme en 3 modes différents appelés stratégies ici:  
* Extraction de données  -> ExtractStratgeyLSB
* Incrustation de données  -> EmbededStrategyLSB
* Détection de données  -> DetectStrategyEmbeded

Extraction:  
```python
from greyfox import ImageLSB  

img_lsb = ImageLSB("image.png", "extract")  
img_lsb.apply_strategy()  
```

Incrustation (voir plus bas pour params_strategy):  
```python
from greyfox import ImageLSB  

img_lsb = ImageLSB("image.png", "embeded")  
p = {"data_to_embeded": "des donnees a cacher"}
img_lsb.apply_strategy(params_strategy=p)  
```

Détection:  
```python
from greyfox import ImageLSB  

img_lsb = ImageLSB("image.png", "detect")  
img_lsb.apply_strategy()  
```

## Options  

Au moment d'appliquer la stratégie choisie il est possible de passer certains paramètres pour affiner le comportement de celle-ci.  
Trois paramètres possibles:
* coor -> un dictionnaire pour définir une plage sur lequel la stratégie va être appliquée  
* color_seq -> un tuple pour définir sur quelles couleurs il faut appliquer la stratégie  
* params_strategy -> un dictionnaire qui contient d'autres paramètres spécifiques aux stratégies  

### coor:  
```python
from greyfox import ImageLSB  

img_lsb = ImageLSB("image.png", "detect") 
coor = {"x": (0, 20), "y": (0, 20)}  
img_lsb.apply_strategy(coor=coor)  
```

les tuples vont être changés en ```slice``` donc il est possible de mettre une troisième valeur dedans qui va être le pas comme ceci:  
```python
coor = {"x": (0, 20, 2), "y": (0, 20)}  
```  
par défaut les ranges sont la hauteur et largeur de l'image.  

### color_seq:  
```python
from greyfox import ImageLSB

img_lsb = ImageLSB("image.png", "detect")  
colors = ("RED", "GREEN")
img_lsb.apply_strategy(color_seq=colors)  
```
Ici la détection va se faire que sur les couleurs rouge et verte.
les différentes valeurs possibles sont :
* RED
* GREEN
* BLUE
* ALPHA (quand l'image supporte)  

Par défaut la séquence vaut RED GREEN BLUE et ALPHA quand il y a, ou BLACK quand l'image est noire et blanc.

### params_strategy:  

paramètre commun aux stratégies:  

- verbose: permet d'activer ou non la verbosité. Prend un booléen. Par défaut à True.  
```python
from greyfox import ImageLSB

img_lsb = ImageLSB("image.png", "detect")  
p = {"verbose": False} # ici on désactive la verbosité  
img_lsb.apply_strategy(params_strategy=p)  
```

paramètres de la stratégie ExtractStrategyLSB:

- mask: permet d'appliquer un 'masque' et donner un ordre d'extraction par couleur. Prend un dictionnaire contenant un tuple par             couleur.  
exemple:  
```python
p = {
  "mask": {
     "RED": (0, 2, 3),
     "BLUE" (0, 1, 2)
  }
}
```
Ici on va appliquer un masque sur les couleurs rouges et bleu. Par défaut un masque vaut (0,) pour les trois couleurs.  Explication du fonctionnement du masque:  
Pour un pixel RGB (73, 128, 70) on va prendre le premier, troisième et quatrième bit pour le rouge et le premier, deuxième et troisième pour le bleu, pour le vert il prend le masque par défaut et prend donc que le premier bit.

exemple avec le rouge:
```
73 -> 01001001  
          ^^ ^  
          || |  
          32 0  
```
L'extraction sur le rouge donnera 101.  
L'ordre dans le tuple est important si on met ```"RED": (0, 3, 2)``` l'extraction donnera 110.  

paramètres de stratégie pour EmbededStrategyLSB:  

- data_to_embeded: données à cacher dans l'image, il est obligatoire si il est vide lèvera une exception de type ValueError.  
- file_name: nom d'enregistrement de l'image avec les données cachées, prend un str, par défaut il enregistre sous le nom 'hidden_<nom de de l'image d'origine>.png'. Si le paramètre est spécifié le nom d'enregistrement sera 'hidden_<file_name>.png'. Pas besoin de spécifier l'extension.  

paramètres de stratégie pour DetectStrategyLSB:  

- detect_all_color: permet de faire une detection sur toutes les couleurs en même temps en plus de chaque couleur. Prend un booléen. Par défaut à False.   
- save:  permet de sauvegarder l'image générée pour la détection. Prend un booléen. Par défaut à False.  
- file_name: pareil que pour EmbededStrategyLSB sauf que le prefixe sera 'detect' au lieu de 'hidden', utile pour save.  
- show: permet de définir si on affiche l'image générée par la détection. Prend un booléen. Par défaut à True.  

### stratégie custom:  

Il est possible de développer sa propre stratégie  

```python
from greyfox import ImageLSB, StrategyLSB

class CustomStrategyLSB(StrategyLSB):
    def action(self, absi:range, ordo: range, colors:dict, params_strategy:dict):
        pass

img_lsb = ImageLSB("image.png", CustomStrategyLSB)
img_lsb.apply_strategy()
```
