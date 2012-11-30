'''
Base test case
'''

from os import environ
import unittest

from lnxproc.logger import set_logger
from lnxproc.readfile import DEFAULT_ROOT

from .mockfiles import get_test_result, DATA_DIR

set_logger(environ.get('LNXPROC_LOGLEVEL', 'CRITICAL'))


class BaseTestCase(unittest.TestCase):
    '''
    Test any class
    '''
    key = None
    module = None
    pid = None
    result = None
    root = None

    @classmethod
    def setUpClass(cls):
        cls.longMessage = True
        cls.maxDiff = None

    def setUp(self):
        '''
        Generic set up
        '''
        self.root = DATA_DIR
        self.result = get_test_result(self.key.lower())

    def tearDown(self):
        '''
        Generic tear_down
        '''
        self.key = None
        self.module = None
        self.pid = None
        self.result = None
        self.root = DEFAULT_ROOT

    def generic_test(self):
        '''
        Test normal instantiation
        '''
        mod = getattr(self.module, self.key)
        dname = mod(root=self.root, pid=self.pid)
        dname.read()
        self.assertEqual(
            dname.normalize(),
            self.result,
            msg='Incorrect results returned from %s' % (mod, ),
        )
