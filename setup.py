#!/usr/bin/env python

from distutils.core import setup
from src import __version__ as version

setup(
    name         = 'bibtex_merger',
    version      = version,
    url          = "https://github.com/njalerikson/bibtex_merger",
    author       = "Ken Odegard",
    license      = "BSD",
    author_email = "",
    description  = "The BibTeX merger tool.",
    packages = ['bibtex_merger'],
)
