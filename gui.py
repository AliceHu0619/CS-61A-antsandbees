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
		




















