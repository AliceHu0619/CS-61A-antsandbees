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



	def wait_for_click(self, seconds = 0):

		elapsed = 0

		while elapsed < seconds or seconds == 0:
			if self._click_pos is not None:
				pos = self._click_pos
				self._click_pos = None

				return pos, elapsed
			self._sleep(FRAME_TIME)

			elapsed += FRAME_TIME
		return None, elapsed



	def _draw_background(self):
		w, h = self.width - 1, self.height -1
		corners = [(0, 0), (0, h), (w, h), (w,0)]
		self.draw_polygon(corners, self.color, fill_color = self.color, fill = True, smooth = False)


	def _click(self, event):
		self._click_pos = (event.x, event.y)


	def _sleep(self, seconds):
		self._tk.update_idletasks()
		self._tk.after(int(1000 * seconds), self._tk.quit)
		self._tk.mainloop()



	def flatterned(points):
		coords = list()
		[coords.extend(p) for p in points]
		return tuple(coords)


	def paired(coords):
		assert len(coords) % 2 == 0, 'coordinates are not paired'
		points = []
		x = None

		for elem in coords:
			if x is None:
				x = elem
			else:
				points.append((x, elem))
				x = None
		return points



	def translate_point(point, angle, distance):
		x, y = point
		dx, dy = offset
		return (x + dx, y + dy)


	def rectangle_points(pos, width, height):
		x1, y1 = pos 
		x2, y2 = width + x1, height + y1
		return [(x1, y1), (x1, y2), (x2,y2),(x2,y1)]


	def format_color(r, g, b):
		return '#{0:02x}{1:02x}{2:02x}'.format(int(r*255), int(g*255), int(b*255))

	


























