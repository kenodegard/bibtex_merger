import unittest, sys, os, tempfile, shutil

python2 = sys.version_info < (3, 0, 0)

if python2:
    from StringIO import StringIO
else:
    from io import StringIO

from bibtex_merger.merger import *
from bibtex_merger.core import CoreError

class test_merger(unittest.TestCase):

	###########
	# Helpers
	###########

	def mergerAttemptImportDirChange(self):
		m = BibTeX_Merger()
		m.importDir = "blue"

	def mergerAttemptNumFilesChange(self):
		m = BibTeX_Merger()
		m.numFiles = "blue"

	def mergerAttemptKillLevelChange(self):
		m = BibTeX_Merger()
		m.killLevel = "blue"

	def mergerAttemptShallowDeepCompDivChange(self):
		m = BibTeX_Merger()
		m.shallowDeepCompDiv = "blue"

	def mergerAttemptSummedPercentErrorDivChange(self):
		m = BibTeX_Merger()
		m.summedPercentErrorDiv = "blue"

	def mergerAttemptLearningModelChange(self):
		m = BibTeX_Merger()
		m.learningModel = "blue"

	def mergerAttemptDoLearningChange(self):
		m = BibTeX_Merger()
		m.doLearning = "blue"

	def mergerAttemptThetaChange(self):
		m = BibTeX_Merger()
		m.theta = "blue"

	###########
	# __init__
	###########

	def test_base(self):
		BibTeX_Merger()

		BibTeX_Merger(importDir='.')
		BibTeX_Merger(importDir='bibtex_merger/tests/data')

		BibTeX_Merger(numFiles=-1)
		BibTeX_Merger(numFiles=10)

		BibTeX_Merger(shallowDeepCompDiv=3.4)
		BibTeX_Merger(shallowDeepCompDiv=3)

		BibTeX_Merger(summedPercentErrorDiv=[0.4, 1.0])
		BibTeX_Merger(summedPercentErrorDiv=[1, 10])

		BibTeX_Merger(learningModel='fminunc')
		BibTeX_Merger(learningModel='glmfit')

		BibTeX_Merger(doLearning='off')
		BibTeX_Merger(doLearning='remakeData')
		BibTeX_Merger(doLearning='remakeModel')

	def test_base_bad(self):
		self.assertRaises(ValueError, BibTeX_Merger, importDir=12345)
		self.assertRaises(ValueError, BibTeX_Merger, importDir='12345')

		self.assertRaises(ValueError, BibTeX_Merger, numFiles='12345')

		self.assertRaises(ValueError, BibTeX_Merger, shallowDeepCompDiv='12345')
		self.assertRaises(ValueError, BibTeX_Merger, shallowDeepCompDiv=-1)

		self.assertRaises(ValueError, BibTeX_Merger, summedPercentErrorDiv=12345)
		self.assertRaises(ValueError, BibTeX_Merger, summedPercentErrorDiv=-1)
		self.assertRaises(ValueError, BibTeX_Merger, summedPercentErrorDiv=['12', 345])
		self.assertRaises(ValueError, BibTeX_Merger, summedPercentErrorDiv=[12, -1])

		self.assertRaises(ValueError, BibTeX_Merger, learningModel=12345)
		self.assertRaises(ValueError, BibTeX_Merger, learningModel='12345')

		self.assertRaises(ValueError, BibTeX_Merger, doLearning=12345)
		self.assertRaises(ValueError, BibTeX_Merger, doLearning='12345')

	###########
	# Properties
	###########

	def test_importDir(self):
		m = BibTeX_Merger()

		m.importDir
		self.assertRaises(AttributeError, self.mergerAttemptImportDirChange)

	def test_numFiles(self):
		m = BibTeX_Merger()

		m.numFiles
		self.assertRaises(AttributeError, self.mergerAttemptNumFilesChange)

	def test_killLevel(self):
		m = BibTeX_Merger()

		m.killLevel
		self.assertRaises(AttributeError, self.mergerAttemptKillLevelChange)

	def test_shallowDeepCompDiv(self):
		m = BibTeX_Merger()

		m.shallowDeepCompDiv
		self.assertRaises(AttributeError, self.mergerAttemptShallowDeepCompDivChange)

	def test_summedPercentErrorDiv(self):
		m = BibTeX_Merger()

		m.summedPercentErrorDiv
		self.assertRaises(AttributeError, self.mergerAttemptSummedPercentErrorDivChange)

	def test_theta(self):
		m = BibTeX_Merger()

		m.theta
		self.assertRaises(AttributeError, self.mergerAttemptThetaChange)

	def test_learningModel(self):
		m = BibTeX_Merger()

		m.learningModel
		self.assertRaises(AttributeError, self.mergerAttemptLearningModelChange)

	def test_doLearning(self):
		m = BibTeX_Merger()

		m.doLearning
		self.assertRaises(AttributeError, self.mergerAttemptDoLearningChange)

	###########
	# Bib Extension
	###########

	dataDir = "bibtex_merger/tests/data"

	def test_bib_extension_read(self):
		m = BibTeX_Merger()

		m.__read__("{}/sample.bib".format(self.dataDir))

	def test_csv_extension_read(self):
		m = BibTeX_Merger()

		m.__read__("{}/sample.csv".format(self.dataDir))

	def test_csv_extension_write_matrix(self):
		m = BibTeX_Merger()

		f = "sample2.csv"
		c = [['1','2','3','4','5'],['6','7','8','9','0']]

		m.__write__("{}/{}".format(self.dataDir, f), c)

		c2 = m.__read__("{}/{}".format(self.dataDir, f))

		self.assertEquals(c, c2)

		os.remove("{}/{}".format(self.dataDir, f))

	def test_csv_extension_write_vector(self):
		m = BibTeX_Merger()

		f = "sample2.csv"
		c = ['1','2','3','4','5','6','7','8','9','0']

		m.__write__("{}/{}".format(self.dataDir, f), c)

		c2 = m.__read__("{}/{}".format(self.dataDir, f))

		self.assertEquals([c], c2)

		os.remove("{}/{}".format(self.dataDir, f))

	def test_csv_extension_write_bad1(self):
		m = BibTeX_Merger()

		f = "sample2.csv"
		c = []

		self.assertRaises(MergerError, m.__write__, "{}/{}".format(self.dataDir, f), c)

	def test_csv_extension_write_bad2(self):
		m = BibTeX_Merger()

		f = "sample2.csv"
		c = "nonlist"

		self.assertRaises(MergerError, m.__write__, "{}/{}".format(self.dataDir, f), c)

	def test_csv_extension_write_bad3(self):
		m = BibTeX_Merger()

		f = "sample2.csv"
		c = None

		self.assertRaises(MergerError, m.__write__, "{}/{}".format(self.dataDir, f), c)

	###########
	# __run__
	###########

	def test_run(self):
		m = BibTeX_Merger(importDir=self.dataDir)

		m.__run__()

	###########
	# Import
	###########

	def test_Import(self):
		m = BibTeX_Merger(importDir=self.dataDir)

		m.Import()

	def test_Import_no_files(self):
		m = BibTeX_Merger()

		self.assertRaises(MergerError, m.Import)

	def test_Import_mutliple_files_same_basename(self):
		tdir = tempfile.mkdtemp()

		with open("{}/sample.bib".format(self.dataDir), "r") as o:
			c = o.read()
			with open("{}/sampleBib 1.bib".format(tdir), "w") as f:
				f.write(c)

			with open("{}/sampleBib:1.bib".format(tdir), "w") as f:
				f.write(c)

			with open("{}/sampleBib_1.bib".format(tdir), "w") as f:
				f.write(c)

		m = BibTeX_Merger(importDir=tdir)

		m.Import()

		shutil.rmtree(tdir)

	def test_Import_bad_bib(self):
		c = """@article(small,
author = {Qux, B.},
title = {A small paper},
journal = {The journal of small papers},
year = 2015,
volume = {-1},
note = {to appear}

@@article{big,
author = {Bar, Foo},
title = {A big paper},
journal = {The journal of big papers},
year = 5102
volume = {MMXV,
}

"""

		tdir = tempfile.mkdtemp()

		with open("{}/sampleBib 1.bib".format(tdir), "w") as f:
			f.write(c)

		m = BibTeX_Merger(importDir=tdir)

		self.assertRaises(MergerError, m.Import)

		shutil.rmtree(tdir)

	###########
	# Bagging
	###########

	def test_Bagging(self):
		m = BibTeX_Merger(importDir=self.dataDir)

		m.Import()
		m.Bagging()

	###########
	# ShallowCompare
	###########

	def test_ShallowCompare(self):
		m = BibTeX_Merger(importDir=self.dataDir)

		m.Import()
		m.Bagging()
		m.ShallowCompare()

