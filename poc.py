#!/usr/bin/python3
# coding: utf-8

import numpy as np
from PIL import Image

img = Image.open("kitty.png")

a = [
    [(0,0,0), (0,0,0), (0,0,0)],
    [(0,0,0), (0,0,0), (0,0,0)],
    [(0,0,0), (0,0,0), (0,0,0)]
]
n = np.array(a, dtype=np.uint8)

a = n[:,:,0:2] + 1

print(n)
print(a)
