'''
Test PidStatus()
'''

from lnxproc import pidstatus

from .basetestcase import BaseTestCase


class TestPidStatus(BaseTestCase):
    '''
    Test PidStatus class
    '''
    key = 'PidStatus'
    module = pidstatus
    pid = '1'

    def test_pidstatus(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
