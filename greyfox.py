# coding: utf-8
# python 3.7.3 x86_64

import binascii
import numpy as np
from PIL import Image
from datetime import datetime
from itertools import chain, islice
from abc import ABCMeta, abstractmethod
from colorama import init, Fore


############################## functions #######################################

def coroutine(func):
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return wrapper

@coroutine
def logger(verbose:bool=True):
    init()
    prefixes = {
        "info": "[+]",
        "error": Fore.RED + "[!]"
    }
    while True:
        type, msg = yield
        if verbose:
            prefixe = prefixes.get(type, "[?]")
            print(f"{prefixe} {msg}")

def iter_by_blockN(iterable, len_bloc=8, format=tuple):
    it = iter(iterable)
    for i in it:
        yield format(chain(i, islice(it, len_bloc-1)))

def str_to_bin(string:str) -> str:
    if string:
        return np.binary_repr(int(string.encode("utf8").hex(), 16), width=8)
    return ""

def bin_to_str(sbin:str) -> bytes:
    b_str = b""
    for i in iter_by_blockN(sbin):
        binary = "".join(i)
        integer = int(binary, 2)
        hexa = f"{integer:02x}"
        b_str += binascii.unhexlify(hexa)
    return b_str

############################## class ###########################################

class PixelLSB:
    def __init__(self, coor:tuple, color:tuple):
        self.coor = coor
        self.color = color
        self._select_color = None

    @property
    def color(self) -> tuple:
        return tuple(self._color)

    @color.setter
    def color(self, color:tuple) -> None:
        self._color = list(color)

    def __lshift__(self, other:int):
        if self._select_color is not None:
            self._color[self._select_color] <<= other
            self.color = self._color
        else:
            self.color = [c << other for c in self.color]
        return self

    def __rshift__(self, other:int):
        if self._select_color is not None:
            self._color[self._select_color] >>= other
            self.color = self._color
        else:
            self.color = [c >> other for c in self.color]
        return self

    def __or__(self, other:int):
        if self._select_color is not None:
            self._color[self._select_color] |= other
        else:
            self.color = [c | other for c in self.color]
        return self

    def __and__(self, other:int):
        if self._select_color is not None:
            self._color[self._select_color] &= other
        else:
            self.color = [c & other for c in self.color]
        return self

    def __getitem__(self, idx:int):
        self._select_color = idx
        return self

    def __repr__(self):
        return f"{self.coor}, {self.color}"

    def extract_bit(self, mask:tuple=(0,)) -> str:
        if self._select_color is not None:
            bit = ""
            for i in mask:
                bit += str((self.color[self._select_color] >> i) & 1)
            return bit
        else:
            raise IndexError("Index is needed for use this method")


class StrategyLSB(metaclass=ABCMeta):
    @abstractmethod
    def action(self, absi, ordo, colors):
        raise NotImplementedError

    @classmethod
    def get_pixel(cls, img:Image, absi:int, ordo:int):
        for y in ordo:
            for x in absi:
                yield PixelLSB((x, y), img.getpixel((x, y)))


class EmbededStrategyLSB(StrategyLSB):
    def action(self, absi:range, ordo:range, colors:dict, params_strategy:dict) -> None:
        data_to_embeded = params_strategy.get("data_to_embeded")
        file_name_ = params_strategy.get('file_name', self.file_name)
        file_name = f"hidden_{file_name_}"

        if not data_to_embeded:
            err_msg = "data_to_embeded is empty"
            self.logger.send(("error", err_msg))
            raise ValueError(f"{err_msg}, data_to_embeded -> "
                f"type: {type(data_to_embeded)}, value: {data_to_embeded}")

        bits = list(str_to_bin(data_to_embeded))
        self.logger.send(("info", f"Data to embeded -> {data_to_embeded}"))

        for pixel in StrategyLSB.get_pixel(self.image, absi, ordo):
            for k_color, v_color in colors.items():
                if bits:
                    ((pixel[v_color] >> 1) << 1) | int(bits[0])
                    bits.pop(0)
            self.image.putpixel(pixel.coor, pixel.color)
            if not bits:
                self.logger.send(("info", f"End embeded here {pixel.coor}"))
                break

        self.logger.send(("info", f"Save file with hidden data -> {file_name}"))
        self.image.save(file_name)


class ExtractStrategyLSB(StrategyLSB):
    def action(self, absi:range, ordo:range, colors:dict, params_strategy:dict) -> None:
        extract = ""
        mask = params_strategy.get("bit_mask", {})
        repr_mask = mask if mask else "Default mask -> (0,)"
        self.logger.send(("info", f"Mask -> {repr_mask}"))

        for pixel in StrategyLSB.get_pixel(self.image, absi, ordo):
            for k_color, v_color in colors.items():
                extract += pixel[v_color].extract_bit(mask.get(k_color, (0,)))

        with open("binary.txt", mode="w") as fp:
            self.logger.send(("info", "File binary.txt write"))
            fp.write(extract)
        with open("binary.bin", mode="bw") as fp:
            self.logger.send(("info", "File binary.bin write"))
            fp.write(bin_to_str(extract))


