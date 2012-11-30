'''
Test NetDev()
'''

from lnxproc import netdev

from .basetestcase import BaseTestCase


class TestNetDev(BaseTestCase):
    '''
    Test NetDev class
    '''
    key = 'NetDev'
    module = netdev

    def test_netdev(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
