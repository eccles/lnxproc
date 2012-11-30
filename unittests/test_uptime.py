'''
Test Uptime()
'''

from lnxproc import uptime

from .basetestcase import BaseTestCase


class TestUptime(BaseTestCase):
    '''
    Test Uptime class
    '''
    key = 'Uptime'
    module = uptime

    def test_uptime(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
