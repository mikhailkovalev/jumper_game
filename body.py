
class Body:
    def __init__(self):
        self.attribs = {}
        self.laws = []
        self.renderers = []

    def getAttrib(self, name):
        return self.attribs[name]

    def setAttrib(self, name, value):
        self.attribs[name] = value

    def getAttribList(self):
        return list(self.attribs.keys())