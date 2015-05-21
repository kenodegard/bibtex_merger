import linecache
import sys

class Error(Exception):
	pass

	def __str__(self):
		return self.msg

class UserError(Error):
	"""Exception raised for errors in the user input.

	Attributes:
		msg  -- explanation of the error
	"""

	def __init__(self, msg):
		self.msg = msg

class BibTeXParserError(Error):
	"""Exception raised for errors in the parser.

	Attributes:
		msg  -- explanation of the error
	"""

	def __init__(self, msg):
		self.msg = msg

class ProgramError(Error):
	"""Exception raised for errors in the actual program. These errors should
	only be occurring in development phases not production phases.

	Attributes:
		msg  -- explanation of the error
	"""

	def __init__(self, msg):
		self.msg = msg

def PrintException(errStr="Error"):
    exc_type, exc_obj, tb = sys.exc_info()

    f = tb.tb_frame

    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals).strip()

    maxlinelen = 25

    print "\n\nERROR ({}) ({}, line {}, \"{}\"):\n{}\n\n".format(errStr, filename, lineno, line[:maxlinelen] + ("..." if len(line) > maxlinelen else ""), exc_obj)