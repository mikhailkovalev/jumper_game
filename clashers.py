from math import fabs, sqrt


class AClasher:
    """
    Абстрактный класс, описывает базовый интерфейс взаимодействия дудла с
    различными видами платформ. Используется в законе взаимодействия дудла и
    платформ. Логика вынесена в отдельный класс, поскольку изменение параметров
    дудла необходимо производить после анализа его взаимодействий со всеми
    платформами, чего нельзя достигнуть, если описывать для каждого вида
    платформ свой закон (в смысле наследник ALaw).
    """
    # Задаём значение "машинного нуля"
    epsilon = 1e-6

    @staticmethod
    def lines_intersects(line1, line2):
        """
        Проверяет, пересекаются ли два горизонтальных отрезка

        :param Iterable line1: контейнер из двух чисел, являющихся границами
            горизонтального отрезка.
        :param Iterable line2: то же самое, что и line1

        :return: True, если пересекаются и False в противном случае
        """
        # Пока что сделаем "лишь бы работало", а потом подумаем об
        # оптимизации... Если, конечно, когда-нибудь об этом вспомним.
        line1 = sorted(line1)
        line2 = sorted(line2)

        return not (line1[1] < line2[0] or line2[1] < line1[0])

    @classmethod
    def square_equation_min_positive_root_or_none(cls, a, b, c):
        """
        Возвращает минимальный неотрицательный корень квадратного уравнения
        a * x**2 + b*x + c = 0
        """
        if fabs(a) < cls.epsilon:
            if fabs(b) < cls.epsilon:
                if fabs(c) < cls.epsilon:
                    # Если по какой-то дурацкой шутке получится так, что вообще
                    # все числа являются корнями, то и вернём минимальное
                    # неотрицательное из всех корней, хуле
                    return 0
                else:
                    # Если вообще ни одно число не является корнем, то вернём
                    # None, как и обещали
                    return None
            else:
                # Обычное линейное уравнение. Найдём его корень. Если он
                # неотрицателен - вернём его, в противном случае вернём None
                x = -c / b
                return x if x >= 0 else None
        else:
            # Обычное квадратное уравнение. Решать будем через D/4.
            b *= 0.5
            d = b * b - a * c

            if d < 0:
                # Ну, если действительных корней нет, то не судьба: вернём None
                return None
            else:
                d = sqrt(d)

                # Находим мЕньший корень уравнения. Если он уже неотрицателен,
                # то второй и считать не надо
                x = -(b + d) / a
                if x >= 0:
                    return x

                # В противном случае вычислим бОльший. Вдруг повезёт:
                x = -(b - d) / a
                if x >= 0:
                    return x

                # Если не повезло, то вернём None
                return None

    def collect_jumper_data(self, jumper):
        """
        Сохраняет параметры дудла в инстансе класса.
        """
        # Платформ много, дудл один (по крайней мере пока), а каждый раз
        # вытаскивать его атрибуты из словарей несколько накладно. Поэтому
        # будем пока сохранять атрибуты дудла в инстансе clasher-а, для
        # хоть какой-то оптимизации
        self.jax, self.jay = jumper.getAttrib('acceleration')
        self.jvx, self.jvy = jumper.getAttrib('velocity')
        self.jx, self.jy = jumper.getAttrib('position')
        self.jw, self.jh = jumper.getAttrib('size')
        self.half_jay = 0.5 * self.jay
        self.half_jax = 0.5 * self.jax
        self.j_bottom = self.jy + self.jh

    def time_to_clash_or_none(self, platform):
        pass

    def resolve_clash(self, platform):
        pass


class StaticClasher(AClasher):
    """
    Реализует интерфейс абстрактного clasher-а для реализации взаимодействия
    дудла со статичными платформами (т.е. неподвижными)
    """

    def time_to_clash_or_none(self, platform):
        px, py = platform.getAttrib('position')

        # Сначала найдём время, за которое дудл и платформа окажутся на одном
        # уровне по оси игрек. Для этого нужно решить квадратное уравнение
        # jy- py + jvy*t + 0.5*jay * t**2 = 0
        t = self.square_equation_min_positive_root_or_none(
                self.half_jay, self.jvy, self.j_bottom - py)

        if t is None:
            # Если дудл никогда не достигнет одного уровня с платформой
            return None

        psx = platform.getAttrib('size')[0]

        # Выясним, действительно ли произойдёт столкновение при достжении
        # дудлом платформы

        njx = self.jx + t*(self.jvx + t*self.half_jax)

        if self.lines_intersects((njx, njx+self.jw), (px, px + psx)):
            # Если отрезки пересекаются, значит столкновение произошло
            return t

        return None
