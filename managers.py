from writers import *
import tkinter as tk
import time
from random import randint, seed
from math import fabs

class AManager:
    def __init__(self, writer = None):
        self.writer = writer
        self.params = {}

    def setWriter(self, writer):
        self.writer = writer

    def loadScene(self, file_name):
        self.scene = self.writer.decode(file_name)

    def saveScene(self, file_name):
        self.writer.encode(file_name, self.scene)

    def createScene(self):
        pass

    def applyLaws(self):
        for law in self.scene.laws:
            law.setParams(self.params)
            law.apply()

    def renderFrame(self):
        for renderer in self.scene.renderers:
            renderer.renderAll()

    def initParams(self):
        pass

    def updateParams(self):
        pass

    def isRunning(self):
        return True

    def afterDisplay(self):
        pass

    def run(self):
        self.initParams()
        while self.isRunning():
            for context in self.scene.contexts:
                context.clear()
            self.renderFrame()
            self.updateParams()
            self.applyLaws()
            self.afterDisplay()

class JumperManager(AManager):
    def __init__(self):
        # seed(10)
        self.root = tk.Tk()
        self.root.title('Jumper')
        self.screen = (400, 533)
        self.canvas = tk.Canvas(self.root)
        self.canvas.config(width = self.screen[0])
        self.canvas.config(height = self.screen[1])
        self.root.bind('<KeyPress>', self.moveJumper)
        self.canvas.pack()
        # self.frame_interval = 42
        self.frame_interval = 21
        self.createScene()
        self.params = {}
        self.game_over = False

    def createScene(self):
        self.scene = Scene()
        self.createContext()
        self.createLaws()
        self.createJumper()
        self.createPlatforms()
        self.createBackground()

    def createContext(self):
        context = TkContext(self.canvas)
        self.scene.contexts.append(context)

    def createLaws(self):
        self.jumper_moving = JumperMoving()
        self.scroller = ScreenScrolling()
        self.scene.laws += [self.jumper_moving, self.scroller]

    def createJumper(self):
        self.jumper = Body()
        self.jumper.setAttrib('mirrored', False)
        self.scene.bodies.append(self.jumper)
        offset = 15
        self.jumper.setAttrib('position', (offset, self.screen[1] - offset))
        start_vy = -600
        self.jumper.setAttrib('velocity', (0, start_vy))
        self.jumper.setAttrib('initial_vertical_velocity', start_vy)
        self.jumper.setAttrib('horizontal_velocity_factor', 0.9)
        self.jumper.setAttrib('max_x_coordinate', self.screen[0])
        self.jumper.setAttrib('epsilon', 1e-3)
        g = 960
        self.jumper.setAttrib('acceleration', (0, g))
        self.jumper_moving.addBody(self.jumper, 'Jumper')
        self.max_jump_length = int(0.5 * start_vy * start_vy / g)
        print(self.max_jump_length)
        # self.collider.addBody(self.jumper, 'Jumper')
        self.scroller.addBody(self.jumper)
        self.scene.renderers.append(JumperRenderer(self.scene.contexts[0]))
        self.scene.renderers[-1].addBody(self.jumper)

    def createPlatforms(self):
        count = 7
        renderer = PlatformRenderer(self.scene.contexts[0])
        # self.scene.renderers.append(renderer)
        self.scene.renderers.insert(0, renderer)
        self.bord = 5
        self.platform_xmax = self.screen[0] - self.bord - renderer.image_size[0]
        self.platform_ymax = self.screen[1] - self.bord - renderer.image_size[1]
        self.platform_min_distance = self.max_jump_length // 2
        self.platform_max_distance = -10 + self.max_jump_length
        top = self.screen[1] + self.jumper.getAttrib('size')[1]
        for i in range(count):
            platform = Body()
            self.scene.bodies.append(platform)
            renderer.addBody(platform)
            # self.collider.addBody(platform, 'Platform')
            self.jumper_moving.addBody(platform, 'Platform')
            self.scroller.addBody(platform)
            x = randint(self.bord, self.platform_xmax)
            # y = randint(self.bord, self.platform_ymax)
            y = top - randint(self.platform_min_distance, self.platform_max_distance)
            top = y
            platform.setAttrib('position', (x, y))

    def updatePlatforms(self):
        top = min((b.getAttrib('position')[1] for b in self.scene.bodies if b != self.jumper))
        top = int(top)
        # old_top = top
        for b in self.scene.bodies:
            if b == self.jumper:
                continue
            x, y = b.getAttrib('position')
            if y > self.screen[1]:
                x = randint(self.bord, self.platform_xmax)
                y = top - randint(self.platform_min_distance, self.platform_max_distance)
                # if y < self.bord:
                #     y = randint(self.bord, old_top)
                # else:
                #     top = y
                b.setAttrib('position', (x, y))

    def moveJumper(self, event):
        vx, vy = self.jumper.getAttrib('velocity')
        offset = 300
        # print('keycode =', event.keycode)
        if event.keycode == 38:
            vx -= offset
            self.jumper.setAttrib('velocity', (vx, vy))
            return
        elif event.keycode == 40:
            vx += offset
            self.jumper.setAttrib('velocity', (vx, vy))
            return


    def createBackground(self):
        pass

    def setScrollSize(self):
        factor = 0.2
        y = self.jumper.getAttrib('position')[1]
        b = self.screen[1] * factor
        if y < b:
            dy = b - y
            # self.scroller.setParams({'scroll_size': dy})
            self.params['scroll_size'] = dy
        else:
            self.params['scroll_size'] = 0

    def updateScene(self):
        tend = time.time()
        # self.params = {'time_span': tend - self.tbeg}
        self.params['time_span'] = tend - self.tbeg
        self.setScrollSize()
        self.tbeg = tend
        self.applyLaws()
        self.scene.contexts[0].clear()
        self.renderFrame()
        # self.deletePlatforms()
        self.updatePlatforms()
        if self.jumper.getAttrib('position')[1] > self.screen[1]:
            self.root.destroy()
        self.root.after(self.frame_interval, self.updateScene)

    def run(self):
        self.tbeg = time.time()
        self.updateScene()
        self.root.mainloop()
