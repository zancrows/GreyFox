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
"""

def str_to_bin(string:str) -> str:
    if string:
        bits = bin(int(binascii.hexlify(bytes(string, "utf8")), 16))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))
    return ""

bits = list(str_to_bin("b"))
print(bits)
# img = Image.open("kitty.png")

# Image.new("RGB", (10, 10), (0, 0, 0)).save("test.png")
# img = ImageLSB("test.png", "embeded")
# p = {"data_to_embeded": "b", "verbose": False}
# img.apply_strategy(params_strategy=p)

img = Image.open("test.png")
# himg = Image.open("hidden_test.png")

n = np.array(img)

# Embeded
# choix couleur OK
# mask NOK
for i in np.nditer(n[:, :, 1:], op_flags=["readwrite"]):
    i[...] = ((i >> 1) << 1) | int(bits[0])
    bits.pop(0)
    if not bits:
        break



for y in n:
    for x in y:
        print(x, end=" ")
    print()

# for i in range(4):
#     print(himg.getpixel((i,0)), img.getpixel((i,0)))
