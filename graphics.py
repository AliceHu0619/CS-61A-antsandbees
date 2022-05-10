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
		
