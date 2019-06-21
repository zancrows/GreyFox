# coding: utf-8
# python 3.7.3 x86_64

import binascii
from PIL import Image
from enum import IntEnum
from datetime import datetime
from itertools import chain, islice, count
from abc import ABCMeta, abstractmethod


def iter_by_blockN(iterable, len_bloc=8, format=tuple):
    it = iter(iterable)
    for i in it:
        yield format(chain(i, islice(it, len_bloc-1)))

def str_to_bin(string:str) -> str:
    if string:
        bits = bin(int(binascii.hexlify(bytes(string, "utf8")), 16))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))
    return ""

def bin_to_str(sbin:str) -> bytes:
    b_str = b""
    for i in iter_by_blockN(sbin):
        binary = "".join(i)
        integer = int(binary, 2)
        hexa = f"{integer:02x}"
        b_str += binascii.unhexlify(hexa)
    return b_str


class StrategyLSB(metaclass=ABCMeta):

    @abstractmethod
    def action(self, absi, ordo):
        raise NotImplementedError()

    @classmethod
    def get_pixel(cls, img, absi, ordo):
        for y in ordo:
            for x in absi:
                yield img.getpixel((x, y))


class EmbededStrategyLSB(StrategyLSB):

    def action(self, absi, ordo) -> None:
        raise NotImplementedError()


class ExtractStrategyLSB(StrategyLSB):

    def action(self, absi, ordo, colors) -> None:
        # TODO être capable de donner une sequence des bit qu'on veut extraire
        _extract = ""
        print("[+] Start Extract with color sequence ...")
        for pixel in StrategyLSB.get_pixel(self.image, absi, ordo):
            for color in colors.values():
                _extract += str(pixel[color] & 1)

        print("[+] End Extract")
        with open("binary.txt", mode="w") as fp:
            print("[+] binary.txt write")
            fp.write(_extract)
        with open("binary.bin", mode="bw") as fp:
            print("[+] binary.bin write")
            fp.write(bin_to_str(_extract))


class DetectStrategyLSB(StrategyLSB):

    def action(self, absi, ordo) -> None:
        raise NotImplementedError()


class ImageLSB():

    def __init__(self, image, strategy_lsb:StrategyLSB=None):
        self.image = image
        self.width, self.height = self.image.size
        self.strategy_lsb = strategy_lsb
        # attention 'filename' indique le chemin  absolu de l'image
        self.file_name = self.image.filename

    @property
    def image(self) -> Image.Image:
        return self._image

    @image.setter
    def image(self, image) -> None:
        if isinstance(image, str):
            self._image = Image.open(image)
        elif isinstance(image, Image.Image):
            self._image = image

    @property
    def color_sequence(self):
        colors = {"RED": 0 , "GREEN": 1, "BLUE": 2}
        if len(self.image.getpixel((0,0))) == 4:
            colors["ALPHA"] = 3
        return  colors

    def apply_strategy(self, coor:dict={}, params_strategy:dict={}) -> None:
        # TODO add params_strategy -> dict() pour configurer les strategies
        absi = range(*coor["x"]) if coor.get("x") else range(self.width)
        ordo = range(*coor["y"]) if coor.get("y") else range(self.height)
        # TODO ajout de modification de sequence, voir modification de l'initialisation de color_sequence
        colors = self.color_sequence

        if issubclass(self.strategy_lsb, StrategyLSB):
            print(f"[+] Start apply strategy with {self.strategy_lsb.__name__}")
            start = datetime.now()
            self.strategy_lsb.action(self, absi, ordo, colors)
            end = datetime.now()
            print(f"[+] time -> {end - start}")
            print(f"[+] End apply strategy with {self.strategy_lsb.__name__}")
        else:
            raise TypeError("[!] self.strategy_lsb is not subclass of StrategyLSB")

if __name__ == "__main__":
    img = ImageLSB("test.png", ExtractStrategyLSB)
    img.apply_strategy()
