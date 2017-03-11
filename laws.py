from body import *
import math
import numpy as np

class ALaw:
	@staticmethod
	def getName():
		pass

	def __init__(self):
		self.params = None

	def addBody(self, body, kind = None):
		# body.laws.append((self.getName(), str(kind)))
		body.laws.append({'lawName': self.getName(), 'kind': str(kind)})

	def removeBody(self, body, kind = None):
		body.laws.remove({'lawName': self.getName(), 'kind': str(kind)})

	def setParams(self, params):
		self.params = params

	def apply(self):
		pass

class JumperPlatformInteraction:
	@staticmethod
	def getName():
		return 'JumperPlatformInteraction'

	def __init__(self):
		super().__init__()
		self.platforms = []
		self.jumper = None
		self.epsilon = 1e-6

	def addBody(self, body, kind = None):
		if kind == 'Jumper':
			self.jumper = body
		elif kind == 'Platform':
			self.platforms.append(body)

	def removeBody(self, body, kind = None):
		if kind == 'Jumper':
			self.jumper = None
		elif kind == 'Platform':
			self.platforms.remove(body)

	def apply(self):
		time_span = self.params['time_span']


# class JumperMoving(ALaw):
# 	@staticmethod
# 	def getName():
# 		return 'JumperMoving'
#
# 	def __init__(self):
# 		super().__init__()
# 		self.platforms = []
# 		self.jumper = None
# 		self.epsilon = 1e-8
#
# 	def addBody(self, body, kind = None):
# 		if kind == 'Jumper':
# 			self.jumper = body
# 		elif kind == 'Platform':
# 			self.platforms.append(body)
#
# 	def removeBody(self, body, kind = None):
# 		if kind == 'Jumper':
# 			self.jumper = None
# 		elif kind == 'Platform' and body in self.platforms:
# 			self.platforms.remove(body)
#
# 	def apply(self):
# 		time_span = self.params['time_span']
# 		jx, jy = self.jumper.getAttrib('position')
# 		js = self.jumper.getAttrib('size')
# 		jvx, jvy = self.jumper.getAttrib('velocity')
# 		jax, jay = self.jumper.getAttrib('acceleration')
# 		jxf = self.jumper.getAttrib('horizontal_velocity_factor')
# 		maxx = self.jumper.getAttrib('max_x_coordinate')
# 		while jx > maxx:
# 			jx -= maxx
# 		while jx < 0:
# 			jx += maxx
# 		if jvx > 0:
# 			self.jumper.setAttrib('mirrored', False)
# 		else:
# 			self.jumper.setAttrib('mirrored', True)
# 		jumper_horizontal_offset = jvx * time_span
# 		jumper_vertical_offset   = jvy * time_span
# 		if jvy < 0:
# 			jx += jumper_horizontal_offset
# 			jy += jumper_vertical_offset
# 			jvx += jax * time_span
# 			jvy += jay * time_span
# 			if np.fabs(jvx) > self.epsilon:
# 				jvx *= jxf
# 			self.jumper.setAttrib('position', (jx, jy))
# 			self.jumper.setAttrib('velocity', (jvx, jvy))
# 			return
# 		for platform in self.platforms:
# 			px, py = platform.getAttrib('position')
# 			ps = platform.getAttrib('size')
# 			if self.intersect(\
# 					jy + js[1],
# 					jx, jx + js[0],
# 					jumper_horizontal_offset,
# 					jumper_vertical_offset,
# 					py, px, px + ps[0]):
# 				# print('old bottom:', jy)
# 				down_moving_time = (py - jy - js[1]) / jvy
# 				up_moving_time = time_span - down_moving_time
# 				jvy = self.jumper.getAttrib('initial_vertical_velocity')
# 				jx += jumper_horizontal_offset
# 				jy = py - js[1] + jvy * up_moving_time
# 				jvx += jax * time_span
# 				jvy += jay * up_moving_time
# 				if np.fabs(jvx) > self.epsilon:
# 					jvx *= jxf
# 				self.jumper.setAttrib('position', (jx, jy))
# 				self.jumper.setAttrib('velocity', (jvx, jvy))
# 				return
# 		jx += jumper_horizontal_offset
# 		jy += jumper_vertical_offset
# 		jvx += jax * time_span
# 		jvy += jay * time_span
# 		if np.fabs(jvx) > self.epsilon:
# 			jvx *= jxf
# 		self.jumper.setAttrib('position', (jx, jy))
# 		self.jumper.setAttrib('velocity', (jvx, jvy))
#
#
# 	def intersect(self,
# 			jumper_bottom,
# 			jumper_left,
# 			jumper_right,
# 			jumper_horizontal_offset,
# 			jumper_vertical_offset,
# 			platform_top,
# 			platform_left,
# 			platform_right):
# 		new_jumper_bottom = jumper_bottom + jumper_vertical_offset
# 		if not (platform_top >= jumper_bottom \
# 				and platform_top <= new_jumper_bottom):
# 			return False
# 		if np.fabs(jumper_vertical_offset) < self.epsilon:
# 			return False
# 		t = (platform_top - jumper_bottom) / jumper_vertical_offset
# 		offset = t * jumper_horizontal_offset
# 		left = jumper_left + offset
# 		right = jumper_right + offset
# 		if platform_right < left \
# 				or platform_left > right:
# 			return False
# 		return True


class ScreenScrolling(ALaw):
	@staticmethod
	def getName():
		return 'ScreenScrolling'

	def __init__(self):
		super().__init__()
		self.bodies = []

	def addBody(self, body, kind = None):
		super().addBody(body, kind)
		self.bodies.append(body)

	def removeBody(self, body, kind = None):
		super().removeBody(body, kind)
		if body in self.bodies:
			self.bodies.remove(body)

	def apply(self):
		scroll_size = self.params['scroll_size']
		for b in self.bodies:
			x, y = b.getAttrib('position')
			y += scroll_size
			b.setAttrib('position', (x, y))
