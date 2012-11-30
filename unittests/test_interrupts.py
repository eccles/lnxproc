'''
Test Diskstats()
'''

from lnxproc import interrupts

from .basetestcase import BaseTestCase


class TestInterrupts(BaseTestCase):
    '''
    Test Interrupts class
    '''
    key = 'Interrupts'
    module = interrupts

    def test_interrupts(self):
        '''
        Test normal instantiation
        '''
        self.generic_test()
