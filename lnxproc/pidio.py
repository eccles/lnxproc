'''
Contains PidIo() class

Typical contents of /proc/<pid>/io file::

   rchar: 143848377
   wchar: 4254218
   syscr: 98216
   syscw: 31339
   read_bytes: 270336
   write_bytes: 3489792
   cancelled_write_bytes: 974848

'''
from logging import getLogger
from os import path as ospath
from re import compile as recompile

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class PidIo(ReadFile):
    '''
    PidIo handling
    '''
    FILENAME = ospath.join('proc', '%s', 'io')
    KEY = 'pidio'
    REGEX = recompile('^[a-zA-Z_]+:')

    def normalize(self):
        '''
        Translates data into dictionary

        The /proc/<pid>/io file is a number records keyed on ':' separator
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}
        for line in lines:
            if self.REGEX.match(line):
                key, vals = line.split(':')
                val = int(vals.strip())
                ret[key] = val

        return ret
