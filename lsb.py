# coding: utf-8
# python 3.7.1 x86_64

import binascii
from abc import ABCMeta, abstractmethod
from PIL import Image


def str_to_bin(string:str) -> str:
    return bin(int(binascii.hexlify(bytes(string, "utf8")), 16))[2:]

def bin_to_str(sbin:str) -> str:
    return binascii.unhexlify(f"{int(sbin, 2):x}").decode("utf-8")


class StrategyLSB(metaclass=ABCMeta):

    @abstractmethod
    def lsb_red(self, coor:tuple):
        raise NotImplementedError

    @abstractmethod
    def lsb_green(self, coor:tuple):
        raise NotImplementedError

    @abstractmethod
    def lsb_blue(self, coor:tuple):
        raise NotImplementedError

    @abstractmethod
    def action(self):
        raise NotImplemented


class EmbededStrategyLSB(StrategyLSB):

    def lsb_red(self, coor:tuple) -> None:
        pass

    def lsb_green(self, coor:tuple) -> None:
        pass

    def lsb_blue(self, coor:tuple) -> None:
        pass

    def action(self) -> None:
        pass


class ExtractStrategyLSB(StrategyLSB):

    def lsb_red(self, coor:tuple):
        print(self.image.getpixel(coor)[0], end=", ")

    def lsb_green(self, coor:tuple):
        print(self.image.getpixel(coor)[1], end=", ")

    def lsb_blue(self, coor:tuple):
        print(self.image.getpixel(coor)[2])

    def action(self):
        print(bin_to_str())


class DetectStrategyLSB(StrategyLSB):

    def lsb_red(self, coor:tuple):
        pass

    def lsb_green(self, coor:tuple):
        pass

    def lsb_blue(self, coor:tuple):
        pass

    def action(self):
        pass

class ImageLSB():

    def __init__(self, image, strategy_lsb=None, lsb_custom=None):
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

    def lsb_apply_strategy(self, *args, **kwargs):
        if self.sb_custom:
            self._lsb_custom_apply_strategy(*args, **kwargs)
        else:
            abs = range(*coor["x"]) if coor.get("x") else range(self.lenght)
            ord = range(*coor["y"]) if coor.get("y") else range(self.width)
            for x in abs:
                for y in ord:
                    self._lsb_red((x, y))
                    self._lsb_green((x, y))
                    self._lsb_blue((x, y))
            self.strategy_lsb.action()


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

    def _lsb_custom_apply_strategy(self, *args, **kwargs):
        self.lsb_custom(*args, **kwargs)

if __name__ == "__main__":
    lsb = ImageLSB("ch9.png", ExtractStrategyLSB)
    #print(lsb.image.getpixel((0,0))[0])
    lsb.lsb_apply()
