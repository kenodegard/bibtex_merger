import unittest

from bibtex_merger.extension import *

class test_extension(unittest.TestCase):

	###########
	# Helpers
	###########

	def tRead(self, filename):
		return "READING"

	def tWrite(self, filename, content):
		return "WRITING"

	def extensionAttemptExtensionChange(self):
		testExt = Extension(ext="test", reader=self.tRead, writer=self.tWrite)
		testExt.extension = "blue"

	def extensionAttemptReextensionChange(self):
		testExt = Extension(ext="test", reader=self.tRead, writer=self.tWrite)
		testExt.reextension = "blue"

	def extensionAttemptReaderChange(self):
		testExt = Extension(ext="test", reader=self.tRead, writer=self.tWrite)
		testExt.reader = "blue"

	def extensionAttemptWriterChange(self):
		testExt = Extension(ext="test", reader=self.tRead, writer=self.tWrite)
		testExt.writer = "blue"

	###########
	# __init__
	###########

	def test_Extension_base(self):
		testExt = Extension(ext="test", reader=self.tRead, writer=self.tWrite)
		self.assertEqual(testExt.extension, r"\.test$")
		self.assertEqual(testExt.read("sample.test"), "READING")
		self.assertEqual(testExt.write("sample.test", None), "WRITING")

	def test_Extension_no_extension(self):
		testExt = Extension(reader=self.tRead, writer=self.tWrite)

		self.assertEqual(testExt.extension, r"\..*$")

		self.assertEqual(testExt.read("sample.test"), "READING")
		self.assertEqual(testExt.write("sample.test", None), "WRITING")

		self.assertEqual(testExt.read("sample.andthis"), "READING")
		self.assertEqual(testExt.write("sample.andthis", None), "WRITING")

		self.assertEqual(testExt.read("sample.butthat"), "READING")
		self.assertEqual(testExt.write("sample.butthat", None), "WRITING")

	def test_Extension_no_read(self):
		testExt = Extension(ext="test", writer=self.tWrite)
		self.assertEqual(testExt.extension, r"\.test$")
		self.assertEqual(testExt.write("sample.test", None), "WRITING")
		self.assertRaises(ExtensionError, testExt.read, "sample.test")

	def test_Extension_no_write(self):
		testExt = Extension(ext="test", reader=self.tRead)
		self.assertEqual(testExt.extension, r"\.test$")
		self.assertEqual(testExt.read("sample.test"), "READING")
		self.assertRaises(ExtensionError, testExt.write, "sample.test", None)

	def test_Extension_no_readwrite(self):
		testExt = Extension(ext="test")
		self.assertEqual(testExt.extension, r"\.test$")
		self.assertRaises(ExtensionError, testExt.read, "sample.test")
		self.assertRaises(ExtensionError, testExt.write, "sample.test", None)

	def test_Extension_bad_extension(self):
		self.assertRaises(ValueError, Extension, ext=12345, reader=self.tRead, writer=self.tWrite)

	def test_Extension_bad_read(self):
		self.assertRaises(ValueError, Extension, ext="test", reader="bad reader", writer=self.tWrite)

	def test_Extension_bad_write(self):
		self.assertRaises(ValueError, Extension, ext="test", reader=self.tRead, writer="bad writer")

	###########
	# read
	###########

	def test_Extension_invalid_ext_read(self):
		testExt = Extension(ext="test", reader=self.tRead, writer=self.tWrite)

		self.assertRaises(ExtensionError, testExt.read, filename="sample.txt")

	###########
	# write
	###########

	def test_Extension_invalid_ext_write(self):
		testExt = Extension(ext="test", reader=self.tRead, writer=self.tWrite)

		self.assertRaises(ExtensionError, testExt.write, filename="sample.txt", content=None)

	###########
	# extension
	###########

	def test_Extension_extension_change(self):
		self.assertRaises(AttributeError, self.extensionAttemptExtensionChange)

	###########
	# reextension
	###########

	def test_Extension_extension_change(self):
		self.assertRaises(AttributeError, self.extensionAttemptReextensionChange)

	###########
	# reader
	###########

	def test_Extension_extension_change(self):
		self.assertRaises(AttributeError, self.extensionAttemptReaderChange)

	###########
	# writer
	###########

	def test_Extension_extension_change(self):
		self.assertRaises(AttributeError, self.extensionAttemptWriterChange)

class test_extension_error(unittest.TestCase):

	###########
	# Helpers
	###########

	def extError(self, ext=None, state=None):
		if ext != None and state != None:
			raise ExtensionError(ext=ext, state=state)
		elif ext != None:
			raise ExtensionError(ext=ext)
		elif state != None:
			raise ExtensionError(state=state)
		else:
			raise ExtensionError()

	def extErrorAttemptExtChange(self):
		ee = ExtensionError(ext="test", state=ExtensionError.READ)
		ee.ext = "blue"
		raise ee

	def extErrorAttemptStateChange(self):
		ee = ExtensionError(ext="test", state=ExtensionError.READ)
		ee.state = -1
		raise ee

	###########
	# __init__
	###########

	def test_ExtensionError_base(self):
		self.assertRaises(ExtensionError, self.extError, ext="test", state=ExtensionError.READ)
		self.assertRaises(ExtensionError, self.extError, ext="test", state=ExtensionError.WRITE)
		self.assertRaises(ExtensionError, self.extError, ext="test", state=ExtensionError.GENERAL)

	def test_ExtensionError_no_extension(self):
		self.assertRaises(ExtensionError, self.extError, state=ExtensionError.READ)
		self.assertRaises(ExtensionError, self.extError, state=ExtensionError.WRITE)
		self.assertRaises(ExtensionError, self.extError, state=ExtensionError.GENERAL)

	def test_ExtensionError_no_state(self):
		self.assertRaises(ValueError, self.extError, ext="test")

	def test_ExtensionError_bad_extension(self):
		self.assertRaises(ValueError, self.extError, ext=12345, state=ExtensionError.READ)
		self.assertRaises(ValueError, self.extError, ext=12345, state=ExtensionError.WRITE)
		self.assertRaises(ValueError, self.extError, ext=12345, state=ExtensionError.GENERAL)

	def test_ExtensionError_bad_state(self):
		self.assertRaises(ValueError, self.extError, ext="test", state=-1)

	def test_ExtensionError_catching(self):
		try:
			raise ExtensionError(ext="SOMESTRING", state=ExtensionError.READ)
		except ExtensionError as e:
			self.assertEqual(str(e), "Attempted to read an unsupported file format (SOMESTRING)")

		try:
			raise ExtensionError(ext="SOMESTRING", state=ExtensionError.WRITE)
		except ExtensionError as e:
			self.assertEqual(str(e), "Attempted to write an unsupported file format (SOMESTRING)")

		try:
			raise ExtensionError(ext="SOMESTRING", state=ExtensionError.GENERAL)
		except ExtensionError as e:
			self.assertEqual(str(e), "Attempted to use an unsupported file format (SOMESTRING)")

	###########
	# ext
	###########

	def test_ExtensionError_ext_change(self):
		self.assertRaises(AttributeError, self.extErrorAttemptExtChange)

	###########
	# state
	###########

	def test_ExtensionError_state_change(self):
		self.assertRaises(AttributeError, self.extErrorAttemptStateChange)


if __name__ == '__main__':
	unittest.main()