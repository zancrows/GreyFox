# stegano_tool

Outil de stéganographie qui permet de faire du LSB (Less Significant Bit).  

## Fonctionnement basique  

Il est possible de faire fonctionner le programme en 3 modes différents appelés stratégies ici:  
* Extraction de données  -> ExtractStratgeyLSB
* Incrustation de données  -> EmbededStrategyLSB
* Détection de données  -> DetectStrategyEmbeded

Extraction:  
```python
from lsb import ImageLSB  

img_lsb = ImageLSB("image.png", "extract")  
img_lsb.apply_strategy()  
```

Incrustation (voir plus bas pour params_strategy):  
```python
from lsb import ImageLSB  

img_lsb = ImageLSB("image.png", "embeded")  
p = {"data_to_embeded": "des donnees a cacher"}
img_lsb.apply_strategy(params_strategy=p)  
```

Détection:  
```python
from lsb import ImageLSB  

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
from lsb import ImageLSB  

img_lsb = ImageLSB("image.png", "detect") 
coor = {"x": (0, 20), "y": (0, 20)}  
img_lsb.apply_strategy()  
```

les tuples vont être changés en ```range``` donc il est possible de mettre une troisième valeur dedans qui va être le pas comme ceci:  
```python
coor = {"x": (0, 20, 2), "y": (0, 20)}  
```  
par défaut les ranges sont la hauteur et largeur de l'image.  

### color_seq:  
```
from lsb import ImageLSB

img_lsb = ImageLSB("image.png", "detect")  
colors = ("RED", "GREEN")
img_lsb.apply_strategy(color_seq=colors)  
```
Ici la détection va se faire que sur les couleurs rouge et verte.
les différentes valeurs possibles sont :
* RED
* GREEN
* BLUE
* META (quand l'image supporte)

### params_strategy:  

### strategie custom:  
