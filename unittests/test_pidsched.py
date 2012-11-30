'''
Test PidSched()()
'''

from lnxproc import pidsched

from .basetestcase import BaseTestCase


class TestPidSched(BaseTestCase):
    '''
    Test PidSched class
    '''
    key = 'PidSched'
    module = pidsched
    pid = '1'

    def test_pidsched(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
