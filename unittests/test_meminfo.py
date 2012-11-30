'''
Test Meminfo()
'''

from lnxproc import meminfo

from .basetestcase import BaseTestCase


class TestMeminfo(BaseTestCase):
    '''
    Test Meminfo class
    '''
    key = 'Meminfo'
    module = meminfo

    def test_loadavg(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
