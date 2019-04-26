# coding: utf-8
# python 3.7.1 x86_64

import binascii
from abc import ABCMeta, abstractmethod
from PIL import Image

__version__ = 1.0

"""
TODO:
Revoir le décodage (bin_to_str)
ajout de commentaire
"""

def str_to_bin(string:str) -> str:
    if string != "":
        return bin(int(binascii.hexlify(bytes(string, "utf8")), 16))[2:]
    return ""

def bin_to_str(sbin:str) -> str:
    return binascii.unhexlify(f"{int(sbin, 2):x}")

def int_to_bin(integer:str) -> str:
    return f"{integer:08b}"

def bin_to_int(bin:str) -> int:
    return int(bin, 2)


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
        b_color = int_to_bin(color_to_edit)
        new_color = b_color[:-1] + bit
        pixel_to_edit[color] = bin_to_int(new_color)
        image.putpixel(coor, tuple(pixel_to_edit))

    def lsb_red(self, coor:tuple, *args, **kwargs) -> None:
        if self.msg_to_embeded == "":
            raise StopIteration
        EmbededStrategyLSB._edit_pixel(self.image, coor, self.msg_to_embeded[0], 0)
        self.msg_to_embeded = self.msg_to_embeded[1:]

    def lsb_green(self, coor:tuple, *args, **kwargs) -> None:
        if self.msg_to_embeded == "":
            raise StopIteration
        EmbededStrategyLSB._edit_pixel(self.image, coor, self.msg_to_embeded[0], 1)
        self.msg_to_embeded = self.msg_to_embeded[1:]

    def lsb_blue(self, coor:tuple, *args, **kwargs) -> None:
        if self.msg_to_embeded == "":
            raise StopIteration
        EmbededStrategyLSB._edit_pixel(self.image, coor, self.msg_to_embeded[0], 2)
        self.msg_to_embeded = self.msg_to_embeded[1:]

    def action(self) -> None:
        # attention 'filename' indique le chemin  absolu dde l'image
        self.image.save(f"lsb_{self.image.filename}")
        del(self.msg_to_embeded)


class ExtractStrategyLSB(StrategyLSB):
    _extract = ""

    def lsb_red(self, coor:tuple, *args, **kwargs) -> None:
        ExtractStrategyLSB._extract += int_to_bin(self.image.getpixel(coor)[0])[-1]

    def lsb_green(self, coor:tuple, *args, **kwargs) -> None:
        ExtractStrategyLSB._extract += int_to_bin(self.image.getpixel(coor)[1])[-1]

    def lsb_blue(self, coor:tuple, *args, **kwargs) -> None:
        ExtractStrategyLSB._extract += int_to_bin(self.image.getpixel(coor)[2])[-1]

    def action(self) -> None:
        with open("binary.txt", "w") as fp:
            fp.write(ExtractStrategyLSB._extract)
        with open("binary", mode="bw") as fp:
            fp.write(bin_to_str(ExtractStrategyLSB._extract))
        print(bin_to_str(ExtractStrategyLSB._extract))
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
            abs = range(*kwargs["coor"]["x"]) if kwargs.get("coor", {}).get("x") else range(self.lenght)
            ord = range(*kwargs["coor"]["y"]) if kwargs.get("coor", {}).get("y") else range(self.width)
            self.msg_to_embeded = str_to_bin(kwargs.get("msg", ""))
            try:
                for y in ord:
                    for x in abs:
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
    lsb = ImageLSB("lsb_poc.png", ExtractStrategyLSB)
    # lsb.lsb_apply_strategy(coor={"y": (0,1)})
