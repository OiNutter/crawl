import os
import unittest

FIXTURE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),'fixtures'))

class TestBase(unittest.TestCase):

	def assertIsNone(self,val):
		if(hasattr(super(TestBase,self),'assertIsNone')):
			super(TestBase,self).assertIsNone(val)
		else:
			self.assertEqual(None,val)

	def assertIsInstance(self,val,klass):
		if(hasattr(super(TestBase,self),'assertIsInstance')):
			super(TestBase,self).assertIsInstance(val,klass)
		else:
			assert isinstance(val,klass)

