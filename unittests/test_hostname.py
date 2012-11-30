'''
Test HostName()
'''


from lnxproc import hostname

from .basetestcase import BaseTestCase


class TestHostName(BaseTestCase):
    '''
    Test HostName class
    '''
    key = 'HostName'
    module = hostname

    def test_hostname(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
