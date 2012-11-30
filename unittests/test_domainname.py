'''
Test DomainName()
'''


from lnxproc import domainname

from .basetestcase import BaseTestCase


class TestDomainName(BaseTestCase):
    '''
    Test DomainName class
    '''
    key = 'DomainName'
    module = domainname

    def test_domainname(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
