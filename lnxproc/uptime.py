'''
Contains Uptime() class

Typical contents of uptime file::

   95857.57 757484.85

'''
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class Uptime(ReadFile):
    '''
    Uptime handling
    '''
    FILENAME = ospath.join('proc', 'uptime')
    KEY = 'uptime'
    FIELDS = ('uptime', 'idle')

    def normalize(self):
        '''
        Translates data into dictionary
        '''
        LOGGER.debug("Nomalize")
        lines = self.lines
        return dict(
            zip(
                self.FIELDS,
                [float(val) for val in lines[0].split()]
            )
        )
