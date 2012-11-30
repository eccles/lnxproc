'''
Test NetRpcNfsd()
'''

from lnxproc import netrpcnfsd

from .basetestcase import BaseTestCase


class TestNetRpcNfsd(BaseTestCase):
    '''
    Test NetRpcNfsd class
    '''
    key = 'NetRpcNfsd'
    module = netrpcnfsd

    def test_netrpcnfsd(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
