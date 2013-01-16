import sys
sys.path.insert(0,'../')
import unittest

from crawl.normalized_list import NormalizedList

class UppercaseList(NormalizedList):

	def normalize_element(self,element):
		return element.upper()

class NormalizedListTest(unittest.TestCase):

	def setUp(self):
		self.list = UppercaseList()

	def testBracketsWithRange(self):


		self.list.extend(["a","b","c"])
		self.list[0:2] = ["d"]

		self.assertEqual(["D","C"],self.list)

	def testBracketsWithIndex(self):
		self.list.extend(["a","b","c"])
		self.list[0] = "d"

		self.assertEqual(['D','B','C'],self.list)

	def testExtend(self):
		self.list.extend(["a","b","c"])
		self.assertEqual(["A","B","C"],self.list)

	def testInsert(self):
		self.list.extend(["a","b","c"])
		self.list.insert(0,'d')
		self.assertEqual(['D','A','B','C'],self.list)

	def testAppend(self):
		self.list.append('a')
		self.list.append('b')
		self.list.append('c')
		self.assertEqual(["A","B","C"],self.list)

if __name__ == '__main__':
	unittest.main()