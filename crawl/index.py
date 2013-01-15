import os
import re
import copy

class Index:

	def __init__(self,root,paths,extensions,aliases):
		self.root = root
		self.extensions = copy.deepcopy(extensions)
		self.aliases= copy.deepcopy(aliases)
		self.paths = copy.deepcopy(paths)
		self.entries_cache = {}
		self.stat_cache = {}
		self.patterns = {}

	def index(self):
		return self

	def is_relative_path(self,path):
		return True if re.match(r"""^\.\.?\/""",path) else False

	def entries(self,path):
		
		if not self.entries_cache.has_key(path):

			entries = []

			if os.path.exists(path) and os.path.isdir(path):
				for dirpath,dirname,filenames in os.walk(path):
					entries = filenames
					break

				entries[:] = [filename for filename in entries if filename != "." and filename != ".."]

			self.entries_cache[path]= entries

		return self.entries_cache[path]

	def stat(self,path):

		if not self.stat_cache.has_key(path):
			self.stat_cache[path] = os.stat(path)

		return self.stat_cache[path]

	def find(self,*logical_paths,**kwargs):
		
		if kwargs.has_key('callback') and kwargs['callback']:

			base_path = kwargs.get('base_path',self.root)

			for path in logical_paths:
				if not self.is_relative_path(path):
					return self.find_in_paths(path,kwargs['callback'])
				else:
					return self.find_in_base_path(path,base_path,kwargs['callback'])

		else:
			return self.find(*logical_paths,callback = lambda path:path)

	def find_in_paths(self,path,callback=None):

		dirname,basename = os.path.split(path)

		for path in self.paths:
			result = self.match(os.path.join(path,dirname),basename,callback)
			if result:
				return result

		return None

	def find_in_base_path(self,path,base_path,callback=None):

		candidate = os.path.join(base_path,path)
		dirname,basename = os.path.split(candidate)
		return self.match(dirname,basename,callback) if self.do_paths_contain(dirname) else None

	def do_paths_contain(self,dirname):
		matches = [path for path in self.paths if str(dirname)[0:len(path)] == path]
		return True if matches else False

	def match(self,dirname,basename,callback=None):
		
		matches = self.entries(dirname)

		pattern = self.get_pattern_for(basename)

		matches[:] = [match for match in matches if pattern.match(match)]

		for path in matches:
			pathname = os.path.abspath(os.path.join(dirname,path))

			if os.path.isfile(pathname):
				return callback(pathname) if callback else pathname

	def get_pattern_for(self,basename):
		if self.patterns.has_key(basename):
			return self.patterns[basename]
		else:
			pattern = self.build_pattern_for(basename)
			self.patterns[basename] = pattern
			return pattern

	def build_pattern_for(self,basename):

		filename, ext = os.path.splitext(basename.lower())
		aliases = self.find_aliases_for_ext(self.extensions.normalize_element(ext))

		basename_re = re.escape(basename)

		if aliases:
			basename_re += "(%s)" % '|'.join([re.escape(ext) for ext in aliases])

		extension_pattern = '|'.join([re.escape(ext) for ext in self.extensions])
		
		return re.compile(r"""^%s(?:%s)*$""" % (basename_re,extension_pattern))

	def find_aliases_for_ext(self,ext):

		exts = []

		for alias,original in self.aliases.iteritems():
			if original == ext:
				exts.append(alias)

		return exts