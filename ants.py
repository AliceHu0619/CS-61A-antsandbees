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
	implemented  = False
	food_cost = 0
	block_path = True 
	container = False


	def __init__(self, armor = 1):
		Insect.__init__(self, armor)

	def can_contains(self, other):
		return self.container and self.ant is None and not other.container



class HarvestAnt(Ant):
	name = 'Harvester'
	implemented = True 
	food_cost = 2

	def action(self, colony):
		colony.food += 1


class ThrowerAnt(Ant):
	name = 'Thrower'
	implemented = True
	damage = 1
	food_cost = 3
	min_range = 0
	max_range = float('inf')


	def nearest_bee(self, hive):
		place = self.place
		dis = 0

		while place != hive:
			bee = random_or_none(place.bee)
			if bee is not None and self.min_range <= dis <= self.max_range:
				return bee
			place = place.entrance
			dis += 1

		return None



	def throw_at(self, target):
		if target is not None:
			target.reduce_armor(self.damage)


	def action(self, colony):
		self.throw_at(self.nearest_bee(colony.hive))


	def random_or_none(s):
		if s:
			return random.choice(s)



class Water(Place):

	def add_insect(self, insect):
		Place.add_insect(self, insect):
		if not insect.watersafe:
			insect.reduce_armor(insect.armor)


class FireAnt(Ant):
	
	name = 'Fire'
	damage = 3
	food_cost = 5
	implemented = True 


	def reduce_armor(self, amout):

		self.armor -= amount
		if self.armor <= 0:
			bees = self.place.bees[:]
			for bee in bees:
				bee.reduce_armor(self.damage)
			self.place.remove_insect(self)



class LongThrower(ThrowerAnt):
	name = 'Long'
	implemented = True
	min_range = 5
	max_range = float('inf')
	food_cost = 2


class ShortThrower(ThrowerAnt):
	name = 'Short'
	implemented = True 
	min_range = 0
	max_range = 3
	food_cost = 2


class WallAnt(Ant):
	name = 'Wall'
	implemented = True 
	food_cost = 4
	armor = 4

	def __init__(self):
		super().__init__(self.armor)



class NinjaAnt(Ant):
	name = 'Ninja'
	damage = 1
	implemented = True 
	block_path = False
	food_cost = 5
	armor = 1


	def action(self, colony):
		bees = self.place.bees[:]
		for bee in bees:
			bee.reduce_armor(self.damage)



class ScubaThrower(ThrowerAnt):
	name = 'Scuba'
	armor = 1
	food_cost = 6
	watersafe = True




class HungryAnt(Ant):
	name = 'Hungry'
	implemented = True 
	time_to_digest = 3
	food_cost = 4
	armor = 1


	def __init__(self):
		self.digesting = 0

	def eat_bee(self, bee):
		bee.armor = 0
		bee.place.remove_insect(bee)
		self.digesting = self.time_to_digest


	def action(self, colony):
		if self.digesting > 0:
			self.digesting -= 1
			return 

		if len(self.place.bees) > 0:
			bee = random.choice(self.place.bees)
			self.eat_bee(bee)

			


















		



















