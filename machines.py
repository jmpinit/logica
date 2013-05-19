#!/usr/bin/python

from random import choice
from random import randint

import math
import os
import libtcodpy as libtcod

from machine_game import *
from circuits import *
from systems import *

# LIBTCOD SETUP

# Import Psyco if available
try:
    import psyco
    psyco.full()
except ImportError:
    pass

LIMIT_FPS = 30
SCREEN_WIDTH = 50
SCREEN_HEIGHT = 30

FONT_WIDTH = 10
FONT_HEIGHT = 10

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, b'machines', False)

libtcod.sys_set_fps(LIMIT_FPS)

# CIRCUIT SIM SETUP

wirenew = None
makingwire = False

board = Board(SCREEN_WIDTH, SCREEN_HEIGHT)
testchip2 = Chip(10, 10, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'], "add")
testchip1 = Chip(20, 14, ['a', 'b', 'c', 'd', 'e', 'f'], "sub")
board.connect(testchip1)
board.connect(testchip2)

# render things with images
# def render(drawables):
	# for d in drawables:
		# if d.solid:
			# for y in range(0, d.image.height):
				# libtcod.console_print_ex(None, d.x, d.y, libtcod.BKGND_SET, libtcod.LEFT, d.image.getrow(y))
		# else:
			# origin_x, origin_y, data = d.represent()
			# for x, y in data.keys():
				# libtcod.console_print_ex(None, x, y, libtcod.BKGND_SET, libtcod.LEFT, data[(x, y)])

def render(drawables):
	for d in drawables:
		for y in range(d.image.height):
			for x in range(d.image.width):
				libtcod.console_set_default_background(None, d.image.get_color(x, y))
				libtcod.console_print_ex(None, d.x+x, d.y+y, libtcod.BKGND_SET, libtcod.LEFT, d.image.get(x, y))

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

	# RENDER STUFF

	libtcod.console_clear(None)
	
	# libtcod.console_set_default_background(None, libtcod.red)
	# libtcod.console_set_default_foreground(None, libtcod.black)
	# render(board.parts)		# draw the devices
	# libtcod.console_set_default_background(None, libtcod.black)
	# libtcod.console_set_default_foreground(None, libtcod.white)
	# render(board.wires)		# draw the wires
	
	# render wires
	for w in board.wires:
		for (x0, y0), (x1, y1) in zip(w.nodes, w.nodes[1:]):
			libtcod.line_init(x0, y0, x1, y1)

			x, y = x0, y0
			while (not x is None):
				libtcod.console_set_char_background(None, x, y, libtcod.blue, flag=libtcod.BKGND_SET)
				x, y = libtcod.line_step()

	# render chips
	libtcod.console_set_default_background(None, libtcod.black)
	libtcod.console_set_default_foreground(None, libtcod.white)
	render(board.parts)

	# draw the mouse cursor
	libtcod.console_set_char_background(None, mouse.x/FONT_WIDTH, mouse.y/FONT_HEIGHT, libtcod.green, flag=libtcod.BKGND_SET)
	
	stats()
	
	#for y in range(0, SCREEN_HEIGHT):
	#	for x in range(0, SCREEN_WIDTH):
	#		if not routing.collide(x, y, board.parts):
	#			libtcod.console_print(None, x, y, "Y")
	
	libtcod.console_set_default_foreground(None, libtcod.grey)
	libtcod.console_set_default_background(None, libtcod.black)

	# mouse handler
	if mouse.lbutton_pressed:
		x = mouse.x/FONT_WIDTH
		y = mouse.y/FONT_HEIGHT

		if x >= 0 and y >= 0 and x < SCREEN_WIDTH and y < SCREEN_HEIGHT:
			if makingwire:
				wirenew.route(x, y)
			else:
				wirenew = Wire(None, None, [(x, y)])
				makingwire = True
	
	if mouse.rbutton_pressed:
		if makingwire:
			board.wires.append(wirenew)
		makingwire = False

		#testchip2.rotate(Chip.directions[(Chip.directions.index(testchip2.dir)+1)%4])
	
	# key handler
	if key.vk == libtcod.KEY_DOWN:
		pass
	elif key.vk == libtcod.KEY_UP:
		pass
	elif key.vk == libtcod.KEY_ENTER and key.lalt:
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
