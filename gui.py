import ants
import utils
import state
import json
import distutils.core
import urllib.request
import os
import shutil
import zipfile
import threading
import importlib
from time import sleep
from ucb import *



VERSION = 1.2
ASSET_DIR = "assets/"
INSECT_DIR = 'insects/'
STRATEGY_SECONDS = 3
INSECT_FILES ={ 'Worker': ASSETS_DIR + INSECT_DIR +  "ant_harvester.gif",
       'Thrower': ASSETS_DIR + INSECT_DIR +  "ant_thrower.gif",
       'Long': ASSETS_DIR + INSECT_DIR +  "ant_longthrower.gif",
       'Short': ASSETS_DIR + INSECT_DIR +  "ant_shortthrower.gif",
       'Harvester': ASSETS_DIR + INSECT_DIR +  "ant_harvester.gif",
       'Fire': ASSETS_DIR + INSECT_DIR +  "ant_fire.gif",
       'Bodyguard': ASSETS_DIR + INSECT_DIR +  "ant_bodyguard.gif",
       'Hungry': ASSETS_DIR + INSECT_DIR +  "ant_hungry.gif",
       'Slow': ASSETS_DIR + INSECT_DIR +  "ant_slow.gif",
       'Stun': ASSETS_DIR + INSECT_DIR +  "ant_stun.gif",
       'Ninja': ASSETS_DIR + INSECT_DIR +  "ant_ninja.gif",
       'Wall': ASSETS_DIR + INSECT_DIR +  "ant_wall.gif",
       'Scuba': ASSETS_DIR + INSECT_DIR +  "ant_scuba.gif",
       'Queen': ASSETS_DIR + INSECT_DIR +  "ant_queen.gif",
       'Tank': ASSETS_DIR + INSECT_DIR + "ant_tank.gif",
       'Bee': ASSETS_DIR + INSECT_DIR +  "bee.gif",
       'Remover': ASSETS_DIR + INSECT_DIR + "remove.png",
	
}


class GUI:


	def __init__(self):
		self.active = True
		self.cleanState()


	def cleanState(self):
		self.initialized = False
		self.state = state.State()
		self.gameOver = False
		self.colony = None
		self.currentBeeId = 0
		self.currentInsectId = 0
		self.insects = []
		self.bees = []
		self.deadbees = []
		self.deadinsects = []
		self.insectToId  = {}
		self.beeToId = {}
		self.beelocations = {}




	def makeHooks(self):
		ants.Insect.reduce_armor = utils.class_method_wrapper(ants.Insect.reduce_armor, post = dead_insects)
		ants.AntColony.remove_ant = utils.class_method_wrapper(ants.AntColony.remove_ant, post = remove_ant)



	def newGameThread(self):
		print('Trying to start new game')
		self.cleanState()
		importlib.reload(ants)
		self.makeHooks()

		self.winner = ants.start_with_strategy(gui.args, gui.strategy)
		self.gameOver = True
		self.saveState('winner', self.winner)
		self.saveState('gameOver', self.gameOver)


		update()


	def killGUI(self):
		self.active = False


	def startGame(self, data = None):
		threading.Thread(target = self.newGameThread).start()
		print('game started')


	def exit(self, data = None):
		self.active = False


	def initialize_colony_graphics(self, colony):
		self.colony = colony 
		self.ant_type_selected = -1
		self.saveState('strategyTime', STRATEGY_SECONDS)
		self.saveState('food', self.colony.food)
		self.ant_types = self.get_ant_types()
		self.__init_places(colony)
		self.saveState('places', self.places)
		self.initialized = True


	def get_ant_types(self, noSave = False):
		ant_types = []

		for name, ant_types in self.colony.ant_types.items():
			ant_types.append({'name': name, "cost": ant_type.food_cost, 'img':self.get_insect_img_file(name)})



		ant_types.sort(key = lambda item: item['cost'])

		if not noSave:
			self.saveState("ant_types", ant_types)
		return ant_types


	def saveState(self, key, val):
		self.state.updateState(key, val)



	def strategy(self, colony):
		if not self.initialized:
			self.initialize_colony_graphics(colony)

		elaspsed = 0

		self.saveState('time', int(elaspsed))

		while elaspsed < STRATEGY_SECONDS:
			self.saveState('time', colony.time)
			self._update_control_panel(colony)
			sleep(0.25)
			elaspsed += 0.25




	def get_place_row(self, name):
		return name.split('_')[1]

	def get_place_column(self, name):
		return name.split('_')[2]


	def _init_places(self, colony):
		self.places = {}
		self.images = {'AntQueen': dict()}
		rows = 0
		cols = 0

		for name, places in colony.places.items():
			if place.name == "HIVE":
				continue


			pCol = self.get_place_column(name)
			pRow = self.get_place_row(name)

			if place.exit.name == 'AntQueen':
				rows += 1
			if not pRow in self.places:
				self.places[pRow] = {}

			self.places[pRow][pCol] = {'name':name, "type": "tunnel", "water": 0, "insects":{}}

			if "water" in name:
				self.places[pRow][pCol]['water'] = 1

			self.images[name] = dict()

		self.places[colony.hive.name] = {"name": name, "type": "hive", "water":0, "insects":{}}

		self.places[colony.hive.name]["insects"] = []

		for bee in colony.hive.bees:
			self.places[colony.hive.name]["insects"].append({"id": self.currentBeeId, "type":"bee"})

			self.beeToId[bee] = self.currentBeeId
			self.currentBeeId += 1

		self.saveState("rows", rows)
		self.saveState("places", self.places)



	def update_food(self):
		self.saveState('food', self.colony.food)


	def _update_control_panel(self, colony):
		self.update_food()

		old_insects = self.insects[:]
		old_bees = self.bees[:]
		self.bees, self.insects = [], []

		for name, place in colony.places.items():
			if place.name == 'HIVE':
				continue

			pCol = self.get_place_column(name)
			pRow = self.get_place_row(name)


			if place.ant is not None:
				if self.insectToId[place.ant] not in self.insects:
					self.insects.append(self.insectToId[place.ant])

				self.places[pRow][pCol]["insects"] ={ "id":self.insectToId[place.ant], "type": place.ant.name, "img":self.get_insect_img_file(place.ant.name)}


			if hasattr(place.ant, "container"):
				self.places[pRow][pCol]["insects"]["container"] = place.ant.container

				if place.ant.container and places.ant.ant:
					self.places[pRow][pCol]["insects"]["container"] = {"type":place.ant.ant.name, "img": self.get_insect_img_file(place.ant.ant.name)}
			else:
				self.places[pRow][pCol]["insects"] = {}


			for bee in places.bees:
				self.beelocations[self.beeToId[bee]] = name
				if self.beeToId[bee] not in self.bees:
					self.bees.append(self.beeToId[bee])

		self.saveState("beelocations", self.beelocations)




















