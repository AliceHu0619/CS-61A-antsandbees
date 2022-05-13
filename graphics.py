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







	def draw_line(self, start, end, color = 'Blue', width = 1):
		x0, y0 = start
		x1, y1 = end

		return self._canvas.create_line(x0, y0, x1, y1. fill = color, width = width)




	def draw_image(self, pos, image_file = None, scale = 1, anchor = tkinter.NW, behind = 0):

		key = (image_file, scale)

		if key not in self._images:
			image = tkinter.PhotoImage(file = image_file)
			if scale >= 1:
				image = image.zoom(int(scale))

			else:
				image = image.subsample(int(1/scale))

			self._images[key] = image



		image = self._images[key]

		x,y = pos 

		id = self._canvas.create_image(x, y, image = image, anchor = anchor)

		if behind > 0:
			self._canvas.tag_lower(id, behind)


		return id 



	def draw_text(self, text, pos, color = 'Black', font = 'Arial', size =12, style = 'normal', anchor = tkinter.NW):

		if color is not None:
			self._canvas.itemconfigure(id, fill = color)

		if text is not None:
			self._canvas.itemconfigure(id, text = text)

		if font is not None:
			self._canvas.itemconfigure(id, font = (font, str(size),style))



	def animate_shape(self, id, duration, points_fn, frame_count = 0):
		max_frame = duration//FRAME_TIME
		points = points_fn(frame_count)

		self._canvas.coords(id, flatterned(points))

		if frame_count < max_frame:
			def tail():

				self.animate_shape(id, duration, points_fn, frame_count + 1)

			self._tk.after(int(FRAME_TIME * 1000), tail)



	def slide_shape(self, id, end_pos, duration, elapsed = 0):
		points = paired(self._canvas.coords(id))

		start_pos = points[0]
		max_frame = duration //FRAME_TIME

		def points_fn(frame_count):
			completed = frame_count / max_frame
			offset = [(e-s) * completed for s, e in zip(start_pos, end_pos)]
			return [shift_point(p, offset) for p in points]

		self.animate_shape(id, duration, points_fn)





















