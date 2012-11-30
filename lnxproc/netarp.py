'''
Contains NetArp() class

Typical contents of file /proc/net/arp::

    IP address  HW type   Flags        HW address  Mask Device
    192.168.1.1 0x1       0x2   50:46:5d:02:05:50     *   eth0

.. note::
   The field names are **not** read from the file because of embedded spaces

'''
from itertools import islice
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class NetArp(ReadFile):
    '''
    NetArp handling
    '''
    FILENAME = ospath.join('proc', 'net', 'arp')
    KEY = 'netarp'
    FIELDS = (
        'HW type',
        'Flags',
        'HW address',
        'Mask',
        'Device',
    )

    def normalize(self):
        '''
        Translates data into dictionary
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}

        for line in islice(lines, 1, None):
            vals = line.split()
            ret[vals[0]] = dict(zip(self.FIELDS, islice(vals, 1, None)))

        return ret
