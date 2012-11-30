'''
Test Stat()
'''

from lnxproc import stat

from .basetestcase import BaseTestCase


class TestStat(BaseTestCase):
    '''
    Test Stat class
    '''
    key = 'Stat'
    module = stat

    def test_stat(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
