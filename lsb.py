# coding: utf-8
# python 3.7.1 x86_64

import binascii
from abc import ABCMeta, abstractmethod
from PIL import Image
from itertools import chain, islice, count
from enum import IntEnum

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
    def action(self):
        raise NotImplementedError

class EmbededStrategyLSB(StrategyLSB):

    def action(self) -> None:
        raise NotImplementedError

class ExtractStrategyLSB(StrategyLSB):

    def action(self) -> None:
        raise NotImplementedError

class DetectStrategyLSB(StrategyLSB):

    def action(self) -> None:
        raise NotImplementedError


class ImageLSB():

    def __init__(self, image, strategy_lsb:StrategyLSB=None):
        self.image = image
        self.width, self.height = self.image.size
        self.strategy_lsb = strategy_lsb
        # attention 'filename' indique le chemin  absolu de l'image
        self.file_name = self.image.filename
        self.colors = self.color_sequence

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
        colors = ["RED", "GREEN", "BLUE"]
        if len(self.image.getpixel((0, 0))) > len(colors):
            colors.append("ALPHA")
        return IntEnum("Color", zip(colors, count()))


    def lsb_apply_strategy(self, coor:dict={}, msg:str="", new_name:str="") -> None:
        absi = range(*coor["x"]) if coor.get("x") else range(self.width)
        ordo = range(*coor["y"]) if coor.get("y") else range(self.height)
        self.msg_to_embeded = list(str_to_bin(msg)) if msg else msg
        print("[+] Start ")
        if issubclass(self.strategy_lsb, StrategyLSB):
            self.strategy_lsb.action(self)
        else:
            raise ValueError("self.strategy_lsb is not subclass of StrategyLSB")


if __name__ == "__main__":
    img = ImageLSB("ch9.png")
    print(img.image.mode)
    for i in img.colors:
        print(i)
