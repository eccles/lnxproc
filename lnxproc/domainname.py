'''
Contains DomainName() class

Typical contents of file /proc/sys/kernel/domainname::

    (none)

.. note::
   This class is **cached**. The file is only read **once**. Subsequent reads
   return the first value read

'''
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class DomainName(ReadFile):
    '''
    Domain name handling
    '''
    FILENAME = ospath.join('proc', 'sys', 'kernel', 'domainname')
    KEY = 'domainname'
    CACHED = True

    def normalize(self):
        '''
        Translates data into dictionary
        '''
        LOGGER.debug("Normalize")
        return self.lines[0]
