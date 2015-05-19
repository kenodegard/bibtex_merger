https://badge.fury.io/hooks/github
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

# Installing

# System Requirements

