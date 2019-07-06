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

def str_to_bin(string:str) -> str:
    if string:
        return np.binary_repr(int(string.encode("utf8").hex(), 16), width=8)
    return ""

# Image.new("RGB", (10, 10), (0, 0, 0)).save("test.png")
img = Image.open("test.png")
m_img = np.array(img)

def m_print(a):
    for x in a:
        for y in x:
            print(y, end=" ")
        print()

bits = list(str_to_bin("u"))
print(bits)

# m_print(m_img)


b = np.array([
    [[0,1,2], [3,4,5], [6,7,8]],
    [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
    [[100, 110, 120], [130, 140, 150], [160, 170, 180]],
])

# x = np.array([[ 0,  1,  2], [ 3,  4,  5], [ 6,  7,  8], [ 9, 10, 11]])
# print(x[[0,1,2]])

colors = [0,1,2]




m_print(m_img)

# bb = np.array([
#     [[0,1,2,9], [3,4,5,9], [6,7,8,9]],
#     [[10, 11, 12, 90], [13, 14, 15, 90], [16, 17, 18, 90]],
#     [[100, 110, 120, 900], [130, 140, 150, 900], [160, 170, 180, 900]],
# ])


# test = ImageLSB("kitty.png", "detect")
# p = {"show": 1,  "detect_all_color": True, "save": True}
# test.apply_strategy(params_strategy=p)
