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
	# __init__
	###########

	def test_base1(self):
		Core(Extension(ext="none"))

	def test_base2(self):
		Core([Extension(ext="none"), Extension(ext="none")])

	def test_base_bad(self):
		self.assertRaises(ValueError, Core, "")

	###########
	# __title__
	###########

	def test_title1(self):
		c = Core(Extension(ext="none"))
		out = StringIO()

		c.__title__(title="Random Title", out=out)
		output = out.getvalue().strip()

		self.assertEqual(output,	"################################################################################\n" +
									"#                                 RANDOM TITLE                                 #\n" +
									"################################################################################")

	def test_title2(self):
		c = Core(Extension(ext="none"))
		out = StringIO()

		c.__title__(title="a" * 100, out=out)
		output = out.getvalue().strip()

		self.assertEqual(output,	"################################################################################\n" +
									"# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA #\n" +
									"################################################################################")

	def test_title3(self):
		c = Core(Extension(ext="none"))
		out = StringIO()

		self.assertRaises(ValueError, c.__title__, title=123, out=out)

	###########
	# __subtitle__
	###########

	def test_subtitle1(self):
		c = Core(Extension(ext="none"))
		out = StringIO()

		c.__subtitle__(title="Random Subtitle", out=out)
		output = out.getvalue().strip()

		self.assertEqual(output,	"||                              RANDOM SUBTITLE                               ||\n" +
									"================================================================================")

	def test_subtitle2(self):
		c = Core(Extension(ext="none"))
		out = StringIO()

		c.__subtitle__(title="a" * 100, out=out)
		output = out.getvalue().strip()

		self.assertEqual(output,	"|| AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA ||\n" +
									"================================================================================")

	def test_subtitle3(self):
		c = Core(Extension(ext="none"))
		out = StringIO()

		self.assertRaises(ValueError, c.__subtitle__, title=123, out=out)

	###########
	# extensionNames
	###########

	def test_extensionNames1(self):
		c = Core(Extension(ext="test"), None)

		self.assertEqual(c.extensionPatterns, [r"\.test"])

	def test_extensionNames2(self):
		c = Core([	Extension(ext="test1"),
					Extension(ext="test2"),
					Extension(ext="test3")	], None)

		self.assertEqual(c.extensionPatterns, [r"\.test1", r"\.test2", r"\.test3"])

	###########
	# extensionObjects
	###########

	def test_extensionObjects1(self):
		c = Core(Extension(ext="test"), None)

		self.assertEqual(all(isinstance(x, Extension) for x in c.extensionObjects), True)
		self.assertEqual(c.extensionObjects[0].extension, r"\.test")

	def test_extensionObjects2(self):
		c = Core([	Extension(ext="test1"),
					Extension(ext="test2"),
					Extension(ext="test3")	], None)

		self.assertEqual(all(isinstance(x, Extension) for x in c.extensionObjects), True)
		self.assertEqual(c.extensionObjects[0].extension, r"\.test1")
		self.assertEqual(c.extensionObjects[1].extension, r"\.test2")
		self.assertEqual(c.extensionObjects[2].extension, r"\.test3")

	###########
	# __read__
	###########

	dataDir = "bibtex_merger/tests/data"

	def tRead(self, filename):
		with open(filename, "r") as f:
			return f.read()

		raise Exception

	def test_read(self):
		c = Core(Extension(ext="txt", reader=self.tRead))

		self.assertEqual(c.__read__("{}/sample.txt".format(self.dataDir)), "Sample file with text")

	def test_read_bad_ext(self):
		c = Core(Extension(ext="txt", reader=self.tRead))

		self.assertRaises(CoreError, c.__read__, "{}/sample.random".format(self.dataDir))

	###########
	# __write__
	###########

	def tWrite(self, filename, content):
		with open(filename, "w") as f:
			return f.write(content)

		raise Exception

	def test_writeread(self):
		c = Core(Extension(ext="txt", reader=self.tRead, writer=self.tWrite))

		f = "sample2.txt"
		t = "Some random text to insert"

		c.__write__("{}/{}".format(self.dataDir, f), t)

		self.assertEqual(c.__read__("{}/{}".format(self.dataDir, f)), t)

		os.remove("{}/{}".format(self.dataDir, f))

	def test_write_bad_ext(self):
		c = Core(Extension(ext="txt", reader=self.tRead, writer=self.tWrite))

		f = "sample2.random"
		t = "Some random text to insert"

		self.assertRaises(CoreError, c.__write__, "{}/{}".format(self.dataDir, f), t)

class TestCoreError(unittest.TestCase):

	###########
	# Helpers
	###########

	def coreError(self, msg=-1):
		if msg == -1:
			raise CoreError()
		else:
			raise CoreError(msg)

	def coreErrorAttemptMsgChange(self):
		ce = CoreError(msg="red")
		ce.msg = "blue"
		raise ee

	###########
	# __init__
	###########

	def test_CoreError_base(self):
		self.assertRaises(CoreError, self.coreError, msg="red")
		self.assertRaises(CoreError, self.coreError, msg=None)
		self.assertRaises(CoreError, self.coreError)

	def test_CoreError_bad_msg(self):
		self.assertRaises(ValueError, self.coreError, msg=12345)

	def test_CoreError_catching(self):
		msg = "test"
		try:
			raise CoreError(msg=msg)
		except CoreError as e:
			self.assertEqual(str(e), msg)

	###########
	# msg
	###########

	def test_CoreError_msg_change(self):
		self.assertRaises(AttributeError, self.coreErrorAttemptMsgChange)

if __name__ == '__main__':
	unittest.main()