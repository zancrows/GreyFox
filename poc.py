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


img = Image.new("RGB", (5, 10), (0, 0, 0)).save("test.png")
# m_img = np.array(Image.open("test.png"))

# m_img = np.array([
#     [[0, 0], [0, 1], [0, 2], [0,3], [0,4]],
#     [[1, 0], [1, 1], [1, 2], [1,3], [1,4]],
#     [[2, 0], [2, 1], [2, 2], [2,3], [2,4]],
#     [[3, 0], [3, 1], [3, 2], [3,3], [3,4]],
#     [[4, 0], [4, 1], [4, 2], [4,3], [4,4]]
# ])

print(str_to_bin("cou"))

img  = ImageLSB("test.png", "embeded")
c = {"x": (0,500), "y": (0,450)}
p = {"data_to_embeded": "couc"}
img.apply_strategy(coor=c, params_strategy=p)

m_img = np.array(Image.open("hidden_test.png"))

img = ImageLSB("kitty.png", "detect")
img.apply_strategy(coor=c)

# print(len(m_img[0:6:2]))

# x = slice(0,1)
# for i in m_img:
#     for j in i[x]:
#         j[...] =1
m_print(m_img[0:9])
