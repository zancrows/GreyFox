# coding: utf-8
# python 3.7.3 x86_64

import binascii
from PIL import Image
from datetime import datetime
from itertools import chain, islice
from abc import ABCMeta, abstractmethod

"""
    TODO: logger centralisé
    TODO: commenter le code
    TODO: tester import dans un autre projet
    TODO: log dans DetectStrategyLSB
    TODO : optimiser DetectStrategyLSB
"""

############################## functions #######################################

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
        if self._select_color:
            self._color[self._select_color] |= other
        else:
            self.color = [c | other for c in self.color]
        return self

    def __and__(self, other:int):
        if self._select_color:
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
            err_msg = "[!] data_to_embeded is empty"
            print(err_msg)
            raise ValueError(f"{err_msg}, data_to_embeded -> "
                f"type: {type(data_to_embeded)}, value: {data_to_embeded}")

        bits = list(str_to_bin(data_to_embeded))
        # TODO print mask/params
        print(f"[+] data to embeded -> {data_to_embeded}")
        for pixel in StrategyLSB.get_pixel(self.image, absi, ordo):
            for k_color, v_color in colors.items():
                if bits:
                    # TODO à adapter avec un mask
                    ((pixel[v_color] >> 1) << 1) | int(bits[0])
                    bits.pop(0)
            self.image.putpixel(pixel.coor, pixel.color)
            if not bits:
                print(f"[+] end embeded here {pixel.coor}")
                break

        print(f"[+] save file with hidden data -> {file_name}")
        self.image.save(file_name)


class ExtractStrategyLSB(StrategyLSB):
    def action(self, absi:range, ordo:range, colors:dict, params_strategy:dict) -> None:
        extract = ""
        mask = params_strategy.get("bit_mask", {})
        # TODO print mask/params
        for pixel in StrategyLSB.get_pixel(self.image, absi, ordo):
            for k_color, v_color in colors.items():
                extract += pixel[v_color].extract_bit(mask.get(k_color, (0,)))

        with open("binary.txt", mode="w") as fp:
            print("[+] binary.txt write")
            fp.write(extract)
        with open("binary.bin", mode="bw") as fp:
            print("[+] binary.bin write")
            fp.write(bin_to_str(extract))


class DetectStrategyLSB(StrategyLSB):
    def action(self, absi:range, ordo:range, colors:dict, params_strategy:dict) -> None:
        nbr_color = len(colors)
        all_color = params_strategy.get("detect_all_color", False)

        if all_color:
            new_size = (self.width*7+6, self.height * (nbr_color+1) + nbr_color)
        else:
            new_size = (self.width*7+6, self.height * nbr_color + (nbr_color-1))
        img_detect = Image.new("RGB", new_size, (0, 0, 0))

        for i, j in enumerate(range(0, new_size[0], self.width), 1):
            for k, v_color in enumerate(colors.values()):
                dimension = (i+j, self.height*k+k)
                new_img = Image.new("L", self.image.size, 0)
                for pixel in StrategyLSB.get_pixel(self.image, absi, ordo):
                    (pixel[v_color] << i) & 128
                    pixel.color = (255,) if pixel.color[v_color] else (0,)
                    new_img.putpixel(pixel.coor, pixel.color)
                img_detect.paste(new_img, dimension)

            if all_color:
                mode, c = "RGB", 0
                if self.nbr_color_pixel == 4:
                    mode, c = "RGBA", (255, 255, 255)
                new_img = Image.new(mode, self.image.size, c)
                dimension = (i+j, dimension[1] + self.height + (k+1))
                for pixel in StrategyLSB.get_pixel(self.image, absi, ordo):
                    (pixel << i) & 128
                    new_img.putpixel(pixel.coor, pixel.color)
                img_detect.paste(new_img, dimension)
        img_detect.show()


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
            err_msg = "[!] image is not a str or PIL.Image instance"
            print(err_msg)
            raise TypeError(f"{err_msg}, image -> {type(image)}, {image}")

    def color_sequence(self, custom:tuple=None) -> dict:
        colors = {"RED": 0 , "GREEN": 1, "BLUE": 2}

        if  self.nbr_color_pixel == 4:
            colors["ALPHA"] = 3
        if custom:
            colors = {c: _colors[c] for c in custom}
        return  colors

    def apply_strategy(self, coor:dict={}, color_seq:tuple=None, params_strategy:dict={}) -> None:
        absi = range(*coor["x"]) if coor.get("x") else range(self.width)
        ordo = range(*coor["y"]) if coor.get("y") else range(self.height)
        colors = self.color_sequence(color_seq)
        repr_colors = " ".join(colors.keys())

        if not isinstance(self.strategy_lsb, type):
            err_msg = "[!] self.strategy_lsb is not class (instance of type)"
            print(err_msg)
            raise TypeError(f"{err_msg}, strategy_lsb -> "
            f"type: {type(self.strategy_lsb)}, value: {self.strategy_lsb}")
        if not issubclass(self.strategy_lsb, StrategyLSB):
            err_msg = "[!] self.strategy_lsb is not subclass of StrategyLSB"
            print(err_msg)
            raise TypeError(f"{err_msg}, strategy_lsb -> "
            f"type: {type(self.strategy_lsb)}, value: {self.strategy_lsb}")
        else:
            print(f"[+] Start apply strategy with {self.strategy_lsb.__name__}")
            print(f"[+] color sequence -> {repr_colors}")
            start = datetime.now()
            self.strategy_lsb.action(self, absi, ordo, colors, params_strategy)
            end = datetime.now()
            print(f"[+] time -> {end - start}")
            print(f"[+] End apply strategy with {self.strategy_lsb.__name__}")
            print("\n###########################################################", end ="\n\n")

if __name__ == "__main__":
    img = ImageLSB("tux_hidden.png", DetectStrategyLSB)
    img.apply_strategy()
