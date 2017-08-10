from PIL import Image, ImageTk

from api import repaint_sprite
from enums import PlatformTypesEnum


class ARenderer:
    @staticmethod
    def getName():
        pass

    def __init__(self, context=None):
        self.context = context
        self.bodies = []

    def addBody(self, body):
        body.renderers.append(self.getName())
        self.bodies.append(body)

    def renderOne(self, body):
        pass

    def renderAll(self):
        for b in self.bodies:
            self.renderOne(b)

    def setContext(self, context):
        self.context = context


class JumperRenderer(ARenderer):

    @staticmethod
    def getName():
        return 'JumperRenderer'

    def __init__(self, context=None):
        super().__init__(context)
        image = Image.open('./images/doodle.png')
        self.image = ImageTk.PhotoImage(image)
        self.image_size = image.size

    def addBody(self, body):
        super().addBody(body)
        body.setAttrib('size', self.image_size)

    def renderOne(self, body):
        x, y = body.getAttrib('position')
        self.context.drawImage(x, y, self.image)
        maxx = body.getAttrib('max_x_coordinate')
        if x + body.getAttrib('size')[0] > maxx:
            x -= maxx
            self.context.drawImage(x, y, self.image)


class PlatformRenderer(ARenderer):

    # Стандартный цвет платформы. Пока задаём хардкодом
    old_color = (133, 194, 38)

    @staticmethod
    def getName():
        return 'PlatformRenderer'

    def __init__(self, context=None):
        super().__init__(context)
        self.collect_sprites()

    def collect_sprites(self):
        default_sprite = Image.open('./images/platform.png')
        self.image_size = default_sprite.size

        colors = PlatformTypesEnum.colors

        self.sprites = {}
        for k in PlatformTypesEnum.keys:
            current_color = colors.get(k)

            if current_color:
                sprite = repaint_sprite(
                    default_sprite,
                    self.old_color,
                    current_color
                )
            else:
                sprite = default_sprite

            self.sprites[k] = ImageTk.PhotoImage(sprite)

    def addBody(self, body):
        super().addBody(body)
        body.setAttrib('size', self.image_size)

    def renderOne(self, body):
        x, y = body.getAttrib('position')
        type_ = body.getAttrib('type')
        self.context.drawImage(x, y, self.sprites[type_])


class BackgroundRenderer(ARenderer):
    @staticmethod
    def getName():
        return 'BackgroundRenderer'

    def __init__(self, context=None):
        super().__init__(context)
        image = Image.open('./images/background.png')
        self.image = ImageTk.PhotoImage(image)
        self.image_size = image.size

    def addBody(self, body):
        super().addBody(body)
        # body.setAttrib('size', self.image_size)

    def renderOne(self, body):
        y = body.getAttrib('position')[1] % self.screen_height
        self.context.drawImage(0, y, self.image)
        self.context.drawImage(0, y-self.image_size[1], self.image)
