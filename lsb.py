# coding: utf-8
# python 3.7.3 x86_64

import binascii
from PIL import Image
from datetime import datetime
from itertools import chain, islice
from abc import ABCMeta, abstractmethod

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

def extract_bit(byte:int, mask:tuple=(0,)) -> str:
    b = ""
    for i in mask:
        b += str((byte >> i) & 1)
    return b

############################## class ###########################################

class StrategyLSB(metaclass=ABCMeta):

    @abstractmethod
    def action(self, absi, ordo, colors):
        raise NotImplementedError()

    @classmethod
    def get_pixel(cls, img, absi:int, ordo:int):
        for y in ordo:
            for x in absi:
                yield (x, y), img.getpixel((x, y)),


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
        print(f"DEBUG -> {bits}")
        # TODO print mask/params
        print(f"[+] data to embeded -> {data_to_embeded}")
        for coor, pixel in StrategyLSB.get_pixel(self.image, absi, ordo):
            new_pixel = list(pixel)
            for k_color, v_color in colors.items():
                if bits:
                    new_pixel[v_color] = (pixel[v_color] >> 1) << 1 | int(bits[0])
                    bits.pop(0)
            self.image.putpixel(coor, tuple(new_pixel))
            if not bits:
                print(f"[+] end embeded here {coor}")
                break

        print(f"[+] save file with hidden data -> {file_name}")
        self.image.save(file_name)


class ExtractStrategyLSB(StrategyLSB):

    def action(self, absi:range, ordo:range, colors:dict, params_strategy:dict) -> None:
        extract = ""
        mask = params_strategy.get("bit_mask", {})

        # TODO print mask/params
        for _, pixel in StrategyLSB.get_pixel(self.image, absi, ordo):
            for k_color, v_color in colors.items():
                extract += extract_bit(pixel[v_color], mask.get(k_color, (0,)))

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
        # /!\ attention 'filename' indique le chemin  absolu de l'image /!\
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
        else:
            err_msg = "[!] image is not a str or PIL.Image instance"
            print(err_msg)
            raise TypeError(f"{err_msg}, image -> {type(image)}, {image}")

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

if __name__ == "__main__":
    img = ImageLSB("test.png", EmbededStrategyLSB)
    # c = ("GREEN", "RED")
    p = {"data_to_embeded": "bonjour"}
    # img.apply_strategy(color_seq=c, params_strategy=p)
    # img.apply_strategy()
    img.apply_strategy(params_strategy=p)
    himg = ImageLSB("hidden_test.png", ExtractStrategyLSB)
    himg.apply_strategy()
