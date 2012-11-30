'''
Contains PidStatm() class

Typical output from /proc/<pid>/statm::

   6770 1061 464 225 0 594 0

Provides information about memory usage, measured in pages. The columns are::

   size       total program size
              (same as VmSize in /proc/[pid]/status)
   resident   resident set size
              (same as VmRSS in /proc/[pid]/status)
   share      shared pages (from shared mappings)
   text       text (code)
   lib        library (unused in Linux 2.6)
   data       data + stack
   dt         dirty pages (unused in Linux 2.6)

'''
from logging import getLogger
from os import sysconf, path as ospath

from .readfile import ReadFile

PAGE_SIZE = sysconf('SC_PAGE_SIZE') // 1024
LOGGER = getLogger(__name__)


class PidStatm(ReadFile):
    '''
    PidStatm handling
    '''
    FILENAME = ospath.join('proc', '%s', 'statm')
    KEY = 'pidstatm'
    FIELDS = ('size', 'resident', 'share',
              'text', 'lib', 'data', 'dt')

    def normalize(self):
        '''
        Translates data into dictionary

        The <pid>/statm file is one record
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        if not lines:
            return {}

        vals = lines[0].split()
        return dict(zip(self.FIELDS, (int(val)*PAGE_SIZE for val in vals)))
