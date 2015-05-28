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
		Core(ext=Extension(ext="none"))

	def test_base2(self):
		Core(ext=[Extension(ext="none"), Extension(ext="none")])

	def test_base_bad1(self):
		self.assertRaises(ValueError, Core, ext="")

	def test_base_bad2(self):
		self.assertRaises(ValueError, Core, ext=["", 1234])

	def test_base_bad3(self):
		self.assertRaises(ValueError, Core, ext=[Extension(ext="none"), 1234])

	def test_prefFile_good(self):
		Core(ext=Extension(ext="none"))
		Core(ext=Extension(ext="none"), prefFile=None)
		Core(ext=Extension(ext="none"), prefFile="pref.cfg")

	def test_prefFile_bad(self):
		self.assertRaises(ValueError, Core, ext=Extension(ext="none"), prefFile=12345)
		self.assertRaises(ValueError, Core, ext=Extension(ext="none"), prefFile=Extension(ext="none"))

	def test_out(self):
		Core(ext=Extension(ext="none"))
		Core(ext=Extension(ext="none"), out=sys.stdout)
		Core(ext=Extension(ext="none"), out=StringIO())

	def test_out_bad(self):	
		self.assertRaises(ValueError, Core, ext=Extension(ext="none"), out="invalid")

	def test_killLevel(self):
		c = Core(ext=Extension(ext="none"))
		self.assertEqual(c.killLevel, c.killLevels['warning'])
		c = Core(ext=Extension(ext="none"), killLevel='warning')
		self.assertEqual(c.killLevel, c.killLevels['warning'])
		c = Core(ext=Extension(ext="none"), killLevel='error')
		self.assertEqual(c.killLevel, c.killLevels['error'])

	def test_killLevel_bad(self):	
		self.assertRaises(ValueError, Core, ext=Extension(ext="none"), killLevel="invalid")
		self.assertRaises(ValueError, Core, ext=Extension(ext="none"), killLevel=12345)

	###########
	# Properties
	###########

	def attemptChange_killLevel(self):
		m = Core(ext=Extension(ext="none"))
		m.killLevel = "bad"

	def attemptChange_out(self):
		m = Core(ext=Extension(ext="none"))
		m.out = "bad"

	def attemptChange_extensionObjects(self):
		m = Core(ext=Extension(ext="none"))
		m.extensionObjects = "bad"

	def attemptChange_extensionRegexs(self):
		m = Core(ext=Extension(ext="none"))
		m.extensionRegexs = "bad"

	def attemptChange_extensionPatterns(self):
		m = Core(ext=Extension(ext="none"))
		m.extensionPatterns = "bad"

	def attemptChange_preferences(self):
		m = Core(ext=Extension(ext="none"))
		m.preferences = "bad"

	def attemptChange_preferencesFile(self):
		m = Core(ext=Extension(ext="none"))
		m.preferencesFile = "bad"

	def test_properties(self):
		m = Core(ext=Extension(ext="none"))

		m.killLevel
		m.out
		m.extensionObjects
		m.extensionRegexs
		m.extensionPatterns
		m.preferences
		m.preferencesFile

	def test_properties_bad(self):
		self.assertRaises(AttributeError, self.attemptChange_killLevel)
		self.assertRaises(AttributeError, self.attemptChange_out)
		self.assertRaises(AttributeError, self.attemptChange_extensionObjects)
		self.assertRaises(AttributeError, self.attemptChange_extensionRegexs)
		self.assertRaises(AttributeError, self.attemptChange_extensionPatterns)
		self.assertRaises(AttributeError, self.attemptChange_preferences)
		self.assertRaises(AttributeError, self.attemptChange_preferencesFile)

	###########
	# __title__
	###########

	def test_title1(self):
		out = StringIO()
		c = Core(ext=Extension(ext="none"), out=out)

		c.__title__(title="Random Title")
		output = out.getvalue().strip()

		self.assertEqual(output,	"################################################################################\n" +
									"#                                 RANDOM TITLE                                 #\n" +
									"################################################################################")

	def test_title2(self):
		out = StringIO()
		c = Core(ext=Extension(ext="none"), out=out)

		c.__title__(title="a" * 100)
		output = out.getvalue().strip()

		self.assertEqual(output,	"################################################################################\n" +
									"# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA #\n" +
									"################################################################################")

	def test_title3(self):
		out = StringIO()
		c = Core(ext=Extension(ext="none"), out=out)

		self.assertRaises(ValueError, c.__title__, title=123)

	###########
	# __subtitle__
	###########

	def test_subtitle1(self):
		out = StringIO()
		c = Core(ext=Extension(ext="none"), out=out)

		c.__subtitle__(title="Random Subtitle")
		output = out.getvalue().strip()

		self.assertEqual(output,	"||                              RANDOM SUBTITLE                               ||\n" +
									"================================================================================")

	def test_subtitle2(self):
		out = StringIO()
		c = Core(ext=Extension(ext="none"), out=out)

		c.__subtitle__(title="a" * 100)
		output = out.getvalue().strip()

		self.assertEqual(output,	"|| AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA ||\n" +
									"================================================================================")

	def test_subtitle3(self):
		out = StringIO()
		c = Core(ext=Extension(ext="none"), out=out)

		self.assertRaises(ValueError, c.__subtitle__, title=123)

	###########
	# extensionNames
	###########

	def test_extensionNames1(self):
		c = Core(ext=Extension(ext="test"), prefFile=None)

		self.assertEqual(c.extensionPatterns, [r"\.test$"])

	def test_extensionNames2(self):
		c = Core(ext=[	Extension(ext="test1"),
						Extension(ext="test2"),
						Extension(ext="test3")	], prefFile=None)

		self.assertEqual(c.extensionPatterns, [r"\.test1$", r"\.test2$", r"\.test3$"])

	###########
	# extensionObjects
	###########

	def test_extensionObjects1(self):
		c = Core(ext=Extension(ext="test"), prefFile=None)

		self.assertEqual(all(isinstance(x, Extension) for x in c.extensionObjects), True)
		self.assertEqual(c.extensionObjects[0].extension, r"\.test$")

	def test_extensionObjects2(self):
		c = Core(ext=[	Extension(ext="test1"),
						Extension(ext="test2"),
						Extension(ext="test3")	], prefFile=None)

		self.assertEqual(all(isinstance(x, Extension) for x in c.extensionObjects), True)
		self.assertEqual(c.extensionObjects[0].extension, r"\.test1$")
		self.assertEqual(c.extensionObjects[1].extension, r"\.test2$")
		self.assertEqual(c.extensionObjects[2].extension, r"\.test3$")

	###########
	# __read__
	###########

	dataDir = "bibtex_merger/tests/data"

	def tRead(self, filename):
		with open(filename, "r") as f:
			return f.read()

		raise Exception

	def test_read(self):
		c = Core(ext=Extension(ext="txt", reader=self.tRead))

		self.assertEqual(c.__read__("{}/sample.txt".format(self.dataDir)), "Sample file with text")

	def test_read_bad_ext(self):
		c = Core(ext=Extension(ext="txt", reader=self.tRead))

		self.assertRaises(CoreError, c.__read__, "{}/sample.random".format(self.dataDir))

	###########
	# __write__
	###########

	def tWrite(self, filename, content):
		with open(filename, "w") as f:
			return f.write(content)

		raise Exception

	def test_writeread(self):
		c = Core(ext=Extension(ext="txt", reader=self.tRead, writer=self.tWrite))

		f = "sample2.txt"
		t = "Some random text to insert"

		c.__write__("{}/{}".format(self.dataDir, f), t)

		self.assertEqual(c.__read__("{}/{}".format(self.dataDir, f)), t)

		os.remove("{}/{}".format(self.dataDir, f))

	def test_write_bad_ext(self):
		c = Core(ext=Extension(ext="txt", reader=self.tRead, writer=self.tWrite))

		f = "sample2.random"
		t = "Some random text to insert"

		self.assertRaises(CoreError, c.__write__, "{}/{}".format(self.dataDir, f), t)

	###########
	# preferences
	###########

	def test_no_preferences_attemptreadwrite(self):
		c = Core(ext=Extension(ext="none"), prefFile=None)

		self.assertRaises(CoreError, c.__preferencesRead__)
		self.assertRaises(CoreError, c.__preferencesWrite__)

	###########
	# __preferencesRead__
	###########

	samplePrefSect = "Preferences"
	samplePrefItems = [('value1', 'Foo'), ('value2', 'Bar'), ('value3', '2015')]

	def test_preferencesRead(self):
		c = Core(ext=Extension(ext="none"), prefFile="{}/sample.cfg".format(self.dataDir))

		pref = c.__preferencesRead__()
		self.assertEqual(pref.sections(), [self.samplePrefSect])
		self.assertEqual(pref.items(self.samplePrefSect), self.samplePrefItems)

	###########
	# __preferencesWrite__
	###########

	def test_preferencesWrite1(self):
		f = "sample2.cfg"
		
		sect = "Random1"
		items = [("n1", "Foo"), ("n2", "Bar"), ("n3", "Baz")]

		c = Core(ext=Extension(ext="none"), prefFile="{}/{}".format(self.dataDir, f))

		pref = c.__preferencesRead__()

		pref.add_section(sect)
		for o, v in items:
			pref.set(sect, o, v)

		pref = c.__preferencesWrite__()

		pref = c.__preferencesRead__()
		self.assertEqual(pref.sections(), [sect])
		self.assertEqual(pref.items(sect), items)

		os.remove("{}/{}".format(self.dataDir, f))

	def test_preferencesWrite2(self):
		f = "sample.cfg"
		
		c = Core(ext=Extension(ext="none"), prefFile="{}/{}".format(self.dataDir, f))

		c.__preferencesWrite__()

		pref = c.__preferencesRead__()
		self.assertEqual(pref.sections(), [self.samplePrefSect])
		self.assertEqual(pref.items(self.samplePrefSect), self.samplePrefItems)

	###########
	# __info__
	###########

	def test_info(self):
		out = StringIO()
		c = Core(ext=Extension(ext="none"), out=out)

		c.__info__("just a message")
		output = out.getvalue().strip()

		self.assertEqual(output, "just a message")

	def test_info_bad(self):
		c = Core(ext=Extension(ext="none"))

		self.assertRaises(ValueError, c.__info__, 12345)

	###########
	# __warning__
	###########

	def test_warning1(self):
		out = StringIO()
		c = Core(ext=Extension(ext="none"), out=out, killLevel='error')

		c.__warning__(ValueError("just a message"))
		output = out.getvalue().strip()

		self.assertEqual(output, "WARNING: ValueError: just a message")

	def test_warning2(self):
		out = StringIO()
		c = Core(ext=Extension(ext="none"), out=out, killLevel='warning')

		self.assertRaises(ValueError, c.__warning__, ValueError("just a message"))

	def test_warning_bad(self):
		c = Core(ext=Extension(ext="none"))

		self.assertRaises(ValueError, c.__warning__, 12345)

	###########
	# __error__
	###########

	def test_error1(self):
		out = StringIO()
		c = Core(ext=Extension(ext="none"), out=out, killLevel='warning')

		self.assertRaises(ValueError, c.__error__, ValueError("just a message"))

	def test_error2(self):
		out = StringIO()
		c = Core(ext=Extension(ext="none"), out=out, killLevel='error')

		self.assertRaises(ValueError, c.__error__, ValueError("just a message"))

	def test_error_bad(self):
		c = Core(ext=Extension(ext="none"))

		self.assertRaises(ValueError, c.__error__, 12345)
		
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