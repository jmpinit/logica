from random import choice
from random import randint

import libtcodpy as libtcod

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

class Player(Body):
	def __init__(self, x, y, rot):
		super(Player, self).__init__(x, y, rot)
		self.px = "P"

	def control(self, key):
		if key == libtcod.KEY_RIGHT:
			self.events.fire('move', self, (self.x+1, self.y))
		elif key == libtcod.KEY_UP:
			self.events.fire('move', self, (self.x, self.y-1))
		elif key == libtcod.KEY_LEFT:
			self.events.fire('move', self, (self.x-1, self.y))
		elif key == libtcod.KEY_DOWN:
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
