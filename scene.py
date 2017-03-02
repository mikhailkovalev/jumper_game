from body import *
from contexts import *
from laws import *
from renderers import *

class Scene:
    def __init__(self):
        self.bodies = []
        self.laws = []
        self.renderers = []
        self.contexts = []
