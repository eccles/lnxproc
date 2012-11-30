'''
Test Cpufreq()
'''

from lnxproc import cpufreq

from .basetestcase import BaseTestCase


class TestCpufreq(BaseTestCase):
    '''
    Test Cpufreq class
    '''
    key = 'Cpufreq'
    module = cpufreq

    def test_cpufreq(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
