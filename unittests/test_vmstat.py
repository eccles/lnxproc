'''
Test VMstat()
'''

from lnxproc import vmstat

from .basetestcase import BaseTestCase


class TestVMstat(BaseTestCase):
    '''
    Test VMstat class
    '''
    key = 'VMstat'
    module = vmstat

    def test_vmstat(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
