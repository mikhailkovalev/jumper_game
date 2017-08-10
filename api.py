from math import log, sqrt, pi, atan
from operator import mul
from collections import deque
from PIL import Image


two_div_pi = 2 / pi


def repaint_sprite(sprite, old_color, new_color):
    def f(x, y):
        """
        Коммутативный критерий оценки близости двух чисел. Возвращаемое
        значение равно нулю, если числа одинаковы; чем больше разница между
        числами, тем больше возвращаемое значение.
        """
        return x/y + y/x - 2

    def euclid_distance(a, b):
        return sqrt(sum(map(lambda x, y: (x-y)**2, a, b)))

    def get_rho(pix):
        """
        Определяет, насколько близко цвет переданного пикселя близок к серому.
        Если цвет пикселя является градацией серого, то возвращаемое значение
        равно нулю.
        """
        pix1 = deque(pix)
        pix1.rotate(1)
        return euclid_distance((0,)*len(pix), map(f, pix, pix1))

    def get_power(alpha, rho):
        return 1 + two_div_pi*(alpha - 1)*atan(rho)

    def convert(c, alpha, rho):
        return int(255 * pow(c/255, get_power(alpha, rho)))

    gamma = tuple(map(lambda x, y: log(y/255) / log(x/255),
                  old_color, new_color))

    old_sprite_data = sprite.getdata()
    new_sprite_data = [None] * mul(*sprite.size)

    for i, old_pix in enumerate(old_sprite_data):
        if not old_pix[3]:
            new_sprite_data[i] = old_pix
        else:
            new_pix = [255] * 4
            rho = get_rho(old_pix[:3])

            for j in range(3):
                new_pix[j] = convert(old_pix[j], gamma[j], rho)

            new_sprite_data[i] = tuple(new_pix)

    new_sprite = Image.new('RGBA', sprite.size)
    new_sprite.putdata(new_sprite_data)
    return new_sprite
