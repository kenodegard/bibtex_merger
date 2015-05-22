#!/usr/bin/env python

from distutils.core import setup
from bibtex_merger import __version__ as version

setup(
    name         = 'BibTeX Merger',
    version      = version,
    url          = "https://github.com/njalerikson/bibtex_merger",
    author       = "Ken Odegard",
    license      = "BSD",
    author_email = "",
    description  = "The BibTeX merger tool.",
    packages = ['bibtex_merger'],
)
