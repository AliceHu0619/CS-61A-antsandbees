import sys
import math


try:
	import tkinter
except Exception as e:
	print('could not load tkinter:' + str(e))


FRAME_TIME = 1/30


class Canvas(object):

	_instance = None

	def __init__(self, width = 1024, height = 768, title = '', color = 'white', tk = None):
		if Canvas._instance is not None:
			raise Exception('only one canvas can be instantiated')
		Canvas._instance = self


		self.color = color
		self.width = width
		self.height = height


		self._tk = tk or tkinter.Tk()
		self._tk.protocol('WM_DELETE_WINDOW', sys.exit)
		self._tk.title(title or 'Graphics Window')
		self._tk.bind('<Button - 1>', self._click)
		self._click_pos = None


		self._canvas = tkinter.Canvas(self._tk, width = width, height = height)
		self._canvas.pack()
		self._draw_background()
		self._canvas.update()
		self._images = dict()



	def clear(self, shape = 'all'):
		self._canvas.delete(shape)
		if shape == 'all':
			self._draw_background()
		self._canvas.update()



	def draw_polygon(self, points, color = 'Black', fill_color = None, filled = 1, smooth = 0, width = 1):

		if fill_color == None:
			fill_color = color 
		if filled == 0:
			fill_color = ""

		return self._canvas.create_polygon(flatterned(points), outline = color, fill = fill_color, smooth = smooth, width = width)




	def draw_circle(self, center, radius, color = 'Black', fill_color = None, filled = 1, width = 1):

		if fill_color == None:
			fill_color = color

		if filled == 0:
			fill_color = ""

		x0, y0 = [c - radius for c in center]
		x1, y1 = [c + radius for c in center]

		return self._canvas.create_oval(x0, y0,x1, y1 outline = color, fill = fill_color,width = width)
		











