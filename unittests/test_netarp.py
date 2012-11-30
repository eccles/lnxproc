'''
Test NetArp()
'''


from lnxproc import netarp

from .basetestcase import BaseTestCase


class TestNetArp(BaseTestCase):
    '''
    Test NetArp class
    '''
    key = 'NetArp'
    module = netarp

    def test_netarp(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
