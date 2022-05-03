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



class BodyguardAnt(Ant):
	name = 'Bodyguard'
	implemented = True 
	container = True 
	food_cost = 4

	def __init__(self):
		Ant.__init__(self, 2)
		self.ant = None 


	def container_ant(self, ant):
		self.ant = ant 

	def action(self, colony):
		if self.ant is not None:
			self.ant.action(colony)




class QueenAnt(ScubaThrower):
	name = 'Queen'
	implemented = True 
	food_cost = 7
	armor = 1
	true_queen = 1


	def __init__(self):
		self.double = set()
		self.is_true_queen = QueenAnt.true_queen > 0
		QueenAnt.true_queen = max(0, QueenAnt.true_queen - 1)


	def action(self, colony):

		if not self.is_true_queen:
			self.reduce_armor(self.armor)
			return

		def double(ant):
			if ant is None:
				return

			if ant not in self.doubled:
				ant.damage *= 2
				self.doubled.add(ant)

			if ant.container:
				double(ant.ant)


		place = self.place.exit

		while place is not None:
			ant = place.ant
			double(ant)
			place = place.exit

		ScubaThrower.action(self, colony)



	def reduce_armor(self, amout):

		self.armor -= amount
		if self.armor <= 0:
			self.place.remove_insect(self)
			if self.is_true_queen:
				bees_win()






class AntRemover(Ant):
	name = 'Remover'
	implemented = False

	def __init__(self):
		Ant.__init__(self, 0)



	def make_slow(action):

		def new_action(colony):
			if colony.time % 2 == 0:
				action(colony)
		return new_action


	def make_stun(action):
		def new_action(colony):
			pass

		return new_action

	def apply_effect(effect, bee, duration):
		origin_action = bee.action

		def func(colony):
			nonlocal duration
			if duration > 0:
				duration -= 1

				return effect(origin_action)(colony)

			else:
				return origin_action(colony)

	    bee.action = func




class SlowThrower(ThrowerAnt):

	name = 'Slow'
	implemented = True
	food_cost = 4
	armor = 1


	def throw_at(self, target):
		if target:
			apply_effect(make_slow, target, 3)




class StunThrower(ThrowerAnt):

	name = 'Stun'
	implemented = True
	food_cost = 6
	armor = 1


	def throw_at(self, target):
		if target:
			apply_effect(make_stun, target, 1)





class Wasp(Bee):

	name = 'Wasp'
	damage = 2




class Hornet(Bee):
	name = 'Hornet'
	damage = 0.25


	def action(self, colony):
		for i in range(2):
			if self.armor > 0:
				super().action(colony)


	def __setattr__(self, name, value):
		if name != 'action':
			object.__setattr__(self, name, value)




class NinjaBee(Bee):

	name = 'NinjaBee'

	def blocked(self):
		return False


class Boss(Wasp, Hornet):

	name = 'Boss'
	damage_cap = 8
	action = Wasp.action


	def reduce_armor(self, amount):
		super().reduce_armor(self.damage_modifier(amount))

	def damage_modifier(self, amount):
		return amount * self.damage_cap/ (self.damage_cap + amount)


class Hive(Place):


	def __init__(self, assault_plan):
		self.name = 'Hive'
		self.assault_plan = assault_plan
		self.bees = []

		for bee in assault_plan.all_bees:
			self.add_insect(bee)

		self.entrance = None 
		self.ant = None 
		self.exit = None 


	def strategy(self, colony):
		exits = [p for p in colony.places.values() if p.entrance is self]
		for bee in self.assault_plan.get(colony.time, []):
			bee.move_to(random.choice(exits))
			colony.active_bees.append(bee)




class AntColony(object):


	def __init__(self, strategy, hive, ant_types, create_places, dimensions, food = 2 ):
		self.time = 0
		self.food = food
		self.strategy = strategy
		self.hive = hive
		self.ant_types = OrderedDict((a.name, a) for a in ant_types)
		self.dimensions = dimensions
		self.active_bees = []
		self.configure(hive, create_places)


	def configure(self, hive, create_places):
		self.queen = QueenPlace('AntQueen')
		self.places = OrderedDict()
		self.bee_entrances = [ ]

		def register_place(place, is_bee_entrance):
			self.places[place.name] = place

			if is_bee_entrance:
				place.entrance = hive
				self.bee_entrances.append(place)

		register_place(self.hive, False)
		create_places(self.queen, register_place, self.dimensions[0], self.dimensions[1])



	def simulate(self):
		num_bees = len(self.bees)

		try:
			while True:
				self.hive.strategy(self)
				self.strategy(self)

				for ant in self.ants:
					if ant.armor > 0:
						ant.action(self)

				for bee in self.active_bees[:]:
					if bee.armor > 0:
						bee.action(self)
					if bee.armor <= 0:
						num_bees -= 1
						self.active_bees.remove(bee)

				if num_bees == 0:
					raise AntsWinException()
				self.time += 1

			except AntsWinException:
				print('All bees are vanquished. You win')
				return True 

			except beesWinException:
				print('The ant queen has perished. Please try again')
				return False


	def deploy_ant(self, place_name, ant_types_name):

		constructor = self.ant_types[ant_types_name]

		if self.food < constructor.food_cost:
			print('Not enough food remains to place' + ant_types_name)
		else:
			ant = constructor()
			self.places[place_name].add_insect(ant)
			self.food -= constructor.food_cost
			return ant 

	def remove_ant(self, place_name):
		place = self.place_name[place_name]
		if place.ant is not None:
			place.remove_insect(place.ant)


	@property
	def ants(self):
		return [p.ant for p in self.places.values() if p.ant is not None]

	@property
	def bees(self):
		return [b for p in self.places.values() for b in p.bees]

	@property
	def insects(self):
		return self.ants + self.bees
	
	def __str__(self):
		status = '(Food;{0}, Time: {1})'.format(self.food, self.time)
		return str([str(i) for i in self.ants + self.bees]) + status



