import logging, os, re

logger = logging.getLogger(__name__)
__all__ = [	'Extension', 'ExtensionError'	]

class Extension(object):
	def __init__(self, ext=r".*", reader=None, writer=None):
		# set arguments
		self._extension = ext
		self._reader = reader
		self._writer = writer

		if not isinstance(self._extension, str):
			raise ValueError("Extension's ext argument ({}) must be a str".format(self._extension))
		self._extension = re.compile(r"\." + self._extension)

		# assert valid reader argument
		if self._reader and not hasattr(self._reader, '__call__'):
			raise ValueError("Extension's reader argument ({}) must be a method reference".format(self._reader))

		# assert valid writer argument
		if self._writer and not hasattr(self._writer, '__call__'):
			raise ValueError("Extension's writer argument ({}) must be a method reference".format(self._writer))
		

	@property
	def extension(self):
		"""
		The file extension (in regular expression) for this Extension object.
		"""
		return self._extension.pattern

	@property
	def reextension(self):
		"""
		The file extension (in regular expression) for this Extension object.
		"""
		return self._extension

	@property
	def reader(self):
		"""
		The reader method reference for this Extension object.
		"""
		return self._reader

	@property
	def writer(self):
		"""
		The writer method reference for this Extension object.
		"""
		return self._writer

	def read(self, filename):
		"""
		The read method for this Extension object.
		"""
		if not self.reader:
			raise ExtensionError(self.extension, ExtensionError.READ)

		ext = os.path.splitext(filename)[1]
		if not re.match(self.reextension, ext):
			raise ExtensionError(self.extension, ExtensionError.GENERAL)

		return self.reader(filename)

	def write(self, filename, content):
		"""
		The write method for this Extension object.
		"""
		if not self.writer:
			raise ExtensionError(self.extension, ExtensionError.WRITE)

		ext = os.path.splitext(filename)[1]
		if not re.match(self.reextension, ext):
			raise ExtensionError(self.extension, ExtensionError.GENERAL)

		return self.writer(filename, content)

class ExtensionError(Exception):
	"""Exception raised for Extension object errors.

	Attributes:
		ext   -- the extension the error occurred with
		state -- what state the error occurred in (READ, WRITE, or GENERAL)
	"""

	READ = 0
	WRITE = 1
	GENERAL = 2

	def __init__(self, ext=r".*", state=None):
		self._ext = ext
		self._state = state

		if not isinstance(self.ext, str):
			raise ValueError("Extension's ext argument must be a str")
		self._ext = ("." if self._ext[0] != "." else "") + self._ext

		if self.state not in [self.READ, self.WRITE, self.GENERAL]:
			raise ValueError("ExtensionError has invalid state ({}), the error state must be either ExtensionError.READ, ExtensionError.WRITE, or ExtensionError.GENERAL".format(self.state))

	@property
	def ext(self):
		return self._ext

	@property
	def state(self):
		return self._state

	def __str__(self):
		if self.state == self.READ:
			return "Attempted to read an unsupported file format ({})".format(self.ext)
		elif self.state == self.WRITE:
			return "Attempted to write an unsupported file format ({})".format(self.ext)
		else:
			return "Attempted to use an unsupported file format ({})".format(self.ext)