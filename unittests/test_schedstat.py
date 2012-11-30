'''
Test Schedstat()
'''

from lnxproc import schedstat

from .basetestcase import BaseTestCase


class TestSchedstat(BaseTestCase):
    '''
    Test Schedstat class
    '''
    key = 'Schedstat'
    module = schedstat

    def test_schedstat(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
