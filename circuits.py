import math
import tcod_utils as util
import routing

# physical object part to stick into circuit board
class Device(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.solid = True
		
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
