'''
Test PidSmaps()()
'''

from lnxproc import pidsmaps

from .basetestcase import BaseTestCase


class TestPidSmaps(BaseTestCase):
    '''
    Test PidSmaps class
    '''
    key = 'PidSmaps'
    module = pidsmaps
    pid = '1'

    def test_pidsmaps(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
