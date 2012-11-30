'''
Test PidEnviron()()
'''

from lnxproc import pidenviron

from .basetestcase import BaseTestCase


class TestPidEnviron(BaseTestCase):
    '''
    Test PidEnviron class
    '''
    key = 'PidEnviron'
    module = pidenviron
    pid = '1'

    def test_pidenviron(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
