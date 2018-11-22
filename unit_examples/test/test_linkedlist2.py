import unittest

from linkedlist import LinkedList


class TestLinkedList(unittest.TestCase):

	def test_append(self):
		l = LinkedList()
		self.assertTrue(l.size() == 0)
		l.append(88)
		self.assertTrue(l.size() == 1)

	def test_remove(self):
		l = LinkedList()
		l.append(1)
		l.append(2)
		l.append(3)
		l.remove(30)
		self.assertTrue(l.size() == 3)

	def test_delete(self):
		l = LinkedList()
		l.append(1)
		l.append(2)
		l.append(22)
		l.delete(5)
		self.assertTrue(l.size() == 3)

if __name__ == '__main__':
	unittest.main()
