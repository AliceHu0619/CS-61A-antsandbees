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


    def _init_control_panel(self, colony):
        self.ant_type_selected = None
        self.ant_type_frame = []
        panel_pos = PANEL_POS

        for name, ant_type in colony.ant_type.items():
            width = ANT_IMAGE_WIDTH + 2 * PANEL_PADDING[0]
            height = ANT_IMAGE_HEIGHT + 6 + 2 * PANEL_PADDING[1]

            def on_click(colony, frame, name = name):
                self.ant_type_frame = name 
                self._update_control_panel(colony)


            frame = self.add_click_rect(panel_pos, width, height, on_click)
            self.ant_type_frame.append((name, frame))
            img_pos = shift_points(panel_pos, PANEL_PADDING)
            self.canvas.draw_image(img_pos, INSECT_FILES[name])
            cost_pos = shift_points(panel_pos, (width/2, ANT_IMAGE_HEIGHT + 4 + PANEL_PADDING[1]))
            food_str = str(ant_type.food_cost)
            self.canvas.draw_image(food_str, cost_pos, anchor = "center")
            panel_pos = shift_points(panel_pos, (width + 2, 0))


    def _init_places(self, colony):

        self.place_points = dict()
        self.image = {'AntQueen': dict()}
        place_pos = PANEL_POS
        width = BEE_IMAGE_WIDTH + 2 * PANEL_PADDING[0]
        height = ANT_IMAGE_HEIGHT + 2* PANEL_PADDING[1]
        rows = 0

        for name, place in colony.places.items():
            if place.name == 'Hive':
                continue
            if place.exit.name == 'AntQueen':
                row_offset = (0, rows *(height + PLACE_MARGIN))
                place_pos = shift_points(PLACE_POS, row_offset)
                rows += 1

            def on_click(colony, frame, name = name):
                ant_type = self.ant_type_selected
                existing_ant = colony.places[name].ant

                if ant_type is 'Remover':
                    if existing_ant is not None:
                        print('colony.remove_ant('{0}')'.format(name))
                        colony.remove_ant(name)
                        self._update_places(colony)
                elif ant_type is not None:
                    try:
                        print('colony.deploy_ant('{0}','{1}')')









	















