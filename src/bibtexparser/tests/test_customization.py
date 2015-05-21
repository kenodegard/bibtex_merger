#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest

from bibtexparser.customization import getnames, author, editor, type, convert_to_unicode, homogenize_latex_encoding, page_double_hyphen, keyword


class TestBibtexParserMethod(unittest.TestCase):

    ###########
    # getnames
    ###########
    def test_getnames(self):
        names = ['Foo Bar',
                 'Foo B. Bar',
                 'F. B. Bar',
                 'F.B. Bar',
                 'F. Bar',
                 'Jean de Savigny',
                 'Jean la Tour',
                 'Jean le Tour',
                 'Mike ben Akar',
                 'Jean de la Tour',
                 'Johannes Diderik van der Waals',
                 ]
        result = getnames(names)
        expected = [['Foo', 'Bar'],
                    ['Foo B.', 'Bar'],
                    ['F. B.', 'Bar'],
                    ['F. B.', 'Bar'],
                    ['F.', 'Bar'],
                    ['Jean', 'de Savigny'],
                    ['Jean', 'la Tour'],
                    ['Jean', 'le Tour'],
                    ['Mike', 'ben Akar'],
                    ['Jean', 'de la Tour'],
                    ['Johannes Diderik', 'van der Waals'],
                    ]
        self.assertEqual(result, expected)

    def test_getnames_add_single_dot(self):
        names = ['F Bar', 'C Lux']
        result = getnames(names)
        expected = [['F.', 'Bar'], ['C.', 'Lux']]
        self.assertEqual(result, expected)

    def test_getnames_add_double_dot(self):
        names = ['FG Bar', 'CQ Lux']
        result = getnames(names)
        expected = [['F. G.', 'Bar'], ['C. Q.', 'Lux']]
        self.assertEqual(result, expected)

    @unittest.skip('Bug #9')
    def test_getnames_braces(self):
        names = ['A. {Delgado de Molina}', 'M. Vign{\\\'e}']
        result = getnames(names)
        expected = ['Delgado de Molina, A.', 'Vigné, M.']
        self.assertEqual(result, expected)

    ###########
    # author
    ###########
    def test_author_none(self):
        record = {'author': None}
        result = author(record)
        expected = {}
        self.assertEqual(result, expected)

    def test_author_basic(self):
        record = {'author': 'Foo G. Bar and Lee B. Smith'}
        result = author(record)
        expected = {'author': [['Foo G.', 'Bar'],['Lee B.', 'Smith']]}
        self.assertEqual(result, expected)

    def test_author_others(self):
        record = {'author': 'Foo G. Bar and Lee B. Smith and others'}
        result = author(record)
        expected = {'author': [['Foo G.', 'Bar'],['Lee B.', 'Smith'],['', 'others']]}
        self.assertEqual(result, expected)

    ###########
    # editor
    ###########
    def test_editor_none(self):
        record = {'editor': None}
        result = editor(record)
        expected = {}
        self.assertEqual(result, expected)

    def test_editor_basic(self):
        record = {'editor': 'Foo G. Bar and Lee B. Smith'}
        result = editor(record)
        expected = {'editor': [ {'ID': 'FooGBar', 'name': ['Foo G.', 'Bar']},
                                {'ID': 'LeeBSmith', 'name': ['Lee B.', 'Smith']}]}
        self.assertEqual(result, expected)

    def test_editor_others(self):
        record = {'editor': 'Foo G. Bar and Lee B. Smith and others'}
        result = editor(record)
        expected = {'editor': [ {'ID': 'FooGBar', 'name': ['Foo G.', 'Bar']},
                                {'ID': 'LeeBSmith', 'name': ['Lee B.', 'Smith']},
                                {'ID': 'others', 'name': ['', 'others']}]}
        self.assertEqual(result, expected)

    ###########
    # type
    ###########
    def test_type1(self):
        record = {'type': 'ARTICLE'}
        result = type(record)
        expected = {'type': 'article'}
        self.assertEqual(result, expected)

    def test_type2(self):
        record = {'type': 'BoOk'}
        result = type(record)
        expected = {'type': 'book'}
        self.assertEqual(result, expected)

    def test_type3(self):
        record = {'type': 'journal'}
        result = type(record)
        expected = {'type': 'journal'}
        self.assertEqual(result, expected)

    ###########
    # page_double_hyphen
    ###########
    def test_page_double_hyphen_alreadyOK(self):
        record = {'pages': '12--24'}
        result = page_double_hyphen(record)
        expected = record
        self.assertEqual(result, expected)

    def test_page_double_hyphen_simple(self):
        record = {'pages': '12-24'}
        result = page_double_hyphen(record)
        expected = {'pages': '12--24'}
        self.assertEqual(result, expected)

    def test_page_double_hyphen_space(self):
        record = {'pages': '12 - 24'}
        result = page_double_hyphen(record)
        expected = {'pages': '12--24'}
        self.assertEqual(result, expected)

    def test_page_double_hyphen_nothing(self):
        record = {'pages': '12 24'}
        result = page_double_hyphen(record)
        expected = {'pages': '12 24'}
        self.assertEqual(result, expected)

    ###########
    # convert to unicode
    ###########
    def test_convert_to_unicode1(self):
        record = {'toto': '{\`a} \`{a}'}
        result = convert_to_unicode(record)
        expected = {'toto': 'à à'}
        self.assertEqual(result, expected)

    def test_convert_to_unicode2(self):
        record = {'toto': '{\\"u} \\"{u}'}
        result = convert_to_unicode(record)
        expected = {'toto': 'ü ü'}
        self.assertEqual(result, expected)

    def test_convert_to_unicode3(self):
        record = {'toto': "\\c \\'"}
        result = convert_to_unicode(record)
        expected = {'toto': " \u0327\u0301"}
        self.assertEqual(result, expected)

    ###########
    # homogeneize
    ###########
    def test_homogeneize(self):
        record = {'toto': 'à {\`a} \`{a}'}
        result = homogenize_latex_encoding(record)
        expected = {'toto': '{\`a} {\`a} {\`a}'}
        self.assertEqual(result, expected)

    ###########
    # keywords
    ###########
    def test_keywords(self):
        record = {'keyword': "a b, a b , a b;a b ; a b, a b\n"}
        result = keyword(record)
        expected = {'keyword': ['a b'] * 6}
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
