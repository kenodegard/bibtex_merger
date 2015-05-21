#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A set of functions useful for customizing bibtex fields.
You can find inspiration from these functions to design yours.
Each of them takes a record and return the modified record.
"""

import itertools
import re
import logging
import sys

python2 = sys.version_info < (3, 0, 0)
range = xrange if python2 else range

from .latexenc import unicode_to_latex, unicode_to_crappy_latex1, unicode_to_crappy_latex2, string_to_latex, protect_uppercase

logger = logging.getLogger(__name__)

__all__ = [	'getnames', 'author', 'editor', 'journal', 'keyword',
			'page_double_hyphen', 'type', 'convert_to_unicode',
			'homogenize_latex_encoding']


def getnames(names):
	"""
	Make people names as [first, last] or [initials, last].

	:param names: a list of names
	:type names: list
	:returns: list -- Correctly formated names
	"""
	tidynames = []
	for namestring in names:
		namestring = namestring.strip()
		if len(namestring) > 0:
			# simply just remove jnr., jr., and junior
			namestring = re.sub(r"jnr\.*|jr\.*|junior", "", namestring, flags=re.IGNORECASE)

			if ',' in namestring:
				namesplit = namestring.split(',', 1)
				last = [namesplit[0].strip()]
				firsts = namesplit[1].split()
			else:
				namesplit = namestring.split()
				last = [namesplit.pop()]
				firsts = namesplit

			for i in range(0, len(firsts)):
				firsts[i] = re.sub(r'\.', '. ', firsts[i])

				# error check for initials without the .
				if len(firsts[i]) == 1:
					firsts[i] += '. '
				elif len(firsts[i]) == 2 and firsts[i] not in ["ben", "van", "der", "de", "la", "le"] and not (firsts[i][1] is '.'):
					firsts[i] = firsts[i][0].upper() + '. ' + firsts[i][1].upper() + '. '

				firsts[i] = firsts[i].strip()

			for i in range(len(firsts) - 1, 0, -1):
				item = firsts[i]
				if re.match(r"ben|van|der|de|la|le", item, flags=re.IGNORECASE):
					last = [firsts.pop(i)] + last

			tidynames.append([' '.join(firsts), ' '.join(last)])
	return tidynames


def author(record):
	"""
	Split author field into a list of "Name, Surname".

	:param record: the record.
	:type record: dict
	:returns: dict -- the modified record.

	"""

	if "author" in record:
		if record["author"]:
			author = record["author"]
			author = re.sub(r"\n", " ", author)
			# error check for incorrect et al.
			author = re.sub(r"et al\.*", "and others", author, flags=re.IGNORECASE)

			author = re.split(r"\s+and\s+", author, flags=re.IGNORECASE)

			record["author"] = getnames(author)
		else:
			del record["author"]
	return record


def editor(record):
	"""
	Turn the editor field into a dict composed of the original editor name
	and a editor id (without coma or blank).

	:param record: the record.
	:type record: dict
	:returns: dict -- the modified record.

	"""
	if "editor" in record:
		if record["editor"]:
			editor = record["editor"]
			editor = re.sub(r"\n", " ", editor)
			# error check for incorrect et al.
			editor = re.sub(r"et al\.*", "and others", editor, flags=re.IGNORECASE)

			editor = re.split(r"\s+and\s+", editor, flags=re.IGNORECASE)

			editor = getnames(editor)
			# convert editor to object
			record["editor"] = [	{	"ID": re.sub(r",| |\.", "", "".join(e), flags=re.IGNORECASE), "name": e} for e in editor]
		else:
			del record["editor"]
	return record


def page_double_hyphen(record):
	"""
	Separate pages by a double hyphen (--).

	:param record: the record.
	:type record: dict
	:returns: dict -- the modified record.

	"""
	if "pages" in record:
		record["pages"] = re.sub(r"\s*-+\s*", "--", record["pages"], flags=re.IGNORECASE)

		# if "-" in record["pages"]:
		# 	p = [i.strip().strip('-') for i in record["pages"].split("-")]
		# 	record["pages"] = p[0] + '--' + p[-1]
	return record


def type(record):
	"""
	Put the type into lower case.

	:param record: the record.
	:type record: dict
	:returns: dict -- the modified record.

	"""
	if "type" in record:
		record["type"] = record["type"].lower()
	return record


def journal(record):
	"""
	Turn the journal field into a dict composed of the original journal name
	and a journal id (without coma or blank).

	:param record: the record.
	:type record: dict
	:returns: dict -- the modified record.

	"""
	if "journal" in record:
		# switch journal to object
		if record["journal"]:
			journal = re.sub(r"\n", " ", record["journal"])
			record["journal"] = {	"ID": re.sub(r",| |\.", "", journal, flags=re.IGNORECASE), "name": journal}
	return record


def keyword(record, sep=r",|;"):
	"""
	Split keyword field into a list.

	:param record: the record.
	:type record: dict
	:param sep: pattern used for the splitting regexp.
	:type record: string, optional
	:returns: dict -- the modified record.

	"""
	if "keyword" in record:
		keyword = re.sub(r"\n", " ", record["keyword"])
		keyword = re.split(sep, keyword)
		record["keyword"] = [k.strip() for k in keyword]
	return record

def convert_to_unicode(record):
    """
    Convert accent from latex to unicode style.
    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    for val in record:
        if '\\' in record[val] or '{' in record[val]:
            for k, v in itertools.chain(unicode_to_crappy_latex1, unicode_to_latex):
                if v in record[val]:
                    record[val] = record[val].replace(v, k)

        # If there is still very crappy items
        if '\\' in record[val]:
            for k, v in unicode_to_crappy_latex2:
                if v in record[val]:
                    parts = record[val].split(str(v))
                    for key, record[val] in enumerate(parts):
                        if key+1 < len(parts) and len(parts[key+1]) > 0:
                            # Change order to display accents
                            parts[key] = parts[key] + parts[key+1][0]
                            parts[key+1] = parts[key+1][1:]
                    record[val] = k.join(parts)
    return record


def homogenize_latex_encoding(record):
    """
    Homogenize the latex encoding style for bibtex
    This function is experimental.
    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    # First, we convert everything to unicode
    record = convert_to_unicode(record)
    # And then, we fall back
    for val in record:
        if val not in ['ID']:
            logger.debug('Apply string_to_latex to: %s', val)
            record[val] = string_to_latex(record[val])
            if val == 'title':
                logger.debug('Protect uppercase in title')
                logger.debug('Before: %s', record[val])
                record[val] = protect_uppercase(record[val])
                logger.debug('After: %s', record[val])
    return record