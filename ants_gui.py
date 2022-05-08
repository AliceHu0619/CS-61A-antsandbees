import ants
import graphics
from graphics import shift_points
from ucb import *
from math import pi 

import math
import os

import random


STRATEGY_SECONDS = 3

INSECT_FILES={'Worker': 'img/ant_harvester.gif',
     			'Thrower': 'img/ant_thrower.gif',
                'Long': 'img/ant_longthrower.gif',
                'Short': 'img/ant_shortthrower.gif',
                'Harvester': 'img/ant_harvester.gif',
                'Fire': 'img/ant_fire.gif',
                'Bodyguard': 'img/ant_weeds.gif',
                'Hungry': 'img/ant_hungry.gif',
                'Slow': 'img/ant_freeze.gif',
                'Stun': 'img/ant_stun.gif',
                'Ninja': 'img/ant_ninja.gif',
                'Wall': 'img/ant_wall.gif',
                'Scuba': 'img/ant_scuba.gif',
                'Queen': 'img/ant_queen.gif',
                'Remover': 'img/remover.gif',
                'Tank': 'img/ant_weeds.gif',
                'Bee': 'img/bee.gif',
                'Wasp': 'img/wasp.gif',
                'Hornet': 'img/hornet.gif',
                'NinjaBee': 'img/ninjabee.gif',
                'Boss': 'img/boss.gif',
                }


TUNNEL_FILE ='img/tunnel.gif'
ANT_IMAGE_WIDTH = 65
ANT_IMAGE_HEIGHT = 71
BEE_IMAGE_WIDTH = 58
PANEL_PADDING = (2, 4)
PLACE_PADDING = (10, 10)
PLACE_POS = (40, 180)
PANEL_POS = (20, 40)
CRYPT = 650
MESSAGE_POS = (120, 20)
HIVE_HEIGHT = 300
PLACE_MARGIN = 10
LASER_OFFSET = (60, 40)
LEAF_START_OFFSET =(30, 30)
LEAF_END_OFFSET = (50, 30)
LEAF_COLORS = {'Thrower': 'ForestGreen',
               'Short': 'Green',
               'Long': 'DarkGreen',
               'Slow': 'LightBlue',
               'Stun': 'Red',
               'Scuba': 'Blue',
               'Queen': 'Purple',
               'Laser': 'Blue'
	
}



class AntsGUI:

    def __init__(self):
        self.initialized = False


    def initialize_colony_graphics(self, colony):
        self.initialized = True
        self.canvas = graphics.Canvas()
        self.food_text = self.canvas.draw_text('food: 1 time 0', (20,20))
        self.ant_text = self.canvas.draw_text('Ant selected :None', (20, 140))
        self._click_rectangles = list()
        self._init_control_panel(colony)
        self._init_places(colony)


        star_text = self.canvas.draw_text('click to start', MESSAGE_POS)
        self.canvas.wait_for_click()
        self.canvas.clear(star_text)
        




	















