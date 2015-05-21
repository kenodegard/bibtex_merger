import unittest

from bibtex_merger.extension import *

class TestExtension(unittest.TestCase):

	def tRead(self, *args, **kwargs):
		return "READING"

	def tWrite(self, *args, **kwargs):
		return "WRITING"

	###########
	# Extension
	###########
	def test_Extension_base(self):
		testExt = Extension(ext="test", reader=self.tRead, writer=self.tWrite)
		self.assertEqual(testExt.extension, ".test")
		self.assertEqual(testExt.read(), "READING")
		self.assertEqual(testExt.write(), "WRITING")

	def test_Extension_no_extension(self):
		testExt = Extension(reader=self.tRead, writer=self.tWrite)
		self.assertEqual(testExt.extension, ".*")
		self.assertEqual(testExt.read(), "READING")
		self.assertEqual(testExt.write(), "WRITING")

	def test_Extension_no_read(self):
		testExt = Extension(ext="test", writer=self.tWrite)
		self.assertEqual(testExt.extension, ".test")
		self.assertEqual(testExt.write(), "WRITING")
		self.assertRaises(ExtensionError, testExt.read)

	def test_Extension_no_write(self):
		testExt = Extension(ext="test", reader=self.tRead)
		self.assertEqual(testExt.extension, ".test")
		self.assertEqual(testExt.read(), "READING")
		self.assertRaises(ExtensionError, testExt.write)

	def test_Extension_bad_extension(self):
		self.assertRaises(ValueError, Extension, ext=12345, reader=self.tRead, writer=self.tWrite)

	def test_Extension_bad_read(self):
		self.assertRaises(ValueError, Extension, ext="test", reader="bad reader", writer=self.tWrite)

	def test_Extension_bad_write(self):
		self.assertRaises(ValueError, Extension, ext="test", reader=self.tRead, writer="bad writer")

	###########
	# ExtensionError
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
			raise ExtensionError(ext="test", state=ExtensionError.READ)
		except ExtensionError as e:
			self.assertEqual(str(e), "Attempted to read an unsupported file format (.test)")

		try:
			raise ExtensionError(ext="test", state=ExtensionError.WRITE)
		except ExtensionError as e:
			self.assertEqual(str(e), "Attempted to write an unsupported file format (.test)")

		try:
			raise ExtensionError(ext="test", state=ExtensionError.GENERAL)
		except ExtensionError as e:
			self.assertEqual(str(e), "Attempted to use an unsupported file format (.test)")

	def extErrorMessyState(self):
		ee = ExtensionError(ext="test", state=ExtensionError.READ)
		ee.state = -1
		raise ee

	def test_ExtensionError_catching_bad_state(self):
		self.assertRaises(ValueError)


if __name__ == '__main__':
	unittest.main()