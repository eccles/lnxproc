'''
Contains PidSchedstat() class

Typical contents of file /proc/<pid>/schedstat::

    765507966 715563 2922

'''

from ast import literal_eval
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class PidSchedStat(ReadFile):
    '''
    PidSchedStat handling
    '''
    FILENAME = ospath.join('proc', '%s', 'schedstat')
    KEY = 'pidschedstat'
    FIELDS = ('run', 'wait', 'num', )

    def normalize(self):
        '''
        The <pid>/schedstat file is one record
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        if not lines:
            return {}

        vals = lines[0].split()
        return dict(zip(self.FIELDS, (literal_eval(val) for val in vals)))
