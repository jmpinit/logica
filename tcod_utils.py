import libtcodpy as tcod

class Image(object):
	def __init__(self, w, h):
		self.width = w
		self.height = h
		self.data = [[[" ", tcod.black] for x in xrange(w)] for y in xrange(h)]
		
	@classmethod
	def fromString(cls, x, y, compressed):
		if len(compressed) == 0:
			raise Exception('TCod Utils Error', 'Cannot make Image from empty string.')
	
		img = cls(x, y)
		
		index = 0
		for y in range(0, img.height):
			for x in range(0, img.width):
				img.set(x, y, compressed[index])
				
				index += 1
				if(index >= len(compressed)): break
				
		return img
	
	def getrow(self, y):
		if y >= 0 and y <= self.height:
			return ''.join([char for char, col in self.data[y]])
		else:
			return None

	def get(self, x, y):
		if x >= 0 and x <= self.width and y >= 0 and y <= self.height:
			return self.data[y][x][0]
		else:
			return None
	
	def set(self, x, y, v):
		if not len(v) == 1:
			raise Exception('TCod Utils Error', 'Set was expecting a single character.')
			
		if x >= 0 and x <= self.width and y >= 0 and y <= self.height:
			self.data[y][x][0] = v
	
	def get_color(self, x, y):
		if x >= 0 and x <= self.width and y >= 0 and y <= self.height:
			return self.data[y][x][1]
		else:
			return None
	
	def set_color(self, x, y, col):
		if x >= 0 and x <= self.width and y >= 0 and y <= self.height:
			self.data[y][x][1] = col

	def rotate90(self):
		newimage = Image(self.height, self.width)

		for y in range(0, self.height):
			for x in range(0, self.width):
				newx = self.height-y+1
				newy = x

				newimage.set(newx, newy, self.get(x, y))

	def rotate270(self):
		pass

	def __str__(self):
		msg = "Image - "
		msg += str(self.width)+"x"+str(self.height)+"\n"
		for y in range(0, self.height):
			msg += self.getrow(y)+"\n"

		return msg

 
def pad(msg, length):
	if len(msg)==length:
		return msg
	elif len(msg)>length:
		return msg[0:length]
	else:
		diff = length-len(msg)
		return msg+" "*diff

# like pad but right aligned
def pad_right(msg, length):
	if len(msg)==length:
		return msg
	elif len(msg)>length:
		return msg[0:length]
	else:
		diff = length-len(msg)
		return " "*diff+msg

def abbrev(s):
	shortened = ""
	vowels = set(['a', 'e', 'i', 'o', 'u'])
	for c in s:
		if not c in vowels: shortened += c
		
	return shortened
