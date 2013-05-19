class Op(object):
	# get our value
	def ask(self):
		return 0
	
	# somebody is letting us know of their value
	def notify(self, val):
		pass

class Multiply(Op):
	def __init__(self):
		self.num_inputs = 2

	def ask(self):
		return self.input[0].ask() * self.input[1].ask()
		
class Add(Op):
	def __init__(self):
		self.num_inputs = 2

	def ask(self):
		return self.input[0].ask() + self.input[1].ask()
		
# remembers a value for 1 timestep
class R(Op):
	def __init__(self):
		self.start = 0
		self.reset()

		self.num_inputs = 1
		
	def reset(self):
		self.value = self.start

	def ask(self):
		return self.value
		
	def notify(self, val):
		self.value = val

# just passes through a value
class Output(Op):
	def __init__(self):
		self.num_inputs = 1

	def ask(self):
		return self.input[0].ask()

# always is same value
class Const(Op):
	def __init__(self, val):
		self.value = val

		self.num_inputs = 0

	def ask(self):
		return self.value
