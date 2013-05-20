import libtcodpy as tcod
import tcod_utils as util

# GUI for editing a circuitboard
class Workbench(object):
	# setup a circuitboard on the workbench
	def __init__(self, work):
		self.width = board.width
		self.height = board.height

		# what we're working on
		self.workpiece = work
		
		self.console = tcod.console_new(self.width, self.height)

# entities are single character world things
# ex: enemies, doors, players
class Entity(object):
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.image = util.Image(1, 1)

class Player(object):
	directions = {'up':(0, -1), 'down':(0, 1), 'left':(-1, 0), 'right':(1, 0)}

	def __init__(self, x, y):
		super(Player, self).__init__(x, y)
		self.image = util.Image.fromString(1, 1, "P")

	def move(d):
		if not d in set(directions):
			raise Exception('Player Error', 'Valid directions are up, down, left, or right.')

		dx, dy = directions[d]
		self.x += dx
		self.y += dy

class World(object):
	def __init__(self, w, h):
		self.width = w
		self.height = h

	@classmethod
	def fromFile(cls, filename):
		f = open(filename, 'r')
		data = f.read()

		self.data = [[[" ", tcod.black] for x in xrange(w)] for y in xrange(h)]

	def get
