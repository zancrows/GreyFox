#!/usr/bin/python3
# coding: utf-8

from PIL import Image
from lsb import ImageLSB


"""
    Extraction de données, résultat dans les fichiers binary.bin et binary.txt
"""
img = ImageLSB("tux_hidden.png", "extract")
img.apply_strategy()


"""
    Créé une image test.png, et cache le message 'hello world!'
    dans les premiers pixels.
    Une Extraction montrera le message dans le binary.bin
"""
Image.new("RGB", (50, 50), (0, 0, 0)).save("test.png")
img = ImageLSB("test.png", "embeded")
p = {"data_to_embeded": "hello world!"}
img.apply_strategy(params_strategy=p)


"""
    Lance une detection affiche et enregistre,
    résultat image detect_tux_hidden.png
"""
img = ImageLSB("tux_hidden.png", "detect")
p = {"detect_all_color": True, "save": True}
img.apply_strategy(params_strategy=p)


"""
    Lance une detection affiche et enregistre, avec la détection sur toutes les couleurs
    résultat image detect_tux_hidden2.png
"""
img = ImageLSB("tux_hidden.png", "detect")
p = {"save": True}
img.apply_strategy(params_strategy=p)
