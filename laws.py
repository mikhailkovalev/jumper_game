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
	"""
		Класс отвечает за движение дудлера
		и за его взаимодействие с платформами
	"""
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

	@staticmethod
	def getInteractionMoment(a, b, c, span):
		"""
			Возвращает наименьший корень уравнения
			ax^2 + bx + c = 0
			принадлежащий отрезку от span[0]
			до span[1] или None, если таковой
			отсутствует
		"""
		if np.fabs(a) < 1e-6:
			if np.fabs(b) < 1e-6:
				if np.fabs(c) < 1e-6:
					return span[0]
				return None
			x = -c / b
			if span[0] <= x and x <= span[1]:
				return x
			return None

		d = b * b - 4 * a * c
		if d < 0:
			return None

		d = np.sqrt(d)
		x1 = (-b - d) / (2 * a)
		x2 = (-b + d) / (2 * a)
		if x2 < span[0] or x1 > span[1] or
			x1 < span[0] and x2 > span[1]:
			return None
		if x1 < span[0]:
			return x2
		return x1

	@staticmethod
	def intersectSegments(x1, x2, x3, x4):
		if x1 > x3:
			x1, x3 = x3, x1
			x2, x4 = x4, x2
		if x2 < x3:
			return False
		return True

	def apply(self):
		"""
			Вытаскиваем обрабатываемый временной
			промежуток - time_span.

			Изначально объект особой платформы
			равен None, а tau = time_span.

			Для каждой платформы находим момент
			времени, когда её верхняя
			y-координата поравняется с нижней
			y-координатой дудлера. Если этот
			момент лежит за пределами промежутка
			[0, tau], то игнорируем эту платформу
			и переходим к следующей.

			Иначе - смотрим, пересекаются ли
			отрезки верхней границы платформы и
			нижней границы дудлера в найденный
			момент времени. Если да - то делаем
			текущую платформу особой, а момент
			взаимодействия с ней записываем в tau.
		"""
		time_span = self.params['time_span']

		jx, jy = self.jumper.getAttrib('position')
		jvx, jvy = self.jumper.getAttrib('velocity')
		jax, jay = self.jumper.getAttrib('acceleration')
		jxf = self.jumper.getAttrib('horizontal_velocity_factor')

		# Если дудлер движется вверх, то он никак не
		# взаимодействует с платформами
		if jvy < 0:
			jx += jvx * time_span
			jy += jvy * time_span
			jvx += jax * time_span
			jvy += jay * time_span
			if np.fabs(jvx) > self.epsilon:
				jvx *= jxf;
			self.jumper.setAttrib('position', (jx, jy))
			self.jumper.setAttrib('velocity', (jvx, jvy))
			return

		# Особая платформа - платформа, с
		# которой произойдёт столкновение
		# дудлера в момент времени tau
		#
		# Помимо этого, tau используется
		# для отсеивания платформ, "встреча"
		# с которыми произойдёт слишком поздно
		# поэтому изначально оно равно time_span
		tau = time_span
		special_platform = None

		jsx, jsy = self.jumper.getAttrib('size')

		# чтобы постоянно не половинить ускорение
		# для вычисления коэффициента уравнения
		half_jay = 0.5 * jay

		# начальная y-координата нижней границы дудлера
		jby = jy + jsy

		for platform in self.platforms:
			px, py = platform.getAttrib('position')
			pvx, pvy = platform.getAttrib('velocity')

			# находим момент времени, когда y-координата
			# платформы поравняется с нижней координатой
			# дудлера
			t = self.getInteractionMoment(half_jay, jvy - pvy, jby - py, (0, tau))
			if t:
				psx, psy = platform.getAttrib('size')
				njx = jx + t * jvx + 0.5 * jax * t * t
				npx = px + t * pvx
				if self.intersectSegments(njx, njx + jsx, npx, npx + psx):
					tau = t
					special_platform = platform
		if special_platform:
			# Если значение special_platform не
			# None, то значит произошло столкновение
			# в момент времени tau.
			# В этот момент времени координата дудлера
			# по y будет равна
			njy = -jsy + py + tau*pvy

			# Время, которое осталось для движения вверх:
			up_moving_time = time_span - tau
			# Установить в качестве скорости начальную вертикальную для дудлера
			# jvy =
			njy += up_moving_time * (jvy + half_jay*up_moving_time)
		else:
			njy =

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
