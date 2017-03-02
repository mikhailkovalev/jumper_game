
class AContext:
	@staticmethod
	def getName():
		pass

	def __init__(self):
		self.scale_factor = 1.0
		self.x_offset = 0.0
		self.y_offset = 0.0
		self.pen_color = (0.0, 0.0, 0.0)
		self.brush_color = (1.0, 1.0, 1.0)
		self.background = (0.7, 0.7, 0.7)

	def getSize(self):
		pass

	def setPenColor(self, color):
		self.pen_color = color

	def setBrushColor(self, color):
		self.brush_color = color

	def setBackground(self, color):
		self.background = color

	def drawCircle(self, center_x, center_y, radius, fill = False):
		pass

	def drawLine(self, x1, y1, x2, y2, width = 1):
		pass

	def drawRectangle(self, x1, y1, x2, y2, width = 1):
		pass

	def drawImage(self, x, y, image):
		pass

	def clear(self):
		pass

class TkContext(AContext):
	@staticmethod
	def getName():
		return 'TkContext'

	def __init__(self, canvas):
		super().__init__()
		self.color_convert = lambda c: (int(i * 255 + 0.5) for i in c)
		self.color_temp = '#{:02x}{:02x}{:02x}'
		self.canvas = canvas
		self.setPenColor(self.pen_color)

	def getSize(self):
		w = int(self.canvas['width'])
		h = int(self.canvas['height'])
		return w, h

	def setPenColor(self, color):
		c = self.color_convert(color)
		self.pen_color = self.color_temp.format(*c)

	def setBrushColor(self, color):
		c = self.color_convert(color)
		self.brush_color = self.color_temp.format(*c)

	def setBackground(self, color):
		c = self.color_convert(color)
		self.background = self.color_temp.format(*c)

	def drawCircle(self, center_x, center_y, radius, fill = False):
		args = [center_x - radius, center_y - radius,\
				center_x + radius, center_y + radius]
		for i in range(4):
			args[i] *= self.scale_factor
			if i % 2 == 0:
				args[i] += self.x_offset
			else:
				args[i] += self.y_offset
		color = self.brush_color if fill else ''
		self.canvas.create_oval(args, fill = color, outline = self.pen_color)

	def drawLine(self, x1, y1, x2, y2, width = 1):
		args = [x1, y1, x2, y2]
		for i in range(4):
			args[i] *= self.scale_factor
			if i % 2 == 0:
				args[i] += self.x_offset
			else:
				args[i] += self.y_offset
		self.canvas.create_line(args, fill = self.pen_color, width = width)

	def drawRectangle(self, x1, y1, x2, y2, width = 1):
		args = [x1, y1, x2, y2]
		offset = (self.x_offset, self.y_offset)
		for i in range(4):
			args[i] *= self.scale_factor
			args[i] += offset[i % 2]
		self.canvas.create_rectangle(args, outline = self.pen_color)

	def drawImage(self, x, y, image):
		position = [x, y]
		offset = (self.x_offset, self.y_offset)
		for i in range(2):
			position[i] *= self.scale_factor
			position[i] += offset[i % 2]
		self.canvas.create_image(position, anchor = 'nw', image = image)

	def clear(self):
		self.canvas.delete('all')
