class Image(object):
	def __init__(self, w, h):
		self.width = w
		self.height = h
		self.data = [[" "]*w for x in xrange(h)]
		
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
			return ''.join(self.data[y])
		else:
			return None
	
	def get(self, x, y):
		if x >= 0 and x <= self.width and y >= 0 and y <= self.height:
			return self.data[y][x]
		else:
			return None
	
	def set(self, x, y, v):
		if not len(v) == 1:
			raise Exception('TCod Utils Error', 'Set was expecting a single character.')
			
		if x >= 0 and x <= self.width and y >= 0 and y <= self.height:
			self.data[y][x] = v