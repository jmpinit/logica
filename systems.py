class Op(object):
	def __init__(self, inp, out):
		self.input = inp
		self.output = out
	
	# get our value
	def ask(self):
		return 0
	
	# somebody is letting us know of their value
	def notify(self, val):
		pass

class Multiply(Op):
	def ask(self):
		return this.input[0].ask() * this.input[1].ask()
		
class Add(Op):
	def ask(self):
		return this.input[0].ask() + this.input[1].ask()
		
class R(Op):
	def __init__(self):
		self.start = 0
		self.reset()
		
	def reset(self):
		self.value = self.start

	def ask(self):
		return self.value
		
	def notify(self, val):
		self.value = val
