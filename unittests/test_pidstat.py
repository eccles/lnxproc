'''
Test PidStat()()
'''

from lnxproc import pidstat

from .basetestcase import BaseTestCase


class TestPidStat(BaseTestCase):
    '''
    Test PidStat class
    '''
    key = 'PidStat'
    module = pidstat
    pid = '1'

    def test_pidstat(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
