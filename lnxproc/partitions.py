'''
Contains Partitions() class

Typical layout of /proc/partitions::

   major minor  #blocks  name
      8     0  312571224 sda
      8     1     305203 sda1
      8     2    8385930 sda2
      8     3  303877507 sda3
    253     0   61440000 dm-0
    253     1  179634176 dm-1
    253     2    5111808 dm-2
    253     3   57671680 dm-3

'''
from logging import getLogger
from os import path as ospath
import re

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class Partitions(ReadFile):
    '''
    Partitions handling
    '''
    FILENAME = ospath.join('proc', 'partitions')
    KEY = 'partitions'
    FIELDS = ('major', 'minor', 'blocks')
    REGEX = re.compile('^[ ]*[0-9]')

    def normalize(self):
        '''
        Translates data into dictionary

        The partitions file is a table -
        each record corresponding to the statically defined fields above
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}

        for line in lines:
            if line:
                if self.REGEX.match(line):
                    vals = line.split()
                    key = vals[3]
                    ret[key] = dict(
                        zip(
                            self.FIELDS,
                            [int(val) for val in vals[:-1]]
                        )
                    )

        return ret
