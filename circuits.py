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
	def __init__(self, parent, x, y):
		self.relx = x
		self.rely = y
		self.parent = parent
		
	def x(self):
		return self.parent.x + self.relx
		
	def y(self):
		return self.parent.y + self.rely

	def __str__(self):
		return "<Pin of "+str(self.parent)+" at ("+str(self.relx)+", "+str(self.rely)+")"

class Chip(Device):
	def __init__(self, x, y, pins, name):
		if len(pins)%2 == 0:
			super(Chip, self).__init__(x, y, len(pins)/2, 3, pins, name)
		else:
			super(Chip, self).__init__(x, y, len(pins)/2+1, 3, pins, name)
		
		# TODO Generate rotated images
		# generate image
		top_pins = "|"*self.width
		if len(pins)%2 == 0:
			bottom_pins = top_pins
		else:
			bottom_pins = "|"*(self.width-1)

		label = self.name
		if len(label) > self.width:
			label = util.abbrev(label)

		compressed = top_pins+util.pad(label, self.width)+bottom_pins
		self.image = util.Image.fromString(self.width, self.height, compressed)
		for x in range(self.width):
			self.image.set_color(x, 1, tcod.red)

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
		self.wires.append(Node(self, a, b))

# SPECIFIC DEVICES

class Resistor(Device):
	def __init__(self, x, y):
		super(Resistor, self).__init__(x, y)
		self.pins = [Pin(self, 0, 0), Pin(self, 1, 0)]
		self.image = util.Image.fromString(2, 1, "++")
