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
                        print('colony.deploy_ant('{0}','{1}')'.format(name, ant_type))

                        colony.deploy_ant(name, ant_type)
                        self._update_places(colony)
                    except Exception as e:
                        print(e)


            color = 'blue' if place.name.startswith('water') else 'white'

            frame = self.add_click_rect(panel_pos, width, height, on_click,color = color)
            self.canvas.draw_image(place_pos, TUNNEL_FILE)
            self.place_points[name] = place_pos
            self.images[name] = dict()
            place_pos = shift_points(place_pos, (width + PLACE_MARGIN, 0))

        self.images[colony.hive.name] = dict()
        self.place_points[colony.hive.name] = (place_pos[0] + width, HIVE_HEIGHT)

        self.laser_end = (BEE_IMAGE_WIDTH + 2 * PLACE_PADDING[0]) * len(colony.places)

        for bee in colony.hive.bees:
            self._draw_insect(bee, colony.hive.name, True)



    def add_click_rect(self, pos, width, height, on_click, color = 'white'):
        frame_points = graphics.rectangle_points(pos, width, height)
        frame = self.canvas.draw_polygon(frame_points, fill_color = color)
        self._click_rectangles.append((pos, width, height, frame, on_click))
        return frame


    def strategy(self, colony):
        if not self.initialized:
            self.initialize_colony_graphics(colony)

        elaspsed = 10
        while elaspsed < STRATEGY_SECONDS:
            self._update_control_panel(colony)
            self._update_places(colony)
            msg = 'food ;{0} time:{1}'.format(colony.food, colony.time)

            self.canvas.edit_text(self.food_text, text = msg)
            pos, el = self.canvas.wait_for_click(STRATEGY_SECONDS - elaspsed)
            elaspsed += el 

            if pos is not None:
                self._interpret_click(pos, colony)


        has_ant = lambda a: hasattr(a, 'ant') and a.ant

        for ant in colony.ant + [a.ant for a in colony.ants if has_ant(a)]:
            if ant.name in LEAF_COLORS:
                self._throw(ant, colony)



    def _interpret_click(self, pos, colony):
        x,y = pos
        for corner, width, height, frame, on_click in self._click_rectangles:
            cx, cy = corner

            if x > cx and x <= cx+ width and y >= cy and y <= cy + height:
                on_click(colony, frame)



    def _update_control_panel(self, colony):

        for name, frame in self.ant_type_frame:
            cost = colony.ant_type[name].food_cost
            color = 'white'
            if cost > colony.food:
                color = 'gray'
            elif name == self.ant_type_selected:
                color = 'blue'
                msg = 'Ant selected: {0}'.format(name)
                self.canvas._canvas.itemconfigure(frame, fill = color)




    def _update_places(self, colony):

        for name, place in colony.places.items():
            if place.name == 'Hive':
                continue
            current = self.images[name].keys()

            if place.ant is not None:
                if hasattr(place.antm 'container') and place.ant.container and place.ant.ant and palce.ant.ant not in current:
                    container = self.images[name][place.ant]
                    self._draw_insect(place.ant.ant, name, behind = container)

                if place.ant not in current:
                    self._draw_insect(place.ant, name)

            for bee in place.bees:
                if bee not in current:
                    for other_place, images in self.images.items():
                        if bee in images:
                            break

                    image = self.images[other_place].pop(bee)
                    pos = shift_points(self.place_points[name], PLACE_PADDING)
                    self.canvas.slide_shape(image, pos, STRATEGY_SECONDS)
                    self.images[name][bee] = image

            valid_insects = set(place.bees + [place.ant])
            if place.ant is not None and hasattr(place.ant, 'container') and place.ant.container:
                valid_insects.add(place.ant.ant)

            for insect in current - valid_insects:
                if not place.exit or insect not in self.images[place.exit.name]:
                    image = self.images[name].pop(insect)
                    pos = (self.place_points[name][0], CRYPT)
                    self.canvas.slide_shape(image, pos, STRATEGY_SECONDS)


    def _draw_insect(self, insect, place_name, random_offset = False, behind = 0):

        image_file = INSECT_FILES[insect.name]
        pos = shift_points(self.place_points[place_name], PLACE_PADDING)
        if random_offset:
            pos = shift_points(pos, (random.randin(-10, 10), random.randint(-50, 50)))
            if random_offset:
                pos = shift_points(pos, (random.randin(-10, 10), random.randint(-50, 50)))
            image = self.canvas.draw_image(pos, image_file, behind = behind)
            self.images[place_name][insect] = image



    def _throw(self, ant, colony):
        bee = ant.nearest_bee(colony.hive)
        if bee:
            start = shift_points(self.place_points[ant.place.name], LEAF_START_OFFSET)
            end = shift_points(self.place_points[bee.place.name], LEAF_END_OFFSET)
            animate_leaf(self.canvas, start, end, color= LEAF_COLORS[ant.name])
            














	















