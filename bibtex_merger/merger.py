import bibtexparser as bp

import Levenshtein as le
import fuzzy as fz

import numpy

import scipy.misc as ch

from sklearn import linear_model
from sklearn.cross_validation import train_test_split
# from scipy import misc as ch
# import gmpy2 as ch

import re, csv, os, threading, logging
from sys import argv
from datetime import *
from collections import OrderedDict
import ConfigParser, logging

from bibtex_merger.core import *
from bibtex_merger.extension import *

logger = logging.getLogger(__name__)
__all__ = [	'BibTeX_Merger'	]

class BibTeX_Merger(Core):
	def __init__(self,	numFiles = -1,
						importDir = '.',
						killLevel = 'warning',
						shallowDeepCompDiv = 3.4,
						summedPercentErrorDiv = [0.4, 1.0],
						learningModel = 'fminunc',
						doLearning = 'remakeModel'):
		super(BibTeX_Merger, self).__init__(self.__initExtensions__())

		self.__initConstants__()

		# Optionally passed flag from command line that specifies how many files to use
		# If set to -1 (default) then all files in the data/0_original/ directory will be used
		if not isinstance(numFiles, int):
			raise ValueError("BibTeX_Merger numFiles argument requires int not ({})".format(type(numFiles)))
		self._numFiles = numFiles

		if not isinstance(importDir, str) and os.path.isdir(importDir):
			raise ValueError("BibTeX_Merger importDir argument requires str to a directory not ({} -> {})".format(type(importDir), importDir))
		self._importDir = importDir

		# Verbose level that optionally prints more debugging code'
		if not isinstance(killLevel, str) and killLevel in self.killLevel:
			raise ValueError("BibTeX_Merger killLevel argument must be {} not ({} -> {})".format("|".join(self.killLevel), type(killLevel), killLevel))
		self._killLevel = self.killLevel[killLevel]

		# The manually decided breakpoints
		if not (isinstance(shallowDeepCompDiv, int) or isinstance(shallowDeepCompDiv, float)) and shallowDeepCompDiv < 0:
			raise ValueError("BibTeX_Merger shallowDeepCompDiv argument must be int|float > 0 not ({} -> {})".format(type(shallowDeepCompDiv), shallowDeepCompDiv))
		self._shallowDeepCompDiv = shallowDeepCompDiv

		# Lower and Upper breakpoints, everything lower than lower is assumed duplicate,
		# everything greater than upper is assumed unique
		if not isinstance(summedPercentErrorDiv, list) and not all(isinstance(x, int) or isinstance(x, float) for x in summedPercentErrorDiv) and not all(x > 0 for x in summedPercentErrorDiv):
			raise ValueError("BibTeX_Merger summedPercentErrorDiv argument must be a list of int|float > 0 not ({} -> {})".format(type(summedPercentErrorDiv), summedPercentErrorDiv))
		self._summedPercentErrorDiv = summedPercentErrorDiv

		# Sample fminunc theta
		# self.theta = numpy.array([0.419, 1.036, -3.089,  0.025, -0.387,  0.943,  0.625, -3.326, -2.256, -1.798, 0.536, 1.777,  0.713, -0.026, -1.271,  0.215,  1.444, -12.533, -9.778, -2.590, -1.522])
		# Sample glmfit theta
		self._theta = numpy.array([200.064, 1.192, -3.152, 33.034, 0.000, 0.985, 80.515, -3.527, -2.330, -1.916, 0.006, 1.863, 0.149, -0.108, -1.397, 87.715, 1.519, -13.372, -10.149, -2.609, -1.637])

		# Learning model to use
		# available options: fminunc | glmfit
		if not isinstance(learningModel, str) and learningModel in self.learningModel:
			raise ValueError("BibTeX_Merger learningModel argument must be {} not ({} -> {})".format("|".join(self.learningModel), type(learningModel), learningModel))
		self._learningModel = self.learningModels[learningModel]

		# What to do in this instance of code execution
		# available options: off | remakeData | remakeModel
		if not isinstance(doLearning, str) and doLearning in self.doLearning:
			raise ValueError("BibTeX_Merger doLearning argument must be {} not ({} -> {})".format("|".join(self.doLearning), type(doLearning), doLearning))
		self._doLearning = self.doLearnings[doLearning]

		# self.__run__()

		return

	@property
	def numFiles(self):
		return self._numFiles

	@property
	def importDir(self):
		return self._importDir
	
	@property
	def killLevel(self):
		return self._killLevel
	
	@property
	def shallowDeepCompDiv(self):
		return self._shallowDeepCompDiv
	
	@property
	def summedPercentErrorDiv(self):
		return self._summedPercentErrorDiv

	@property
	def theta(self):
		return self._theta

	@property
	def learningModel(self):
		return self._learningModel

	@property
	def doLearning(self):
		return self._doLearning

	def __initExtensions__(self):
		def cfgRead(filename):
			config = ConfigParser.RawConfigParser()
			config.read(filename)
			return config
		def cfgWrite(filename, content):
			with open(filename, 'wb') as f:
				return content.write(f)
		cfgExt = Extension(ext=r'cfg', reader=cfgRead, writer=cfgWrite)

		def bibRead(filename):
			with open(filename, 'r') as f:
				return bp.load(f, parser=self.parser)
		bibExt = Extension(ext=r'bib', reader=bibRead)

		def csvRead(filename):
			with open(filename) as f:
				return [e for e in csv.reader(f)]
		def csvWrite(filename, content):
			with open(filename, 'wb') as f:
				filecontent = csv.writer(f)

				if type(content) != None:
					if isinstance(content, list):
						if len(content) > 0:
							if isinstance(content[0], list):
								# Matrix, List of lists
								filecontent.writerows(content)
							else:
								# Vector, List
								filecontent.writerow(content)
					return

				raise ProgramError("CSV content has bad format, write failed")
		csvExt = Extension(ext=r'csv', reader=csvRead, writer=csvWrite)

		return [cfgExt, bibExt, csvExt]

	def __initConstants__(self):
		self.logger = logging.getLogger(__name__)

		self.killLevel = ['warning', 'error']
		self.killLevel = dict((v,k) for k, v in enumerate(self.killLevel))

		self.doLearnings = ['off', 'remakeData', 'remakeModel']
		self.doLearnings = dict((v,k) for k, v in enumerate(self.doLearnings))

		self.learningModels = ['fminunc', 'glmfit']
		self.learningModels = dict((v,k) for k, v in enumerate(self.learningModels))

		self.parser = bp.bparser.BibTexParser()
		self.parser.customization = self.__customizations__

		self.id = "ID"
		self.author = "author"
		self.title = "title"
		self.key = "key"

		self.label = "label"

		self.mapToUnderscore = ''.join(chr(c) if chr(c).isupper() or chr(c).islower() or chr(c).isdigit() else '_' for c in range(256))

		# Static vars
		self.entry_types     = {	"STRING":			{
														},
									"PREAMBLE":			{
														},
									"ARTICLE":			{	"requires": ["author", "title", "journal", "year"],
															"optional": ["volume", "number", "pages", "month", "note", "key"],
														},
									"BOOK":				{	"requires": [["author", "editor"], "title", "publisher", "year"],
															"optional": ["volume", "series", "address", "edition", "month", "note", "key"],
														},
									"BOOKLET":			{	"requires": ["title"],
															"optional": ["author", "howpublished", "address", "month", "year", "note", "key"],
														},
									"CONFERENCE":		{	"requires": ["author", "title", "booktitle", "year"],
															"optional": ["editor", "pages", "organization", "publisher", "address", "month", "note", "key"],
														},
									"INPROCEEDINGS":	{	"requires": ["author", "title", "booktitle", "year"],
															"optional": ["editor", "pages", "organization", "publisher", "address", "month", "note", "key"],
														},
									"INBOOK":			{	"requires": [["author", "editor"], "title", ["chapter", "pages"], "publisher", "year"],
															"optional": ["volume", "series", "address", "edition", "month", "note", "key"],
														},
									"INCOLLECTION":		{	"requires": ["author", "title", "booktitle", "year"],
															"optional": ["editor", "pages", "organization", "publisher", "address", "month", "note", "key"],
														},
									"MANUAL":			{	"requires": ["title"],
															"optional": ["author", "organization", "address", "edition", "month", "year", "note", "key"],
														},
									"MASTERSTHESIS": 	{	"requires": ["author", "title", "school", "year"],
															"optional": ["address", "month", "note", "key"],
														},
									"MISC":				{	"requires": [],
															"optional": ["author", "title", "howpublished", "month", "year", "note", "key"],
														},
									"PHDTHESIS":		{	"requires": ["author", "title", "school", "year"],
															"optional": ["address", "month", "note", "key"],
														},
									"PROCEEDINGS":		{	"requires": ["title", "year"],
															"optional": ["editor", "publisher", "organization", "address", "month", "note", "key"],
														},
									"TECHREPORT":		{	"requires": ["author", "title", "institution", "year"],
															"optional": ["type", "number", "address", "month", "note", "key"],
														},
									"UNPUBLISHED":		{	"required": ["author", "title", "note"],
															"optional": ["month", "year", "key"],
														},
								}
		self.defaultKeysToDeepComp = set()
		for k, d in self.entry_types.iteritems():
			for k2, l in d.iteritems():
				for i in l:
					if type(i) is type(str()):
						self.defaultKeysToDeepComp = self.defaultKeysToDeepComp.union(set([i]))
					else:
						self.defaultKeysToDeepComp = self.defaultKeysToDeepComp.union(set(i))
		self.defaultKeysToDeepComp.remove(self.author)
		self.defaultKeysToDeepComp.remove(self.key)
		# self.defaultKeysToDeepComp.remove(self.id)

		self.defaultKeysToDeepCompSorted = list(self.defaultKeysToDeepComp)
		self.defaultKeysToDeepCompSorted.sort()
		
		self.originalDir	= "../data/0_original"
		self.learningDir	= "../data/2_prelearning"
		self.installDir		= "~/.bibtex_merger"

		self.configFile		= ".pref.cfg"

		# self.reRemComment = re.compile(r'@COMMENT.*', re.IGNORECASE)
		# self.reSplit=re.compile(r'(?=(?:' + '|'.join(["@" + et for et in self.entry_types.keys()]) + r'))',re.IGNORECASE)

		return

	def __run__(self):
		self.Import()
		self.PreProcessor()
		self.Bagging()
		self.ShallowCompare()

		if self.doLearning != self.doLearnings['off']:
			self.Learner()

		return

	def __customizations__(self, record):
		# This is a formating specification of the BibtexParser package
		# see https://bibtexparser.readthedocs.org/en/latest/bibtexparser.html#module-customization

		# record = bp.customization.homogenize_latex_encoding(record)

		record = bp.customization.type(record)
		record = bp.customization.author(record)
		# record = bp.customization.editor(record)
		# record = bp.customization.journal(record)
		# record = bp.customization.keyword(record)
		# record = bp.customization.page_double_hyphen(record)
		
		return record

	def Import(self):
		self.__title__("Import")

		importDirFiles = [f for f in os.listdir(self.importDir) if os.path.isfile(os.path.join(self.importDir, f)) and os.path.splitext(f)[1] == ".bib"]

		maxNumFiles = len(importDirFiles)
		if maxNumFiles == 0:
			raise UserError("No files were imported. Need at least one.")

		# determine whether we are only reading in the first subset or whether we are reading in the maximum
		self.numFiles = maxNumFiles if self.numFiles < 0 else min(self.numFiles, maxNumFiles)

		# self.db = None
		self.db = bp.bibdatabase.BibDatabase()

		lengths = []

		self.tags = []
		for filename in importDirFiles[0:self.numFiles]:
			self.__subtitle__("Importing '{}'".format(filename))

			# pull out the filename w/o the extension
			# map any non-alpha-numeric to '_'
			coreFN = filename[:filename.index(".")]
			coreFN = coreFN.translate(self.mapToUnderscore)

			# find a unique tag (this should rarely occur)
			while coreFN in self.tags:
				coreFN += "_"

			# try to import the specified file and parse
			try:
				temp_db = self.__read__(self.originalDir, filename)

				# append all ids in the entries dictionary with this file's unique tag
				# s.t. all resulting ids are entirely unique w/r to all of the imported files
				for i, e in enumerate(temp_db.entries):
					if self.id not in e.keys():
						raise BibTeXParserError("'{}' key not in this entry ({})".format(self.id, e.keys()))

					e[self.id] = "{}_{}".format(coreFN, e[self.id])

				# append all ids in the string dictionary with this file's unique tag
				# s.t. all resulting ids are entirely unique w/r to all of the imported files
				temp_strings = OrderedDict()
				for k, v in temp_db.strings.iteritems():
					newID = "{}_{}".format(coreFN, k)
					temp_strings[newID] = v
				temp_db.strings = temp_strings

				self.tags += coreFN
			except ValueError:
				self.logger.warning("This file ({}) has formatting errors and could not be parsed. Skipping.".format(filename))

			if not self.db:
				self.db = temp_db
			else:
				# merge the following from the current temp_dic to the master self.db
				self.db.entries += temp_db.entries
				self.db.comments += temp_db.comments
				self.db.preambles += temp_db.preambles
				self.db.strings.update(temp_db.strings)

			lengths.append(len(temp_db.entries))

		return

	def PreProcessor(self):
		self.__title__("PreProcessor")

		# Noisy First and/or Last Names
		# Mistakenly Separated and/or Merged Name Units

		return

	def Bagging(self):
		self.__title__("Bagging")

		# Bagging based on initials
		
		# pull out author entires
		self.db_fixed     = [e for e in self.db.entries if self.author     in e.keys() and not (e[self.author][-1][-1] == "others")]
		self.db_etal      = [e for e in self.db.entries if self.author     in e.keys() and     (e[self.author][-1][-1] == "others")]

		# pull out non-author entries
		self.db_nonauthor = [e for e in self.db.entries if self.author not in e.keys()]

		print("db_fixed:      ", len(self.db_fixed))
		print("db_etal:       ", len(self.db_etal))
		print("db_nonauthor:  ", len(self.db_nonauthor))

		print("")
		print("by none split costs")
		# print("(num entries)", len(self.db_fixed) + len(self.db_etal))
		bc = len(self.db_fixed) + len(self.db_etal)
		print("best-case:", bc, ch.comb(bc, 2))
		wc = bc
		print("worst-case:", wc, ch.comb(wc, 2))

		self.bagged = {}
		for e in self.db_fixed:
			try:
				numAuthors = len(e[self.author])

				if numAuthors not in self.bagged:
					self.bagged[numAuthors] = [e]
				else:
					self.bagged[numAuthors].append(e)
			except IndexError:
				if self.killLevel:
					print("ERROR: fixed num: skipping ({})".format(e[self.author]))

		for e in self.db_etal:
			try:
				numAuthors = len(e[self.author])

				for k in self.bagged.keys():
					if numAuthors <= k:
						self.bagged[k].append(e)

				if numAuthors not in self.bagged:
					self.bagged[numAuthors] = [e]
				else:
					self.bagged[numAuthors].append(e)
			except IndexError:
				if self.killLevel:
					print("ERROR: etal num: skipping ({})".format(e[self.author]))

		print("")
		print("by # authors split costs")
		# print("(len: num entries)", [[i, len(e)] for i, e in self.bagged.iteritems()])
		bc = min([len(e) for i, e in self.bagged.iteritems()])
		print("best-case:", bc, ch.comb(bc, 2))
		wc = max([len(e) for i, e in self.bagged.iteritems()])
		print("worst-case:", wc, ch.comb(wc, 2))

		for groupID, groupValues in dict(self.bagged).iteritems():
			alphaBagged = {}

			for e in groupValues:
				try:
					letter = ""
					for a in e[self.author]:
						if a[1] != "others":
							letter += a[0][0].lower()
							letter += a[1][0].lower()
						# else:
						# 	print("ignore 'others' author")

					added = False
					for key in [key for key in alphaBagged.keys() if key.find(letter) == 0]:
						added = True
						alphaBagged[key].append(e)

					if not added:
						if letter not in alphaBagged:
							alphaBagged[letter] = [e]
						else:
							alphaBagged[letter].append(e)
				except IndexError:
					if self.killLevel:
						print("ERROR: letter: skipping ({})".format(e[self.author]))

			self.bagged[groupID] = alphaBagged

		print("")
		print("by # authors and alpha key split costs")
		# print("(len: (alpha: num entries))", [[i, [[a, len(e)] for a, e in d.iteritems()]] for i, d in self.bagged.iteritems()])
		bc = min([min([len(e) for a, e in d.iteritems()]) for i, d in self.bagged.iteritems()])
		print("best-case:", bc, ch.comb(bc, 2))
		wc = max([max([len(e) for a, e in d.iteritems()]) for i, d in self.bagged.iteritems()])
		print("worst-case:", wc, ch.comb(wc, 2))

		return

	def ShallowCompare(self):
		self.__title__("Shallow Compare")

		lenSoundex = 10
		soundex = fz.Soundex(lenSoundex)

		combDist = {}
		numComp = {}
		self.deepComp = {}
		self.learning = []
		# self.learningKeys = set()
		self.allPredictions = []
		self.allPredictionsClass = []

		self.shallowCompares = 0
		self.deepCompares = 0
		self.maxCompares = sum([sum([ch.comb(len(e), 2) for a, e in d.iteritems() if len(e) > 1]) for i, d in self.bagged.iteritems()])

		for lenID, lenDic in self.bagged.iteritems():
			numComp[lenID] = {}
			for alphaID, entries in lenDic.iteritems():
				numComp[lenID][alphaID] = 0
				for e1 in xrange(0, len(entries)):
					entry1 = entries[e1]
					# authors1 = [l + ", " + f for f, l in entry1[self.author]]
					authors1 = entry1[self.author]

					lenAuthors1 = len(authors1)
					if "others" in authors1[-1]:
						lenAuthors1 -= 1


					for e2 in xrange(e1 + 1, len(entries)):

						self.shallowCompares += 1

						try: 
							entry2 = entries[e2]
							# authors2 = [l + ", " + f for f, l in entry2[self.author]]
							authors2 = entry2[self.author]

							lenAuthors2 = len(authors2)
							if "others" in authors2[-1]:
								lenAuthors2 -= 1
							
							numCompare = min(lenAuthors1, lenAuthors2)

							editDistance = 0
							phonDistance = 0
							for compareIndex in xrange(0, numCompare):
								a1 = authors1[compareIndex]
								a2 = authors2[compareIndex]

								f1 = a1[0]
								l1 = a1[1]
								f2 = a2[0]
								l2 = a2[1]

								if f1[1] == '.' or f2[1] == '.':
									# one of the authors' first name is an abbreviation
									# hence a perfect match
									editDistance += 1
									phonDistance += 1
								else:
									# neither first name is an abbreviation
									# test for similarity
									editDistance += le.jaro_winkler(f1, f2)
									phonDistance += 1.0 - (le.distance(soundex(f1), soundex(f2)) / float(lenSoundex))

								editDistance += le.jaro_winkler(l1, l2)
								phonDistance += 1.0 - (le.distance(soundex(l1), soundex(l2)) / float(lenSoundex))

							editDistance /= numCompare
							phonDistance /= numCompare


							if (editDistance * phonDistance) >= self.shallowDeepCompDiv:
								# print("COMPARE", editDistance, phonDistance, editDistance * phonDistance, authors1, authors2)
								self.DeepCompare(entry1, entry2)
								numComp[lenID][alphaID] += 1


							combDist[editDistance * phonDistance] = [authors1, authors2]
						except UnicodeEncodeError:
							if self.killLevel:
								print("ERROR: skipping")

		
		# statistical output
		# maxDistance = combDist.keys()
		# maxDistance.sort()

		# for m in xrange(0, len(maxDistance)):
		# 	maxD = maxDistance[m]

		# 	print("combDist:", maxD)
		# 	print("authors1:", combDist[maxD][0])
		# 	print("authors2:", combDist[maxD][1])
		# 	print("")

		# 
		print("")
		print("deep compare done")
		bc = min([min([n for a, n in d.iteritems()]) for l, d in numComp.iteritems()])
		print("best-case:", bc)
		wc = max([max([n for a, n in d.iteritems()]) for l, d in numComp.iteritems()])
		print("worst-case:", wc)

		print("")
		print("predictions")
		print("# duplicate matches:", sum(self.allPredictionsClass))
		print("# of deep comparisons:", self.deepCompares)
		print("# of shallow comparisons:", self.shallowCompares)
		print("max # comparisons:", self.maxCompares)
		print("")

		return

	def DeepCompare(self, entry1, entry2):
		# self.__title__("deepCompare")

		self.deepCompares += 1

		try:
			keys1 = entry1.keys()
			keys2 = entry2.keys()

			keysToComp = set(keys1).intersection(set(keys2))
			keysToComp = keysToComp.intersection(self.defaultKeysToDeepComp)

			l = {}
			for k in keysToComp:
				v1 = entry1[k]
				v2 = entry2[k]

				if v1 and v2:
					l[k] = le.distance(v1, v2) / float(max(len(v1), len(v2)))
			
			if self.doLearning == self.doLearnings['remakeData']:
				sv = sum(l.values())
				if sv <= self.summedPercentErrorDiv[0]:
					# assume identical due to very low summed percent error
					l[self.label] = 1
				elif self.summedPercentErrorDiv[1] <= sv:
					# assume unique due to very high summed percent error
					l[self.label] = 0
				else:
					# prompt user to decide this gray area
					label = None
					while not label:
						os.system('clear')
						# progress bar equivalent, print out which comparison we are on
						print("{}/{}".format(self.shallowCompares, self.maxCompares))
						# print out the summed percent error
						print("prediction: {} (0.4 means low error, 1 means high error)".format(sv))
						# display all of the shared fields to manually compare
						# CONSIDER: maybe also outputting non-shared fields is also useful???
						for k in keysToComp:
							print("e1: {}\ne2: {}\n".format(entry1[k], entry2[k]))
						label = raw_input("Are the entries the same? [y, n] ")

						label = str(label).lower()
						if label == "y":
							l[self.label] = 1
						elif label == "n":
							l[self.label] = 0
						else:
							label = None

				self.learning.append(l)
			elif self.doLearning == self.doLearnings['off']:
				data = [1]
				for k in self.defaultKeysToDeepCompSorted:
					if k in l:
						data.append(l[k])
					else:
						data.append(-1)
				prediction = sum(numpy.array(data) * self.theta)
				prediction = 1/(numpy.exp(-prediction) + 1)

				self.allPredictions.append(prediction)

				if prediction > 0.5:
					self.allPredictionsClass.append(1)
					print("duplicates", entry1[self.id], entry2[self.id])
				else:
					self.allPredictionsClass.append(0)
		except KeyError:
			if self.killLevel:
				print("ERROR: skipping")

		return

	def Learner(self):
		self.__title__("Learner")

		print("defaultKeysToDeepCompSorted:", self.defaultKeysToDeepCompSorted)
		print("# defaultKeysToDeepCompSorted:", len(self.defaultKeysToDeepCompSorted))

		dataset = []
		if self.doLearning == self.doLearnings['remakeData']:
			for e in self.learning:
				new_e = [e[self.label]]
				for k in self.defaultKeysToDeepCompSorted:
					if k in e:
						new_e.append(e[k])
					else:
						new_e.append(-1)

				dataset.append(new_e)

			self.__write__(self.learningDir, "deepComparisonLearner.csv", array=dataset)
		else:
			dataset = self.__read__(self.learningDir, "deepComparisonLearner.csv")

		dataset = numpy.array(dataset, dtype=numpy.float)
		
		X = numpy.c_[numpy.ones(len(dataset)), dataset[:,1:]]
		y = dataset[:, 0]

		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=numpy.random.RandomState(2))

		# model = linear_model.Lasso(alpha=0.0000001, max_iter=2000)
		model = linear_model.LogisticRegression()
		model.fit(X_train, y_train)

		y_train_prediction = model.predict(X_train)
		y_test_prediction = model.predict(X_test)

		train_accuracy = float(numpy.mean(y_train_prediction == y_train) * 100)
		test_accuracy  = float(numpy.mean(y_test_prediction  == y_test)  * 100)

		#(print model.coef_)

		# if self.learningModel == self.learningModels['fminunc']:
		# 	os.system("matlab -nodesktop -nodisplay -nosplash -r {}".format(
		# 		"\"cd('fminunc');optimize_fminunc();exit();\""))
		# elif self.learningModel == self.learningModels['glmfit']:
		# 	os.system("matlab -nodesktop -nodisplay -nosplash -r {}".format(
		# 		"\"cd('glmfit');optimize_glmfit();exit();\""))
		# else:
		# 	raise ValueError("ERROR: bad model specified")
		return

	def PostProcessor(self):
		self.__title__("PostProcessor")
		
		return

	

if __name__ == '__main__':
	try:
		if len(argv) == 2:
			s = str(argv[1])
			BibTeX_Merger(importDir=s)
		elif len(argv) == 3:
			s = str(argv[1])
			n = int(argv[2])
			BibTeX_Merger(importDir=s, numFiles=n)
		else:
			BibTeX_Merger()
	except UserError:
		PrintException("UserError")
	except ProgramError:
		PrintException("ProgramError")
	except BibTeXParserError:
		PrintException("BibTeXParserError")