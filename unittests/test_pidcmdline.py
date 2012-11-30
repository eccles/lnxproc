'''
Test Pidcmdline()()
'''

from lnxproc import pidcmdline

from .basetestcase import BaseTestCase


class TestPidCmdline(BaseTestCase):
    '''
    Test PidCmdline class
    '''
    key = 'PidCmdline'
    module = pidcmdline
    pid = '1'

    def test_pidcmdline(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
