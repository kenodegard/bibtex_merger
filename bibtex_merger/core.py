import os, abc, sys, logging, re

python2 = sys.version_info < (3, 0, 0)

if python2:
    import ConfigParser
else:
    import configparser as ConfigParser

from bibtex_merger.extension import *

logger = logging.getLogger(__name__)
__all__ = [	'Core', 'CoreError'	]

class Core(object):
	DEBUG		= logging.DEBUG
	INFO		= logging.INFO
	WANRING		= logging.WANRING
	ERROR		= logging.ERROR
	CRITICAL	= logging.CRITICAL

	_SOFT_LOG_LIST_	= [DEBUG, INFO]
	_HARD_LOG_LIST_	= [WARNING, ERROR, CRITICAL]
	_ALL_LOG_LIST_	= _SOFT_LOG_LVLS + _HARD_LOG_LVLS

	_LOG_DICT_TO_INT_	= dict((lvl, getattr(Core, lvl)) for lvl in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
	_LOG_DICT_TO_STR_	= dict((getattr(Core, lvl), lvl) for lvl in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])

	def __LOG_LVL_TO_INT__(self, lvl):
		try:
			return self._LOG_DICT_TO_INT_[lvl]
		except KeyError:
			return None
	def __LOG_LVL_TO_STR__(self, lvl):
		try:
			return self._LOG_DICT_TO_STR_[lvl]
		except KeyError:
			return None

	killLevels = ['warning', 'error']
	killLevels = dict((v,k) for k, v in enumerate(killLevels))

	"""The core program. Processes and deals with the base functionality
	
	Attributes:
		ext	--	The Extension objects that this Core accepts. Ordered from
				most specific to generic extensions since the first match
				found for a filename is the one used.
		prefFile -- The filename for the preferences file. Default: "pref.cfg"
	"""
	def __init__(self, ext, prefFile='pref.cfg', out=OUT, loglvl=LOG_LVL, killlvl=KILL_LVL):
		if not callable(getattr(out, "write", None)):
			self.critical("Core <out> attribute must be a writable type (dflt: sys.stdout)")
		self._OUT = out

		# Verbose level that optionally prints more debugging code
		if kill_lvl not in _HARD_LOG_LIST_:
			self.critical("Core <kill_lvl> argument must be one of the accepted hard logging levels (dflt: WARNING)")
		self._KILL_LVL = kill_lvl

		if log_lvl not in _ALL_LOG_LIST_:
			self.critical("Core <log_lvl> argument must be one of the accepted logging levels (dflt: INFO)")
		self._LOG_LVL = log_lvl


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
	def OUT(self):
		try:
			return self._OUT
		except AttributeError:
			self._OUT = sys.stdout
			return self._OUT

	@property
	def LOG_LVL(self):
		try:
			return self._LOG_LVL
		except AttributeError:
			self._LOG_LVL = Core.INFO
			return self._LOG_LVL

	@property
	def KILL_LVL(self):
		try:
			return self._KILL_LVL
		except AttributeError:
			self._KILL_LVL = Core.WARNING
			return self._KILL_LVL

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

	def __title__(self, title, sym="#"):
		"""
		Pretty title maker
		"""
		title	= str(title).upper()
		sym		= str(sym).upper()

		if len(sym) == 0:
			self.info("Core.__title__: empty sym provided is reverting to the default")
			sym = "#"
		if len(sym) > 1:
			self.info("Core.__title__: sym is being truncated to a single character")
			sym = sym[0]

		width, height = shutil.get_terminal_size()
		border_width = 1
		whitespace_width = 2

		maxtextspace = width - ((border_width + whitespace_width) * 2)
		whitespace = width - len(title) - (border_width * 2)

		if whitespace < (whitespace_width * 2):
			self.info("Core.__title__: title is too long, trimming")
			whitespace = (whitespace_width * 2)

			title = title[:maxtextspace - 3] + "..."

		# get half of the whitespace and round down (truncate to remove decimal)
		left_whitespace		= int(whitespace / 2)
		# collect remaining whitespace on the right side
		right_whitespace	= whitespace - lspace

		if sym in ["#", "!", "?"]:
			text  = (sym * width) + "\n"
			text += sym + (" " * lspace) + title + (" " * rspace) + sym + "\n"
			text += (sym * width) + "\n"
		else:
			left_whitespace = left_symspace
			right_whitespace = right_symspace
			text =  (sym * left_symspace) + " " + title + " " + (sym * right_symspace) + "\n"

		return text

	def __subtitle__(self, subtitle):
		"""
		Pretty subtitle maker
		"""
		return self.__title__(subtitle, sym="!")

	def __text__(self, text):
		"""
		Pretty text maker
		"""
		if isinstance(text, list):
			return "\n".join(self.__text__(line) for line in text) + "\n"
		else:
			width, height = shutil.get_terminal_size()

			return textwrap.indent(textwrap.fill(text=text, width=width - 4), " ")

	def title(self, title):
		self.OUT.write(self.__title__(title))

	def subtitle(self, subtitle):
		self.OUT.write(self.__subtitle__(subtitle))

	def text(self, text):
		self.OUT.write(self.__text__(text))

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

	def __log_kill__(self, lvl, msgexpt):
		if lvl in self.HARD_LOG_LVLS:
			if isinstance(msgexpt, Exception):
				text = "({}) {}".format(msgexpt.__class__.__name__, str(msgexpt))
			else:
				self.critical(ValueError("Core.__log_kill__ msgexpt must be an Exception for lvl {}".format(self._LOG_DICT_TO_STR_[lvl])))
		elif lvl in self.SOFT_LOG_LVLS:
			if isinstance(msgexpt, str) or isinstance(expt, list):
				text = self.__text__(msgexpt)
			else:
				self.critical(ValueError("Core.__log_kill__ msgexpt must be a str/list for lvl {}".format(self._LOG_DICT_TO_STR_[lvl])))
		else:
			self.critical(ValueError("Core.__log_kill__ only accepts the following lvls: {}".format(", ".join(self._LOG_DICT_TO_STR_[l] for l in self._ALL_LOG_LIST_))))

		try:
			if lvl == self.DEBUG:
				self.logger.debug(text)
			elif lvl == self.INFO:
				self.logger.info(text)
			elif lvl == self.WARNING:
				self.logger.warning(text)
			elif lvl == self.ERROR:
				self.logger.error(text)
			elif lvl == self.CRITICAL:
				self.logger.critical(text)
		except AttributeError:
			# logger hasn't been initialized yet
			pass

		if lvl >= self.KILL_LVL:
			raise expt

	def debug(self, msg):
		self.__log_kill__(self.DEBUG, msg)
		

	def info(self, msg):
		self.__log_kill__(self.INFO, msg)

	def warning(self, expt):
		self.__log_kill__(self.WARNING, expt)

	def error(self, expt):
		self.__log_kill__(self.ERROR, expt)

	def critical(self, expt):
		self.__log_kill__(self.CRITICAL, expt)
	
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


