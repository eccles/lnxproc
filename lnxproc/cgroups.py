'''Contains Cgroups() class from lnxproc package

typical contents of /proc/cgroups file::

   #subsys_name    hierarchy    num_cgroups    enabled
   cpuset                 1              4    1
   cpu                    2              4    1
   cpuacct                3              4    1
   memory                 4              4    1
   devices                5              4    1
   freezer                6              4    1
   blkio                  7              4    1
   perf_event             8              1    1

'''

from itertools import islice
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class Cgroups(ReadFile):
    '''
    Cgroups handling
    '''
    FILENAME = ospath.join('proc', 'cgroups')
    KEY = 'cgroups'

    def normalize(self):
        '''
        Translates data into dictionary
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}
        if lines:
            titles = lines[0].split()[1:]
            for rec in islice(lines, 1, None):
                fields = rec.split()
                key = fields[0].strip()
                ret[key] = dict(
                    zip(
                        titles,
                        (self.convert(val) for val in islice(fields, 1, None))
                    )
                )

        return ret
