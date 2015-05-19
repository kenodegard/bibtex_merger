[![GitHub version](https://badge.fury.io/gh/njalerikson%2Fbibtex_merger.svg)](http://badge.fury.io/gh/njalerikson%2Fbibtex_merger)
[![Build Status](https://travis-ci.org/njalerikson/bibtex_merger.svg)](https://travis-ci.org/njalerikson/bibtex_merger)
[![Coverage Status](https://coveralls.io/repos/njalerikson/bibtex_merger/badge.svg)](https://coveralls.io/r/njalerikson/bibtex_merger)


# bibtex_merger
The BibTeX merger tool.

Identifies duplicate entries based on similarity levels in author names as well
as other shared fields.

Utilizes a divide and conquer approach to quickly make
large merge tasks manageable. Once the dataset is spliced into manageable
chunks a quick scan is made analyzing the similarity of the author field (all
non-author entries are lumped together and processed separately). Those entries
that are still deemed highly similar are then compared for other shared fields
within the entry. Based on the similarity levels of the shared fields, a
logistic regression learning model is trained to determine a classification
model. Note that the solution comes prepackaged with a standard model but has
the option for retraining with a custom dataset.

# System Requirements
The code requires:
	python 2.6 or better
		numpy 1.9.2 or better
		Levenshtein 0.12.0 or better
		fuzzy 1.0 or better
		gmpy2 2.0.5 or better
	MATLAB 2014a or better
		Bioinformatics Toolbox
		Neural Network Toolbox
		Optimization Toolbox
		Parallel Computing Toolbox
		Statistics and Machine Learning Toolbox

# Running merger.py

1. First navigate into the src/ directory.
2. python merger.py

Look into the ```__init__()``` method to toggle flags for the various functions.
These flags are also explained in the code.

There are 3 ways to run the code and the corresponding value that must be
set for flag self.doLearning:

1. ```self.learning_remakeData```	Building the dataset for the learning model
									training.
2. ```self.learning_modeling```		Recreating the learning models based on
									preexisting dataset. Note that this step
									requires there to be datasets in the
									1_prelearning directory.
3. ```self.learning_off```			Detect duplicates using a preexisting
									prediction model. Note that this step
									requires theta values to be set in the
									self.theta value.

There are 2 available learning models that can be toggled via the
self.learningModel flag:

1. ```'fminunc'```
2. ```'glmfit'```