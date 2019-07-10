#!/usr/bin/python3
# coding: utf-8

import numpy as np
from PIL import Image, ImageColor
from greyfox import ImageLSB, str_to_bin

"""
    NumPy:
    - optimiser les utilsiations des arrays:
        - Embeded
        - Extract
        - Detect
    - Multi process
    - Vérifier quand il y a qu'une couleur
"""

def m_print(a, absi=None, ordo=None):
    for y in a:
        for x in y:
            print(f"{x}", end=" ")
        print()


# Image.new("RGB", (5, 10), (0, 0, 0)).save("test.png")
# m_img = np.array(Image.open("test.png"))
img = Image.open("avion.png")



# m_img = np.array([
#     [[0, 0], [0, 1], [0, 2], [0,3], [0,4]],
#     [[1, 0], [1, 1], [1, 2], [1,3], [1,4]],
#     [[2, 0], [2, 1], [2, 2], [2,3], [2,4]],
#     [[3, 0], [3, 1], [3, 2], [3,3], [3,4]],
#     [[4, 0], [4, 1], [4, 2], [4,3], [4,4]]
# ])
m_img = np.array([
    [1,2,3,4,5,6,7,8,9,0],
    [1,2,3,4,5,6,7,8,9,0],
    [1,2,3,4,5,6,7,8,9,0],
    [1,2,3,4,5,6,7,8,9,0],
    [1,2,3,4,5,6,7,8,9,0]
])

m_img = m_img.reshape(len(m_img), len(m_img[0]), 1)
img = ImageLSB("hidden_avion.png", "extract")
p = {"data_to_embeded": "coucou"}
img.apply_strategy(params_strategy=p)

# m_img = np.array(Image.open("hidden_test.png"))
# m_print(m_img)
