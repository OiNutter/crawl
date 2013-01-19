import sys
sys.path.insert(0,'../')
import unittest
import os

import crawl
from crawl_test import FIXTURE_ROOT,TestBase

class SharedTests(object):

	def new_crawl(self,callback=None):
		search_path = crawl.Crawl(FIXTURE_ROOT)
		search_path.append_paths("app/views","vendor/plugins/signal_id/app/views",".")
		search_path.append_extensions("builder","coffee","str",".erb")
		search_path.alias_extension('htm',"html")
		search_path.alias_extension('xhtml',"html")
		search_path.alias_extension('php',"html")
		search_path.alias_extension('coffee',"js")

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

	def testFindWithLeadingSlash(self):
		self.assertEqual(
				self.fixture_path("app/views/projects/index.html.erb"),
				self.crawl.find("/projects/index.html")
			)

	def testFindRespectsPathOrder(self):

		self.assertEqual(
				self.fixture_path("app/views/layouts/interstitial.html.erb"),
				self.crawl.find('layouts/interstitial.html')
			)

		def reverse_paths(search):
			search.paths.reverse()
			return search

		search = self.new_crawl(callback=reverse_paths)

		self.assertEqual(
				self.fixture_path("vendor/plugins/signal_id/app/views/layouts/interstitial.html.erb"),
				search.find('layouts/interstitial.html')
			)

	def testFindRespectsExtensionOrder(self):

		self.assertEqual(
				self.fixture_path("app/views/recordings/index.atom.builder"),
				self.crawl.find("recordings/index.atom")
			)

		def reverse_exts(search):
			search.extensions.reverse()
			return search

		search = self.new_crawl(callback=reverse_exts)

		self.assertEqual(
				self.fixture_path("app/views/recordings/index.atom.erb"),
				search.find("recordings/index.atom")
			)

	def testFindWithMultipleLogicalPathsReturnsFirstMatch(self):

		self.assertEqual(
				self.fixture_path("app/views/recordings/index.html.erb"),
				self.crawl.find("recordings/index.txt","recordings/index.html","recordings/index.atom")
			)

	def testFindFileInPathRootReturnsExpandedPath(self):
		self.assertEqual(
				self.fixture_path("app/views/index.html.erb"),
				self.crawl.find("index.html")
			)

	def testFindExtensionlessFile(self):
		self.assertEqual(
				self.fixture_path('README'),
				self.crawl.find('README')
			)

	def testFindFileWithMultipleExtensions(self):
		self.assertEqual(
				self.fixture_path("app/views/projects/project.js.coffee.erb"),
				self.crawl.find("projects/project.js")
			)

	def testFindFileWithMultipleExtensionsRespectsExtensionOrder(self):
		self.assertEqual(
				self.fixture_path("app/views/application.js.coffee.str"),
				self.crawl.find("application.js")
			)

		def reverse_exts(search):
			search.extensions.reverse()
			return search

		search = self.new_crawl(callback=reverse_exts)

		self.assertEqual(
				self.fixture_path("app/views/application.js.coffee.erb"),
				search.find("application.js")
			)

	def testFindFileByAliasedExtension(self):

		self.assertEqual(
				self.fixture_path("app/views/people.coffee"),
				self.crawl.find('people.coffee')
			)

		self.assertEqual(
				self.fixture_path("app/views/people.coffee"),
				self.crawl.find('people.js')
			)

		self.assertEqual(
				self.fixture_path("app/views/people.htm"),
				self.crawl.find('people.htm')
			)

		self.assertEqual(
				self.fixture_path("app/views/people.htm"),
				self.crawl.find('people.html')
			)

	def testFindFileWithAliasesPrefersPrimaryExtension(self):

		self.assertEqual(
				self.fixture_path("app/views/index.html.erb"),
				self.crawl.find("index.html")
			)

		self.assertEqual(
				self.fixture_path("app/views/index.php"),
				self.crawl.find("index.php")
			)

	def testFindWithBasePathOptionAndRelativeLogicalPath(self):
		self.assertEqual(
				self.fixture_path("app/views/projects/index.html.erb"),
				self.crawl.find("./index.html",base_path = self.fixture_path("app/views/projects"))
			)

	def testFindIgnoresBasePathOptionWhenLogicalPathNotRelative(self):
		self.assertEqual(
				self.fixture_path("app/views/index.html.erb"),
				self.crawl.find("index.html",base_path = self.fixture_path("app/views/projects"))
			)

	def testBasePathOptionMustBeExpanded(self):
		self.setUp()
		self.assertIsNone(self.crawl.find('./index.html',base_path='app/views/projects'))

	def testFindAllRespectsPathOrder(self):

		results = []
		def callback(paths):
			results.extend(paths)

		self.crawl.find("layouts/interstitial.html",callback=callback)

		self.assertEqual(
				[
					self.fixture_path("app/views/layouts/interstitial.html.erb"),
					self.fixture_path("vendor/plugins/signal_id/app/views/layouts/interstitial.html.erb")
				],
				results
			)

	def testFindAllWithMultipleExtensionsRespectsExtensionOrder(self):

		results = []

		def callback(paths):
			results.extend(paths)

		self.crawl.find("application.js",callback=callback)

		self.assertEqual(
				[
					self.fixture_path("app/views/application.js.coffee.str"),
					self.fixture_path("app/views/application.js.coffee.erb")
				],
				results
			)

	def testFindFilenameInsteadOfDirectory(self):
		self.assertEqual(
				self.fixture_path("app/views/projects.erb"),
				self.crawl.find("projects")
			)

	def testIgnoresDirectories(self):
		self.assertIsNone(self.crawl.find("recordings"))

	def testEntries(self):
		expected = [
			"application.js.coffee.erb",
			"application.js.coffee.str",
			"index.html.erb",
			"index.php",
			"layouts",
			"people.coffee",
			"people.htm",
			"projects",
			"projects.erb",
			"recordings"
		]

		self.assertEqual(
				expected,
				sorted(self.crawl.entries(self.fixture_path("app/views")))
			)

	def testStat(self):
		assert self.crawl.stat(self.fixture_path("app/views/index.html.erb"))
		assert self.crawl.stat(self.fixture_path("app/views"))

		self.assertIsNone(self.crawl.stat(self.fixture_path("app/views/missing.html")))

