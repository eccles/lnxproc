'''
Test OSrelease()
'''

from lnxproc import osrelease

from .basetestcase import BaseTestCase


class TestOSrelease(BaseTestCase):
    '''
    Test OSrelease class
    '''
    key = 'OSrelease'
    module = osrelease

    def test_osrelease(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
