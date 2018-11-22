class Node:

	def ___init__(self, value):
		self.value = value
		self.next_node = None

	def set_next_node(self, node):
		self.next_node = node


node1 = Node([1,2,3])
node2 = Node("Jon")
node3 = Node("Lisa")
node4 = Node("James")


node1.next_node = node2
node2.next_node = node3

node1.set_next_node(node2)
node2.set_next_node(node3)
node3.set_next_node(node4)


class LinkedList:
	
	def __init__(self):
		self.start_node = None


	def append(self, node):
		if not self.start_node:
			self.start_node = node
