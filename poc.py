#!/usr/bin/python3
# coding: utf-8

import binascii
import numpy as np
from PIL import Image, ImageColor
from greyfox import ImageLSB
from itertools import chain, islice

"""
    NumPy:
    - tester pour traiter sur des ranges -> slice
    - applications par couleurs avec mask
    - récupération de données
"""

def str_to_bin(string:str) -> str:
    if string:
        bits = np.binary_repr(int(string.encode("utf8").hex(), 16))
        return bits.zfill(8 * ((len(bits) + 7) // 8))
    return ""

img = Image.new("RGB", (100, 100), (0, 0, 0)).save("test.png")
img = Image.open("test.png")
m_img = np.array(img)


def m_print(a):
    for y in a:
        for x in y:
            print(f"{x}", end=" ")
        print()

# m_img = np.array([
#     [[1, 11, 111], [2, 22, 222], [3, 33, 333]],
#     [[4, 44, 444], [5, 55, 555], [6, 66, 666]],
#     [[7, 77, 777], [8, 88, 888], [9, 99, 999]]
# ])






img  = ImageLSB("test.png", "embeded")
p = {"data_to_embeded": "aurevoir"}
c = ("RED",)
img.apply_strategy(color_seq=c ,params_strategy=p)
# p = {"detect_all_color": True, "save": True}
# color = ("RED","BLUE")
# img.apply_strategy(color_seq=color)
# coor
img  = ImageLSB("hidden_test.png", "extract")
img.apply_strategy(color_seq=c)
