# coding: utf-8
# python 3.7.3 x86_64

import binascii
from PIL import Image
from datetime import datetime
from itertools import chain, islice
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

def extract_bit(byte:int, mask:tuple=(0,)) -> str:
    b = ""
    for i in mask:
        b += str((byte >> i) & 1)
    return b


class StrategyLSB(metaclass=ABCMeta):

    @abstractmethod
    def action(self, absi, ordo, colors):
        raise NotImplementedError()

    @classmethod
    def get_pixel(cls, img, absi:int, ordo:int):
        for y in ordo:
            for x in absi:
                yield img.getpixel((x, y))


class EmbededStrategyLSB(StrategyLSB):

    def action(self, absi:range, ordo:range, colors:dict, params_strategy:dict) -> None:
        raise NotImplementedError()


class ExtractStrategyLSB(StrategyLSB):

    def action(self, absi:range, ordo:range, colors:dict, params_strategy:dict) -> None:
        extract = ""
        repr_colors = " ".join(colors.keys())
        mask = params_strategy.get("bit_mask", {})
        print(f"[+] Start Extract with color sequence -> {repr_colors}")
        for pixel in StrategyLSB.get_pixel(self.image, absi, ordo):
            for k_color, v_color in colors.items():
                extract += extract_bit(pixel[v_color], mask.get(k_color, (0,)))

        print("[+] End Extract")
        with open("binary.txt", mode="w") as fp:
            print("[+] binary.txt write")
            fp.write(extract)
        with open("binary.bin", mode="bw") as fp:
            print("[+] binary.bin write")
            fp.write(bin_to_str(extract))


class DetectStrategyLSB(StrategyLSB):

    def action(self, absi:range, ordo:range, colors:dict, params_strategy:dict) -> None:
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

    def color_sequence(self, custom:tuple=None):
        _colors = {"RED": 0 , "GREEN": 1, "BLUE": 2}
        if len(self.image.getpixel((0,0))) == 4:
            _colors["ALPHA"] = 3
        if custom:
            _colors = {c: _colors[c] for c in custom}
        return  _colors

    def apply_strategy(self, coor:dict={}, color_seq:tuple=None, params_strategy:dict={}) -> None:
        absi = range(*coor["x"]) if coor.get("x") else range(self.width)
        ordo = range(*coor["y"]) if coor.get("y") else range(self.height)
        colors = self.color_sequence(color_seq)

        if issubclass(self.strategy_lsb, StrategyLSB):
            print(f"[+] Start apply strategy with {self.strategy_lsb.__name__}")
            start = datetime.now()
            self.strategy_lsb.action(self, absi, ordo, colors, params_strategy)
            end = datetime.now()
            print(f"[+] time -> {end - start}")
            print(f"[+] End apply strategy with {self.strategy_lsb.__name__}")
        else:
            raise TypeError("[!] self.strategy_lsb is not subclass of StrategyLSB")

if __name__ == "__main__":
    img = ImageLSB("test.png", ExtractStrategyLSB)
    # c = ("GREEN", "RED")
    # p = {"bit_mask": {
    #     "RED": (7,6),
    #     "GREEN":(5,4),
    #     "BLUE": (4,)
    # }}
    # img.apply_strategy(color_seq=c, params_strategy=p)
    # img.apply_strategy(params_strategy=p)
    img.apply_strategy()
