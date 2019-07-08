#!/usr/bin/python3
# coding: utf-8

import binascii
import numpy as np
from PIL import Image
from greyfox import ImageLSB
from itertools import chain, islice

"""
    NumPy:
    - tester pour traiter sur des ranges -> slice
    - applications par couleurs avec mask
    - récupération de données
"""
def iter_by_blockN(iterable, len_bloc=8, format_=tuple):
    it = iter(iterable)
    for i in it:
        yield format_(chain(i, islice(it, len_bloc-1)))


def str_to_bin(string:str) -> str:
    if string:
        bits = np.binary_repr(int(string.encode("utf8").hex(), 16))
        return bits.zfill(8 * ((len(bits) + 7) // 8))
    return ""

# def bin_to_str(sbin:str) -> bytes:
#     hexa = np.base_repr(int(sbin, 2), base=16)
#     return binascii.unhexlify(hexa)



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

# Embeded OK
bits = list(str_to_bin("coucou ça va ç?"))

# def bit_editor(ibyte:int, bit:int, mask:int) -> int:
#         return (((ibyte >> (mask+1) << 1) | bit) << mask) | (ibyte & ((1 << mask) - 1))

def bit_editor(ibyte:int, bit:int, mask:int) -> int:
        return (((ibyte >> (mask+1) << 1) | bit) << mask) | (ibyte & ((1 << mask) - 1))

n = 73
bits = [1,0,1]
mask = (0,4,5)


for i, m in zip(bits, mask):
    print(n)
    n = bit_editor(n ,i, m)
    print(n)


# print(bit_editor(72, 0, mask=(3,)))

colors = [0, 1, 2]
# m_img.shape = (1, -1, 3)
# for y in m_img[:]:
#     for x in y[:]:
#         for c in colors:
#             if bits:
#                 x[c] = bit_editor(x[c], int(bits[0]), (0,))
#                 bits.pop(0)

img = Image.fromarray(m_img)
img.save("test.png")
# m_img.shape = (10, 10, 3)

# m_print(m_img)




# img  = ImageLSB("test.png", "extract")
# p = {"detect_all_color": True, "save": True}
# color = ("RED","BLUE")
# img.apply_strategy(color_seq=color)
# coor
# img.apply_strategy()

# img.apply_strategy(params_strategy=p)
