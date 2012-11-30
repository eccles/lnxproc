'''
Test NetRpcNfs()
'''

from lnxproc import netrpcnfs

from .basetestcase import BaseTestCase


class TestNetRpcNfsd(BaseTestCase):
    '''
    Test NetRpcNfsd class
    '''
    key = 'NetRpcNfs'
    module = netrpcnfs

    def test_netrpcnfs(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
