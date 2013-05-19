import tcod_utils as util

# connection pt relative to parent device
class Pin(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

# physical object part to stick into circuit board
class Device(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
		# self.pins = []
		# self.image = Image(1, 1)
		
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

# connect two or more pins
class Node(object):
	def __init__(self, src, dest):
		if not (type(src) == Pin and type(dest) == Pin):
			raise Exception('Circuits Error', 'Nodes only connect Pins.')
		
		self.src = src
		self.dest = dest
	
# a circuit board
class Board(object):
	def __init__(self, w, h):
		self.width = w
		self.height = h
		
		self.map = {}
		
	#def connect(
	

# SPECIFIC DEVICES

class Resistor(Device):
	def __init__(self, x, y):
		super(Resistor, self).__init__(x, y)
		self.pins = [Pin(0, 0), Pin(1, 0)]
		self.image = util.Image.fromString(2, 1, "++")
		
	