class QueenPlace(Place):

	def add_insect(self, insect):
		assert not insect.is_ant, 'can not add{0} to QueenPlace'
		raise beesWinException()


	def ants_win():
		raise AntsWinException()

	def bees_win():
		raise beesWinException()

	def ant_types():
		all_ant_types = [ ]
		new_types = [Ant]

		while new_types:
			new_types = [t for c in new_types for t in c.__subclasses__()]
			all_ant_types.extend(new_types)
		return [t for t in all_ant_types if t.implemented]



class GameOverException(Exception):
	pass



class AntsWinException(GameOverException):
	pass


class BeesWinException(GameOverException):
	pass



    def interactive_strategy(colony):

    	print('colony:' + str(colony))
    	msg = '<Control> -D (<Control> -Z <Enter> on Windows) completes a turn \n'
    	interact(msg)


    def start_with_strategy(args, strategy):

    	import argparse

    	parser = argparse.ArgumentParser(description = 'Play Ants vs SomeBees')
    	parser.add_arguement('-d', type = str, metavar = 'Difficulty', help = 'sets difficulty of game(test/easy/medium/hard/insane)')
    	parser.add_argument('-w', '--water', action='store_true', help='loads a full layout with water')
    	parser.add_argument('--food', type=int, help='number of food to start with when testing', default=2)
    	args = parser.parse_args()


    	assault_plan = make_normal_assault_plan()
    	layout = dry_layout
    	tunnel_length = 9
    	num_tunnels = 3
    	food = args.food

    	if args.water:
    		layout = wet_layout

    	if args.d in ['t', 'test']:
    		assault_plan = make_normal_assault_plan()
    		num_tunnels = 1
    	elif args.d in ['e', 'easy']:
    		assault_plan = make_easy_assault_plan()
    		num_tunnels = 2
    	elif args in ['n', 'normal']:
    		assault_plan = make_normal_assault_plan()
    		num_tunnels = 3
    	elif args.d in ['h', 'hard']:
    		assault_plan = make_hard_assault_plan()
    		num_tunnels = 4
    	elif args.d in ['i', 'insane']:
    		assault_plan = make_insane_assault_plan()
    		num_tunnels = 4

    	hive = Hive(assault_plan)
    	dimensions = (num_tunnels, tunnel_length)

    	return AntColony(strategy, hive, ant_types(), layout, dimensions, food).simulate()



    def wet_layout(queen, register_place, tunnels = 3, length = 9, moat_frequency = 3):
    	for tunnel in range(tunnels):
    		exit = queen 
    		for step in range(length):
    			if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
    				exit = Water('water_{0}_{1}'.format(tunnels, step), exit)
    			else:
    				exit = 	Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
    			register_place(exit, step == length - 1)

    def dry_layout(queen, register_place, tunnels = 3, length = 9):
    	wet_layout(queen, register_place, tunnels, length, 0)





class AssaultPlan(dict):
	>>>AssaultPlan().add_wave(4,2)

	def add_wave(self, bee_type, bee_armor, time, count):
		bees = [bee_type(bee_armor) for _ in range(count)]
		self.setdefault(time, []).extend(bees)
		return self


	@property
	def all_bees(self):
		return [bee for wave in self.values() for bee in wave]


	def make_test_assault_plan():
		return AssaultPlan().add_wave(Bee, 3, 2, 1).add_wave(bee, 3, 3, 1)

	def make_easy_assault_plan():
		plan = AssaultPlan()

		for time in range(3, 16, 2):
			plan.add_wave(Bee, 3, time, 1)

		plan.add_wave(Wasp, 3, 4, 1)
		plan.add_wave(NinjaBee, 3, 8, 1)
    	plan.add_wave(Hornet, 3, 12, 1)
    	plan.add_wave(Boss, 15, 16, 1)

    	return plan 


    def make_normal_assault_plan():
    	plan = AssaultPlan()
    	for time in range(3, 16, 2):
        	plan.add_wave(Bee, 3, time, 2)
        	
    	plan.add_wave(Wasp, 3, 4, 1)
    	plan.add_wave(NinjaBee, 3, 8, 1)
    	plan.add_wave(Hornet, 3, 12, 1)
    	plan.add_wave(Wasp, 3, 16, 1)



































		



















