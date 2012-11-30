'''
Test NetSnmp()
'''

from lnxproc import netsnmp

from .basetestcase import BaseTestCase


class TestNetSnmp(BaseTestCase):
    '''
    Test NetSnmp class
    '''
    key = 'NetSnmp'
    module = netsnmp

    def test_netsnmp(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
