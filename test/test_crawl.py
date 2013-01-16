import sys
sys.path.insert(0,'../')
import unittest
import os

import crawl
from crawl_test import FIXTURE_ROOT

class TestCrawl(unittest.TestCase):

	def new_crawl(self,callback=None):
		search_path = crawl.Crawl(FIXTURE_ROOT)
		search_path.append_paths("app/views","vendor/plugins/signal_id/app/views",".")
		search_path.append_extensions("builder","coffee","str",".erb")
		search_path.alias_extension('htm',"html")
		search_path.alias_extension('xhtml',"html")
		search_path.alias_extension('php',"html")
		search_path.alias_extension('coffee',"html")

		return callback(search_path) if callback else search_path

	def setUp(self):
		self.crawl = self.new_crawl()

	def fixture_path(self,path):
		return os.path.abspath(os.path.join(FIXTURE_ROOT,path))

	def testRoot(self):
		self.assertEqual(FIXTURE_ROOT,self.crawl.root)

	def testPaths(self):
		self.assertEqual(
			[
				self.fixture_path('app/views'),
				self.fixture_path('vendor/plugins/signal_id/app/views'),
				self.fixture_path('.')
			],
			self.crawl.paths
		)

	def testExtensions(self):
		self.assertEqual([".builder",".coffee",".str",".erb"],self.crawl.extensions)

	def testIndex(self):
		self.assertIsInstance(self.crawl.index(),crawl.index.Index)

	def testFindNonexistantFile(self):
		self.assertIsNone(self.crawl.find("people/show.html"))

	def testFindWithoutExtension(self):
		self.assertEqual(
				self.fixture_path("app/views/projects/index.html.erb"),
				self.crawl.find("projects/index.html")
			)

	def testFindWithExtension(self):
		self.assertEqual(
				self.fixture_path("app/views/projects/index.html.erb"),
				self.crawl.find("projects/index.html.erb")
			)