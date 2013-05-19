#!/usr/bin/python

import math
import os
import libtcodpy as libtcod

from circuits import *

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

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, b'machines', False)

libtcod.sys_set_fps(LIMIT_FPS)

# CIRCUIT SIM SETUP

a = Resistor(4, 4)
b = Resistor(40, 8)
c = Resistor(25, 20)

board = Board(SCREEN_WIDTH, SCREEN_HEIGHT, [a, b, c])
board.wire(a.pins[1], b.pins[0])
board.wire(c.pins[0], a.pins[0])
board.wire(c.pins[1], b.pins[1])

# render things with images
def render(drawables):
	libtcod.console_set_default_foreground(None, libtcod.white)
	
	for d in drawables:
		if d.solid:
			for y in range(0, d.image.height):
				libtcod.console_print(None, d.x, d.y, d.image.getrow(y))
		else:
			origin_x, origin_y, data = d.represent()
			for x, y in data.keys():
				libtcod.console_print(None, x, y, data[(x, y)])

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
	
	render(board.wires)		# draw the wires
	render(board.parts)		# draw the devices
	
	stats()
	
	#for y in range(0, SCREEN_HEIGHT):
	#	for x in range(0, SCREEN_WIDTH):
	#		if not routing.collide(x, y, board.parts):
	#			libtcod.console_print(None, x, y, "Y")

	libtcod.console_set_default_foreground(None, libtcod.grey)
	libtcod.console_set_default_background(None, libtcod.black)
	
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