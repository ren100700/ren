import unittest
from utils.mymathlib import *

math_obj = 0

def setUpModule():
	"""called once, before anything else in the module"""
	print("In setUpModule()...")
	global math_obj
	math_obj = mymathlib()

def tearDownModule():
	"""called once, after everything else in the module"""
	print("In tearDownModule()...")
	global math_obj
	del math_obj
 

class TestMyMathlib(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""called only once, before any test in the class"""
		print("In setUpClass()...")
	
	def setUp(self):
		"""called once before every test method"""
		print("\nIn setUp()...")
	
	def test_case01(self):
		print("In test_case01()")
		self.assertEqual(math_obj.add(2, 5), 7)
	
	def test_case02(self):
		print("In test_case02()")

		self.assertEqual(math_obj.sub(9, 5), 4)

	def test_case03(self):
		print("In test_case02()")
		self.assertTrue(math_obj.mul(3, 5) == 15)

	def test_case04(self):
		print("In test_case02()")
		self.assertTrue(4 > math_obj.div(10, 3) > 3)
	
	def tearDown(self):
		"""called once after every test method"""
		print("In tearDown()...")
	
	@classmethod
	def tearDownClass(cls):
		"""called once, after all the tests in the class"""
		print("In tearDownClass()...")