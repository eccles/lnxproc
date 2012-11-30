'''
Test Cpufreq()
'''

from lnxproc import cgroups

from .basetestcase import BaseTestCase


class TestCgroups(BaseTestCase):
    '''
    Test Cgroups class
    '''
    key = 'Cgroups'
    module = cgroups

    def test_cpufreq(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
