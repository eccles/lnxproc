'''
Test Partitions()
'''

from lnxproc import partitions

from .basetestcase import BaseTestCase


class TestPartitions(BaseTestCase):
    '''
    Test Partitions class
    '''
    key = 'Partitions'
    module = partitions

    def test_partitions(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
