#!/usr/bin/python3
# coding: utf-8

import binascii
import numpy as np
from PIL import Image
from greyfox import ImageLSB

"""
    NumPy:
    - tester pour traiter sur des ranges -> slice
    - applications par couleurs avec mask
    - récupération de données
    - TODO utiliser np.binary_repr
"""

# print(bits)
# img = Image.open("kitty.png")

# Image.new("RGB", (10, 10), (0, 0, 0)).save("test.png")
# img = ImageLSB("test.png", "embeded")
# p = {"data_to_embeded": "b", "verbose": False}
# img.apply_strategy(params_strategy=p)

img = Image.open("test.png")
# himg = Image.open("hidden_test.png")

n = np.array(img)

def myfunc(a, decal):
    if (a << decal) & 128:
        return 255
    return 0

vfunc = np.vectorize(myfunc)

b = np.array([
    [[0,1,2], [3,4,5], [6,7,8]],
    [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
    [[100, 110, 120], [130, 140, 150], [160, 170, 180]],
])

b += 1



#
# bb = np.array([
#     [[0,1,2,9], [3,4,5,9], [6,7,8,9]],
#     [[10, 11, 12, 90], [13, 14, 15, 90], [16, 17, 18, 90]],
#     [[100, 110, 120, 900], [130, 140, 150, 900], [160, 170, 180, 900]],
# ])


# with np.nditer(b[:,:,0]) as it:
#     for i in it:
#         print(i)
#
# for y in b:
#     for x in y:
#         print(x, end=" ")
#     print()

test = ImageLSB("kitty.png", "detect")
p = {"save": True,  "detect_all_color": True}
c= ("RED",)
test.apply_strategy()
