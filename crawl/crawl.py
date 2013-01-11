from extensions import normalize_element
import os
import re

class Crawl:

	def __init__(self,root="."):
		self.root = str(os.path.abspath(root))
		self.extensions = []
		self.aliases={}
		self.paths = []
		self.results = []
		self.patterns = {}

	def append_extension(self,extension):
		if extension not in self.extensions:
			self.extensions.append(normalize_element(extension))

	def append_extensions(self,*extensions):
		for ext in extensions:
			self.append_extension(normalize_element(ext))

	def alias_extensions(self,alias,extension):
		self.aliases[alias] = normalize_element(extension)

	def append_path(self,path):
		if path not in self.paths:
			self.paths.append(str(path))

	def append_paths(self,*args):
		for path in args:
			self.append_path(path)

	def is_relative_path(self,path):
		return True if re.match(r"""^\.\.?\/""",path) else False

	def entries(self,target):
		
		entries = []
		for dirpath,dirname,filenames in os.walk(target):
			entries = filenames
			break

		entries[:] = [filename for filename in entries if filename != "." and filename != ".."]

		return entries

	def find(self,*logical_paths,**kwargs):
		
		if kwargs.has_key('callback') and kwargs['callback']:

			for path in logical_paths:
				if not self.is_relative_path(path):
					return self.find_in_paths(path,kwargs['callback'])
				else:
					return self.find_in_base_path(path,self.root,kwargs['callback'])

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
		aliases = self.find_aliases_for_ext(normalize_element(ext))

		basename_re = re.escape(basename)

		if aliases:
			basename_re += "(%s)" % '|'.join([re.escape(ext) for ext in aliases])

		extension_pattern = '|'.join([re.escape(ext) for ext in self.extensions])
		
		return re.compile(r"""^%s(?:%s)*$""" % (basename_re,extension_pattern))

	def 	find_aliases_for_ext(self,ext):

		exts = []

		for alias,original in self.aliases:
			if original == ext:
				exts.append(alias)

		return exts