'''
Test Cpuinfo()
'''

from lnxproc import cpuinfo

from .basetestcase import BaseTestCase


class TestCpuinfo(BaseTestCase):
    '''
    Test Cpuinfo class
    '''
    key = 'Cpuinfo'
    module = cpuinfo

    def test_cpuinfo(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
