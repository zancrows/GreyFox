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
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def lsb_red(self):
        raise NotImplementedError

    @abstractmethod
    def lsb_green(self):
        raise NotImplementedError

    @abstractmethod
    def lsb_blue(self):
        raise NotImplementedError


class EmbededStrategyLSB(StrategyLSB):

    def __init__(self):
        pass

    def lsb_red(self) -> None:
        pass

    def lsb_green(self) -> None:
        pass

    def lsb_blue(self) -> None:
        pass


class ExtractStrategyLSB(StrategyLSB):

    def __init__(self):
        pass

    def lsb_red(self):
        pass

    def lsb_green(self):
        pass

    def lsb_blue(self):
        pass


class DetectStrategyLSB(StrategyLSB):

    def __init__(self):
        pass

    def lsb_red(self):
        pass

    def lsb_green(self):
        pass

    def lsb_blue(self):
        pass


class PicLSB:

    def __init__(self, image, strategy_lsb=None):
        self.image = image
        self.lenght, self.width = self.image.size
        self.strategy_lsb = strategy_lsb

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        if isinstance(image, str):
            self._image = Image.open(image)
        elif isinstance(image, Image.Image):
            self._image = image

    def lsb_red(self):
        if self.strategy_lsb is not None:
            self.strategy_lsb.lsb_red(self)
        else:
            raise ValueError("strategy_lsb object is None")

    def lsb_green(self):
        if self.strategy_lsb is not None:
            self.strategy_lsb.lsb_green(self)
        else:
            raise ValueError("strategy_lsb object is None")

    def lsb_blue(self):
        if self.strategy_lsb is not None:
            self.strategy_lsb.lsb_blue(self)
        else:
            raise ValueError("strategy_lsb object is None")

    def lsb_other(self):
        raise NotImplementedError


if __name__ == "__main__":
    pass
