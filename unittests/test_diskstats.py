'''
Test Diskstats()
'''

from lnxproc import diskstats

from .basetestcase import BaseTestCase


class TestDiskstats(BaseTestCase):
    '''
    Test Diskstats class
    '''
    key = 'Diskstats'
    module = diskstats

    def test_diskstats(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
