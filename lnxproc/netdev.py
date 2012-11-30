'''
Contains NetDev() class

Typical contents of file /proc/net/dev::

    Inter-|   Receive
          |  Transmit
    face  |bytes    packets errs drop fifo frame compressed multicast
          |bytes    packets errs drop fifo colls carrier compressed
      eth0:  122768     429    0    0    0     0           0     0
              21660     194    0    0    0     0       0           0
        lo:    5529      70    0    0    0     0           0     0
               5529      70    0    0    0     0       0           0
     wlan0:       0       0    0    0    0     0           0     0
                  0       0    0    0    0     0       0           0

.. note::
   The field names are **not** read from the file

'''

from itertools import islice
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class NetDev(ReadFile):
    '''
    NetDev handling
    '''
    FILENAME = ospath.join('proc', 'net', 'dev')
    KEY = 'netdev'
    FIELDS = (
        'rbytes',
        'rpackets',
        'rerrs',
        'rdrop',
        'rfifo',
        'rframe',
        'rcompressed',
        'rmulticast',
        'tbytes',
        'tpackets',
        'terrs',
        'tdrop',
        'tfifo',
        'tframe',
        'tcompressed',
        'tmulticast',
    )

    def normalize(self):
        '''
        Translates data into dictionary
        '''
        LOGGER.debug("Nomalize")
        lines = self.lines
        ret = {}

        for line in islice(lines, 2, None):
            cols = line.split(':')
            key = cols[0].lstrip()
            vals = cols[1].lstrip().split()
            ret[key] = dict(zip(self.FIELDS, (int(val) for val in vals)))

        return ret
