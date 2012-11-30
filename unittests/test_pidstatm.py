'''
Test PidStatm()()
'''

from lnxproc import pidstatm

from .basetestcase import BaseTestCase


class TestPidStatm(BaseTestCase):
    '''
    Test PidStatm class
    '''
    key = 'PidStatm'
    module = pidstatm
    pid = '1'

    def test_pidstatm(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