class CrawlTest(SharedTests,TestBase):

	def testRootDefaultsToCWD(self):
		cur_dir = os.curdir
		os.chdir(FIXTURE_ROOT)
		search = crawl.Crawl()
		self.assertEqual(FIXTURE_ROOT,search.root)
		os.chdir(cur_dir)

	def testFindReflectsChangesInTheFileSystem(self):
		try:
			self.assertIsNone(self.crawl.find("dashboard.html"))
			f = open(self.fixture_path('dashboard.html'),'w')
			f.write('dashboard')
			f.close()
			self.assertEqual(
					self.fixture_path('dashboard.html'),
					self.crawl.find('dashboard.html')
				)
		finally:
			os.unlink(self.fixture_path('dashboard.html'))
			assert not os.path.exists(self.fixture_path('dashboard.html'))

class IndexTest(SharedTests,TestBase):

	def new_crawl(self,callback=None):
		search = super(IndexTest,self).new_crawl(callback=callback)
		return search.index()

	def testChangingTrailPathDoesntAffectIndex(self):
		search = crawl.Crawl(FIXTURE_ROOT)
		search.paths.append('.')

		index = search.index()

		self.assertEqual([self.fixture_path('.')],search.paths)
		self.assertEqual([self.fixture_path('.')],index.paths)

		search.paths.append("app/views")

		self.assertEqual(
				[self.fixture_path("."),self.fixture_path("app/views")],
				search.paths
			)

		self.assertEqual([self.fixture_path('.')],index.paths)

	def testChangingTrailExtensionsDoesntAffectIndex(self):
		search = crawl.Crawl(FIXTURE_ROOT)
		search.extensions.append('builder')

		index = search.index()

		self.assertEqual(['.builder'],search.extensions)
		self.assertEqual(['.builder'],index.extensions)

		search.extensions.append('str')

		self.assertEqual(['.builder','.str'],search.extensions)
		self.assertEqual(['.builder'],index.extensions)

	def testFindDoesNotReflectChangesInTheFileSystem(self):
		try:
			self.assertIsNone(self.crawl.find("dashboard.html"))
			f = open(self.fixture_path('dashboard.html'),'w')
			f.write('dashboard')
			f.close()
			if hasattr(self,'assertIsNone'):
				self.assertIsNone(self.crawl.find("dashboard.html"))
			else:
				self.assertEquals(None,self.crawl.find("dashboard.html"))
		finally:
			os.unlink(self.fixture_path('dashboard.html'))
			assert not os.path.exists(self.fixture_path('dashboard.html'))


