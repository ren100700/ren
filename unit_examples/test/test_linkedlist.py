import unittest
from utils.linkedlist import LinkTable

class TestLinkedList(unittest.TestCase):

	def test_add(self):
		linktable = LinkTable()
		self.assertTrue(linktable.counts() == 0)
		linktable.add('xiao')
		self.assertTrue(linktable.counts() == 1)
		linktable.add(10)
		self.assertTrue(linktable.counts() == 2)
		for i in range(100):
			linktable.add(i)
		self.assertTrue(linktable.counts() == 102)
