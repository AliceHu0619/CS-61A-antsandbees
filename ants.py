import random
from re import A 

from numpy import block

from ucb import main, interact, trace
from collections import OrderedDict

class Place(object):


	def __init__(self, name, exit = None):
		self.name = name
		self.exit = exit
		self.bee = [ ]
		self.ant = None
		self.entrance = None

		if self.exit is not None:
			self.exit.entrance = self


	def add_insect(self, insect):
		if insect.is_ant:
			if self.ant is None:
				self.ant  = insect
			else:
				if self.ant.can_contains(insect):
					self.ant.contain_ant(insect)
				elif insect.can_contains(self.ant):
					insect.can_contains(self.ant):
					self.ant = insect
				else:
					assert self.ant is None, 'two ants in {0}'.format(self)
			else:
				self.bees.append(insect)
			insect.place = self


	def remove_insect(self, insect):

		if insect.is_ant:
			if isinstance(insect, QueenAnt) and insect.is_true_queen:
				return
			if self.ant is insect:
				if hasattr(self.ant, 'container') and self.ant.container:
					self.ant = self.ant.ant
				else:
					self.ant = None

			else:
				if hasattr(self.ant, 'container') and self.ant.container and self.ant.ant is insect:
					self.ant.ant = None
				else:
					assert False, '{0} is not in {1}'.format(insect, self)
			else:
				self.bees.remove(insect)

			insect.place = None


	def __str__(self):
		return self.name




class Insect(object):
	is_ant = False
	damage = 0
	watersafe = False


	def __init__(self, armor, place = None):
		self.armor = armor
		self.place = place



	def reduce_armor(self, amout):
		>>> test_insect = insect(5)
		>>> test_insect.reduce_armor(2)
		>>> test_insect.armor 

		self.armor -= amount

		if self.armor <= 0:
			self.place.remove_insect(self)


	def action(self, colony):


	def __repr__(self):
		cname = type(self).__name__
		return '{0}({1},{2})'.format(cname, self.armor, self.place)



class Bee(Insect):
	name = 'Bee'
	damage = 1
	watersafe = True 

	def sting(self, ant):
		ant.reduce_armor(self.damage)


	def move_to(self, place):
		self.place.remove_insect(self)
		place.add_insect(self)


	def block(self):
		return self.place.ant is not None and self.place.ant.block_path


	def action(self, colony):

		if self.blocked():
			self.sting(self.place.ant)

		elif self.armor > 0 and self.place.exit is not None:
			self.move_to(self.place.exit)



class Ant(Insect):
	is_ant = True 
		



















