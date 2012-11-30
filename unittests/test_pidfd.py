'''
Test PidFd()()
'''
from lnxproc import pidfd

from .basetestcase import BaseTestCase


class TestPidFd(BaseTestCase):
    '''
    Test PidFd class
    '''
    key = 'PidFd'
    module = pidfd
    pid = '1'

    def test_pidfd(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
