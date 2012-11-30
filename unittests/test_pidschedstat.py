'''
Test PidSchedStat()()
'''

from lnxproc import pidschedstat

from .basetestcase import BaseTestCase


class TestPidSchedStat(BaseTestCase):
    '''
    Test PidSchedStat class
    '''
    key = 'PidSchedStat'
    module = pidschedstat
    pid = '1'

    def test_pidschedstat(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
