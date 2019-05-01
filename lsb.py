# coding: utf-8
# python 3.7.1 x86_64

import binascii
from abc import ABCMeta, abstractmethod
from PIL import Image
from itertools import chain, islice

__version__ = 1.0

"""
TODO:
- Implementation de DetectStrategyLSB
"""

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
    def lsb_red(self, coor:tuple, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def lsb_green(self, coor:tuple, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def lsb_blue(self, coor:tuple, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def action(self):
        raise NotImplemented


class EmbededStrategyLSB(StrategyLSB):

    @staticmethod
    def _edit_pixel(image:Image, coor:tuple, bit:str, color:int) -> None:
        pixel_to_edit = list(image.getpixel(coor))
        color_to_edit = pixel_to_edit[color]
        pixel_to_edit[color] = ((color_to_edit >> 1) << 1) | int(bit)
        image.putpixel(coor, tuple(pixel_to_edit))

    def lsb_red(self, coor:tuple, *args, **kwargs) -> None:
        if not self.msg_to_embeded:
            raise StopIteration
        EmbededStrategyLSB._edit_pixel(self.image, coor, self.msg_to_embeded[0], 0)
        self.msg_to_embeded.pop(0)

    def lsb_green(self, coor:tuple, *args, **kwargs) -> None:
        if not self.msg_to_embeded:
            raise StopIteration
        EmbededStrategyLSB._edit_pixel(self.image, coor, self.msg_to_embeded[0], 1)
        self.msg_to_embeded.pop(0)

    def lsb_blue(self, coor:tuple, *args, **kwargs) -> None:
        if not self.msg_to_embeded:
            raise StopIteration
        EmbededStrategyLSB._edit_pixel(self.image, coor, self.msg_to_embeded[0], 2)
        self.msg_to_embeded.pop(0)

    def action(self) -> None:
        # attention 'filename' indique le chemin  absolu dde l'image
        self.image.save(f"lsb_{self.image.filename}")
        del(self.msg_to_embeded)


class ExtractStrategyLSB(StrategyLSB):
    _extract = ""

    def lsb_red(self, coor:tuple, *args, **kwargs) -> None:
        ExtractStrategyLSB._extract += str(self.image.getpixel(coor)[0] & 1)

    def lsb_green(self, coor:tuple, *args, **kwargs) -> None:
        ExtractStrategyLSB._extract += str(self.image.getpixel(coor)[1] & 1)

    def lsb_blue(self, coor:tuple, *args, **kwargs) -> None:
        ExtractStrategyLSB._extract += str(self.image.getpixel(coor)[2] & 1)

    def action(self):
        with open("binary.txt", mode="w") as fp:
            fp.write(ExtractStrategyLSB._extract)
        with open("binary.bin", mode="bw") as fp:
            fp.write(bin_to_str(ExtractStrategyLSB._extract))
        del(ExtractStrategyLSB._extract)


class DetectStrategyLSB(StrategyLSB):

    def lsb_red(self, coor:tuple, *args, **kwargs) -> None:
        pass

    def lsb_green(self, coor:tuple, *args, **kwargs) -> None:
        pass

    def lsb_blue(self, coor:tuple, *args, **kwargs) -> None:
        pass

    def action(self) -> None:
        pass

class ImageLSB():

    def __init__(self, image, strategy_lsb:StrategyLSB=None, lsb_custom:callable=None):
        self.image = image
        self.lenght, self.width = self.image.size
        self.strategy_lsb = strategy_lsb
        self.lsb_custom = lsb_custom

    @property
    def image(self) -> Image.Image:
        return self._image

    @image.setter
    def image(self, image) -> None:
        if isinstance(image, str):
            self._image = Image.open(image)
        elif isinstance(image, Image.Image):
            self._image = image

    def lsb_apply_strategy(self, *args, **kwargs) -> None:
        if self.lsb_custom:
            self._lsb_custom_apply_strategy(*args, **kwargs)
        else:
            # tricky get()
            absi = range(*kwargs["coor"]["x"]) if kwargs.get("coor", {}).get("x") else range(self.lenght)
            ordo = range(*kwargs["coor"]["y"]) if kwargs.get("coor", {}).get("y") else range(self.width)
            self.msg_to_embeded = list(str_to_bin(kwargs.get("msg", "")))
            try:
                for y in ordo:
                    for x in absi:
                        self._lsb_red((x, y))
                        self._lsb_green((x, y))
                        self._lsb_blue((x, y))
            except StopIteration:
                print(f"embeded end -> {kwargs['msg']}")
                self.strategy_lsb.action(self)
            else:
                self.strategy_lsb.action(self)

    def _lsb_red(self, coor:tuple) -> None:
        if self.strategy_lsb is not None:
            self.strategy_lsb.lsb_red(self, coor)
        else:
            raise ValueError("strategy_lsb object is None")

    def _lsb_green(self, coor:tuple) -> None:
        if self.strategy_lsb is not None:
            self.strategy_lsb.lsb_green(self, coor)
        else:
            raise ValueError("strategy_lsb object is None")

    def _lsb_blue(self, coor:tuple) -> None:
        if self.strategy_lsb is not None:
            self.strategy_lsb.lsb_blue(self, coor)
        else:
            raise ValueError("strategy_lsb object is None")

    def _lsb_custom_apply_strategy(self, *args, **kwargs) -> None:
        self.lsb_custom(*args, **kwargs)

if __name__ == "__main__":
    # lsb = ImageLSB("poc.png", EmbededStrategyLSB)
    # lsb.lsb_apply_strategy(msg="salut ca va ?")
    lsb = ImageLSB("lsb_poc.png", ExtractStrategyLSB)
    lsb.lsb_apply_strategy()
