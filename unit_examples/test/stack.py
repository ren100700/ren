class Stack:



	def __init__(self):
		self.max_size = 5
		self.stack_list = []

	def push(self, item):
		self.stack_list.append(item)

