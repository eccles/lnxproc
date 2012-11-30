'''
Test Loadavg()
'''

from lnxproc import loadavg

from .basetestcase import BaseTestCase


class TestLoadavg(BaseTestCase):
    '''
    Test Loadavg class
    '''
    key = 'Loadavg'
    module = loadavg

    def test_loadavg(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
