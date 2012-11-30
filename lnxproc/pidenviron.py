'''
Contains PidEnviron() class

    Reads the /proc/<pid>/environ file

'''
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class PidEnviron(ReadFile):
    '''
    PidEnviron handling
    '''
    FILENAME = ospath.join('proc', '%s', 'environ')
    KEY = 'pidenviron'
    CACHED = True

    def normalize(self):
        '''
        Translates data into dictionary
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}
        if lines:
            myvars = lines[0].split('\0')
            for var in myvars:
                if var and '=' in var:
                    top, tail = var.split('=', 1)
                    ret[top] = tail

        return ret