class DetectStrategyLSB(StrategyLSB):
    def action(self, absi:range, ordo:range, colors:dict, params_strategy:dict) -> None:
        all_color = params_strategy.get("detect_all_color", False)
        nbr_color = len(colors)
        width, height = len(absi), len(ordo)
        file_name_ = params_strategy.get('file_name', self.file_name)
        file_name = f"detect_{file_name_}"
        vfunc_detect = np.vectorize(lambda x, d: 255 if ((x << d) & 128) else 0)
        array_img = np.array(self.image)



        if all_color:
            self.logger.send(("info", f"All color -> Yes"))
            new_size = (width*7+6, height * (nbr_color+1) + nbr_color)
            mode, c = "RGB", (0, 0, 0)
        else:
            self.logger.send(("info", f"All color -> No"))
            new_size = (width*7+6, height * nbr_color + (nbr_color-1))
            mode, c= "L", 0
        img_detect = Image.new(mode, new_size, c)

        start = datetime.now()
        for i, j in enumerate(range(0, new_size[0], self.width), 1):
            for k, v_color in enumerate(colors.values()):
                dimension = (i+j, self.height*k+k)
                # TODO appliquer avec les dimensions
                m_img = vfunc_detect(array_img[:, :, v_color], i)
                new_img = Image.fromarray(m_img)
                img_detect.paste(new_img, dimension)
            if all_color:
                dimension = (i+j, dimension[1] + self.height + (k+1))
                new_img = Image.fromarray((array_img << i) & 128)
                img_detect.paste(new_img, dimension)
        end = datetime.now()
        self.logger.send(("info", f"Detect traitement time -> {end - start}"))

        if params_strategy.get("show", True):
            img_detect.show()
        if params_strategy.get("save", False):
            start_save = datetime.now()
            img_detect.save(file_name)
            end_save = datetime.now()
            self.logger.send(("info", f"End save {file_name} -> {end_save - start_save}"))


class ImageLSB():
    def __init__(self, image:Image, strategy_lsb:StrategyLSB=None):
        self.image = image
        self.width, self.height = self.image.size
        self.strategy_lsb = strategy_lsb
        # /!\ attention 'filename' indique le chemin  absolu de l'image /!\
        self.file_name = self.image.filename
        self.nbr_color_pixel = len(self.image.getpixel((0,0))) #Ugly :(

    @property
    def image(self) -> Image.Image:
        return self._image

    @image.setter
    def image(self, image) -> None:
        if isinstance(image, str):
            self._image = Image.open(image)
        elif isinstance(image, Image.Image):
            self._image = image
        else:
            err_msg = "image is not a str or PIL.Image instance"
            raise TypeError(f"{err_msg}, image -> {type(image)}, {image}")

    @property
    def strategy_lsb(self):
        return self._strategy_lsb

    @strategy_lsb.setter
    def strategy_lsb(self, strategy_lsb):
        strategy = {
            "detect": DetectStrategyLSB,
            "extract": ExtractStrategyLSB,
            "embeded": EmbededStrategyLSB
        }

        self._strategy_lsb = strategy.get(strategy_lsb, strategy_lsb)

    def color_sequence(self, custom:tuple=None) -> dict:
        colors = {"RED": 0 , "GREEN": 1, "BLUE": 2}

        if  self.nbr_color_pixel == 4:
            colors["ALPHA"] = 3
        if custom:
            colors = {c: colors[c] for c in custom}
        return  colors

    def apply_strategy(self, coor:dict={}, color_seq:tuple=None, params_strategy:dict={}) -> None:
        absi = range(*coor["x"]) if coor.get("x") else range(self.width)
        ordo = range(*coor["y"]) if coor.get("y") else range(self.height)
        colors = self.color_sequence(color_seq)
        repr_colors = " ".join(colors.keys())
        self.logger = logger(params_strategy.get("verbose", True))

        if not isinstance(self.strategy_lsb, type):
            err_msg = "self.strategy_lsb is not class (instance of type)"
            self.logger.send(("error", err_msg))
            raise TypeError(f"{err_msg}, strategy_lsb -> "
            f"type: {type(self.strategy_lsb)}, value: {self.strategy_lsb}")
        if not issubclass(self.strategy_lsb, StrategyLSB):
            err_msg = "self.strategy_lsb is not subclass of StrategyLSB"
            self.logger.send(("error", err_msg))
            raise TypeError(f"{err_msg}, strategy_lsb -> "
            f"type: {type(self.strategy_lsb)}, value: {self.strategy_lsb}")
        else:
            self.logger.send(("info", f"Start apply strategy with {self.strategy_lsb.__name__}"))
            self.logger.send(("info", f"Color sequence -> {repr_colors}"))
            start = datetime.now()
            self.strategy_lsb.action(self, absi, ordo, colors, params_strategy)
            end = datetime.now()
            self.logger.send(("info", f"Total time -> {end - start}"))
            self.logger.send(("info", f"End apply strategy with {self.strategy_lsb.__name__}"))
            self.logger.send(("", "\n\n" + "#" * 60 + "\n"))
