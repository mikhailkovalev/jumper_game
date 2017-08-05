from collections import defaultdict
from random import randint

from enums import PlatformTypesEnum


class ALaw:
    @staticmethod
    def getName():
        pass

    def __init__(self):
        self.params = None

    def addBody(self, body, kind=None):
        body.laws.append({'lawName': self.getName(), 'kind': str(kind)})

    def removeBody(self, body, kind=None):
        body.laws.remove({'lawName': self.getName(), 'kind': str(kind)})

    def setParams(self, params):
        self.params = params

    def apply(self):
        pass


class OneBodiesContainerLaw(ALaw):
    """
    Имеет единственный контейнер для хранения тел.
    Параметр kind, передаваемый в функции
    addBody и removeBody игнорируется.
    """
    def __init__(self):
        super().__init__()
        self.bodies = []

    def addBody(self, body, kind=None):
        super().addBody(body, kind)
        self.bodies.append(body)

    def removeBody(self, body, kind=None):
        super().removeBody(body, kind)
        try:
            self.bodies.remove(body)
        except:
            pass


class BodiesDictLaw(ALaw):
    """
    Хранит тела в defaultdict-е. Ключи - значения kind.
    """
    def __init__(self):
        super().__init__()
        self.bodies = defaultdict(list)

    def addBody(self, body, kind=None):
        super().addBody(body, kind)
        self.bodies[kind].append(body)

    def removeBody(self, body, kind=None):
        super().removeBody(body, kind)
        try:
            self.bodies[kind].remove(body)
        except:
            pass


class JumperMoving(ALaw):
    @staticmethod
    def getName():
        return 'JumperMoving'

    def __init__(self):
        super().__init__()
        self.platforms = []
        self.jumper = None
        self.epsilon = 1e-8

    def addBody(self, body, kind=None):
        if kind == 'Jumper':
            self.jumper = body
        elif kind == 'Platform':
            self.platforms.append(body)

    def removeBody(self, body, kind=None):
        if kind == 'Jumper':
            self.jumper = None
        elif kind == 'Platform' and body in self.platforms:
            self.platforms.remove(body)

    def apply(self):
        time_span = self.params['time_span']
        self.collect_jumper_data()
        self.normalize_jumper()

        if self.jvy < 0:
            self.simple_moving()
            return

        # Пока всё ещё считаем, что
        # будем двигаться без столкновений
        clash_detected = False
        time_to_first_clash = None
        clashed_platform = None

        self.send_jumper_data()
        for platform in self.platforms:
            clasher = PlatformTypesEnum.clashers[platform.getAttrib('type')]
            time_to_clash = clasher.time_to_clash_or_none(platform)
            if (time_to_clash is None or
                    time_to_clash > time_span):
                continue

            clash_detected = True

            if (time_to_first_clash is None or
                    time_to_first_clash > time_to_clash):
                # Если время первого столкновения ещё не проинициализировано
                # или текущее выявленное столкновение произойдёт раньше
                time_to_first_clash = time_to_clash
                clashed_platform = platform

        if not clash_detected:
            self.simple_moving()
        else:
            up_moving_time = time_span - time_to_first_clash
            self.jvy = self.jumper.getAttrib('initial_vertical_velocity')

            self.jx += time_span * self.jvx
            self.jy = (clashed_platform.getAttrib('position')[1]-self.jheight +
                       self.jvy*up_moving_time)
            self.jvx += self.jax * time_span
            self.jvy += self.jay * up_moving_time

            self.export_jumper_data()

    def collect_jumper_data(self):
        self.jx, self.jy = self.jumper.getAttrib('position')
        self.jvx, self.jvy = self.jumper.getAttrib('velocity')
        self.jax, self.jay = self.jumper.getAttrib('acceleration')
        self.jwidth, self.jheight = self.jumper.getAttrib('size')

    def normalize_jumper(self):
        self.jx %= self.params['screen_width']
        self.jumper.setAttrib('mirrored', self.jvx <= 0)

    def simple_moving(self):
        time_span = self.params['time_span']
        self.jx += time_span * self.jvx
        self.jy += time_span * self.jvy
        self.jvx += time_span * self.jax
        self.jvy += time_span * self.jay
        self.export_jumper_data()

    def export_jumper_data(self):
        self.jumper.setAttrib('position', (self.jx, self.jy))
        self.jumper.setAttrib('velocity', (self.jvx, self.jvy))

    def send_jumper_data(self):
        # Выделим множество всех текущих типов платформ и передадим clasher-у
        # каждого типа инфу о дудле. Выборка делается на случай, если видов
        # платформ очень много, но в текущий момент юзается много меньше
        types = {p.getAttrib('type') for p in self.platforms}
        for t in types:
            PlatformTypesEnum.clashers[t].collect_jumper_data(
                self.jumper)


class ScreenScrolling(OneBodiesContainerLaw):
    @staticmethod
    def getName():
        return 'ScreenScrolling'

    def apply(self):
        scroll_size = self.params.get('scroll_size')

        if scroll_size is None:
            return

        for b in self.bodies:
            x, y = b.getAttrib('position')
            y += scroll_size
            b.setAttrib('position', (x, y))


class PlatformValidator(OneBodiesContainerLaw):
    """
    Проверяет платформы на валидность.

    Логика валидации платформ и генерации новых разделена, поскольку в
    перспективе планируется добавить исчезающие платформы с новыми правилами
    валидации, при этом логика генерации новых платформ должна оставаться
    нетронутой.
    """
    @staticmethod
    def getName():
        return 'PlatformValidator'

    def apply(self):
        """
        Ожидает в params-ах ключ screen_height.
        Все подписанные тела, игрек-координата
        которых больше этого значения
        становятся невалидными.
        """
        screen_height = self.params.get('screen_height')

        if screen_height is None:
            return

        for body in self.bodies:
            if body.getAttrib('position')[1] > screen_height:
                body.setAttrib('valid', False)


class PlatformUpdater(OneBodiesContainerLaw):
    """
    Обновляет положения невалидных платформ и
    делает их снова валидными.

    Смотри описание класса PlatformValidator для более подробной информации.
    """
    @staticmethod
    def getName():
        return 'PlatformUpdater'

    def apply(self):
        """
        Ожидает в params-ах ключи
        platform_xmin, platform_xmax,
        platform_min_distance, platform_max_distance
        """
        top = int(min((b.getAttrib('position')[1]
                       for b in self.bodies if b.getAttrib('valid'))))

        xmin = self.params.get('platform_xmin')
        xmax = self.params.get('platform_xmax')
        min_distance = self.params.get('platform_min_distance')
        max_distance = self.params.get('platform_max_distance')
        for body in self.bodies:
            if body.getAttrib('valid'):
                continue

            x = randint(xmin, xmax)
            y = top - randint(
                min_distance, max_distance)
            body.setAttrib('position', (x, y))
            body.setAttrib('valid', True)
