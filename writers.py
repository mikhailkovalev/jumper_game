import json

from scene import Scene
from body import Body
from laws import ALaw
from renderers import ARenderer


class AFileWriter:
    def encode(self, file_name, scene):
        pass

    def decode(self, file_name):
        pass


class JSONWriter(AFileWriter):
    def encode(self, file_name, scene):
        open(file_name, 'w').write(json.dumps(
             [{
                   'attribs': body.attribs,
                   'laws': body.laws,
                   'renderers': body.renderers
              }
              for body in scene.bodies]))

    def decode(self, file_name):
        with open(file_name) as f:
            data = json.loads(f.read())
        scene = Scene()
        usedRenderers = {}
        usedLaws = {}
        for bodyData in data:
            body = Body()
            scene.bodies.append(body)
            for name, value in bodyData['attribs'].items():
                body.setAttrib(name, value)
            for lawData in bodyData['laws']:
                name = lawData['lawName']
                law = usedLaws.get(name)
                if law is None:
                    law = ALaw.factory[name]()
                    usedLaws[name] = law
                law.addBody(body, lawData['kind'])
            for name in bodyData['renderers']:
                renderer = usedRenderers.get(name)
                if renderer is None:
                    renderer = ARenderer.factory[name]()
                    usedRenderers[name] = renderer
                renderer.addBody(body)
        scene.laws = usedLaws.values()
        scene.renderers = usedRenderers.values()
        return scene
