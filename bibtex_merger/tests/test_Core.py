import unittest, sys, os

python2 = sys.version_info < (3, 0, 0)

if python2:
    from StringIO import StringIO
else:
    from io import StringIO

from bibtex_merger.core import *
from bibtex_merger.extension import *

class TestCore(unittest.TestCase):

	###########
	# __title__
	###########

	def test_title1(self):
		c = Core(Extension("none"))
		out = StringIO()

		c.__title__(title="Random Title", out=out)
		output = out.getvalue().strip()

		self.assertEqual(output, """################################################################################
#                                 RANDOM TITLE                                 #
################################################################################""")

	def test_title2(self):
		c = Core(Extension("none"))
		out = StringIO()

		c.__title__(title="a" * 100, out=out)
		output = out.getvalue().strip()

		self.assertEqual(output, """################################################################################
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA #
################################################################################""")

	def test_title3(self):
		c = Core(Extension("none"))
		out = StringIO()

		self.assertRaises(ValueError, c.__title__, title=123, out=out)

	###########
	# __subtitle__
	###########

	def test_subtitle1(self):
		c = Core(Extension("none"))
		out = StringIO()

		c.__subtitle__(title="Random Subtitle", out=out)
		output = out.getvalue().strip()

		self.assertEqual(output, """||                              RANDOM SUBTITLE                               ||
================================================================================""")

	def test_subtitle2(self):
		c = Core(Extension("none"))
		out = StringIO()

		c.__subtitle__(title="a" * 100, out=out)
		output = out.getvalue().strip()

		self.assertEqual(output, """|| AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA ||
================================================================================""")

	def test_subtitle3(self):
		c = Core(Extension("none"))
		out = StringIO()

		self.assertRaises(ValueError, c.__subtitle__, title=123, out=out)

	###########
	# extensionNames
	###########

	def test_extensionNames1(self):
		c = Core(Extension(ext="test"))

		self.assertEqual(c.extensionNames, [".test"])

	def test_extensionNames2(self):
		c = Core([	Extension(ext="test1"),
					Extension(ext="test2"),
					Extension(ext="test3")	])

		self.assertEqual(c.extensionNames, [".test1", ".test2", ".test3"])

	###########
	# extensionObjects
	###########

	def test_extensionObjects1(self):
		c = Core(Extension(ext="test"))

		self.assertEqual(all(isinstance(x, Extension) for x in c.extensionObjects), True)
		self.assertEqual(c.extensionObjects[0].extension, ".test")

	def test_extensionObjects2(self):
		c = Core([	Extension(ext="test1"),
					Extension(ext="test2"),
					Extension(ext="test3")	])

		self.assertEqual(all(isinstance(x, Extension) for x in c.extensionObjects), True)
		self.assertEqual(c.extensionObjects[0].extension, ".test1")
		self.assertEqual(c.extensionObjects[1].extension, ".test2")
		self.assertEqual(c.extensionObjects[2].extension, ".test3")

	###########
	# __read__
	###########

	def tRead(self, filename):
		with open(filename, "r") as f:
			return f.read()

		raise Exception

	def test_read(self):
		c = Core(Extension(ext="txt", reader=self.tRead))

		self.assertEqual(c.__read__("data/sample.txt"), "Sample file with text")

	###########
	# __write__
	###########

	def tWrite(self, filename, content):
		with open(filename, "w") as f:
			f.write(content)
			return

		raise Exception

	def test_writeread(self):
		c = Core(Extension(ext="txt", reader=self.tRead, writer=self.tWrite))

		f = "data/sample2.txt"
		t = "Some random text to insert"

		c.__write__(f, t)

		self.assertEqual(c.__read__(f), t)

		os.remove(f)

if __name__ == '__main__':
	unittest.main()