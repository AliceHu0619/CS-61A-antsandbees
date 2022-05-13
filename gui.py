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
