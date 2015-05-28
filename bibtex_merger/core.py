import os, abc, sys, logging, re, ConfigParser

from bibtex_merger.extension import *

logger = logging.getLogger(__name__)
__all__ = [	'Core', 'CoreError'	]

class Core(object):
	killLevels = ['warning', 'error']
	killLevels = dict((v,k) for k, v in enumerate(killLevels))

	"""The core program. Processes and deals with the base functionality
	
	Attributes:
		ext	--	The Extension objects that this Core accepts. Ordered from
				most specific to generic extensions since the first match
				found for a filename is the one used.
		prefFile -- The filename for the preferences file. Default: "pref.cfg"
	"""
	def __init__(self, ext, prefFile='pref.cfg', out=sys.stdout, killLevel='warning'):
		if not callable(getattr(out, "write", None)):
			raise ValueError("Core out attribute must be a file type (not {}). Default is sys.stdout".format(type(out)))
		self._out = out

		# Verbose level that optionally prints more debugging code
		if not (isinstance(killLevel, str) and killLevel in self.killLevels):
			raise ValueError("BibTeX_Merger killLevel argument must be {} not ({} -> {})".format("|".join(self.killLevels), type(killLevel), killLevel))
		self._killLevel = self.killLevels[killLevel]

		if isinstance(ext, Extension):
			self._extensionObjects	= [ext]
		elif isinstance(ext, list):
			if all(isinstance(x, Extension) for x in ext):
				self._extensionObjects	= ext
			else:
				raise ValueError("Core ext attribute only accepts Extensions, you have included a non-Extension object")
		else:
			raise ValueError("Core expects either a single Extension or a list of Extensions")

		if prefFile != None:
			if not isinstance(prefFile, str):
				raise ValueError("Core prefFile attribute must be a file name of str not ({} -> {})".format(type(prefFile), prefFile))

			def prefRead(filename):
				config = ConfigParser.RawConfigParser()
				config.read(self._preferencesFile)
				return config
			def prefWrite(filename, content):
				with open(self._preferencesFile, 'wb') as f:
					return self.preferences.write(f)

			self._preferencesFile	=	prefFile
			self._extensionObjects	+=	[Extension(ext=r'^' + re.escape(prefFile) + r'$', reader=prefRead, writer=prefWrite)]
		else:
			self._preferencesFile	=	None

		self._preferences		= None

		self._extensionRegexs	= [x.reextension for x in self.extensionObjects]
		self._extensionPatters	= [x.extension   for x in self.extensionObjects]

		return

	@property
	def killLevel(self):
		return self._killLevel

	@property
	def out(self):
		return self._out

	@property
	def extensionObjects(self):
	    return self._extensionObjects

	@property
	def extensionRegexs(self):
		return self._extensionRegexs

	@property
	def extensionPatterns(self):
		return self._extensionPatters

	@property
	def preferences(self):
		return self._preferences

	@property
	def preferencesFile(self):
		return self._preferencesFile

	def __title__(self, title):
		if not isinstance(title, str):
			raise ValueError("Core.__title__'s title argument ({}) must be str".format(title))

		width = 80
		maxTextWidth = width - 4
		title = title.upper()
		
		if len(title) > maxTextWidth:
			title = title[:maxTextWidth]
		
		left  = int(((width - len(title)) / 2) - 1)
		right = int(left + ((width - len(title)) % 2))
		string = "\n" + ("#" * width) + "\n"
		string += "#" + (" " * left) + title + (" " * right) + "#\n"
		string += ("#" * width) + "\n"
		
		self.out.write(string)
		
		return

	def __subtitle__(self, title):
		if not isinstance(title, str):
			raise ValueError("Core.__subtitle__'s title argument ({}) must be str".format(title))

		width = 80
		maxTextWidth = width - 6
		title = title.upper()

		if len(title) > maxTextWidth:
			title = title[:maxTextWidth]

		left  = int(((width - len(title)) / 2) - 2)
		right = int(left + ((width - len(title)) % 2))
		string = "||" + (" " * left) + title + (" " * right) + "||\n"
		string += ("=" * width) + "\n"

		self.out.write(string)
		
		return

	def __read__(self, filename):
		try:
			indeces = [bool(re.search(reex, filename)) for reex in self.extensionRegexs]
			index   = indeces.index(True)

			assert bool(re.search(self.extensionObjects[index].reextension, filename)) == True
		except ValueError:
			# unsupported extension
			raise CoreError("Attempted to read an unsupported file format ({})".format(filename))

		# if an error is thrown in the reading process then that should be dealt with by
		# the Extension module
		return self.extensionObjects[index].read(filename=filename)

	def __write__(self, filename, content):
		try:
			indeces = [bool(re.search(reex, filename)) for reex in self.extensionRegexs]
			index   = indeces.index(True)

			assert bool(re.search(self.extensionObjects[index].reextension, filename)) == True

			return self.extensionObjects[index].write(filename=filename, content=content)
		except ValueError:
			# unsupported extension
			raise CoreError("Attempted to write an unsupported file format ({})".format(filename))

	def __info__(self, msg):
		if not isinstance(msg, str):
			raise ValueError("Core.__info__ msg attribute must be of str not {}".format(type(msg)))

		self.out.write(msg + "\n")

	def __warning__(self, exception):
		if not isinstance(exception, Exception):
			raise ValueError("Core.__warning__ exception attribute must be an instance of Exception not {}".format(type(exception)))

		if self.killLevel == self.killLevels['warning']:
			raise exception
		else:
			self.out.write("WARNING: {}: {}\n".format(type(exception).__name__, str(exception)))

	def __error__(self, exception):
		if not isinstance(exception, Exception):
			raise ValueError("Core.__error__ exception attribute must be an instance of Exception not {}".format(type(exception)))

		raise exception
	
	def __preferencesRead__(self):
		if self.preferencesFile == None:
			raise CoreError("This core does not support preferences")

		# preferences have not been imported yet
		if self.preferences == None:
			self._preferences = self.__read__(self.preferencesFile)

		return self.preferences

	def __preferencesWrite__(self):
		if self.preferencesFile == None:
			raise CoreError("This core does not support preferences")

		# preferences have not been imported yet
		if self.preferences == None:
			self._preferences = self.__read__(self.preferencesFile)

		return self.__write__(self.preferencesFile, self.preferences)

class CoreError(Exception):
	"""Exception raised for Core object errors.

	Attributes:
		msg -- the message addressing the error thrown
	"""

	def __init__(self, msg=None):
		self._msg = msg
		
		if self.msg != None and not isinstance(self.msg, str):
			raise ValueError("Extension's msg argument must be a str")

	@property
	def msg(self):
		return self._msg

	def __str__(self):
		return self.msg


