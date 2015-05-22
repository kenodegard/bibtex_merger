import os, abc, sys, logging

from extension import *

logger = logging.getLogger(__name__)
__all__ = [	'Core'	]

class Core(object):
	def __init__(self, ext):
		if isinstance(ext, Extension):
			self._extensionObjects	= [ext]
		elif isinstance(ext, list) and all(isinstance(x, Extension) for x in ext):
			self._extensionObjects	= ext
		else:
			raise ValueError("Core expects either a single Extension or a list of Extensions")

		self._extensionNames	= [x.extension for x in self.extensionObjects]
		return

	@property
	def extensionObjects(self):
	    return self._extensionObjects

	@property
	def extensionNames(self):
		return self._extensionNames

	def __title__(self, title, out=sys.stdout):
		if not isinstance(title, str):
			raise ValueError("Core.__title__'s title argument ({}) must be str".format(title))

		width = 80
		maxTextWidth = width - 4
		title = title.upper()
		
		if len(title) > maxTextWidth:
			title = title[:maxTextWidth]
		
		left  = ((width - len(title)) / 2) - 1
		right = left + ((width - len(title)) % 2)
		string = "\n" + ("#" * width) + "\n"
		string += "#" + (" " * left) + title + (" " * right) + "#\n"
		string += ("#" * width)
		
		out.write(string)
		
		return

	def __subtitle__(self, title, out=sys.stdout):
		if not isinstance(title, str):
			raise ValueError("Core.__subtitle__'s title argument ({}) must be str".format(title))

		width = 80
		maxTextWidth = width - 6
		title = title.upper()

		if len(title) > maxTextWidth:
			title = title[:maxTextWidth]

		left  = ((width - len(title)) / 2) - 2
		right = left + ((width - len(title)) % 2)
		string = "||" + (" " * left) + title + (" " * right) + "||\n"
		string += ("=" * width)

		out.write(string)
		
		return

	def __read__(self, filename):

		ext = os.path.splitext(filename)[1]

		try:
			index = self.extensionNames.index(ext)

			assert self.extensionObjects[index].extension == ext

			return self.extensionObjects[index].read(filename=filename)
		except ExtensionError:
			# unsupported extension
			raise ("Attempted to read an unsupported file format ({})".format(filename))

		# if extension == ".cfg":
		# 	config = ConfigParser.RawConfigParser()
		# 	config.read(filename)
		
		# 	return config
		# elif extension == ".bib":
		# 	with open("{}/{}".format(directory, filename)) as f:
		# 		return bp.load(f, parser=self.parser)
 
		# elif extension == ".csv":
		# 	with open("{}/{}".format(directory, filename)) as f:
		# 		return [e for e in csv.reader(f)]

	def __write__(self, filename, content):
		# if not os.path.exists(directory):
		# 	os.makedirs(directory)

		ext = os.path.splitext(filename)[1]

		try:
			index = self.extensionNames.index(ext)

			assert self.extensionObjects[index].extension == ext

			return self.extensionObjects[index].write(filename=filename, content=content)
		except ValueError:
			# unsupported extension
			raise ExtensionError("({}/{})".format(directory, filename))

		# if extension == ".cfg":
		# 	with open("{}/{}".format(directory, filename), 'wb') as f:
		# 		content.write(f)
		# 		return

		# 	raise ProgramError("Something went wrong with writing ({}/{})".format(directory, filename))

		# elif extension == ".bib":
		# 	raise ProgramError("BIBs aren't supposed to be made (yet)")

		# elif extension == ".csv":
		# 	with open("{}/{}".format(directory, filename), 'wb') as f:
		# 		filecontent = csv.writer(f)

		# 		if type(content) != None:
		# 			if type(content) == type([]):
		# 				if len(content) > 0:
		# 					if type(content[0]) == type([]):
		# 						# Matrix, List of lists
		# 						filecontent.writerows(content)
		# 					elif type(content[0]) != type([]):
		# 						# Vector, List
		# 						filecontent.writerow(content)
		# 			return

		# 		raise ProgramError("CSV content has bad format, write failed")

		# elif extension == ".txt":
		# 	with open("{}/{}".format(directory, filename), 'a') as f:
		# 		f.write(text)

		# 		return

		# 	print "ERROR: write({}/{}) with text failed".format(directory, filename)
		# 	return

	# def __preferences__(self):

	# 	# reading
	# 	config = self.__read__(self.installDir, self.configFile)

	# 	print(config)

	# 	# writing
	# 	config.add_section('Section1')
	# 	config.set('Section1', 'an_int', '15')
	# 	config.set('Section1', 'a_bool', 'true')
	# 	config.set('Section1', 'a_float', '3.1415')
	# 	config.set('Section1', 'baz', 'fun')
	# 	config.set('Section1', 'bar', 'Python')
	# 	config.set('Section1', 'foo', '%(bar)s is %(baz)s!')

	# 	# Writing our configuration file to 'example.cfg'
	# 	self.__write__(self.installDir, self.configFile, config)






