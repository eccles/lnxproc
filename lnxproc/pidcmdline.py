'''Contains PidCmdline() class

    Reads the /proc/<pid>/cmdline file and returns tuple
'''
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class PidCmdline(ReadFile):
    '''
    PidCmdline handling
    '''
    FILENAME = ospath.join('proc', '%s', 'cmdline')
    KEY = 'pidcmdline'
    CACHED = True

    def normalize(self):
        '''
        Translates data into dictionary
        '''
        LOGGER.debug("Normalize")
        try:
            ret = self.lines[0].strip('\0').split('\0')

        except IndexError:
            ret = None

        return ret
