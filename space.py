#!/usr/bin/python

from random import choice
from random import randint

import abc
import math
import os
import libtcodpy as libtcod

# LIBTCOD SETUP

LIMIT_FPS = 30
SCREEN_WIDTH = 50
SCREEN_HEIGHT = 30

FONT_WIDTH = 10
FONT_HEIGHT = 10

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, b'space', False)

libtcod.sys_set_fps(LIMIT_FPS)

# GAME SETUP

# handles game events
class Eventer(object):
	def __init__(self):
		self.events = {}

	def fire(self, event, *data):
		if event in self.events:
			listeners = self.events[event]
			for callback in listeners:
				callback(data)

	def listen(self, func, event):
		if event in self.events:
			self.events[event].append(func)
		else:
			self.events[event] = [func]

	def unlisten(self, func, event):
		if event in self.events:
			listeners = self.events[event]
			if func in listeners:
				listeners.remove(func)

# a creature's presence in the world
class Body(object):
	directions = ['right', 'up', 'left', 'down']

	def __init__(self, x, y, rot):
		self.x = x
		self.y = y
		self.rot = rot
		self.px = " "

		self.events = Eventer()

class Renderer(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def render(self, cons):
		pass

class BodyRenderer(Renderer):
	def __init__(self, bodies):
		self.bodies = bodies

	def render(self, cons):
		libtcod.console_set_default_background(cons, libtcod.black)
		for body in self.bodies:
			libtcod.console_print_ex(cons, body.x, body.y, libtcod.BKGND_SET, libtcod.LEFT, body.px)

class RoomRenderer(Renderer):
	def __init__(self, room):
		self.room = room

	def render(self, cons):
		libtcod.console_set_default_background(cons, libtcod.red)
		
		for y in range(0, SCREEN_HEIGHT):
			for x in range(0, SCREEN_WIDTH):
				t = self.room.get(x, y)
				if t:
					libtcod.console_print_ex(cons, x, y, libtcod.BKGND_SET, libtcod.LEFT, t)

class Player(Body):
	def __init__(self, x, y, rot):
		super(Player, self).__init__(x, y, rot)
		self.px = "P"

		event_sys.listen(self.control, 'keypress')

	def control(self, keys):
		if keys[0] == libtcod.KEY_RIGHT:
			self.events.fire('move', self, (self.x+1, self.y))
		elif keys[0] == libtcod.KEY_UP:
			self.events.fire('move', self, (self.x, self.y-1))
		elif keys[0] == libtcod.KEY_LEFT:
			self.events.fire('move', self, (self.x-1, self.y))
		elif keys[0] == libtcod.KEY_DOWN:
			self.events.fire('move', self, (self.x, self.y+1))

# basically just a 2D hashmap
class Room(object):
	def __init__(self):
		self.tiles = {}

	def set(self, x, y, obj):
		self.tiles[(x, y)] = obj

	def get(self, x, y):
		if (x, y) in self.tiles:
			return self.tiles[(x, y)]
		else:
			return None

	def clear(self, x, y):
		del self.tiles[(x, y)]
	
	def width(self):
		xmax, y_of_xmax = max(self.tiles, key = lambda x, y: x)
		return xmax

	def height(self):
		x_of_ymax, ymax = max(self.tiles, key = lambda x, y: y)
		return ymax

	def size(self):
		return (self.width(), self.height())

# knows about physics 'n' stuff
class World(object):
	def __init__(self):
		self.rooms = [Room()]
		self.current_room = self.rooms[0]
		self.bodies = []

		# create a test room
		for y in range(0, 100):
			for x in range(0, 100):
				self.current_room.set(x, y, choice(['X', ' ', ' ']))

	def add_body(self, body):
		self.bodies.append(body)
		body.events.listen(self.move_me, 'move')

	# check whether a given position is solid
	def solid(self, x, y):
		nonsolid = [' ']

		t = self.current_room.get(x, y)

		if t == None:
			return False
		elif t in nonsolid:
			return False
		else:
			return True

	def move_me(self, data):
		body, path = data

		if type(path) == tuple:
			x, y = path
			if not self.solid(x, y):
				body.x = x
				body.y = y
		elif type(path) == List:
			pass

event_sys = Eventer()
world = World()
bodies = [Player(10, 10, 'up')]

for b in bodies:
	world.add_body(b)

renderers = [RoomRenderer(world.rooms[0]), BodyRenderer(bodies)]

# render stats
def stats():
	libtcod.console_set_default_foreground(None, libtcod.grey)
	
	libtcod.console_print_ex (
		None, 79, 46, libtcod.BKGND_NONE, libtcod.RIGHT,
		'last frame : %3d ms (%3d fps)' %
		(
			int(libtcod.sys_get_last_frame_length() * 1000.0),
			libtcod.sys_get_fps()
		)
	)
	
	libtcod.console_print_ex (
		None, 79, 47, libtcod.BKGND_NONE, libtcod.RIGHT,
		'elapsed : %8d ms %4.2fs' %
		(
			libtcod.sys_elapsed_milli(),
			libtcod.sys_elapsed_seconds()
		)
	)

key = libtcod.Key()
mouse = libtcod.Mouse()
while not libtcod.console_is_window_closed():
	libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)

	# UPDATE

	# RENDER
	libtcod.console_clear(None)

	libtcod.console_set_default_foreground(None, libtcod.white)

	for r in renderers:
		r.render(None)

	# draw the mouse cursor
	libtcod.console_set_char_background(None, mouse.x/FONT_WIDTH, mouse.y/FONT_HEIGHT, libtcod.green, flag=libtcod.BKGND_SET)
	
	stats()
	
	# mouse handler
	if mouse.lbutton_pressed:
		x = mouse.x/FONT_WIDTH
		y = mouse.y/FONT_HEIGHT
	
	if mouse.rbutton_pressed:
		x = mouse.x/FONT_WIDTH
		y = mouse.y/FONT_HEIGHT
	
	# key handler
	event_sys.fire('keypress', key.vk)

	if key.vk == libtcod.KEY_ENTER and key.lalt:
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
	elif key.vk == libtcod.KEY_PRINTSCREEN or key.c == 'p':
		print ("screenshot")
		if key.lalt :
			libtcod.console_save_apf(None,"samples.apf")
			print ("apf")
		else :
			libtcod.sys_save_screenshot()
			print ("png")
	elif key.vk == libtcod.KEY_ESCAPE:
		break
	elif key.vk == libtcod.KEY_F1:
		libtcod.sys_set_renderer(libtcod.RENDERER_GLSL)
	elif key.vk == libtcod.KEY_F2:
		libtcod.sys_set_renderer(libtcod.RENDERER_OPENGL)
	elif key.vk == libtcod.KEY_F3:
		libtcod.sys_set_renderer(libtcod.RENDERER_SDL)
	libtcod.console_flush()
