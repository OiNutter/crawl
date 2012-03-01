from normalized_array import NormalizedArray

class Extensions(NormalizedArray):

	def normalize_element(self,extension):
		if extension.match('/^\./'):
			return extension
		else:
			return "." + extension