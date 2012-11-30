'''
Test PidIo()()
'''
from lnxproc import pidio

from .basetestcase import BaseTestCase


class TestPidIo(BaseTestCase):
    '''
    Test PidIo class
    '''
    key = 'PidIo'
    module = pidio
    pid = '1'

    def test_pidio(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
