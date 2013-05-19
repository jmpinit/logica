import tcod_utils as util

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
	def __init__(self, x, y):
		super(Player, self).__init__(x, y)
