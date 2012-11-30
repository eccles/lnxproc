'''
Contains Diskstats() class from lnxproc package

This is the order of metrics in /proc/diskstats::

   0 major        Major number
   1 minor        Minor number
   2 name         Name
   3 reads        This is the total number of reads completed successfully.
   4 merge_read   Reads and writes which are adjacent to each other may be
                  merged for efficiency. Thus two 4K reads may become one 8K
                  read before it is ultimately handed to the disk, and so it
                  will be counted (and queued) as only one I/O. This field lets
                  you know how often this was done.
   5 s_read       This is the total number of sectors read successfully.
   6 ms_read      This is the total number of milliseconds spent by all reads.
   7 writes       This is the total number of writes completed successfully.
   8 merge_write  Reads and writes which are adjacent to each other may be
                  merged for efficiency. Thus two 4K reads may become one 8K
                  read before it is ultimately handed to the disk, and so it
                  will be counted (and queued) as only one I/O. This field lets
                  you know how often this was done.
   9 s_write      This is the total number of sectors written successfully.
   10 ms_write    This is the total number of milliseconds spent by all writes.
   11 ios         The only field that should go to zero. Incremented as
                  requests are given to appropriate request_queue_t and
                  decremented as they finish.
   12 ms_io       This field is increases so long as field 9 is nonzero.
   13 ms_weighted This field is incremented at each I/O start, I/O completion
                  and I/O

Typical contents of /proc/diskstats::

    1    0 ram0 0 0 0 0 0 0 0 0 0 0 0
    1    1 ram1 0 0 0 0 0 0 0 0 0 0 0
    1    2 ram2 0 0 0 0 0 0 0 0 0 0 0
    1    3 ram3 0 0 0 0 0 0 0 0 0 0 0
    1    4 ram4 0 0 0 0 0 0 0 0 0 0 0
    1    5 ram5 0 0 0 0 0 0 0 0 0 0 0
    1    6 ram6 0 0 0 0 0 0 0 0 0 0 0
    1    7 ram7 0 0 0 0 0 0 0 0 0 0 0
    1    8 ram8 0 0 0 0 0 0 0 0 0 0 0
    1    9 ram9 0 0 0 0 0 0 0 0 0 0 0
    1   10 ram10 0 0 0 0 0 0 0 0 0 0 0
    1   11 ram11 0 0 0 0 0 0 0 0 0 0 0
    1   12 ram12 0 0 0 0 0 0 0 0 0 0 0
    1   13 ram13 0 0 0 0 0 0 0 0 0 0 0
    1   14 ram14 0 0 0 0 0 0 0 0 0 0 0
    1   15 ram15 0 0 0 0 0 0 0 0 0 0 0
    8    0 sda 1958502 875995 119654702 27720992 10620346 8610695 154141942
               2172968844 0 30623307 2201458835
    8    1 sda1 152 1853 2287 1849 89 27 230 7932 0 9737 9781
    8    2 sda2 227184 610491 6699952 3069044 138618 740443 7256536 32485911 0
                2201739 36166789
    8    3 sda3 1731147 263634 112952175 24649802 10481639 7870225 146885176
                2140475001 0 29931840 2165282323
  253    0 dm-0 791292 0 18866082 11314325 10345209 0 82761672 2133498386 0
                26344873 2144813575
  253    1 dm-1 1188117 0 93835442 17701655 3557810 0 28462480 1190191767 0
                10791972 1207900801
  253    2 dm-2 15848 0 247890 163041 4457625 0 35661000 373930544 0 6793367
                374095145
  253    3 dm-3 307 0 2450 1354 3 0 24 1 0 295 1355
   11    0 sr0 0 0 0 0 0 0 0 0 0 0 0
    9    0 md0 0 0 0 0 0 0 0 0 0 0 0
'''

import errno
from logging import getLogger
from os import path as ospath
import re

from .readfile import ReadFile

DISKFILE = ospath.join('sys', 'block', '%s', 'queue', 'hw_sector_size')
LOGGER = getLogger(__name__)


class Diskstats(ReadFile):
    '''
    Diskstats handling
    '''
    FILENAME = ospath.join('proc', 'diskstats')
    KEY = 'diskstats'

    FIELDS = (
        'major', 'minor',
        'reads', 'merge_read', 's_read',
        'ms_read', 'writes', 'merge_write',
        's_write', 'ms_write', 'ios',
        'ms_io', 'ms_weighted',
    )

    def __init__(self, **kwargs):
        '''
        Instantiate ReadFile object
        '''
        super().__init__(**kwargs)
        self.sector_size = {}

    def _sector_size_read(self, key):
        '''
        Reads sector size
        '''
        LOGGER.debug("sector_size_read for %s", key)
        filename = ospath.join(
            self.root,
            DISKFILE % (key, ),
        )
        LOGGER.debug("sector_size_read file %s", filename)

        sector_size = None
        try:

            with open(filename, 'rt') as fhandle:
                sector_size = int(fhandle.read())

        except OSError as ex:
            if ex.errno != errno.ENOENT:
                raise

            LOGGER.debug("sector_size_read file %s does not exist", filename)

        LOGGER.debug("sector_size_read is %s", sector_size)
        return sector_size

    def _sector_size(self, key):
        '''
        Calculates sector size
        '''
        sector_size = self._sector_size_read(key)

        # get sector size from disk entry if partition entry is unavailable
        if sector_size is None:
            key1 = re.sub(r'[0-9]', '', key)
            sector_size = self._sector_size_read(key1)

        if sector_size is not None:
            self.sector_size[key] = sector_size

    def _derive(self, key, vals):
        '''
        Convert units into KiB

        :param key: name of disk e.g. 'sda'
        :param vals: dictionary of values
        '''
        LOGGER.debug("Convert values to bytes for %s", key)
        if key not in self.sector_size:
            self._sector_size(key)

        sector_size = self.sector_size[key]

        # convert into bytes
        vals['sectorsize'] = sector_size
        vals['s_read'] *= sector_size
        vals['s_write'] *= sector_size

    def normalize(self):
        '''
        Translates data into dictionary
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}
        for line in lines:
            vals = line.split()
            key = vals[2]
            vals.remove(key)
            ret[key] = dict(zip(self.FIELDS, (int(i) for i in vals)))
            self._derive(key, ret[key])

        return ret
