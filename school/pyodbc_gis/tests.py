__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import doctest
from django.test import TestCase


# Create your tests here.

DOCFILES = [
        'doc.rst',
    ]
DOCTESTS = [
        'pyodbc_gis.base',
        'pyodbc_gis.operations',
        'pyodbc_gis.schema',
    ]

def setUp(test):
    pass

def tearDown(test):
    pass

def load_tests(loader, tests, ignore):
    list_of_docfiles = DOCFILES
    for p in list_of_docfiles:
        tests.addTest(doctest.DocFileSuite(
            p, setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        ))

    list_of_doctests = DOCTESTS

    for m in list_of_doctests:
        tests.addTest(doctest.DocTestSuite(
            __import__(m, globals(), locals(), fromlist=["*"]),
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        ))

    return tests
