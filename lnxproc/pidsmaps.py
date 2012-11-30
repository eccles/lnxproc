'''
Contains PidSmaps() class

Typical contents - this data is repeated for each map::

   2b89e798c000-2b89e856d000 rw-p 2b89e798c000 00:00 0 [heap]
   Size:             12164 kB
   Rss:               9416 kB
   Shared_Clean:       108 kB
   Shared_Dirty:      6248 kB
   Private_Clean:        0 kB
   Private_Dirty:     3060 kB
   Swap:              2348 kB
   Pss:               3766 kB

.. note::
   requires root access or CAP_SYS_PTRACE or to be run as owner of <pid>

'''

from ast import literal_eval
from logging import getLogger
from os import path as ospath
import re

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class PidSmaps(ReadFile):
    '''
    PidSmaps handling

    WARN - requires root access or CAP_SYS_PTRACE or to be run as owner of
           <pid>
    '''
    FILENAME = ospath.join('proc', '%s', 'smaps')
    KEY = 'pidsmaps'
    RE1 = re.compile(
        r'([0-9a-fA-F]+)-([0-9a-fA-F]+)\s+.+\s+[0-9a-fA-F]+\s+(.*)'
    )
    RE2 = re.compile(r'^([a-zA-Z_]+):\s+(\d+)\s+(.*)')

    def normalize(self):
        '''
        Translates data into dictionary

        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}
        ref = {}
        for line in lines:
            i = self.RE1.match(line)
            if i:
                start = i.group(1)
                end = i.group(2)
                name = i.group(3)
                ref = ret[start] = {}

                ref['end'] = end
                ref['name'] = name

            elif ref:
                i = self.RE2.match(line)
                if i:
                    key = i.group(1).strip()
                    val = literal_eval(i.group(2).strip())
                    ref[key] = val

                else:
                    ref = None

        return ret
