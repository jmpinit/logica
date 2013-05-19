import libtcodpy as tcod
import math
import tcod_utils as util
import routing
from machine_game import *

# physical circuit object
class Device(Entity):
	# pins is a list of pin names
	def __init__(self, x, y, w, h, pins, name):
		super(Device, self).__init__(x, y, w, h)
		
		self.name = name
		self.pins = pins
		
# connection pt relative to parent device
class Pin(object):
	def __init__(self, parent, x, y, name):
		self.relx = x
		self.rely = y
		self.parent = parent

		self.name = name
		
	def x(self):
		return self.parent.x + self.relx
		
	def y(self):
		return self.parent.y + self.rely

	def __str__(self):
		return "<Pin of "+str(self.parent)+" at ("+str(self.relx)+", "+str(self.rely)+")"

class Chip(Device):
	directions = ['up', 'right', 'down', 'left']

	def __init__(self, x, y, pins, name):
		super(Chip, self).__init__(x, y, len(pins)/2+len(pins)%2, 3, pins, name)

		self.dir = 'up'

		# create pins
		self.pins = []
		for i in range(len(pins)):
			self.pins.append(Pin(self, 0, 0, pins[i]))

		self.bake_images()
		self.rotate(self.dir)

	def bake_images(self):
		# generate images (all rotations)
		self.images = {}

		label = self.name
		if len(label) > self.width:
			label = util.abbrev(label)
		label_l = util.pad(label, self.width)
		label_r = util.pad_right(label, self.width)

		# up
		top_pins = "|"*self.width
		if len(self.pins)%2 == 0:
			bottom_pins = top_pins
		else:
			bottom_pins = "|"*(self.width-1)+" "

		compressed = top_pins+label_l+bottom_pins
		self.images['up'] = util.Image.fromString(self.width, self.height, compressed)
		for x in range(self.width):
			self.images['up'].set_color(x, 1, tcod.red)

		# down
		bottom_pins = "|"*self.width
		if len(self.pins)%2 == 0:
			top_pins = top_pins
		else:
			top_pins = " "+"|"*(self.width-1)

		compressed = top_pins+label_r+bottom_pins
		self.images['down'] = util.Image.fromString(self.width, self.height, compressed)
		for x in range(self.width):
			self.images['down'].set_color(x, 1, tcod.red)

		# left
		uncompressed = []
		for c in label_l:
			uncompressed += ["-", c, "-"]
		if len(self.pins)%2 == 1: uncompressed[-3] = " "

		compressed = ''.join(uncompressed)

		self.images['left'] = util.Image.fromString(self.height, self.width, compressed)
		for y in range(self.width):
			self.images['left'].set_color(1, y, tcod.red)

		# right
		uncompressed = []
		for c in label_r:
			uncompressed += ["-", c, "-"]
		if len(self.pins)%2 == 1: uncompressed[2] = " "

		compressed = ''.join(uncompressed)

		self.images['right'] = util.Image.fromString(self.height, self.width, compressed)
		for y in range(self.width):
			self.images['right'].set_color(1, y, tcod.red)
	
	def rotate(self, direction):
		if not direction in set(['up', 'down', 'left', 'right']):
			raise Exception('Chip Error', 'Valid directions are up, down, left, or right.')

		self.image = self.images[direction]

		# correct dimensions
		if(direction == 'up' or direction == 'down'):
			self.width = len(self.pins)/2+len(self.pins)%2
			self.height = 3
		else:
			self.width = 3
			self.height = len(self.pins)/2+len(self.pins)%2

		if(direction == 'up'):
			for i, p in enumerate(self.pins):
				p.relx = i%self.width
				if(i < self.width):
					p.rely = 0
				else:
					p.rely = 2
		elif(direction == 'down'):
			for i, p in enumerate(self.pins):
				p.relx = (self.width-i-1)%self.width
				if(i < self.width):
					p.rely = 2
				else:
					p.rely = 0
		elif(direction == 'left'):
			for i, p in enumerate(self.pins):
				p.rely = i%self.height
				if(i < self.height):
					p.relx = 2
				else:
					p.relx = 0
		elif(direction == 'right'):
			for i, p in enumerate(self.pins):
				p.rely = (self.height-i-1)%self.height
				if(i < self.height):
					p.relx = 0
				else:
					p.relx = 2
		
		self.dir = direction

		# draw for debugging
		for p in self.pins:
			self.image.set(p.relx, p.rely, hex(self.pins.index(p))[2])

class Wire(object):
	def __init__(self, src, sink, nodes=[]):
		self.src = src		# output pin
		self.sink = sink	# input pin
		self.nodes = nodes	# spots to route between
	
	# add a new node
	def route(self, x, y):
		self.nodes.append((x, y))

# connect two or more pins
class Node(object):
	def __init__(self, parent, src, dest):
		if not (type(src) == Pin and type(dest) == Pin):
			raise Exception('Circuits Error', 'Nodes only connect Pins.')
		
		self.parent = parent
		self.src = src
		self.dest = dest
		
		self.solid = False
		self.image = None
	
	# get pts along connection
	def route(self):
		return routing.ucSearch (
			routing.CircuitSearchNode(
				self.parent,
				[self.src.parent],
				(self.src.x(), self.src.y()),
				None, 0, 3
			),
			lambda x: any([x == (self.dest.x()+dx, self.dest.y()+dy) for dx, dy in [(1,0),(0,1),(-1,0),(0,-1)]]),
			lambda (x, y): math.sqrt((self.dest.x()-x)**2+(self.dest.y()-y)**2)
		)
	
	def represent(self):
		if self.image == None:
			path = self.route()
			
			self.image = {}
			if(path):
				for pt in path:
					self.image[pt] = "*"
			else:
				self.image[(self.src.x(), self.src.y())] = "X"
		
		return (0, 0, self.image)

# a circuit board
class Board(object):
	def __init__(self, w, h, parts=[]):
		self.width = w
		self.height = h
		
		self.parts = parts
		self.wires = []
		
	def connect(self, device):
		self.parts.append(device)
	
	# connect two pins with a wire
	def wire(self, a, b):
		self.wires.append(Wire(self, a, b))

# SPECIFIC DEVICES

class Resistor(Device):
	def __init__(self, x, y):
		super(Resistor, self).__init__(x, y)
		self.pins = [Pin(self, 0, 0), Pin(self, 1, 0)]
		self.image = util.Image.fromString(2, 1, "++")
